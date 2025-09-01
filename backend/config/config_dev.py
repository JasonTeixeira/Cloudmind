"""
Development Configuration for CloudMind
Phase 1: Foundation Fixes
"""

import os
from pathlib import Path

# Development environment variables
os.environ.setdefault("ENVIRONMENT", "development")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Database configuration - SQLite for development
os.environ.setdefault("DATABASE_URL", "sqlite:///./cloudmind.db")

# Security - Development keys (change in production)
os.environ.setdefault("SECRET_KEY", "dev-secret-key-change-this-in-production-64-characters-long")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

# JWT Security
os.environ.setdefault("JWT_AUDIENCE", "cloudmind-api")
os.environ.setdefault("JWT_ISSUER", "cloudmind-auth")
os.environ.setdefault("JWT_LEEWAY", "10")

# Redis configuration - Local Redis
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

# CORS settings - Development
os.environ.setdefault("ALLOWED_ORIGINS", '["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]')

# Rate limiting - Development (more lenient)
os.environ.setdefault("RATE_LIMIT_PER_MINUTE", "100")
os.environ.setdefault("RATE_LIMIT_PER_HOUR", "1000")

# Storage configuration
os.environ.setdefault("LOCAL_STORAGE_PATH", "./storage")
os.environ.setdefault("GIT_REPOSITORIES_PATH", "./git-repos")
os.environ.setdefault("TEMPLATE_STORAGE_PATH", "./templates")

# Database pool settings - Development
os.environ.setdefault("DB_POOL_SIZE", "5")
os.environ.setdefault("DB_MAX_OVERFLOW", "10")
os.environ.setdefault("DB_POOL_TIMEOUT", "30")
os.environ.setdefault("DB_POOL_RECYCLE", "1800")

# Feature flags - Development
os.environ.setdefault("ENABLE_AI_FEATURES", "true")
os.environ.setdefault("ENABLE_REAL_TIME_UPDATES", "true")
os.environ.setdefault("ENABLE_AUDIT_LOGGING", "true")
os.environ.setdefault("ENABLE_METRICS_COLLECTION", "true")
os.environ.setdefault("ENABLE_SECURITY_SCANNING", "true")

# Performance - Development
os.environ.setdefault("CACHE_TTL", "1800")
os.environ.setdefault("SESSION_TIMEOUT", "1800")
os.environ.setdefault("MAX_CONCURRENT_REQUESTS", "100")

# Security headers - Development
os.environ.setdefault("ENABLE_HSTS", "false")
os.environ.setdefault("ENABLE_CSP", "false")
os.environ.setdefault("ENABLE_XSS_PROTECTION", "true")
os.environ.setdefault("ENABLE_CONTENT_TYPE_NOSNIFF", "true")
os.environ.setdefault("ENABLE_FRAME_OPTIONS", "true")

# Logging - Development
os.environ.setdefault("LOG_FORMAT", "text")
os.environ.setdefault("LOG_FILE", "./logs/cloudmind.log")
os.environ.setdefault("LOG_MAX_SIZE", "10485760")  # 10MB
os.environ.setdefault("LOG_BACKUP_COUNT", "5")
os.environ.setdefault("LOG_SECURITY_EVENTS", "true")

# Health check - Development
os.environ.setdefault("HEALTH_CHECK_ENABLED", "true")
os.environ.setdefault("HEALTH_CHECK_INTERVAL", "30")
os.environ.setdefault("HEALTH_CHECK_TIMEOUT", "10")
os.environ.setdefault("HEALTH_CHECK_AUTHENTICATION", "false")

# Performance monitoring - Development
os.environ.setdefault("PERFORMANCE_MONITORING_ENABLED", "true")
os.environ.setdefault("PERFORMANCE_MONITORING_INTERVAL", "60")
os.environ.setdefault("PERFORMANCE_MONITORING_RETENTION_DAYS", "7")
os.environ.setdefault("PERFORMANCE_DATA_ENCRYPTION", "false")

# Error tracking - Development
os.environ.setdefault("ERROR_TRACKING_ENABLED", "true")
os.environ.setdefault("ERROR_TRACKING_SAMPLE_RATE", "1.0")
os.environ.setdefault("ERROR_DATA_ENCRYPTION", "false")

# Audit logging - Development
os.environ.setdefault("AUDIT_LOGGING_ENABLED", "true")
os.environ.setdefault("AUDIT_LOG_RETENTION_DAYS", "30")
os.environ.setdefault("AUDIT_LOG_LEVEL", "INFO")
os.environ.setdefault("AUDIT_LOG_ENCRYPTION", "false")

# Data retention - Development
os.environ.setdefault("DATA_RETENTION_DAYS", "30")
os.environ.setdefault("DATA_ARCHIVAL_ENABLED", "false")
os.environ.setdefault("DATA_ARCHIVAL_INTERVAL", "86400")
os.environ.setdefault("DATA_ARCHIVAL_ENCRYPTION", "false")

# Multi-tenancy - Development
os.environ.setdefault("MULTI_TENANCY_ENABLED", "false")
os.environ.setdefault("TENANT_ISOLATION_LEVEL", "none")
os.environ.setdefault("TENANT_DATA_ENCRYPTION", "false")

# API documentation - Development
os.environ.setdefault("API_DOCS_ENABLED", "true")
os.environ.setdefault("API_DOCS_TITLE", "CloudMind API")
os.environ.setdefault("API_DOCS_DESCRIPTION", "The Ultimate Cloud Engineering Platform API")
os.environ.setdefault("API_DOCS_VERSION", "1.0.0")

# Frontend configuration
os.environ.setdefault("NEXT_PUBLIC_API_URL", "http://localhost:8000")
os.environ.setdefault("NEXT_PUBLIC_APP_NAME", "CloudMind")
os.environ.setdefault("NEXT_PUBLIC_APP_VERSION", "1.0.0")

print("✅ Development configuration loaded successfully!")
print("📋 Environment variables set for development mode")
print("🔧 Database: SQLite (./cloudmind.db)")
print("🔧 Redis: Local (localhost:6379)")
print("🔧 CORS: Enabled for localhost")
print("🔧 Security: Development mode (less restrictive)")
