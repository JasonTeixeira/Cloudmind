"""
User Schemas for Enhanced Authentication System
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator
from enum import Enum

from app.models.user import UserRole, UserStatus


class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")


class LoginResponse(BaseModel):
    """Login response model"""
    user: Dict[str, Any] = Field(..., description="User information")
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class UserCreate(BaseModel):
    """User creation model (flexible to accept frontend variations)."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    username: Optional[str] = Field(None, min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    # Accept camelCase from frontend while keeping snake_case internally
    first_name: Optional[str] = Field(None, alias="firstName", description="First name")
    last_name: Optional[str] = Field(None, alias="lastName", description="Last name")
    role: UserRole = Field(default=UserRole.VIEWER, description="User role")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    job_title: Optional[str] = Field(None, max_length=255, description="Job title")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    location: Optional[str] = Field(None, max_length=255, description="Location")
    timezone: Optional[str] = Field(default="UTC", description="Timezone")
    is_master_user: bool = Field(default=False, description="Master user flag")

    @field_validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        # Require at least one special character
        special_chars = set("!@#$%^&*()-_=+[]{}|;:'\",.<>/?`~")
        if not any(c in special_chars for c in v):
            raise ValueError('Password must contain at least one special character')
        # Block common weak passwords
        common_weak = {"password", "123456", "qwerty", "abc123", "letmein", "admin"}
        if v.lower() in common_weak:
            raise ValueError('Password is too common and easily guessable')
        return v

    @field_validator('username')
    def validate_username(cls, v):
        """Validate username"""
        if v is None:
            return v
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v

    model_config = {
        "populate_by_name": True,
        "extra": "allow",
    }


class UserUpdate(BaseModel):
    """User update model"""
    email: Optional[EmailStr] = Field(None, description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=100, description="Username")
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    role: Optional[UserRole] = Field(None, description="User role")
    status: Optional[UserStatus] = Field(None, description="User status")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    job_title: Optional[str] = Field(None, max_length=255, description="Job title")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    location: Optional[str] = Field(None, max_length=255, description="Location")
    timezone: Optional[str] = Field(None, description="Timezone")
    is_active: Optional[bool] = Field(None, description="Active status")
    is_verified: Optional[bool] = Field(None, description="Verified status")
    is_master_user: Optional[bool] = Field(None, description="Master user flag")


class UserProfileUpdate(BaseModel):
    """User profile update model (for current user)"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Full name")
    company: Optional[str] = Field(None, max_length=255, description="Company name")
    job_title: Optional[str] = Field(None, max_length=255, description="Job title")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    location: Optional[str] = Field(None, max_length=255, description="Location")
    timezone: Optional[str] = Field(None, description="Timezone")
    bio: Optional[str] = Field(None, max_length=1000, description="User bio")
    avatar_url: Optional[str] = Field(None, max_length=500, description="Avatar URL")
    preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    notification_settings: Optional[Dict[str, Any]] = Field(None, description="Notification settings")
    ui_settings: Optional[Dict[str, Any]] = Field(None, description="UI settings")


class UserResponse(BaseModel):
    """User response model"""
    id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    role: UserRole = Field(..., description="User role")
    is_master_user: bool = Field(..., description="Master user flag")
    is_superuser: bool = Field(..., description="Superuser flag")
    is_verified: bool = Field(..., description="Verified status")
    is_active: bool = Field(..., description="Active status")
    status: UserStatus = Field(..., description="User status")
    avatar_url: Optional[str] = Field(None, description="Avatar URL")
    company: Optional[str] = Field(None, description="Company name")
    job_title: Optional[str] = Field(None, description="Job title")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Location")
    timezone: str = Field(..., description="Timezone")
    last_login: Optional[datetime] = Field(None, description="Last login time")
    last_activity: Optional[datetime] = Field(None, description="Last activity time")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    permissions: Dict[str, bool] = Field(..., description="User permissions")


class UserListResponse(BaseModel):
    """User list response model"""
    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    skip: int = Field(..., description="Number of skipped users")
    limit: int = Field(..., description="Number of users per page")


class ChangePasswordRequest(BaseModel):
    """Change password request model"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")
    
    @field_validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class ResetPasswordRequest(BaseModel):
    """Reset password request model"""
    email: EmailStr = Field(..., description="User email address")


class UserActivityResponse(BaseModel):
    """User activity response model"""
    id: UUID = Field(..., description="Activity ID")
    user_id: UUID = Field(..., description="User ID")
    activity_type: str = Field(..., description="Activity type")
    description: str = Field(..., description="Activity description")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(..., description="Activity timestamp")


class MasterDashboardData(BaseModel):
    """Master dashboard data model"""
    total_users: int = Field(..., description="Total number of users")
    active_users: int = Field(..., description="Number of active users")
    total_projects: int = Field(..., description="Total number of projects")
    total_cost_analyses: int = Field(..., description="Total number of cost analyses")
    total_security_scans: int = Field(..., description="Total number of security scans")
    recent_activities: List[UserActivityResponse] = Field(..., description="Recent user activities")
    user_stats: Dict[str, int] = Field(..., description="User statistics by role")
    system_health: Dict[str, Any] = Field(..., description="System health metrics")


class UserPermissions(BaseModel):
    """User permissions model"""
    can_access_all_projects: bool = Field(..., description="Can access all projects")
    can_manage_users: bool = Field(..., description="Can manage users")
    can_view_reports: bool = Field(..., description="Can view advanced reports")
    is_master: bool = Field(..., description="Is master user")
    can_create_projects: bool = Field(..., description="Can create projects")
    can_delete_projects: bool = Field(..., description="Can delete projects")
    can_manage_infrastructure: bool = Field(..., description="Can manage infrastructure")
    can_view_analytics: bool = Field(..., description="Can view analytics")


class UserSession(BaseModel):
    """User session model"""
    user_id: UUID = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    ip_address: str = Field(..., description="IP address")
    user_agent: str = Field(..., description="User agent")
    created_at: datetime = Field(..., description="Session creation time")
    last_activity: datetime = Field(..., description="Last activity time")
    expires_at: datetime = Field(..., description="Session expiration time") 