# CloudMind Deployment Guide

## Overview

This guide covers deploying CloudMind across different environments, from local development to production. The platform supports multiple deployment strategies including Docker Compose, Kubernetes, and cloud-native deployments.

## Prerequisites

### System Requirements

- **CPU**: 4+ cores (8+ for production)
- **RAM**: 8GB minimum (16GB+ for production)
- **Storage**: 50GB+ SSD storage
- **Network**: Stable internet connection for cloud provider APIs

### Software Requirements

- **Docker**: 20.10+ with Docker Compose
- **Docker Compose**: 2.0+
- **Git**: Latest version
- **Make**: For automation scripts
- **kubectl**: For Kubernetes deployments
- **helm**: For Kubernetes package management

### Cloud Provider Access

- **AWS**: IAM credentials with appropriate permissions
- **Azure**: Service Principal with contributor role
- **GCP**: Service account with compute admin role

## Local Development Deployment

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/cloudmind.git
   cd cloudmind
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   make dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Documentation: http://localhost:8080

### Development Environment Configuration

Create a `.env` file for local development:

```bash
# Application
APP_NAME=CloudMind
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/cloudmind_dev

# Redis
REDIS_URL=redis://localhost:6379/0

# Cloud Provider Credentials
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_REGION=us-east-1

# AI/ML Services
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

### Docker Compose Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## Staging Environment

### Deployment Steps

1. **Prepare staging environment**
   ```bash
   # Set environment
   export ENV=staging
   
   # Create staging configuration
   cp env.example .env.staging
   ```

2. **Deploy to staging**
   ```bash
   make deploy-staging
   ```

3. **Run staging tests**
   ```bash
   make test-staging
   ```

### Staging Configuration

```bash
# Staging environment variables
APP_ENV=staging
DEBUG=false
DATABASE_URL=postgresql://user:pass@staging-db:5432/cloudmind_staging
REDIS_URL=redis://staging-redis:6379/0

# Staging-specific settings
LOG_LEVEL=info
CORS_ORIGINS=https://staging.cloudmind.local
RATE_LIMIT_ENABLED=true
```

## Production Deployment

### Pre-deployment Checklist

- [ ] Security audit completed
- [ ] Performance testing passed
- [ ] Database migrations tested
- [ ] SSL certificates configured
- [ ] Monitoring and alerting set up
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan ready

### Production Configuration

```bash
# Production environment variables
APP_ENV=production
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@prod-db:5432/cloudmind_prod
REDIS_URL=redis://prod-redis:6379/0

# Security settings
CORS_ORIGINS=https://cloudmind.local
RATE_LIMIT_ENABLED=true
SECURITY_HEADERS_ENABLED=true

# Performance settings
WORKER_PROCESSES=4
MAX_CONNECTIONS=1000
```

### Production Deployment Steps

1. **Prepare production environment**
   ```bash
   # Set production environment
   export ENV=production
   
   # Create production configuration
   cp env.example .env.production
   ```

2. **Run pre-deployment checks**
   ```bash
   make pre-deploy-check
   ```

3. **Deploy to production**
   ```bash
   make deploy-production
   ```

4. **Verify deployment**
   ```bash
   make verify-deployment
   ```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.20+)
- Helm 3.0+
- kubectl configured
- Ingress controller installed

### Helm Chart Deployment

1. **Add the Helm repository**
   ```bash
   helm repo add cloudmind https://charts.cloudmind.local
   helm repo update
   ```

2. **Create namespace**
   ```bash
   kubectl create namespace cloudmind
   ```

3. **Install CloudMind**
   ```bash
   helm install cloudmind cloudmind/cloudmind \
     --namespace cloudmind \
     --values values-production.yaml
   ```

### Custom Values File

Create `values-production.yaml`:

```yaml
# Application configuration
app:
  replicaCount: 3
  image:
    repository: cloudmind/backend
    tag: latest
    pullPolicy: Always
  
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "500m"

# Database configuration
database:
  enabled: true
  type: postgresql
  host: cloudmind-postgresql
  port: 5432
  database: cloudmind_prod
  username: cloudmind
  password: your-secure-password

# Redis configuration
redis:
  enabled: true
  host: cloudmind-redis
  port: 6379
  password: your-redis-password

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: cloudmind.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: cloudmind-tls
      hosts:
        - cloudmind.local

# Monitoring
monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
```

### Kubernetes Commands

```bash
# Deploy application
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n cloudmind

# View logs
kubectl logs -f deployment/cloudmind-backend -n cloudmind

# Scale deployment
kubectl scale deployment cloudmind-backend --replicas=5 -n cloudmind

