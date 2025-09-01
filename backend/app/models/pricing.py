"""
Tokenized Pricing Models for CloudMind Consulting Platform
"""

from sqlalchemy import Column, String, Numeric, Integer, DateTime, Text, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
import uuid

from app.core.database import Base


class UnitType(str, Enum):
    """Pricing unit types for service tokens"""
    PER_RESOURCE = "per_resource"
    PER_HOUR = "per_hour"
    FLAT_RATE = "flat_rate"
    PERCENTAGE_SAVINGS = "percentage_savings"
    PER_GB = "per_gb"
    PER_API_CALL = "per_api_call"


class ServiceCategory(str, Enum):
    """Service categories for organization"""
    SCANNING = "scanning"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"
    IMPLEMENTATION = "implementation"
    MONITORING = "monitoring"
    CONSULTING = "consulting"
    TRAINING = "training"


class EngagementStatus(str, Enum):
    """Client engagement status"""
    DRAFT = "draft"
    PROPOSED = "proposed"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class ServiceToken(Base):
    """Tokenized services for transparent pricing"""
    __tablename__ = "service_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    unit_type = Column(SQLEnum(UnitType), nullable=False)
    category = Column(SQLEnum(ServiceCategory), nullable=False)
    
    # Pricing modifiers
    minimum_quantity = Column(Integer, default=1)
    maximum_quantity = Column(Integer, nullable=True)
    volume_discount_threshold = Column(Integer, nullable=True)
    volume_discount_rate = Column(Numeric(5, 4), nullable=True)  # e.g., 0.15 for 15%
    
    # Metadata
    is_active = Column(Boolean, default=True)
    requires_approval = Column(Boolean, default=False)
    estimated_duration_hours = Column(Numeric(5, 2), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    engagement_items = relationship("EngagementItem", back_populates="service_token")


class ClientEngagement(Base):
    """Client consulting engagement tracking"""
    __tablename__ = "client_engagements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    # Engagement details
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(EngagementStatus), default=EngagementStatus.DRAFT)
    
    # Pricing
    total_cost = Column(Numeric(12, 2), default=0)
    estimated_cost = Column(Numeric(12, 2), nullable=True)
    approved_budget = Column(Numeric(12, 2), nullable=True)
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0)
    resources_discovered = Column(Integer, default=0)
    resources_analyzed = Column(Integer, default=0)
    optimizations_identified = Column(Integer, default=0)
    
    # Financial metrics
    projected_monthly_savings = Column(Numeric(12, 2), default=0)
    actual_monthly_savings = Column(Numeric(12, 2), nullable=True)
    roi_percentage = Column(Numeric(8, 2), nullable=True)
    payback_months = Column(Numeric(5, 2), nullable=True)
    
    # Timeline
    start_date = Column(DateTime(timezone=True), nullable=True)
    estimated_completion_date = Column(DateTime(timezone=True), nullable=True)
    actual_completion_date = Column(DateTime(timezone=True), nullable=True)
    
    # GitHub integration
    github_repo_url = Column(String(500), nullable=True)
    github_repo_created = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    client = relationship("User", back_populates="engagements")
    items = relationship("EngagementItem", back_populates="engagement", cascade="all, delete-orphan")
    progress_events = relationship("ProgressEvent", back_populates="engagement", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="engagement", cascade="all, delete-orphan")


class EngagementItem(Base):
    """Individual service items within an engagement"""
    __tablename__ = "engagement_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engagement_id = Column(UUID(as_uuid=True), ForeignKey('client_engagements.id'), nullable=False)
    service_token_id = Column(UUID(as_uuid=True), ForeignKey('service_tokens.id'), nullable=False)
    
    # Pricing details
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(12, 2), nullable=False)
    discount_applied = Column(Numeric(5, 4), default=0)  # Percentage discount
    
    # Status
    is_completed = Column(Boolean, default=False)
    completion_date = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    notes = Column(Text, nullable=True)
    estimated_hours = Column(Numeric(5, 2), nullable=True)
    actual_hours = Column(Numeric(5, 2), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    engagement = relationship("ClientEngagement", back_populates="items")
    service_token = relationship("ServiceToken", back_populates="engagement_items")


class ProgressEvent(Base):
    """Real-time progress tracking events"""
    __tablename__ = "progress_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engagement_id = Column(UUID(as_uuid=True), ForeignKey('client_engagements.id'), nullable=False)
    
    # Event details
    event_type = Column(String(100), nullable=False)  # 'scan_started', 'resource_analyzed', etc.
    event_description = Column(Text, nullable=False)
    
    # Progress metrics
    progress_percentage = Column(Numeric(5, 2), nullable=True)
    resources_processed = Column(Integer, nullable=True)
    cost_incurred = Column(Numeric(10, 2), default=0)
    savings_identified = Column(Numeric(12, 2), default=0)
    
    # Context data (JSON)
    event_data = Column(Text, nullable=True)  # JSON string for additional context
    
    # Visibility
    visible_to_client = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    engagement = relationship("ClientEngagement", back_populates="progress_events")


class Invoice(Base):
    """Generated invoices for client engagements"""
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engagement_id = Column(UUID(as_uuid=True), ForeignKey('client_engagements.id'), nullable=False)
    
    # Invoice details
    invoice_number = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0)
    discount_amount = Column(Numeric(10, 2), default=0)
    
    # Status and dates
    status = Column(String(50), default='draft')  # draft, sent, paid, overdue, cancelled
    issue_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True), nullable=False)
    paid_date = Column(DateTime(timezone=True), nullable=True)
    
    # Payment details
    payment_method = Column(String(100), nullable=True)
    payment_reference = Column(String(255), nullable=True)
    
    # File paths
    pdf_path = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    engagement = relationship("ClientEngagement", back_populates="invoices")


class PricingRule(Base):
    """Dynamic pricing rules for automated discounts/premiums"""
    __tablename__ = "pricing_rules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Rule details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    condition_expression = Column(Text, nullable=False)  # e.g., "total_resources > 100"
    
    # Modifier
    modifier_type = Column(String(50), nullable=False)  # 'discount', 'premium', 'flat_fee'
    modifier_value = Column(Numeric(10, 4), nullable=False)  # e.g., 0.85 for 15% discount
    
    # Applicability
    applies_to_categories = Column(Text, nullable=True)  # JSON array of categories
    minimum_engagement_value = Column(Numeric(12, 2), nullable=True)
    maximum_engagement_value = Column(Numeric(12, 2), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Higher priority rules apply first
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
