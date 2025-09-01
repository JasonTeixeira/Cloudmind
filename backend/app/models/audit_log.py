"""
Audit Log Model for CloudMind
Tracks system activities, security events, and compliance requirements
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AuditEventType(str, Enum):
    """Audit event types"""
    # Authentication events
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    PASSWORD_RESET = "password_reset"
    
    # Project events
    PROJECT_CREATE = "project_create"
    PROJECT_UPDATE = "project_update"
    PROJECT_DELETE = "project_delete"
    PROJECT_ACCESS = "project_access"
    
    # User management
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    USER_ROLE_CHANGE = "user_role_change"
    
    # Security events
    SECURITY_SCAN = "security_scan"
    VULNERABILITY_DETECTED = "vulnerability_detected"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    ACCESS_DENIED = "access_denied"
    
    # System events
    SYSTEM_CONFIG_CHANGE = "system_config_change"
    BACKUP_CREATED = "backup_created"
    MAINTENANCE_MODE = "maintenance_mode"
    
    # Data events
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    DATA_DELETION = "data_deletion"
    
    # API events
    API_CALL = "api_call"
    API_ERROR = "api_error"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class AuditSeverity(str, Enum):
    """Audit event severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AuditLog(Base):
    """Audit log model for tracking system activities"""
    
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Event details
    event_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False, default=AuditSeverity.INFO)
    
    # User and session info
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    session_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 compatible
    user_agent = Column(Text, nullable=True)
    
    # Resource info
    resource_type = Column(String(50), nullable=True)  # project, user, system, etc.
    resource_id = Column(String(255), nullable=True)
    project_id = Column(PostgresUUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    
    # Event details
    description = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)  # Additional structured data
    audit_metadata = Column(JSON, nullable=True)  # System metadata
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    project = relationship("Project")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, user_id={self.user_id}, created_at={self.created_at})>"
    
    @property
    def is_critical(self) -> bool:
        """Check if audit event is critical severity"""
        return self.severity == AuditSeverity.CRITICAL
    
    @property
    def is_security_event(self) -> bool:
        """Check if this is a security-related event"""
        security_events = [
            AuditEventType.LOGIN_FAILED,
            AuditEventType.SUSPICIOUS_ACTIVITY,
            AuditEventType.ACCESS_DENIED,
            AuditEventType.VULNERABILITY_DETECTED,
            AuditEventType.PASSWORD_CHANGE,
            AuditEventType.PASSWORD_RESET
        ]
        return self.event_type in security_events
    
    def get_details(self, key: str, default: Any = None) -> Any:
        """Get details from audit log JSON field"""
        if not self.details:
            return default
        return self.details.get(key, default)
    
    def set_details(self, key: str, value: Any) -> None:
        """Set details in audit log JSON field"""
        if not self.details:
            self.details = {}
        self.details[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata from audit log JSON field"""
        if not self.audit_metadata:
            return default
        return self.audit_metadata.get(key, default)
    
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata in audit log JSON field"""
        if not self.audit_metadata:
            self.audit_metadata = {}
        self.audit_metadata[key] = value 