# Update deployment
kubectl set image deployment/cloudmind-backend backend=cloudmind/backend:v2.0.0 -n cloudmind
```

## Cloud-Native Deployment

### AWS ECS Deployment

1. **Create ECS cluster**
   ```bash
   aws ecs create-cluster --cluster-name cloudmind
   ```

2. **Create task definition**
   ```json
   {
     "family": "cloudmind",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "backend",
         "image": "cloudmind/backend:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "APP_ENV",
             "value": "production"
           }
         ]
       }
     ]
   }
   ```

3. **Deploy service**
   ```bash
   aws ecs create-service \
     --cluster cloudmind \
     --service-name cloudmind-backend \
     --task-definition cloudmind:1 \
     --desired-count 3
   ```

### Google Cloud Run

1. **Build and push image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/cloudmind
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy cloudmind \
     --image gcr.io/PROJECT_ID/cloudmind \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Database Migration

### Migration Commands

```bash
# Create migration
alembic revision --autogenerate -m "Add new table"

# Run migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
alembic history
```

### Production Migration Checklist

- [ ] Backup database before migration
- [ ] Test migration on staging environment
- [ ] Schedule maintenance window
- [ ] Monitor migration progress
- [ ] Verify data integrity after migration
- [ ] Update application configuration if needed

## SSL/TLS Configuration

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot

# Obtain certificate
sudo certbot certonly --standalone -d cloudmind.local

# Configure nginx
sudo cp /etc/letsencrypt/live/cloudmind.local/fullchain.pem /etc/nginx/ssl/
sudo cp /etc/letsencrypt/live/cloudmind.local/privkey.pem /etc/nginx/ssl/
```

### Auto-renewal

```bash
# Add to crontab
sudo crontab -e

# Add this line
0 12 * * * /usr/bin/certbot renew --quiet
```

## Monitoring and Logging

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'cloudmind'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

### Grafana Dashboard

Import the CloudMind dashboard JSON to Grafana for comprehensive monitoring.

### Log Aggregation

```bash
# Configure log forwarding
docker run -d \
  --name fluentd \
  -v /var/log:/var/log \
  -v /var/lib/docker/containers:/var/lib/docker/containers \
  fluent/fluentd-kubernetes-daemonset:v1.14-debian-elasticsearch7-1.0
```

## Backup and Recovery

### Database Backup

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump cloudmind_prod > $BACKUP_DIR/cloudmind_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/cloudmind_$DATE.sql

# Upload to S3
aws s3 cp $BACKUP_DIR/cloudmind_$DATE.sql.gz s3://cloudmind-backups/
```

### Automated Backup Schedule

```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Disaster Recovery

1. **Create recovery plan**
   ```bash
   # Document recovery procedures
   # Test recovery procedures regularly
   # Maintain backup verification
   ```

2. **Recovery testing**
   ```bash
   # Test backup restoration
   # Verify data integrity
   # Document recovery time objectives
   ```

## Security Hardening

### Network Security

```bash
# Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### Application Security

```bash
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000" always;
```

### Secrets Management

```bash
# Use external secrets manager
aws secretsmanager create-secret \
  --name cloudmind/database \
  --secret-string '{"username":"cloudmind","password":"secure-password"}'
```

## Performance Optimization

### Application Tuning

```bash
# Optimize worker processes
WORKER_PROCESSES=4
MAX_CONNECTIONS=1000

# Enable caching
REDIS_CACHE_ENABLED=true
CACHE_TTL=3600
```

### Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_projects_user_id ON projects(user_id);

-- Optimize queries
EXPLAIN ANALYZE SELECT * FROM projects WHERE user_id = ?;
```

### CDN Configuration

```bash
# Configure CloudFront
aws cloudfront create-distribution \
  --origin-domain-name cloudmind.local \
  --default-root-object index.html
```

## Troubleshooting

### Common Issues

1. **Database connection issues**
   ```bash
   # Check database connectivity
   nc -zv database-host 5432
   
   # Test connection
   psql -h database-host -U username -d database
   ```

2. **Redis connection issues**
   ```bash
   # Check Redis connectivity
   redis-cli -h redis-host ping
   
   # Monitor Redis
   redis-cli -h redis-host monitor
   ```

3. **Application startup issues**
   ```bash
   # Check application logs
   docker-compose logs backend
   
   # Check environment variables
   docker-compose exec backend env
   ```

### Debug Commands

```bash
# Check system resources
htop
df -h
free -h

# Check network connectivity
netstat -tulpn
ss -tulpn

# Check application status
curl -f http://localhost:8000/health
```

## Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Review application logs
   - Check system resources
   - Update security patches

2. **Monthly**
   - Review performance metrics
   - Update dependencies
   - Test backup restoration

3. **Quarterly**
   - Security audit
   - Performance optimization
   - Disaster recovery testing

### Update Procedures

```bash
# Update application
git pull origin main
docker-compose build
docker-compose up -d

# Update dependencies
pip install -r requirements.txt --upgrade
npm update

# Database migrations
alembic upgrade head
```

## Support and Documentation

### Getting Help

- **Documentation**: https://docs.cloudmind.local
- **GitHub Issues**: https://github.com/cloudmind/issues
- **Support Email**: support@cloudmind.local
- **Slack Channel**: #cloudmind-support

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Release Process

```bash
# Create release
git tag v1.0.0
git push origin v1.0.0

# Deploy release
make release v1.0.0
```

This deployment guide provides comprehensive instructions for deploying CloudMind across various environments. Always test changes in staging before deploying to production. 