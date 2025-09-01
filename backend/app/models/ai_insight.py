"""
AI insight models for CloudMind
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, ForeignKey, Integer, Float, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class InsightType(str, enum.Enum):
    """Types of AI insights"""
    COST_OPTIMIZATION = "cost_optimization"
    SECURITY_RECOMMENDATION = "security_recommendation"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    ARCHITECTURE_SUGGESTION = "architecture_suggestion"
    COMPLIANCE_CHECK = "compliance_check"
    RESOURCE_PLANNING = "resource_planning"
    ANOMALY_DETECTION = "anomaly_detection"


class InsightPriority(str, enum.Enum):
    """Insight priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AIInsight(Base):
    """AI insight model for storing AI-generated recommendations"""
    
    __tablename__ = "ai_insights"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    # Insight metadata
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    insight_type = Column(Enum(InsightType), nullable=False)
    priority = Column(Enum(InsightPriority), default=InsightPriority.MEDIUM, nullable=False)
    
    # AI model information
    ai_model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=True)
    confidence_score = Column(Float, nullable=True)  # 0-1 confidence score
    ai_model_version = Column(String(50), nullable=True)
    
    # Insight data
    analysis_data = Column(JSON, nullable=True)  # Raw analysis data
    recommendations = Column(JSON, nullable=True)  # Structured recommendations
    impact_analysis = Column(JSON, nullable=True)  # Impact assessment
    implementation_steps = Column(JSON, nullable=True)  # Step-by-step implementation
    
    # Context and scope
    affected_resources = Column(JSON, nullable=True)  # Resources this insight affects
    tags = Column(JSON, nullable=True)  # Categorization tags
    categories = Column(JSON, nullable=True)  # Insight categories
    
    # Status and tracking
    is_implemented = Column(Boolean, default=False, nullable=False)
    is_acknowledged = Column(Boolean, default=False, nullable=False)
    is_dismissed = Column(Boolean, default=False, nullable=False)
    
    # Implementation tracking
    implemented_at = Column(DateTime(timezone=True), nullable=True)
    implemented_by = Column(String(255), nullable=True)
    implementation_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="ai_insights")
    project = relationship("Project", back_populates="ai_insights")
    ai_model = relationship("AIModel", back_populates="insights")
    
    def __repr__(self):
        return f"<AIInsight(id={self.id}, title={self.title}, type={self.insight_type})>"
    
    @property
    def priority_color(self) -> str:
        """Get priority color for UI"""
        if self.priority == InsightPriority.CRITICAL:
            return "red"
        elif self.priority == InsightPriority.HIGH:
            return "orange"
        elif self.priority == InsightPriority.MEDIUM:
            return "yellow"
        elif self.priority == InsightPriority.LOW:
            return "blue"
        return "gray"
    
    @property
    def is_actionable(self) -> bool:
        """Check if insight is actionable"""
        return not self.is_dismissed and not self.is_implemented
    
    @property
    def status(self) -> str:
        """Get insight status"""
        if self.is_implemented:
            return "implemented"
        elif self.is_dismissed:
            return "dismissed"
        elif self.is_acknowledged:
            return "acknowledged"
        return "new"
    
    def to_dict(self) -> dict:
        """Convert AI insight to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "project_id": str(self.project_id) if self.project_id else None,
            "title": self.title,
            "description": self.description,
            "insight_type": self.insight_type.value,
            "priority": self.priority.value,
            "ai_model_id": str(self.ai_model_id) if self.ai_model_id else None,
            "confidence_score": self.confidence_score,
            "ai_model_version": self.ai_model_version,
            "analysis_data": self.analysis_data,
            "recommendations": self.recommendations,
            "impact_analysis": self.impact_analysis,
            "implementation_steps": self.implementation_steps,
            "affected_resources": self.affected_resources,
            "tags": self.tags,
            "categories": self.categories,
            "is_implemented": self.is_implemented,
            "is_acknowledged": self.is_acknowledged,
            "is_dismissed": self.is_dismissed,
            "implemented_at": self.implemented_at.isoformat() if self.implemented_at else None,
            "implemented_by": self.implemented_by,
            "implementation_notes": self.implementation_notes,
            "priority_color": self.priority_color,
            "is_actionable": self.is_actionable,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class AIModel(Base):
    """AI model model for tracking AI models used"""
    
    __tablename__ = "ai_models"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Model identification
    name = Column(String(255), nullable=False)
    version = Column(String(50), nullable=False)
    provider = Column(String(100), nullable=False)  # OpenAI, Anthropic, Local, etc.
    model_type = Column(String(100), nullable=False)  # LLM, Embedding, Classification, etc.
    
    # Model configuration
    parameters = Column(JSON, nullable=True)  # Model parameters
    capabilities = Column(JSON, nullable=True)  # Model capabilities
    limitations = Column(JSON, nullable=True)  # Model limitations
    
    # Performance metrics
    accuracy_score = Column(Float, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    cost_per_token = Column(Float, nullable=True)
    
    # Usage tracking
    total_requests = Column(Integer, default=0, nullable=False)
    successful_requests = Column(Integer, default=0, nullable=False)
    failed_requests = Column(Integer, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    insights = relationship("AIInsight", back_populates="ai_model", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AIModel(id={self.id}, name={self.name}, version={self.version}, provider={self.provider})>"
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def failure_rate(self) -> float:
        """Calculate failure rate"""
        if self.total_requests == 0:
            return 0.0
        return self.failed_requests / self.total_requests
    
    @property
    def full_name(self) -> str:
        """Get full model name"""
        return f"{self.name}-{self.version}"
    
    def to_dict(self) -> dict:
        """Convert AI model to dictionary"""
        return {
            "id": str(self.id),
            "name": self.name,
            "version": self.version,
            "provider": self.provider,
            "model_type": self.model_type,
            "parameters": self.parameters,
            "capabilities": self.capabilities,
            "limitations": self.limitations,
            "accuracy_score": self.accuracy_score,
            "latency_ms": self.latency_ms,
            "cost_per_token": self.cost_per_token,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "is_active": self.is_active,
            "is_default": self.is_default,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used": self.last_used.isoformat() if self.last_used else None,
        } 