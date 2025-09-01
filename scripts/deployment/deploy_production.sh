#!/bin/bash

# CloudMind Production Deployment Script
# This script automates the complete production deployment process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOMAIN="${DOMAIN:-cloudmind.local}"
EMAIL="${EMAIL:-admin@cloudmind.local}"
DB_PASSWORD="${DB_PASSWORD:-changeme123}"
REDIS_PASSWORD="${REDIS_PASSWORD:-changeme123}"
SECRET_KEY="${SECRET_KEY:-$(openssl rand -hex 32)}"
GRAFANA_PASSWORD="${GRAFANA_PASSWORD:-changeme123}"
SLACK_WEBHOOK_URL="${SLACK_WEBHOOK_URL:-}"

echo -e "${BLUE}🚀 CloudMind Production Deployment${NC}"
echo -e "${BLUE}================================${NC}"
echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo "Project Root: $PROJECT_ROOT"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"
if ! command_exists docker; then
    print_error "Docker is not installed"
    exit 1
fi

if ! command_exists docker-compose; then
    print_error "Docker Compose is not installed"
    exit 1
fi

print_status "Prerequisites check passed"

# Create necessary directories
echo -e "${BLUE}Creating directories...${NC}"
mkdir -p "$PROJECT_ROOT/infrastructure/docker/nginx/ssl"
mkdir -p "$PROJECT_ROOT/infrastructure/docker/nginx/certbot"
mkdir -p "$PROJECT_ROOT/logs"
print_status "Directories created"

# Set environment variables
echo -e "${BLUE}Setting environment variables...${NC}"
export DOMAIN="$DOMAIN"
export EMAIL="$EMAIL"
export DB_PASSWORD="$DB_PASSWORD"
export REDIS_PASSWORD="$REDIS_PASSWORD"
export SECRET_KEY="$SECRET_KEY"
export GRAFANA_PASSWORD="$GRAFANA_PASSWORD"
export SLACK_WEBHOOK_URL="$SLACK_WEBHOOK_URL"
print_status "Environment variables set"

# Start base services (DB, Redis, Nginx for ACME)
echo -e "${BLUE}Starting base services...${NC}"
cd "$PROJECT_ROOT"
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d postgres redis nginx

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
if ! docker-compose -f infrastructure/docker/docker-compose.prod.yml ps | grep -q "Up"; then
    print_error "Base services failed to start"
    docker-compose -f infrastructure/docker/docker-compose.prod.yml logs
    exit 1
fi
print_status "Base services started"

# Issue TLS certificate
echo -e "${BLUE}Issuing TLS certificate...${NC}"
if [ "$DOMAIN" != "cloudmind.local" ]; then
    docker run --rm \
        -v "$PROJECT_ROOT/infrastructure/docker/nginx/ssl:/etc/letsencrypt" \
        -v "$PROJECT_ROOT/infrastructure/docker/nginx/certbot:/var/www/certbot" \
        certbot/certbot certonly --webroot -w /var/www/certbot \
        -d "$DOMAIN" -m "$EMAIL" --agree-tos --non-interactive --staging
    
    if [ $? -eq 0 ]; then
        print_status "TLS certificate issued (staging)"
        print_warning "For production, remove --staging flag"
    else
        print_warning "TLS certificate issuance failed, continuing with HTTP"
    fi
else
    print_warning "Using local domain, skipping TLS certificate"
fi

# Start full production stack
echo -e "${BLUE}Starting full production stack...${NC}"
docker-compose -f infrastructure/docker/docker-compose.prod.yml up -d

# Start tracing stack
echo -e "${BLUE}Starting tracing stack...${NC}"
docker-compose -f infrastructure/docker/tempo/docker-compose.tempo.yml up -d

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
sleep 15

# Run database migrations
echo -e "${BLUE}Running database migrations...${NC}"
docker-compose -f infrastructure/docker/docker-compose.prod.yml exec -T cloudmind-backend alembic upgrade head
if [ $? -eq 0 ]; then
    print_status "Database migrations completed"
else
    print_error "Database migrations failed"
    exit 1
fi

# Health checks
echo -e "${BLUE}Performing health checks...${NC}"
PROTOCOL="http"
if [ "$DOMAIN" != "cloudmind.local" ]; then
    PROTOCOL="https"
fi

# Wait a bit more for services to fully initialize
sleep 10

# Check health endpoints
HEALTH_URL="$PROTOCOL://$DOMAIN/health"
READYZ_URL="$PROTOCOL://$DOMAIN/readyz"

echo "Checking health endpoint: $HEALTH_URL"
if curl -f -k "$HEALTH_URL" >/dev/null 2>&1; then
    print_status "Health endpoint is responding"
else
    print_error "Health endpoint is not responding"
    exit 1
fi

echo "Checking readyz endpoint: $READYZ_URL"
if curl -f -k "$READYZ_URL" >/dev/null 2>&1; then
    print_status "Readyz endpoint is responding"
else
    print_error "Readyz endpoint is not responding"
    exit 1
fi

# Load testing
echo -e "${BLUE}Running load tests...${NC}"
if command_exists k6; then
    echo "Running k6 load test..."
    k6 run -e BASE_URL="$PROTOCOL://$DOMAIN" "$PROJECT_ROOT/scripts/testing/k6_load_test.js"
    if [ $? -eq 0 ]; then
        print_status "Load tests passed"
    else
        print_warning "Load tests failed or exceeded thresholds"
    fi
else
    print_warning "k6 not installed, skipping load tests"
    echo "Install k6: https://k6.io/docs/getting-started/installation/"
fi

# Final status
echo -e "${BLUE}Deployment Summary${NC}"
echo -e "${BLUE}==================${NC}"
print_status "Production deployment completed successfully!"
echo ""
echo -e "${BLUE}Access URLs:${NC}"
echo "Frontend: $PROTOCOL://$DOMAIN"
echo "API: $PROTOCOL://$DOMAIN/api"
echo "Health: $PROTOCOL://$DOMAIN/health"
echo ""
echo -e "${BLUE}Monitoring URLs:${NC}"
echo "Prometheus: http://localhost:9090"
echo "Grafana (Metrics): http://localhost:3000 (admin/$GRAFANA_PASSWORD)"
echo "Grafana (Traces): http://localhost:3002"
echo "Alertmanager: http://localhost:9093"
echo ""
echo -e "${BLUE}Useful Commands:${NC}"
echo "View logs: docker-compose -f infrastructure/docker/docker-compose.prod.yml logs -f"
echo "Stop services: docker-compose -f infrastructure/docker/docker-compose.prod.yml down"
echo "Restart backend: docker-compose -f infrastructure/docker/docker-compose.prod.yml restart cloudmind-backend"
echo ""
print_status "🎉 CloudMind is now running in production mode!"
