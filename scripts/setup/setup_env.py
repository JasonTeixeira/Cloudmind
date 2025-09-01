#!/usr/bin/env python3
"""
Simple Environment Setup for CloudMind Development
Phase 1: Foundation Fixes
"""

import os
import sys

def setup_development_environment():
    """Set up development environment variables"""
    
    # Basic application settings
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("DEBUG", "true")
    os.environ.setdefault("LOG_LEVEL", "INFO")
    
    # Database - Use SQLite for development
    os.environ.setdefault("DATABASE_URL", "sqlite:///./cloudmind.db")
    
    # Security - Development keys
    os.environ.setdefault("SECRET_KEY", "dev-secret-key-change-this-in-production-64-characters-long")
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    
    # JWT Security
    os.environ.setdefault("JWT_AUDIENCE", "cloudmind-api")
    os.environ.setdefault("JWT_ISSUER", "cloudmind-auth")
    os.environ.setdefault("JWT_LEEWAY", "10")
    
    # Redis - Local Redis
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS - Development
    os.environ.setdefault("ALLOWED_ORIGINS", '["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]')
    
    # Storage paths
    os.environ.setdefault("LOCAL_STORAGE_PATH", "./storage")
    os.environ.setdefault("GIT_REPOSITORIES_PATH", "./git-repos")
    os.environ.setdefault("TEMPLATE_STORAGE_PATH", "./templates")
    
    # Database pool settings
    os.environ.setdefault("DB_POOL_SIZE", "5")
    os.environ.setdefault("DB_MAX_OVERFLOW", "10")
    os.environ.setdefault("DB_POOL_TIMEOUT", "30")
    os.environ.setdefault("DB_POOL_RECYCLE", "1800")
    
    # Feature flags
    os.environ.setdefault("ENABLE_AI_FEATURES", "true")
    os.environ.setdefault("ENABLE_REAL_TIME_UPDATES", "true")
    os.environ.setdefault("ENABLE_AUDIT_LOGGING", "true")
    os.environ.setdefault("ENABLE_METRICS_COLLECTION", "true")
    os.environ.setdefault("ENABLE_SECURITY_SCANNING", "true")
    
    # Performance settings
    os.environ.setdefault("CACHE_TTL", "1800")
    os.environ.setdefault("SESSION_TIMEOUT", "1800")
    os.environ.setdefault("MAX_CONCURRENT_REQUESTS", "100")
    
    # Security headers - Development
    os.environ.setdefault("ENABLE_HSTS", "false")
    os.environ.setdefault("ENABLE_CSP", "false")
    os.environ.setdefault("ENABLE_XSS_PROTECTION", "true")
    os.environ.setdefault("ENABLE_CONTENT_TYPE_NOSNIFF", "true")
    os.environ.setdefault("ENABLE_FRAME_OPTIONS", "true")
    
    # Logging
    os.environ.setdefault("LOG_FORMAT", "text")
    os.environ.setdefault("LOG_FILE", "./logs/cloudmind.log")
    os.environ.setdefault("LOG_MAX_SIZE", "10485760")
    os.environ.setdefault("LOG_BACKUP_COUNT", "5")
    os.environ.setdefault("LOG_SECURITY_EVENTS", "true")
    
    # Health check
    os.environ.setdefault("HEALTH_CHECK_ENABLED", "true")
    os.environ.setdefault("HEALTH_CHECK_INTERVAL", "30")
    os.environ.setdefault("HEALTH_CHECK_TIMEOUT", "10")
    os.environ.setdefault("HEALTH_CHECK_AUTHENTICATION", "false")
    
    # Performance monitoring
    os.environ.setdefault("PERFORMANCE_MONITORING_ENABLED", "true")
    os.environ.setdefault("PERFORMANCE_MONITORING_INTERVAL", "60")
    os.environ.setdefault("PERFORMANCE_MONITORING_RETENTION_DAYS", "7")
    os.environ.setdefault("PERFORMANCE_DATA_ENCRYPTION", "false")
    
    # Error tracking
    os.environ.setdefault("ERROR_TRACKING_ENABLED", "true")
    os.environ.setdefault("ERROR_TRACKING_SAMPLE_RATE", "1.0")
    os.environ.setdefault("ERROR_DATA_ENCRYPTION", "false")
    
    # Audit logging
    os.environ.setdefault("AUDIT_LOGGING_ENABLED", "true")
    os.environ.setdefault("AUDIT_LOG_RETENTION_DAYS", "30")
    os.environ.setdefault("AUDIT_LOG_LEVEL", "INFO")
    os.environ.setdefault("AUDIT_LOG_ENCRYPTION", "false")
    
    # Data retention
    os.environ.setdefault("DATA_RETENTION_DAYS", "30")
    os.environ.setdefault("DATA_ARCHIVAL_ENABLED", "false")
    os.environ.setdefault("DATA_ARCHIVAL_INTERVAL", "86400")
    os.environ.setdefault("DATA_ARCHIVAL_ENCRYPTION", "false")
    
    # Multi-tenancy
    os.environ.setdefault("MULTI_TENANCY_ENABLED", "false")
    os.environ.setdefault("TENANT_ISOLATION_LEVEL", "none")
    os.environ.setdefault("TENANT_DATA_ENCRYPTION", "false")
    
    # API documentation
    os.environ.setdefault("API_DOCS_ENABLED", "true")
    os.environ.setdefault("API_DOCS_TITLE", "CloudMind API")
    os.environ.setdefault("API_DOCS_DESCRIPTION", "The Ultimate Cloud Engineering Platform API")
    os.environ.setdefault("API_DOCS_VERSION", "1.0.0")
    
    # Frontend configuration
    os.environ.setdefault("NEXT_PUBLIC_API_URL", "http://localhost:8000")
    os.environ.setdefault("NEXT_PUBLIC_APP_NAME", "CloudMind")
    os.environ.setdefault("NEXT_PUBLIC_APP_VERSION", "1.0.0")
    
    # Cloud Provider Configuration - Phase 2
    # AWS Configuration
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "your_aws_access_key_here")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "your_aws_secret_key_here")
    os.environ.setdefault("AWS_REGION", "us-east-1")
    os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
    
    # Azure Configuration
    os.environ.setdefault("AZURE_SUBSCRIPTION_ID", "your_azure_subscription_id_here")
    os.environ.setdefault("AZURE_TENANT_ID", "your_azure_tenant_id_here")
    os.environ.setdefault("AZURE_CLIENT_ID", "your_azure_client_id_here")
    os.environ.setdefault("AZURE_CLIENT_SECRET", "your_azure_client_secret_here")
    
    # GCP Configuration
    os.environ.setdefault("GCP_PROJECT_ID", "your_gcp_project_id_here")
    os.environ.setdefault("GCP_SERVICE_ACCOUNT_KEY", "your_gcp_service_account_key_here")
    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", "./gcp-credentials.json")
    
    # Cloud Scanner Configuration
    os.environ.setdefault("ENABLE_CLOUD_SCANNING", "true")
    os.environ.setdefault("SCANNER_TIMEOUT", "300")  # 5 minutes
    os.environ.setdefault("SCANNER_MAX_RESOURCES", "10000")
    os.environ.setdefault("SCANNER_RATE_LIMIT", "100")  # requests per second
    
    # AI/ML Configuration - Phase 3
    # OpenAI Configuration
    os.environ.setdefault("OPENAI_API_KEY", "your_openai_api_key_here")
    os.environ.setdefault("OPENAI_MODEL", "gpt-4")
    os.environ.setdefault("OPENAI_MAX_TOKENS", "4000")
    os.environ.setdefault("OPENAI_TEMPERATURE", "0.1")
    
    # Anthropic Configuration
    os.environ.setdefault("ANTHROPIC_API_KEY", "your_anthropic_api_key_here")
    os.environ.setdefault("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")
    os.environ.setdefault("ANTHROPIC_MAX_TOKENS", "4000")
    os.environ.setdefault("ANTHROPIC_TEMPERATURE", "0.1")
    
    # Google AI Configuration
    os.environ.setdefault("GOOGLE_AI_API_KEY", "your_google_ai_api_key_here")
    os.environ.setdefault("GOOGLE_AI_MODEL", "gemini-pro")
    
    # Ollama Configuration
    os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434")
    os.environ.setdefault("OLLAMA_MODEL", "llama2:70b")
    
    # AI Engine Configuration
    os.environ.setdefault("ENABLE_AI_FEATURES", "true")
    os.environ.setdefault("AI_ANALYSIS_TIMEOUT", "60")  # seconds
    os.environ.setdefault("AI_MAX_CONCURRENT_REQUESTS", "10")
    os.environ.setdefault("AI_CACHE_ENABLED", "true")
    os.environ.setdefault("AI_CACHE_TTL", "3600")  # 1 hour
    
    # ML Model Configuration
    os.environ.setdefault("ML_MODEL_PATH", "./ml_models")
    os.environ.setdefault("ML_PREDICTION_ENABLED", "true")
    os.environ.setdefault("ML_TRAINING_ENABLED", "false")
    os.environ.setdefault("ML_MODEL_VERSION", "1.0.0")
    
    # Enterprise Security Configuration - Phase 4
    # Security Hardening
    os.environ.setdefault("ENABLE_ENTERPRISE_SECURITY", "true")
    os.environ.setdefault("SECURITY_LEVEL", "enterprise")
    os.environ.setdefault("ENABLE_ZERO_TRUST", "true")
    os.environ.setdefault("ENABLE_MFA_ENFORCEMENT", "true")
    os.environ.setdefault("ENABLE_AUDIT_LOGGING", "true")
    
    # Compliance Frameworks
    os.environ.setdefault("ENABLE_SOC2_COMPLIANCE", "true")
    os.environ.setdefault("ENABLE_HIPAA_COMPLIANCE", "true")
    os.environ.setdefault("ENABLE_GDPR_COMPLIANCE", "true")
    os.environ.setdefault("ENABLE_PCI_DSS_COMPLIANCE", "true")
    os.environ.setdefault("ENABLE_ISO_27001_COMPLIANCE", "true")
    
    # Encryption and Security
    os.environ.setdefault("ENCRYPTION_ALGORITHM", "AES-256-GCM")
    os.environ.setdefault("KEY_ROTATION_INTERVAL", "90")  # days
    os.environ.setdefault("SESSION_TIMEOUT", "3600")  # seconds
    os.environ.setdefault("MAX_LOGIN_ATTEMPTS", "5")
    os.environ.setdefault("ACCOUNT_LOCKOUT_DURATION", "1800")  # seconds
    
    # Production Security
    os.environ.setdefault("ENABLE_RATE_LIMITING", "true")
    os.environ.setdefault("RATE_LIMIT_REQUESTS", "1000")  # per minute
    os.environ.setdefault("ENABLE_CORS", "true")
    os.environ.setdefault("ALLOWED_ORIGINS", "https://cloudmind.local,https://app.cloudmind.com")
    os.environ.setdefault("ENABLE_HTTPS_ENFORCEMENT", "true")
    
    # Monitoring and Alerting
    os.environ.setdefault("ENABLE_SECURITY_MONITORING", "true")
    os.environ.setdefault("ENABLE_THREAT_DETECTION", "true")
    os.environ.setdefault("ENABLE_INTRUSION_DETECTION", "true")
    os.environ.setdefault("SECURITY_ALERT_EMAIL", "security@cloudmind.com")
    
    # Backup and Disaster Recovery
    os.environ.setdefault("ENABLE_AUTOMATED_BACKUPS", "true")
    os.environ.setdefault("BACKUP_RETENTION_DAYS", "90")
    os.environ.setdefault("ENABLE_DISASTER_RECOVERY", "true")
    os.environ.setdefault("DR_RPO", "3600")  # 1 hour Recovery Point Objective
    os.environ.setdefault("DR_RTO", "7200")  # 2 hours Recovery Time Objective
    
    print("✅ Development environment variables set successfully!")
    print("🔧 Database: SQLite (./cloudmind.db)")
    print("🔧 Redis: Local (localhost:6379)")
    print("🔧 CORS: Enabled for localhost")
    print("🔧 Security: Development mode (less restrictive)")

if __name__ == "__main__":
    setup_development_environment()
