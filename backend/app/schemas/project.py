"""
Project schemas for CloudMind API
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator
import re


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = False
    is_active: bool = True
    # Accept either a dict or a simple list of providers for flexibility
    cloud_providers: Optional[Any] = None
    regions: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    monthly_budget: Optional[int] = Field(None, ge=0)  # Budget in cents
    cost_alerts_enabled: bool = True
    cost_alert_threshold: int = Field(default=80, ge=1, le=100)  # Percentage
    security_scan_enabled: bool = True
    compliance_frameworks: Optional[List[str]] = None
    ai_insights_enabled: bool = True
    ai_model_preferences: Optional[Dict[str, Any]] = None
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate project name"""
        if not v.strip():
            raise ValueError('Project name cannot be empty')
        return v.strip()
    
    @field_validator('monthly_budget')
    def validate_monthly_budget(cls, v):
        """Validate monthly budget"""
        if v is not None and v < 0:
            raise ValueError('Monthly budget cannot be negative')
        return v
    
    @field_validator('cost_alert_threshold')
    def validate_cost_alert_threshold(cls, v):
        """Validate cost alert threshold"""
        if v < 1 or v > 100:
            raise ValueError('Cost alert threshold must be between 1 and 100')
        return v


class ProjectCreate(ProjectBase):
    """Schema for creating a new project"""
    slug: Optional[str] = Field(None, min_length=1, max_length=100)
    
    @field_validator('slug')
    def validate_slug(cls, v):
        """Validate project slug"""
        if v is not None:
            if not re.match(r'^[a-z0-9-]+$', v):
                raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v


class ProjectUpdate(BaseModel):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None
    cloud_providers: Optional[Dict[str, Any]] = None
    regions: Optional[List[str]] = None
    tags: Optional[Dict[str, str]] = None
    monthly_budget: Optional[int] = Field(None, ge=0)
    cost_alerts_enabled: Optional[bool] = None
    cost_alert_threshold: Optional[int] = Field(None, ge=1, le=100)
    security_scan_enabled: Optional[bool] = None
    compliance_frameworks: Optional[List[str]] = None
    ai_insights_enabled: Optional[bool] = None
    ai_model_preferences: Optional[Dict[str, Any]] = None
    
    @field_validator('name')
    def validate_name(cls, v):
        """Validate project name if provided"""
        if v is not None and not v.strip():
            raise ValueError('Project name cannot be empty')
        return v.strip() if v is not None else v
    
    @field_validator('monthly_budget')
    def validate_monthly_budget(cls, v):
        """Validate monthly budget if provided"""
        if v is not None and v < 0:
            raise ValueError('Monthly budget cannot be negative')
        return v
    
    @field_validator('cost_alert_threshold')
    def validate_cost_alert_threshold(cls, v):
        """Validate cost alert threshold if provided"""
        if v is not None and (v < 1 or v > 100):
            raise ValueError('Cost alert threshold must be between 1 and 100')
        return v


class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: str
    slug: str
    owner_id: str
    total_cost: int  # Total cost in cents
    monthly_cost: int  # Monthly cost in cents
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    """Schema for project summary"""
    id: str
    name: str
    slug: str
    description: Optional[str]
    is_public: bool
    is_active: bool
    total_cost: int
    monthly_cost: int
    total_resources: int
    running_resources: int
    security_score: Optional[float]
    compliance_score: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProjectStats(BaseModel):
    """Schema for project statistics"""
    total_projects: int
    active_projects: int
    total_cost: int
    monthly_cost: int
    total_resources: int
    running_resources: int
    security_vulnerabilities: int
    cost_savings: int
    ai_insights: int


class ProjectInvite(BaseModel):
    """Schema for project invitation"""
    email: str = Field(..., min_length=1, max_length=255)
    role: str = Field(default="member", pattern="^(owner|admin|member|viewer)$")
    message: Optional[str] = None


class ProjectMember(BaseModel):
    """Schema for project member"""
    user_id: str
    email: str
    username: str
    full_name: Optional[str]
    role: str
    joined_at: datetime
    last_active: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProjectRole(BaseModel):
    """Schema for project role"""
    role: str = Field(..., pattern="^(owner|admin|member|viewer)$")
    permissions: List[str] = Field(default_factory=list)
    description: Optional[str] = None


class ProjectSettings(BaseModel):
    """Schema for project settings"""
    cost_alerts_enabled: bool
    cost_alert_threshold: int
    security_scan_enabled: bool
    ai_insights_enabled: bool
    monitoring_enabled: bool
    backup_enabled: bool
    compliance_frameworks: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)
    tags: Dict[str, str] = Field(default_factory=dict) 