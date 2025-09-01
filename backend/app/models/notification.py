"""
Notification Model for CloudMind
Handles system notifications, alerts, and user communications
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class NotificationType(str, Enum):
    """Notification types"""
    SYSTEM = "system"           # System notifications
    PROJECT = "project"         # Project-related notifications
    SECURITY = "security"       # Security alerts
    COST = "cost"              # Cost alerts
    PERFORMANCE = "performance" # Performance alerts
    INVITATION = "invitation"   # Project invitations
    ALERT = "alert"            # General alerts
    INFO = "info"              # Information messages


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationStatus(str, Enum):
    """Notification status"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"


class Notification(Base):
    """Notification model for user communications"""
    
    __tablename__ = "notifications"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    project_id = Column(PostgresUUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    
    # Notification details
    type = Column(String(20), nullable=False, default=NotificationType.SYSTEM)
    priority = Column(String(20), nullable=False, default=NotificationPriority.MEDIUM)
    status = Column(String(20), nullable=False, default=NotificationStatus.PENDING)
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)  # Additional structured data
    
    # Delivery
    email_sent = Column(Boolean, default=False, nullable=False)
    push_sent = Column(Boolean, default=False, nullable=False)
    in_app_sent = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    project = relationship("Project")
    
    def __repr__(self):
        return f"<Notification(id={self.id}, user_id={self.user_id}, type={self.type}, status={self.status})>"
    
    @property
    def is_read(self) -> bool:
        """Check if notification has been read"""
        return self.status == NotificationStatus.READ
    
    @property
    def is_expired(self) -> bool:
        """Check if notification has expired"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_critical(self) -> bool:
        """Check if notification is critical priority"""
        return self.priority == NotificationPriority.CRITICAL
    
    def mark_as_read(self) -> None:
        """Mark notification as read"""
        self.status = NotificationStatus.READ
        self.read_at = datetime.utcnow()
    
    def mark_as_sent(self, delivery_method: str = "email") -> None:
        """Mark notification as sent via specified method"""
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.utcnow()
        
        if delivery_method == "email":
            self.email_sent = True
        elif delivery_method == "push":
            self.push_sent = True
        elif delivery_method == "in_app":
            self.in_app_sent = True
    
    def mark_as_delivered(self) -> None:
        """Mark notification as delivered"""
        self.status = NotificationStatus.DELIVERED
    
    def mark_as_failed(self) -> None:
        """Mark notification as failed"""
        self.status = NotificationStatus.FAILED
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Get data from notification JSON field"""
        if not self.data:
            return default
        return self.data.get(key, default)
    
    def set_data(self, key: str, value: Any) -> None:
        """Set data in notification JSON field"""
        if not self.data:
            self.data = {}
        self.data[key] = value 