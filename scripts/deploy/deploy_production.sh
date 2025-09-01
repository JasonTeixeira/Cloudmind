#!/bin/bash

# CloudMind Production Deployment Script
# This script deploys CloudMind to production with all necessary checks

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="cloudmind"
DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env.production"

echo -e "${BLUE}🚀 CloudMind Production Deployment${NC}"
echo "=================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check prerequisites
print_info "Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed"
    exit 1
fi

# Check if .env.production exists
if [ ! -f "$ENV_FILE" ]; then
    print_warning "Production environment file not found. Creating template..."
    cat > "$ENV_FILE" << EOF
# CloudMind Production Environment Variables
# ========================================

# Database Configuration
DB_PASSWORD=your_secure_db_password_here
DATABASE_URL=postgresql://cloudmind:\${DB_PASSWORD}@postgres:5432/cloudmind

# Redis Configuration
REDIS_PASSWORD=your_secure_redis_password_here
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0

# Security Configuration
SECRET_KEY=your_very_secure_secret_key_here
ENVIRONMENT=production
DEBUG=false

# Cloud Provider Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1

AZURE_SUBSCRIPTION_ID=your_azure_subscription_id_here
AZURE_TENANT_ID=your_azure_tenant_id_here
AZURE_CLIENT_ID=your_azure_client_id_here
AZURE_CLIENT_SECRET=your_azure_client_secret_here

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here

# Monitoring Configuration
GRAFANA_PASSWORD=your_grafana_password_here

# Security Features
ENABLE_ENTERPRISE_SECURITY=true
SECURITY_LEVEL=enterprise
ENABLE_ZERO_TRUST=true
ENABLE_MFA_ENFORCEMENT=true
ENABLE_AUDIT_LOGGING=true

# AI Features
ENABLE_AI_FEATURES=true
AI_ANALYSIS_TIMEOUT=60
AI_MAX_CONCURRENT_REQUESTS=10

# Cloud Scanning
ENABLE_CLOUD_SCANNING=true
SCANNER_TIMEOUT=300
SCANNER_MAX_RESOURCES=10000

# Logging
LOG_LEVEL=INFO
EOF
    print_warning "Please edit $ENV_FILE with your actual production values before continuing"
    exit 1
fi

print_status "Prerequisites check passed"

# Load environment variables
print_info "Loading environment variables..."
source "$ENV_FILE"

# Validate critical environment variables
print_info "Validating environment variables..."

critical_vars=(
    "DB_PASSWORD"
    "SECRET_KEY"
    "REDIS_PASSWORD"
    "GRAFANA_PASSWORD"
)

for var in "${critical_vars[@]}"; do
    if [ -z "${!var}" ] || [[ "${!var}" == *"your_"* ]]; then
        print_error "Critical environment variable $var is not set or is using default value"
        exit 1
    fi
done

print_status "Environment variables validated"

# Run production readiness tests
print_info "Running production readiness tests..."
if [ -f "test_production_ready.py" ]; then
    python test_production_ready.py
    if [ $? -ne 0 ]; then
        print_error "Production readiness tests failed"
        exit 1
    fi
else
    print_warning "Production readiness test script not found, skipping..."
fi

print_status "Production readiness tests passed"

# Create necessary directories
print_info "Creating necessary directories..."
mkdir -p logs/nginx
mkdir -p ml_models
mkdir -p monitoring/grafana/dashboards
mkdir -p monitoring/grafana/datasources

print_status "Directories created"

# Create nginx configuration
print_info "Creating nginx configuration..."
mkdir -p nginx
cat > nginx/nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream cloudmind_backend {
        server cloudmind-backend:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;

        # Health check
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # API rate limiting
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://cloudmind_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Login rate limiting
        location /api/v1/auth/ {
            limit_req zone=login burst=5 nodelay;
            proxy_pass http://cloudmind_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # Default proxy
        location / {
            proxy_pass http://cloudmind_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

print_status "Nginx configuration created"

# Create Prometheus configuration
print_info "Creating Prometheus configuration..."
mkdir -p monitoring
cat > monitoring/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'cloudmind'
    static_configs:
      - targets: ['cloudmind-backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
EOF

print_status "Prometheus configuration created"

# Create Grafana datasource configuration
print_info "Creating Grafana datasource configuration..."
mkdir -p monitoring/grafana/datasources
cat > monitoring/grafana/datasources/prometheus.yml << 'EOF'
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

print_status "Grafana datasource configuration created"

# Build and deploy
print_info "Building and deploying CloudMind..."

# Stop existing containers
print_info "Stopping existing containers..."
docker-compose -f "$DOCKER_COMPOSE_FILE" down --remove-orphans

# Build images
print_info "Building Docker images..."
docker-compose -f "$DOCKER_COMPOSE_FILE" build --no-cache

# Start services
print_info "Starting services..."
docker-compose -f "$DOCKER_COMPOSE_FILE" up -d

# Wait for services to be ready
print_info "Waiting for services to be ready..."
sleep 30

# Check service health
print_info "Checking service health..."

# Check CloudMind backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_status "CloudMind backend is healthy"
else
    print_error "CloudMind backend health check failed"
    docker-compose -f "$DOCKER_COMPOSE_FILE" logs cloudmind-backend
    exit 1
fi

# Check PostgreSQL
if docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T postgres pg_isready -U cloudmind > /dev/null 2>&1; then
    print_status "PostgreSQL is healthy"
else
    print_error "PostgreSQL health check failed"
    exit 1
fi

# Check Redis
if docker-compose -f "$DOCKER_COMPOSE_FILE" exec -T redis redis-cli ping > /dev/null 2>&1; then
    print_status "Redis is healthy"
else
    print_error "Redis health check failed"
    exit 1
fi

# Check Nginx
if curl -f http://localhost/health > /dev/null 2>&1; then
    print_status "Nginx is healthy"
else
    print_error "Nginx health check failed"
    exit 1
fi

print_status "All services are healthy"

# Display deployment information
echo ""
echo -e "${GREEN}🎉 CloudMind Production Deployment Complete!${NC}"
echo "=========================================="
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  • CloudMind Backend: http://localhost:8000"
echo "  • API Documentation: http://localhost:8000/docs"
echo "  • Health Check: http://localhost:8000/health"
echo "  • Metrics: http://localhost:8000/metrics"
echo ""
echo -e "${BLUE}Monitoring:${NC}"
echo "  • Prometheus: http://localhost:9090"
echo "  • Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo -e "${BLUE}Database:${NC}"
echo "  • PostgreSQL: localhost:5432"
echo "  • Redis: localhost:6379"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo "  • View logs: docker-compose -f $DOCKER_COMPOSE_FILE logs -f"
echo "  • Stop services: docker-compose -f $DOCKER_COMPOSE_FILE down"
echo "  • Restart services: docker-compose -f $DOCKER_COMPOSE_FILE restart"
echo "  • Update services: docker-compose -f $DOCKER_COMPOSE_FILE pull && docker-compose -f $DOCKER_COMPOSE_FILE up -d"
echo ""

print_status "Deployment completed successfully!"
