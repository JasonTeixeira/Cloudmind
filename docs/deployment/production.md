# 🚀 **Production Deployment Guide**

Complete guide for deploying CloudMind to production environments.

## 📋 **Prerequisites**

### **System Requirements**
- **OS**: Linux (Ubuntu 20.04+ recommended) or macOS
- **Docker**: 20.10+ with Docker Compose
- **Memory**: 8GB+ RAM (16GB+ recommended)
- **Storage**: 50GB+ available disk space
- **Network**: Stable internet connection for container pulls

### **Software Requirements**
```bash
# Check Docker installation
docker --version
docker-compose --version

# Check system resources
free -h
df -h
```

## 🔧 **Environment Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/your-org/cloudmind.git
cd cloudmind
```

### **2. Configure Environment**
```bash
# Copy environment template
cp env.example .env.production

# Edit production configuration
nano .env.production
```

### **3. Required Environment Variables**
```bash
# Critical (must be set)
DB_PASSWORD=your_secure_password_here
SECRET_KEY=your_very_secure_secret_key_here
REDIS_PASSWORD=your_redis_password_here
GRAFANA_PASSWORD=your_grafana_password_here

# Environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
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
```

### **4. Optional: Cloud Provider Integration**
```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_REGION=us-east-1

# Azure Configuration
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id_here
AZURE_TENANT_ID=your_azure_tenant_id_here
AZURE_CLIENT_ID=your_azure_client_id_here
AZURE_CLIENT_SECRET=your_azure_client_secret_here

# AI Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
```

## 🚀 **Deployment Process**

### **1. Pre-Deployment Validation**
```bash
cd backend

# Run comprehensive tests
python test_final_comprehensive.py

# Validate environment
python -c "import os; print('Environment validation:', all(os.getenv(k) for k in ['DB_PASSWORD', 'SECRET_KEY', 'REDIS_PASSWORD']))"
```

### **2. Deploy to Production**
```bash
# Make deployment script executable
chmod +x deploy_production.sh

# Run deployment
./deploy_production.sh
```

### **3. Verify Deployment**
```bash
# Check all services are running
docker-compose -f docker-compose.prod.yml ps

# Test health endpoints
curl -f http://localhost:8000/health
curl -f http://localhost/health

# Check logs for any errors
docker-compose -f docker-compose.prod.yml logs --tail=50
```

## 📊 **Post-Deployment Configuration**

### **1. Access Your Application**
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

### **2. Initial Setup**
```bash
# Create admin user (if needed)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@cloudmind.com", "password": "secure_password"}'

# Verify database connection
docker-compose -f docker-compose.prod.yml exec postgres psql -U cloudmind -d cloudmind -c "SELECT version();"
```

### **3. Configure Monitoring**
```bash
# Access Grafana and set up dashboards
# Default credentials: admin/admin
# Change password on first login

# Set up Prometheus alerts (optional)
# Edit monitoring/prometheus.yml for custom alerting rules
```

## 🔒 **Security Hardening**

### **1. SSL/TLS Configuration**
```bash
# For production, set up SSL certificates
# Update nginx/nginx.conf with SSL configuration
# Add certificates to nginx/ssl/ directory
```

### **2. Firewall Configuration**
```bash
# Configure firewall to allow only necessary ports
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw allow 22/tcp   # SSH
sudo ufw enable
```

### **3. Regular Security Updates**
```bash
# Set up automated security updates
sudo apt update && sudo apt upgrade -y

# Update Docker images regularly
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 📈 **Monitoring & Maintenance**

### **1. Health Monitoring**
```bash
# Set up health check monitoring
# Monitor these endpoints:
# - http://localhost:8000/health
# - http://localhost:8000/metrics
# - http://localhost:9090/-/healthy
```

### **2. Log Management**
```bash
# View application logs
docker-compose -f docker-compose.prod.yml logs -f cloudmind-backend

# View database logs
docker-compose -f docker-compose.prod.yml logs -f postgres

# Set up log rotation (recommended)
# Configure logrotate for /var/log/cloudmind/
```

### **3. Backup Strategy**
```bash
# Database backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U cloudmind cloudmind > backup_$(date +%Y%m%d_%H%M%S).sql

# Configuration backup
tar -czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz .env.production nginx/ monitoring/
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Service Won't Start**
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs [service-name]

# Check resource usage
docker stats

# Restart specific service
docker-compose -f docker-compose.prod.yml restart [service-name]
```

#### **2. Database Connection Issues**
```bash
# Check database status
docker-compose -f docker-compose.prod.yml exec postgres pg_isready -U cloudmind

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres
```

#### **3. Memory Issues**
```bash
# Check memory usage
free -h
docker stats

# Increase Docker memory limit if needed
# Edit /etc/docker/daemon.json
```

## 📚 **Next Steps**

1. **[Monitoring Setup](monitoring.md)** - Configure advanced monitoring
2. **[Security Configuration](security.md)** - Advanced security setup
3. **[Scaling Guide](scaling.md)** - Scale your deployment
4. **[Backup & Recovery](backup.md)** - Set up backup strategies

## 🆘 **Support**

- **Documentation**: [Complete Documentation Hub](../README.md)
- **Issues**: [GitHub Issues](https://github.com/cloudmind/issues)
- **Emergency**: [Emergency Procedures](emergency.md)

---

*For development deployment, see [Development Setup](../development/setup.md)*
