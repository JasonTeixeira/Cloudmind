#!/bin/bash

# Security Maintenance Script for Self-Hosted CloudMind
# This script provides ongoing security maintenance without cloud services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LOG_DIR="./logs"
SECRETS_DIR="./secrets"
BACKUP_DIR="./backups"
MAINTENANCE_LOG="$LOG_DIR/maintenance.log"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "$(date): [INFO] $1" >> "$MAINTENANCE_LOG"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
    echo "$(date): [WARNING] $1" >> "$MAINTENANCE_LOG"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "$(date): [ERROR] $1" >> "$MAINTENANCE_LOG"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE} $1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Create log directory
mkdir -p "$LOG_DIR"

# Daily security maintenance
daily_maintenance() {
    print_header "Daily Security Maintenance"
    
    # Check service health
    print_status "Checking service health..."
    local services=("backend" "frontend" "nginx" "postgres" "redis" "minio" "neo4j")
    local unhealthy_services=()
    
    for service in "${services[@]}"; do
        if ! docker ps | grep -q "cloudmind-$service"; then
            unhealthy_services+=("$service")
            print_warning "Service $service is down"
        fi
    done
    
    if [ ${#unhealthy_services[@]} -gt 0 ]; then
        print_error "Unhealthy services detected: ${unhealthy_services[*]}"
        # Attempt to restart unhealthy services
        for service in "${unhealthy_services[@]}"; do
            print_status "Restarting $service..."
            docker restart "cloudmind-$service" || print_error "Failed to restart $service"
        done
    else
        print_status "All services are healthy"
    fi
    
    # Check disk space
    print_status "Checking disk space..."
    local disk_usage=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 80 ]; then
        print_warning "Disk usage is high: ${disk_usage}%"
        # Clean up old logs
        find "$LOG_DIR" -name "*.log" -mtime +7 -delete
        print_status "Cleaned up old log files"
    else
        print_status "Disk usage is normal: ${disk_usage}%"
    fi
    
    # Check for security events
    print_status "Checking security events..."
    local security_events=$(grep -c "WARNING\|ERROR" "$LOG_DIR/security.log" 2>/dev/null || echo "0")
    if [ "$security_events" -gt 10 ]; then
        print_warning "High number of security events: $security_events"
    else
        print_status "Security events are normal: $security_events"
    fi
    
    # Rotate logs
    print_status "Rotating logs..."
    if [ -f "$LOG_DIR/security.log" ] && [ $(stat -f%z "$LOG_DIR/security.log" 2>/dev/null || echo "0") -gt 10485760 ]; then
        mv "$LOG_DIR/security.log" "$LOG_DIR/security.log.$(date +%Y%m%d)"
        print_status "Rotated security log"
    fi
}

# Weekly security maintenance
weekly_maintenance() {
    print_header "Weekly Security Maintenance"
    
    # Update system packages
    print_status "Updating system packages..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get upgrade -y
    elif command -v yum &> /dev/null; then
        sudo yum update -y
    fi
    
    # Update Docker images
    print_status "Updating Docker images..."
    docker system prune -f
    docker-compose -f infrastructure/docker/security-hardened.yml pull
    
    # Backup secrets
    print_status "Backing up secrets..."
    if [ -f "$SECRETS_DIR/secrets.env" ]; then
        cp "$SECRETS_DIR/secrets.env" "$BACKUP_DIR/secrets_backup_$(date +%Y%m%d).env"
    fi
    
    # Check SSL certificate expiration
    print_status "Checking SSL certificate..."
    if [ -f "./infrastructure/docker/nginx/ssl/cert.pem" ]; then
        local expiry_date=$(openssl x509 -enddate -noout -in "./infrastructure/docker/nginx/ssl/cert.pem" | cut -d= -f2)
        local expiry_timestamp=$(date -j -f "%b %d %H:%M:%S %Y %Z" "$expiry_date" +%s 2>/dev/null || echo "0")
        local current_timestamp=$(date +%s)
        local days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
        
        if [ "$days_until_expiry" -lt 30 ]; then
            print_warning "SSL certificate expires in $days_until_expiry days"
        else
            print_status "SSL certificate is valid for $days_until_expiry days"
        fi
    fi
    
    # Security audit
    print_status "Running security audit..."
    if [ -f "scripts/security/security_test.py" ]; then
        python scripts/security/security_test.py --silent
    fi
    
    # Clean up old backups
    print_status "Cleaning up old backups..."
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +30 -delete
    find "$BACKUP_DIR" -name "secrets_backup_*.env" -mtime +30 -delete
}

# Monthly security maintenance
monthly_maintenance() {
    print_header "Monthly Security Maintenance"
    
    # Rotate secrets
    print_status "Rotating secrets..."
    if [ -f "scripts/security/manage_secrets.sh" ]; then
        ./scripts/security/manage_secrets.sh rotate
    fi
    
    # Generate new SSL certificates
    print_status "Generating new SSL certificates..."
    if [ -f "./infrastructure/docker/nginx/ssl/cert.pem" ]; then
        local cert_age=$(find "./infrastructure/docker/nginx/ssl/cert.pem" -printf '%T@' | cut -d. -f1)
        local current_time=$(date +%s)
        local days_old=$(( (current_time - cert_age) / 86400 ))
        
        if [ "$days_old" -gt 30 ]; then
            print_status "Generating new SSL certificate..."
            openssl genrsa -out "./infrastructure/docker/nginx/ssl/key.pem" 2048
            openssl req -new -key "./infrastructure/docker/nginx/ssl/key.pem" \
                -out "./infrastructure/docker/nginx/ssl/cert.csr" \
                -subj "/C=US/ST=State/L=City/O=CloudMind/OU=IT/CN=cloudmind.local"
            openssl x509 -req -in "./infrastructure/docker/nginx/ssl/cert.csr" \
                -signkey "./infrastructure/docker/nginx/ssl/key.pem" \
                -out "./infrastructure/docker/nginx/ssl/cert.pem" \
                -days 365
            chmod 600 "./infrastructure/docker/nginx/ssl/key.pem"
            chmod 644 "./infrastructure/docker/nginx/ssl/cert.pem"
            
            # Restart nginx to use new certificate
            docker restart cloudmind-nginx
        fi
    fi
    
    # Comprehensive security scan
    print_status "Running comprehensive security scan..."
    
    # Check for vulnerabilities in dependencies
    if [ -d "backend" ]; then
        cd backend
        pip-audit --format=json --output=security_audit.json || true
        if [ -f "security_audit.json" ]; then
            local vulnerabilities=$(jq '.vulnerabilities | length' security_audit.json 2>/dev/null || echo "0")
            if [ "$vulnerabilities" -gt 0 ]; then
                print_warning "Found $vulnerabilities vulnerabilities in backend dependencies"
            else
                print_status "Backend dependencies are secure"
            fi
            rm -f security_audit.json
        fi
        cd ..
    fi
    
    if [ -d "frontend" ]; then
        cd frontend
        npm audit --audit-level=high || true
        cd ..
    fi
    
    # Database maintenance
    print_status "Performing database maintenance..."
    docker exec cloudmind-postgres psql -U cloudmind -d cloudmind -c "VACUUM ANALYZE;" || true
    
    # Backup database
    print_status "Creating database backup..."
    docker exec cloudmind-postgres pg_dumpall -U cloudmind > "$BACKUP_DIR/database_backup_$(date +%Y%m%d).sql"
}

# Emergency security response
emergency_response() {
    print_header "Emergency Security Response"
    
    # Stop all services
    print_status "Stopping all services..."
    docker-compose -f infrastructure/docker/security-hardened.yml down
    
    # Backup current state
    print_status "Creating emergency backup..."
    tar -czf "$BACKUP_DIR/emergency_backup_$(date +%Y%m%d_%H%M%S).tar.gz" \
        --exclude=node_modules \
        --exclude=.git \
        .
    
    # Rotate all secrets
    print_status "Rotating all secrets..."
    if [ -f "scripts/security/manage_secrets.sh" ]; then
        ./scripts/security/manage_secrets.sh rotate
    fi
    
    # Generate new SSL certificates
    print_status "Generating new SSL certificates..."
    rm -f "./infrastructure/docker/nginx/ssl/cert.pem" "./infrastructure/docker/nginx/ssl/key.pem"
    openssl genrsa -out "./infrastructure/docker/nginx/ssl/key.pem" 2048
    openssl req -new -key "./infrastructure/docker/nginx/ssl/key.pem" \
        -out "./infrastructure/docker/nginx/ssl/cert.csr" \
        -subj "/C=US/ST=State/L=City/O=CloudMind/OU=IT/CN=cloudmind.local"
    openssl x509 -req -in "./infrastructure/docker/nginx/ssl/cert.csr" \
        -signkey "./infrastructure/docker/nginx/ssl/key.pem" \
        -out "./infrastructure/docker/nginx/ssl/cert.pem" \
        -days 365
    chmod 600 "./infrastructure/docker/nginx/ssl/key.pem"
    chmod 644 "./infrastructure/docker/nginx/ssl/cert.pem"
    
    # Restart services
    print_status "Restarting services..."
    docker-compose -f infrastructure/docker/security-hardened.yml up -d
    
    print_status "Emergency response completed"
}

# Security monitoring
security_monitoring() {
    print_header "Security Monitoring"
    
    # Check for failed login attempts
    local failed_logins=$(docker logs cloudmind-backend 2>&1 | grep -c "Failed login attempt" || echo "0")
    if [ "$failed_logins" -gt 5 ]; then
        print_warning "High number of failed login attempts: $failed_logins"
    fi
    
    # Check for suspicious requests
    local suspicious_requests=$(docker logs cloudmind-nginx 2>&1 | grep -c "suspicious\|blocked" || echo "0")
    if [ "$suspicious_requests" -gt 10 ]; then
        print_warning "High number of suspicious requests: $suspicious_requests"
    fi
    
    # Check for system resources
    local memory_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
    if [ "$memory_usage" -gt 80 ]; then
        print_warning "High memory usage: ${memory_usage}%"
    fi
    
    local cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    if [ "$cpu_usage" -gt 80 ]; then
        print_warning "High CPU usage: ${cpu_usage}%"
    fi
    
    # Check for unauthorized access attempts
    local unauthorized_attempts=$(docker logs cloudmind-nginx 2>&1 | grep -c "403\|401" || echo "0")
    if [ "$unauthorized_attempts" -gt 20 ]; then
        print_warning "High number of unauthorized access attempts: $unauthorized_attempts"
    fi
}

# Main script logic
case "${1:-daily}" in
    "daily")
        daily_maintenance
        ;;
    "weekly")
        weekly_maintenance
        ;;
    "monthly")
        monthly_maintenance
        ;;
    "emergency")
        emergency_response
        ;;
    "monitor")
        security_monitoring
        ;;
    "help"|*)
        echo "CloudMind Security Maintenance"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  daily     - Run daily security maintenance"
        echo "  weekly    - Run weekly security maintenance"
        echo "  monthly   - Run monthly security maintenance"
        echo "  emergency - Emergency security response"
        echo "  monitor   - Security monitoring check"
        echo "  help      - Show this help message"
        echo ""
        echo "Maintenance Features:"
        echo "  - Service health monitoring"
        echo "  - Security event tracking"
        echo "  - Log rotation and cleanup"
        echo "  - SSL certificate management"
        echo "  - Secret rotation"
        echo "  - System updates"
        echo "  - Database maintenance"
        echo "  - Emergency response procedures"
        ;;
esac 