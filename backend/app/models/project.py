"""
Project model for CloudMind
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Project(Base):
    """Project model for organizing cloud resources and analyses"""
    
    __tablename__ = "projects"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic fields
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    
    # Owner
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Project settings
    is_public = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Cloud provider settings
    cloud_providers = Column(JSON, nullable=True)  # AWS, Azure, GCP configs
    regions = Column(JSON, nullable=True)  # Target regions
    tags = Column(JSON, nullable=True)  # Resource tags
    
    # Budget and cost settings
    monthly_budget = Column(Integer, nullable=True)  # Monthly budget in cents
    cost_alerts_enabled = Column(Boolean, default=True, nullable=False)
    cost_alert_threshold = Column(Integer, default=80, nullable=False)  # Percentage
    
    # Security settings
    security_scan_enabled = Column(Boolean, default=True, nullable=False)
    compliance_frameworks = Column(JSON, nullable=True)  # SOC2, HIPAA, etc.
    
    # AI settings
    ai_insights_enabled = Column(Boolean, default=True, nullable=False)
    ai_model_preferences = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    cost_analyses = relationship("CostAnalysis", back_populates="project", cascade="all, delete-orphan")
    security_scans = relationship("SecurityScan", back_populates="project", cascade="all, delete-orphan")
    infrastructures = relationship("Infrastructure", back_populates="project", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="project", cascade="all, delete-orphan")
    
    # New relationships for collaboration and notifications
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="project", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.name}, slug={self.slug})>"
    
    @property
    def total_cost(self) -> int:
        """Calculate total cost for the project"""
        if not self.cost_analyses:
            return 0
        return sum(analysis.total_cost for analysis in self.cost_analyses if analysis.total_cost)
    
    @property
    def monthly_cost(self) -> int:
        """Calculate monthly cost for the project"""
        if not self.cost_analyses:
            return 0
        # Get the most recent cost analysis
        latest_analysis = max(self.cost_analyses, key=lambda x: x.created_at) if self.cost_analyses else None
        return latest_analysis.total_cost if latest_analysis else 0
    
    def to_dict(self) -> dict:
        """Convert project to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "slug": self.slug,
            "owner_id": str(self.owner_id),
            "is_public": self.is_public,
            "is_active": self.is_active,
            "cloud_providers": self.cloud_providers,
            "regions": self.regions,
            "tags": self.tags,
            "monthly_budget": self.monthly_budget,
            "cost_alerts_enabled": self.cost_alerts_enabled,
            "cost_alert_threshold": self.cost_alert_threshold,
            "security_scan_enabled": self.security_scan_enabled,
            "compliance_frameworks": self.compliance_frameworks,
            "ai_insights_enabled": self.ai_insights_enabled,
            "ai_model_preferences": self.ai_model_preferences,
            "total_cost": self.total_cost,
            "monthly_cost": self.monthly_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 