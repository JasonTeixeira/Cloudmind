#!/bin/bash
# =============================================================================
# CLOUDMIND DEPLOYMENT SCRIPT
# =============================================================================

set -e

# Configuration
DOMAIN="cloudmind.local"
EMAIL="admin@cloudmind.local"
BACKUP_DIR="/backup/cloudmind"
LOG_FILE="/var/log/cloudmind/deploy.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a $LOG_FILE
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a $LOG_FILE
    exit 1
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a $LOG_FILE
}

# Pre-deployment checks
pre_deploy_checks() {
    log "Running pre-deployment checks..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
    fi
    
    # Check disk space
    available_space=$(df -BG / | awk 'NR==2 {print $4}' | sed 's/G//')
    if [ $available_space -lt 50 ]; then
        error "Insufficient disk space. At least 50GB required."
    fi
    
    # Check memory
    total_memory=$(free -g | awk 'NR==2 {print $2}')
    if [ $total_memory -lt 16 ]; then
        warning "Less than 16GB RAM detected. Performance may be impacted."
    fi
    
    log "Pre-deployment checks passed"
}

# Backup current deployment
backup_current() {
    log "Creating backup of current deployment..."
    
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_path="$BACKUP_DIR/$timestamp"
    mkdir -p $backup_path
    
    # Backup databases
    log "Backing up PostgreSQL..."
    docker exec cloudmind_postgres_1 pg_dumpall -U cloudmind > $backup_path/postgres_backup.sql
    
    log "Backing up Redis..."
    docker exec cloudmind_redis_1 redis-cli BGSAVE
    docker cp cloudmind_redis_1:/data/dump.rdb $backup_path/
    
    # Backup volumes
    log "Backing up Docker volumes..."
    for volume in $(docker volume ls -q | grep cloudmind); do
        docker run --rm -v $volume:/data -v $backup_path:/backup alpine tar czf /backup/$volume.tar.gz -C /data .
    done
    
    # Backup configurations
    cp -r ./infrastructure $backup_path/
    
    log "Backup completed at $backup_path"
}

# Update code
update_code() {
    log "Updating code from repository..."
    
    # Stash local changes
    git stash
    
    # Pull latest changes
    git pull origin main
    
    # Update submodules if any
    git submodule update --init --recursive
    
    log "Code updated successfully"
}

# Build images
build_images() {
    log "Building Docker images..."
    
    # Build with BuildKit for better caching
    export DOCKER_BUILDKIT=1
    
    # Build all services
    docker-compose -f docker-compose.prod.yml build --parallel
    
    log "Images built successfully"
}

# Database migrations
run_migrations() {
    log "Running database migrations..."
    
    # Run Alembic migrations
    docker-compose -f docker-compose.prod.yml run --rm backend alembic upgrade head
    
    log "Migrations completed"
}

# Deploy services
deploy_services() {
    log "Deploying services..."
    
    # Stop current services
    docker-compose -f docker-compose.prod.yml down
    
    # Start new services
    docker-compose -f docker-compose.prod.yml up -d
    
    # Wait for services to be healthy
    log "Waiting for services to be healthy..."
    sleep 30
    
    # Check health
    services=("frontend" "backend" "postgres" "redis")
    for service in "${services[@]}"; do
        if docker-compose -f docker-compose.prod.yml ps | grep -q "${service}.*Up"; then
            log "$service is running"
        else
            error "$service failed to start"
        fi
    done
    
    log "All services deployed successfully"
}

# Post-deployment tasks
post_deployment() {
    log "Running post-deployment tasks..."
    
    # Warm up caches
    docker-compose -f docker-compose.prod.yml exec -T backend python -m app.scripts.warm_cache
    
    # Run initial cost analysis for all projects
    docker-compose -f docker-compose.prod.yml exec -T backend python -m app.scripts.initial_analysis
    
    # Update search indices
    docker-compose -f docker-compose.prod.yml exec -T backend python -m app.scripts.update_search_index
    
    # Generate sitemap
    docker-compose -f docker-compose.prod.yml exec -T frontend npm run generate-sitemap
    
    log "Post-deployment tasks completed"
}

# SSL setup
setup_ssl() {
    log "Setting up SSL certificates..."
    
    # Check if certificates exist
    if [ ! -f "./infrastructure/nginx/ssl/cert.pem" ]; then
        # Use certbot for Let's Encrypt
        docker run --rm -v $(pwd)/infrastructure/nginx/ssl:/etc/letsencrypt \
            -v $(pwd)/infrastructure/nginx/ssl:/var/lib/letsencrypt \
            -p 80:80 \
            certbot/certbot certonly \
            --standalone \
            --non-interactive \
            --agree-tos \
            --email $EMAIL \
            -d $DOMAIN
    else
        log "SSL certificates already exist"
    fi
}

# Health check
health_check() {
    log "Running health checks..."
    
    # Check frontend
    if curl -f http://localhost:3000/health > /dev/null 2>&1; then
        log "Frontend health check passed"
    else
        error "Frontend health check failed"
    fi
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log "Backend health check passed"
    else
        error "Backend health check failed"
    fi
    
    # Check databases
    docker-compose -f docker-compose.prod.yml exec -T postgres pg_isready -U cloudmind
    docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping
    
    log "All health checks passed"
}

# Monitoring setup
setup_monitoring() {
    log "Setting up monitoring alerts..."
    
    # Configure Prometheus alerts
    docker-compose -f docker-compose.prod.yml exec -T prometheus promtool check rules /etc/prometheus/rules/*.yml
    
    # Reload Prometheus configuration
    docker-compose -f docker-compose.prod.yml exec -T prometheus kill -HUP 1
    
    log "Monitoring configured"
}

# Main deployment flow
main() {
    log "Starting CloudMind deployment..."
    
    pre_deploy_checks
    backup_current
    update_code
    build_images
    run_migrations
    deploy_services
    post_deployment
    setup_ssl
    health_check
    setup_monitoring
    
    log "CloudMind deployment completed successfully!"
    log "Access the application at https://$DOMAIN"
}

# Run main function
main 