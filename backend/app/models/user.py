"""
Enhanced User Model with Master User Capabilities
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from enum import Enum

from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.ext.declarative import declarative_base

from app.core.database import Base

logger = logging.getLogger(__name__)


class UserRole(str, Enum):
    """User roles enumeration"""
    MASTER = "master"
    ADMIN = "admin"
    MANAGER = "manager"
    ENGINEER = "engineer"
    VIEWER = "viewer"


class UserStatus(str, Enum):
    """User status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class User(Base):
    """Enhanced User model with master user capabilities"""
    
    __tablename__ = "users"
    
    # Core fields
    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Role and permissions
    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.VIEWER, nullable=False)
    is_master_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[UserStatus] = mapped_column(String(50), default=UserStatus.ACTIVE, nullable=False)
    
    # Profile information
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    timezone: Mapped[Optional[str]] = mapped_column(String(50), default="UTC", nullable=True)
    
    # Preferences
    preferences: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    notification_settings: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    ui_settings: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    
    # Security
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    last_activity: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    password_changed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Audit fields
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by: Mapped[Optional[UUID]] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_by: Mapped[Optional[UUID]] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    cost_analyses = relationship("CostAnalysis", back_populates="user", cascade="all, delete-orphan")
    security_scans = relationship("SecurityScan", back_populates="user", cascade="all, delete-orphan")
    # Removed invalid relationship to Infrastructure (no FK on infrastructure -> users)
    ai_insights = relationship("AIInsight", back_populates="user", cascade="all, delete-orphan")
    user_activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
    
    # New relationships for collaboration and notifications
    project_memberships = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="ProjectMember.user_id",
    )
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    
    # Consulting engagement relationships
    engagements = relationship(
        "ClientEngagement",
        back_populates="client",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def is_master(self) -> bool:
        """Check if user is a master user"""
        return self.is_master_user or self.role == UserRole.MASTER
    
    @property
    def can_access_all_projects(self) -> bool:
        """Check if user can access all projects"""
        return self.is_master or self.role in [UserRole.MASTER, UserRole.ADMIN]
    
    @property
    def can_manage_users(self) -> bool:
        """Check if user can manage other users"""
        return self.is_master or self.role in [UserRole.MASTER, UserRole.ADMIN]
    
    @property
    def can_view_reports(self) -> bool:
        """Check if user can view advanced reports"""
        return self.is_master or self.role in [UserRole.MASTER, UserRole.ADMIN, UserRole.MANAGER]
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked"""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def update_last_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.utcnow()
    
    def increment_failed_login_attempts(self):
        """Increment failed login attempts and lock if necessary"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = datetime.utcnow() + timedelta(minutes=30)
    
    def reset_failed_login_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        self.locked_until = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary"""
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "role": self.role,
            "is_master_user": self.is_master_user,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "is_active": self.is_active,
            "status": self.status,
            "avatar_url": self.avatar_url,
            "company": self.company,
            "job_title": self.job_title,
            "location": self.location,
            "timezone": self.timezone,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "permissions": {
                "can_access_all_projects": self.can_access_all_projects,
                "can_manage_users": self.can_manage_users,
                "can_view_reports": self.can_view_reports,
                "is_master": self.is_master
            }
        }


class UserActivity(Base):
    """User activity tracking model"""
    
    __tablename__ = "user_activities"
    
    id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(PostgresUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Activity details
    activity_type: Mapped[str] = mapped_column(String(100), nullable=False)  # login, logout, create_project, etc.
    description: Mapped[str] = mapped_column(Text, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional data
    activity_metadata: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="user_activities")
    
    def __repr__(self):
        return f"<UserActivity(id={self.id}, user_id={self.user_id}, type='{self.activity_type}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert activity to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "activity_type": self.activity_type,
            "description": self.description,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "activity_metadata": self.activity_metadata,
            "created_at": self.created_at.isoformat()
        } 