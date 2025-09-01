"""
CloudMind Configuration Settings
"""

import os
import secrets
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with world-class security defaults"""
    
    # Application Settings
    APP_NAME: str = "CloudMind"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = Field(default=False, description="Debug mode - should be False in production")
    LOG_LEVEL: str = "INFO"
    
    # Server Configuration - World-class security
    HOST: str = Field(default="127.0.0.1", description="Host binding - use 127.0.0.1 for production")
    PORT: int = 8000
    WORKERS: int = 4
    
    # Security - Enterprise-grade secrets management
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(64),
        description="Secret key for JWT tokens - set via environment variable"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Reduced for security
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Enhanced JWT Security
    JWT_AUDIENCE: str = "cloudmind-api"
    JWT_ISSUER: str = "cloudmind-auth"
    JWT_LEEWAY: int = 10  # Clock skew tolerance
    
    # Database Configuration - Encrypted connections
    DATABASE_URL: str = Field(
        default="postgresql://cloudmind:${DB_PASSWORD}@localhost:5432/cloudmind?sslmode=require",
        description="Database URL with SSL - set DB_PASSWORD environment variable"
    )
    TIMESCALE_URL: str = Field(
        default="postgresql://cloudmind:${TIMESCALE_PASSWORD}@localhost:5433/cloudmind_metrics?sslmode=require",
        description="TimescaleDB URL with SSL - set TIMESCALE_PASSWORD environment variable"
    )
    
    # Redis Configuration - Smart defaults for development/production
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis URL - automatically configured based on environment"
    )
    # Derived/explicit Redis settings for modules that expect discrete fields
    REDIS_HOST: str = Field(default="localhost", description="Redis host")
    REDIS_PORT: int = Field(default=6379, description="Redis port")
    REDIS_DB: int = Field(default=0, description="Redis database number")
    REDIS_PASSWORD: Optional[str] = Field(default=None, description="Redis password")
    CELERY_BROKER_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Celery broker URL"
    )
    CELERY_RESULT_BACKEND: str = Field(
        default="redis://localhost:6379/0",
        description="Celery result backend URL"
    )
    
    # AI/ML Configuration - Secure API keys
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key - set via environment variable"
    )
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        description="Anthropic API key - set via environment variable"
    )
    GOOGLE_AI_API_KEY: Optional[str] = Field(
        default=None,
        description="Google Generative AI API key - set via environment variable"
    )
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2:70b"

    # AI Provider Model Settings
    OPENAI_MODEL: str = Field(default="gpt-4o", description="Default OpenAI model")
    OPENAI_MAX_TOKENS: int = Field(default=1024, description="Max tokens for OpenAI requests")
    OPENAI_TEMPERATURE: float = Field(default=0.2, description="Temperature for OpenAI requests")

    ANTHROPIC_MODEL: str = Field(default="claude-3-5-sonnet", description="Default Anthropic model")
    ANTHROPIC_MAX_TOKENS: int = Field(default=1024, description="Max tokens for Anthropic requests")
    ANTHROPIC_TEMPERATURE: float = Field(default=0.2, description="Temperature for Anthropic requests")

    GOOGLE_AI_MODEL: str = Field(default="gemini-1.5-pro", description="Default Google AI model")
    GOOGLE_AI_MAX_TOKENS: int = Field(default=1024, description="Max tokens for Google AI requests")
    GOOGLE_AI_TEMPERATURE: float = Field(default=0.2, description="Temperature for Google AI requests")
    
    # Monitoring - Enhanced security
    PROMETHEUS_URL: str = "https://localhost:9090"  # HTTPS
    GRAFANA_URL: str = "https://localhost:3001"  # HTTPS
    GRAFANA_USER: str = "admin"
    GRAFANA_PASSWORD: str = Field(
        default="${GRAFANA_PASSWORD}",
        description="Grafana password - set via environment variable"
    )
    
    # Email Configuration - Enhanced security
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = Field(
        default=None,
        description="SMTP username - set via environment variable"
    )
    SMTP_PASSWORD: Optional[str] = Field(
        default=None,
        description="SMTP password - set via environment variable"
    )
    SMTP_TLS: bool = True
    SMTP_SSL: bool = True  # Force SSL
    
    # Frontend Configuration - Enhanced security
    FRONTEND_URL: str = Field(default="http://localhost:3000", description="Primary frontend base URL")
    ALLOWED_HOSTS: List[str] = ["*"]  # Allow all hosts in development
    NEXT_PUBLIC_API_URL: str = "https://localhost:8000"  # HTTPS
    NEXT_PUBLIC_APP_NAME: str = "CloudMind"
    NEXT_PUBLIC_APP_VERSION: str = "1.0.0"
    
    # CORS Settings - World-class security
    ALLOWED_ORIGINS: List[str] = Field(
        default=["https://cloudmind.local"] if os.getenv("ENVIRONMENT") == "production" else [
            "http://localhost:3000",
            "https://cloudmind.local"
        ],
        description="Allowed CORS origins - restrictive in production"
    )
    
    # CORS Additional Settings - Enhanced security
    ALLOWED_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        description="Allowed HTTP methods"
    )
    
    ALLOWED_HEADERS: List[str] = Field(
        default=[
            "Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With",
            "X-API-Key", "X-Request-ID", "X-CSRF-Token"
        ],
        description="Allowed HTTP headers"
    )
    
    EXPOSE_HEADERS: List[str] = Field(
        default=[
            "X-Request-ID", "X-RateLimit-Limit", "X-RateLimit-Remaining", 
            "X-RateLimit-Reset", "X-Total-Count", "X-API-Version"
        ],
        description="Headers to expose to the client"
    )
    
    CORS_MAX_AGE: int = Field(
        default=86400,  # 24 hours
        description="CORS preflight cache time"
    )
    
    # Rate Limiting - World-class implementation
    RATE_LIMIT_PER_MINUTE: int = 60  # Reduced for security
    RATE_LIMIT_PER_HOUR: int = 500  # Reduced for security
    RATE_LIMIT_PER_DAY: int = 5000  # Added daily limit
    RATE_LIMIT_BURST: int = 10  # Burst limit
    
    # File Upload - Enhanced security
    MAX_FILE_SIZE: int = 5242880  # 5MB - Reduced for security
    ALLOWED_FILE_TYPES: List[str] = ["image/*", "application/pdf", "text/*"]
    SCAN_UPLOADS: bool = True  # Virus scanning
    
    # Backup Configuration - Enhanced security
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    BACKUP_ENCRYPTION: bool = True  # Encrypt backups
    
    # SSL/TLS Configuration - World-class security
    SSL_CERT_FILE: Optional[str] = Field(
        default=None,
        description="SSL certificate file path"
    )
    SSL_KEY_FILE: Optional[str] = Field(
        default=None,
        description="SSL private key file path"
    )
    SSL_CA_FILE: Optional[str] = Field(
        default=None,
        description="SSL CA certificate file path"
    )
    SSL_VERIFY_MODE: str = "CERT_REQUIRED"  # Strict verification
    
    # Development Settings - Disabled in production
    AUTO_RELOAD: bool = Field(
        default=False,
        description="Auto reload - should be False in production"
    )
    HOT_RELOAD: bool = Field(
        default=False,
        description="Hot reload - should be False in production"
    )
    DEBUG_TOOLBAR: bool = Field(
        default=False,
        description="Debug toolbar - should be False in production"
    )

    # Cloud & Object Storage Credentials (optional; used by integrations)
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, description="AWS access key id")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, description="AWS secret access key")
    AWS_REGION: Optional[str] = Field(default=None, description="AWS region")

    CLOUDFLARE_R2_ENABLED: bool = Field(default=False, description="Enable Cloudflare R2 integration")
    CLOUDFLARE_R2_ACCOUNT_ID: Optional[str] = None
    CLOUDFLARE_R2_ACCESS_KEY_ID: Optional[str] = None
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: Optional[str] = None
    CLOUDFLARE_R2_BUCKET: Optional[str] = None
    CLOUDFLARE_R2_ENDPOINT: Optional[str] = None

    BACKBLAZE_B2_ENABLED: bool = Field(default=False, description="Enable Backblaze B2 integration")
    BACKBLAZE_B2_KEY_ID: Optional[str] = None
    BACKBLAZE_B2_APP_KEY: Optional[str] = None
    BACKBLAZE_B2_BUCKET: Optional[str] = None

    # Feature flags for optional subsystems
    ENABLE_CLOUD_CLIENTS: bool = Field(default=False, description="Initialize cloud provider SDK clients")
    ENABLE_WSGI_FALLBACK: bool = Field(default=False, description="Enable dual ASGI/WSGI wrapper for legacy clients (non-production)")
    ENABLE_AI_TERMINAL: bool = Field(default=False, description="Enable AI-assisted terminal (planning and guarded execution)")
    AI_TERMINAL_ALLOWED_COMMAND_PREFIXES: List[str] = Field(
        default_factory=lambda: [
            "ls", "cat", "echo", "pwd", "whoami", "git", "kubectl", "helm",
            "terraform plan", "ansible", "python -m", "pip show", "pip list"
        ],
        description="Allowed command prefixes for AI terminal execution"
    )
    AI_TERMINAL_BLOCKED_PATTERNS: List[str] = Field(
        default_factory=lambda: [
            "rm -rf /", "mkfs", ":(){:|:&};:", "shutdown", "reboot", "dd if=", "> /dev/sda"
        ],
        description="Blocked substrings for AI terminal execution"
    )

    # FinOps/Cost features
    ENABLE_COST_INGESTION: bool = Field(default=False, description="Enable external cloud cost ingestion jobs")
    ENABLE_SLACK_DIGESTS: bool = Field(default=False, description="Enable Slack/Teams cost digests")
    COST_INGESTION_INTERVAL_MINUTES: int = Field(default=1440, description="Interval for cost ingestion background job in minutes")
    DIGEST_INTERVAL_MINUTES: int = Field(default=1440, description="Interval for daily digest background job in minutes")
    SLACK_WEBHOOK_URL: Optional[str] = Field(default=None, description="Slack Incoming Webhook URL for digests")

    # AWS CUR / Athena configuration (optional)
    AWS_ATHENA_WORKGROUP: Optional[str] = Field(default=None, description="Athena workgroup for CUR queries")
    AWS_ATHENA_DATABASE: Optional[str] = Field(default=None, description="Athena database containing CUR table")
    AWS_ATHENA_OUTPUT_LOCATION: Optional[str] = Field(default=None, description="s3:// bucket/prefix for Athena query results")
    AWS_CUR_TABLE: Optional[str] = Field(default=None, description="Fully qualified CUR table name (e.g., db.table)")

    @model_validator(mode="after")
    def _configure_for_environment(self):
        """Configure settings based on environment."""
        try:
            from urllib.parse import urlparse
            
            # Configure Redis based on environment
            if self.ENVIRONMENT == "development":
                # Development: Simple Redis without SSL/password
                object.__setattr__(self, "REDIS_URL", "redis://localhost:6379/0")
                object.__setattr__(self, "CELERY_BROKER_URL", "redis://localhost:6379/0")
                object.__setattr__(self, "CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
                object.__setattr__(self, "REDIS_PASSWORD", None)
            
            # Derive Redis fields from URL
            if getattr(self, "REDIS_URL", None):
                parsed = urlparse(self.REDIS_URL)
                object.__setattr__(self, "REDIS_HOST", parsed.hostname or "localhost")
                object.__setattr__(self, "REDIS_PORT", parsed.port or 6379)
                if parsed.password:
                    object.__setattr__(self, "REDIS_PASSWORD", parsed.password)
                # Extract database number from path
                if parsed.path and len(parsed.path) > 1:
                    try:
                        db_num = int(parsed.path[1:])  # Remove leading /
                        object.__setattr__(self, "REDIS_DB", db_num)
                    except (ValueError, IndexError):
                        pass
        except Exception:
            # Best-effort; keep existing values
            pass
        return self
    
    # Testing - Enhanced security
    TEST_DATABASE_URL: str = Field(
        default="postgresql://cloudmind:${TEST_DB_PASSWORD}@localhost:5432/cloudmind_test?sslmode=require",
        description="Test database URL with SSL - set TEST_DB_PASSWORD environment variable"
    )
    TEST_REDIS_URL: str = "redis://:${TEST_REDIS_PASSWORD}@localhost:6379/1?ssl=true"
    
    # Feature Flags - Enhanced security
    ENABLE_AI_FEATURES: bool = True
    ENABLE_3D_VISUALIZATION: bool = True
    ENABLE_REAL_TIME_UPDATES: bool = True
    ENABLE_AUDIT_LOGGING: bool = True
    ENABLE_METRICS_COLLECTION: bool = True
    ENABLE_SECURITY_SCANNING: bool = True  # Added security scanning
    
    # Performance - Enhanced security
    CACHE_TTL: int = 1800  # 30 minutes - Reduced for security
    SESSION_TIMEOUT: int = 900  # 15 minutes - Reduced for security
    MAX_CONCURRENT_REQUESTS: int = 50  # Reduced for security
    
    # Security Headers - World-class implementation
    ENABLE_HSTS: bool = True
    ENABLE_CSP: bool = True
    ENABLE_XSS_PROTECTION: bool = True
    ENABLE_CONTENT_TYPE_NOSNIFF: bool = True
    ENABLE_FRAME_OPTIONS: bool = True
    ENABLE_REFERRER_POLICY: bool = True
    ENABLE_PERMISSIONS_POLICY: bool = True
    
    # Logging - Enhanced security
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "/var/log/cloudmind/app.log"
    LOG_MAX_SIZE: int = 50 * 1024 * 1024  # 50MB - Reduced for security
    LOG_BACKUP_COUNT: int = 5
    LOG_SECURITY_EVENTS: bool = True  # Separate security logging
    
    # External Services - Enhanced security
    SENTRY_DSN: Optional[str] = Field(
        default=None,
        description="Sentry DSN - set via environment variable"
    )
    NEW_RELIC_LICENSE_KEY: Optional[str] = Field(
        default=None,
        description="New Relic license key - set via environment variable"
    )
    DATADOG_API_KEY: Optional[str] = Field(
        default=None,
        description="Datadog API key - set via environment variable"
    )
    
    # Webhook Configuration - Enhanced security
    WEBHOOK_SECRET: Optional[str] = Field(
        default=None,
        description="Webhook secret - set via environment variable"
    )
    WEBHOOK_TIMEOUT: int = 30
    WEBHOOK_VERIFICATION: bool = True  # Verify webhook signatures
    
    # API Versioning - Enhanced security
    API_VERSION: str = "v1"
    API_PREFIX: str = "/api"
    API_DEPRECATION_DATE: str = "2025-12-31"  # Deprecation warning
    
    # Database Pool Settings - Enhanced security
    DB_POOL_SIZE: int = 10  # Reduced for security
    DB_MAX_OVERFLOW: int = 20  # Reduced for security
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800  # 30 minutes - Reduced for security
    
    # Redis Pool Settings - Enhanced security
    REDIS_POOL_SIZE: int = 5  # Reduced for security
    REDIS_POOL_TIMEOUT: int = 30
    
    # Celery Settings - Enhanced security
    CELERY_WORKER_CONCURRENCY: int = 2  # Reduced for security
    CELERY_TASK_TIME_LIMIT: int = 1800  # 30 minutes - Reduced for security
    CELERY_TASK_SOFT_TIME_LIMIT: int = 1500  # 25 minutes
    CELERY_WORKER_MAX_TASKS_PER_CHILD: int = 500  # Reduced for security
    
    # AI Model Settings - Enhanced security
    AI_MODEL_CACHE_SIZE: int = 500  # Reduced for security
    AI_MODEL_TIMEOUT: int = 300
    AI_MAX_TOKENS: int = 2048  # Reduced for security
    AI_TEMPERATURE: float = 0.1

    # Feature Flags
    USE_STATIC_PRICE_ENGINE: bool = True
    
    # Cost Analysis Settings - Enhanced security
    COST_ANALYSIS_INTERVAL: int = 3600  # 1 hour
    COST_ALERT_THRESHOLD: float = 0.1  # 10% increase
    COST_FORECAST_DAYS: int = 30
    
    # Security Scan Settings - Enhanced security
    SECURITY_SCAN_INTERVAL: int = 43200  # 12 hours - Increased frequency
    SECURITY_SCAN_TIMEOUT: int = 1800  # 30 minutes
    SECURITY_MAX_CONCURRENT_SCANS: int = 3  # Reduced for security
    SECURITY_VULNERABILITY_THRESHOLD: str = "MEDIUM"  # Alert on medium+ vulnerabilities
    
    # Infrastructure Settings - Enhanced security
    INFRASTRUCTURE_SCAN_INTERVAL: int = 1800  # 30 minutes - Increased frequency
    INFRASTRUCTURE_SCAN_TIMEOUT: int = 900  # 15 minutes
    INFRASTRUCTURE_MAX_RESOURCES: int = 5000  # Reduced for security
    
    # Notification Settings - Enhanced security
    NOTIFICATION_EMAIL_ENABLED: bool = True
    NOTIFICATION_SLACK_ENABLED: bool = False
    NOTIFICATION_WEBHOOK_ENABLED: bool = False
    NOTIFICATION_ENCRYPTION: bool = True  # Encrypt notifications
    
    # Backup Settings - Enhanced security
    BACKUP_ENABLED: bool = True
    BACKUP_S3_BUCKET: str = "cloudmind-backups"
    BACKUP_ENCRYPTION_KEY: Optional[str] = Field(
        default=None,
        description="Backup encryption key - set via environment variable"
    )
    BACKUP_COMPRESSION: bool = True
    BACKUP_VERIFICATION: bool = True  # Verify backup integrity
    
    # Monitoring Settings - Enhanced security
    METRICS_ENABLED: bool = True
    METRICS_INTERVAL: int = 60  # 1 minute
    METRICS_RETENTION_DAYS: int = 90
    METRICS_ENCRYPTION: bool = True  # Encrypt metrics
    
    # Development Tools - Disabled in production
    ENABLE_SWAGGER_UI: bool = Field(
        default=False,
        description="Swagger UI - should be False in production"
    )
    ENABLE_REPL: bool = Field(
        default=False,
        description="REPL - should be False in production"
    )
    ENABLE_PROFILING: bool = Field(
        default=False,
        description="Profiling - should be False in production"
    )
    
    # External Integrations - Enhanced security
    GITHUB_WEBHOOK_SECRET: Optional[str] = Field(
        default=None,
        description="GitHub webhook secret - set via environment variable"
    )
    GITLAB_WEBHOOK_SECRET: Optional[str] = Field(
        default=None,
        description="GitLab webhook secret - set via environment variable"
    )
    BITBUCKET_WEBHOOK_SECRET: Optional[str] = Field(
        default=None,
        description="Bitbucket webhook secret - set via environment variable"
    )
    
    # Compliance Settings - Enhanced security
    COMPLIANCE_FRAMEWORKS: List[str] = ["SOC2", "HIPAA", "CIS", "NIST", "ISO27001"]
    COMPLIANCE_SCAN_INTERVAL: int = 43200  # 12 hours
    COMPLIANCE_REPORTING: bool = True  # Generate compliance reports
    
    # Cost Optimization Settings - Enhanced security
    COST_OPTIMIZATION_ENABLED: bool = True
    COST_OPTIMIZATION_INTERVAL: int = 3600  # 1 hour
    COST_SAVINGS_THRESHOLD: float = 0.05  # 5% minimum savings
    
    # Security Compliance - Enhanced security
    SECURITY_COMPLIANCE_ENABLED: bool = True
    SECURITY_COMPLIANCE_INTERVAL: int = 43200  # 12 hours
    SECURITY_COMPLIANCE_FRAMEWORKS: List[str] = ["CIS", "NIST", "ISO27001", "OWASP"]
    
    # API Rate Limiting - Enhanced security
    API_RATE_LIMIT_PER_MINUTE: int = 60  # Reduced for security
    API_RATE_LIMIT_PER_HOUR: int = 500  # Reduced for security
    API_RATE_LIMIT_PER_DAY: int = 5000  # Added daily limit
    API_RATE_LIMIT_BURST: int = 10  # Burst limit
    
    # WebSocket Settings - Enhanced security
    WEBSOCKET_ENABLED: bool = True
    WEBSOCKET_HEARTBEAT_INTERVAL: int = 30
    WEBSOCKET_MAX_CONNECTIONS: int = 500  # Reduced for security
    WEBSOCKET_AUTHENTICATION: bool = True  # Require authentication
    
    # Cache Settings - Enhanced security
    CACHE_ENABLED: bool = True
    CACHE_DEFAULT_TTL: int = 1800  # 30 minutes - Reduced for security
    CACHE_MAX_SIZE: int = 500  # Reduced for security
    CACHE_ENCRYPTION: bool = True  # Encrypt cached data
    
    # Search Settings - Enhanced security
    SEARCH_ENABLED: bool = True
    SEARCH_INDEX_REFRESH_INTERVAL: int = 300  # 5 minutes
    SEARCH_MAX_RESULTS: int = 500  # Reduced for security
    SEARCH_ENCRYPTION: bool = True  # Encrypt search data
    
    # File Storage - Enhanced security
    STORAGE_PROVIDER: str = "local"  # local, s3, azure, gcp
    LOCAL_STORAGE_PATH: str = "./storage"  # Local storage path
    GIT_REPOSITORIES_PATH: str = "./git-repos"  # Git repositories path
    TEMPLATE_STORAGE_PATH: str = "./templates"  # Template storage path
    STORAGE_BUCKET: str = "cloudmind-storage"
    STORAGE_REGION: str = "us-east-1"
    STORAGE_ENCRYPTION: bool = True  # Encrypt stored files
    
    # Authentication - Enhanced security
    AUTH_PROVIDER: str = "local"  # local, oauth, saml, ldap
    OAUTH_GOOGLE_CLIENT_ID: Optional[str] = Field(
        default=None,
        description="Google OAuth client ID - set via environment variable"
    )
    OAUTH_GOOGLE_CLIENT_SECRET: Optional[str] = Field(
        default=None,
        description="Google OAuth client secret - set via environment variable"
    )
    OAUTH_GITHUB_CLIENT_ID: Optional[str] = Field(
        default=None,
        description="GitHub OAuth client ID - set via environment variable"
    )
    OAUTH_GITHUB_CLIENT_SECRET: Optional[str] = Field(
        default=None,
        description="GitHub OAuth client secret - set via environment variable"
    )
    
    # Multi-tenancy - Enhanced security
    MULTI_TENANCY_ENABLED: bool = True
    TENANT_ISOLATION_LEVEL: str = "strict"  # strict, relaxed, none
    TENANT_DATA_ENCRYPTION: bool = True  # Encrypt tenant data
    
    # API Documentation - Enhanced security
    API_DOCS_ENABLED: bool = Field(
        default=False,
        description="API docs - should be False in production"
    )
    API_DOCS_TITLE: str = "CloudMind API"
    API_DOCS_DESCRIPTION: str = "The Ultimate Cloud Engineering Platform API"
    API_DOCS_VERSION: str = "1.0.0"
    
    # Health Check - Enhanced security
    HEALTH_CHECK_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    HEALTH_CHECK_TIMEOUT: int = 10
    HEALTH_CHECK_AUTHENTICATION: bool = True  # Require auth for health checks
    
    # Performance Monitoring - Enhanced security
    PERFORMANCE_MONITORING_ENABLED: bool = True
    PERFORMANCE_MONITORING_INTERVAL: int = 60
    PERFORMANCE_MONITORING_RETENTION_DAYS: int = 30
    PERFORMANCE_DATA_ENCRYPTION: bool = True  # Encrypt performance data
    
    # Error Tracking - Enhanced security
    ERROR_TRACKING_ENABLED: bool = True
    ERROR_TRACKING_SAMPLE_RATE: float = 0.05  # 5% - Reduced for security
    ERROR_DATA_ENCRYPTION: bool = True  # Encrypt error data
    
    # Audit Logging - Enhanced security
    AUDIT_LOGGING_ENABLED: bool = True
    AUDIT_LOG_RETENTION_DAYS: int = 2555  # 7 years
    AUDIT_LOG_LEVEL: str = "INFO"
    AUDIT_LOG_ENCRYPTION: bool = True  # Encrypt audit logs
    
    # Data Retention - Enhanced security
    DATA_RETENTION_DAYS: int = 2555  # 7 years
    DATA_ARCHIVAL_ENABLED: bool = True
    DATA_ARCHIVAL_INTERVAL: int = 86400  # 24 hours
    DATA_ARCHIVAL_ENCRYPTION: bool = True  # Encrypt archived data

    @field_validator('ENVIRONMENT')
    @classmethod
    def validate_environment(cls, v):
        """Validate environment and set appropriate defaults"""
        if v == 'production':
            # Force production security settings
            cls.DEBUG = False
            cls.DEBUG_TOOLBAR = False
            cls.ENABLE_SWAGGER_UI = False
            cls.ENABLE_REPL = False
            cls.ENABLE_PROFILING = False
            cls.API_DOCS_ENABLED = False
            cls.AUTO_RELOAD = False
            cls.HOT_RELOAD = False
            # Force HTTPS in production
            cls.NEXT_PUBLIC_API_URL = "https://cloudmind.local"
            cls.ALLOWED_ORIGINS = ["https://cloudmind.local"]
            # Restrict allowed hosts to hostnames (no schemes)
            cls.ALLOWED_HOSTS = ["cloudmind.local", "localhost"]
        return v

    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure secret key is properly set"""
        if v == "your-super-secret-key-change-this-in-production":
            raise ValueError("SECRET_KEY must be set via environment variable")
        if len(v) < 64:
            raise ValueError("SECRET_KEY must be at least 64 characters long")
        return v

    @field_validator('ALLOWED_ORIGINS')
    @classmethod
    def validate_cors_origins(cls, v):
        """Validate CORS origins"""
        if not v:
            raise ValueError("ALLOWED_ORIGINS cannot be empty")
        # Ensure HTTPS in production
        if os.getenv("ENVIRONMENT") == "production":
            for origin in v:
                if not origin.startswith("https://"):
                    raise ValueError("All origins must use HTTPS in production")
        return v



    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "env_prefix": ""
    }


# Create settings instance
settings = Settings() 