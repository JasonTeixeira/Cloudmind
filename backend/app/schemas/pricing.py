"""
Pydantic schemas for tokenized pricing system
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from app.models.pricing import UnitType, ServiceCategory, EngagementStatus


class ServiceTokenBase(BaseModel):
    """Base schema for service tokens"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    base_price: Decimal = Field(..., gt=0)
    unit_type: UnitType
    category: ServiceCategory
    minimum_quantity: int = Field(default=1, ge=1)
    maximum_quantity: Optional[int] = Field(default=None, ge=1)
    volume_discount_threshold: Optional[int] = Field(default=None, ge=1)
    volume_discount_rate: Optional[Decimal] = Field(default=None, ge=0, le=1)
    is_active: bool = Field(default=True)
    requires_approval: bool = Field(default=False)
    estimated_duration_hours: Optional[Decimal] = Field(default=None, ge=0)


class ServiceTokenCreate(ServiceTokenBase):
    """Schema for creating service tokens"""
    pass


class ServiceTokenUpdate(BaseModel):
    """Schema for updating service tokens"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    base_price: Optional[Decimal] = Field(None, gt=0)
    unit_type: Optional[UnitType] = None
    category: Optional[ServiceCategory] = None
    minimum_quantity: Optional[int] = Field(None, ge=1)
    maximum_quantity: Optional[int] = Field(None, ge=1)
    volume_discount_threshold: Optional[int] = Field(None, ge=1)
    volume_discount_rate: Optional[Decimal] = Field(None, ge=0, le=1)
    is_active: Optional[bool] = None
    requires_approval: Optional[bool] = None
    estimated_duration_hours: Optional[Decimal] = Field(None, ge=0)


class ServiceToken(ServiceTokenBase):
    """Schema for service token responses"""
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EngagementItemBase(BaseModel):
    """Base schema for engagement items"""
    service_token_id: UUID
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., gt=0)
    total_price: Decimal = Field(..., gt=0)
    discount_applied: Decimal = Field(default=Decimal('0'), ge=0, le=1)
    notes: Optional[str] = None
    estimated_hours: Optional[Decimal] = Field(default=None, ge=0)


class EngagementItemCreate(EngagementItemBase):
    """Schema for creating engagement items"""
    pass


class EngagementItem(EngagementItemBase):
    """Schema for engagement item responses"""
    id: UUID
    engagement_id: UUID
    is_completed: bool = False
    completion_date: Optional[datetime] = None
    actual_hours: Optional[Decimal] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Relationships
    service_token: Optional[ServiceToken] = None

    class Config:
        from_attributes = True


class ClientEngagementBase(BaseModel):
    """Base schema for client engagements"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    estimated_cost: Optional[Decimal] = Field(default=None, ge=0)
    approved_budget: Optional[Decimal] = Field(default=None, ge=0)
    start_date: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None


class ClientEngagementCreate(ClientEngagementBase):
    """Schema for creating client engagements"""
    client_id: UUID
    items: List[EngagementItemCreate] = Field(default_factory=list)


class ClientEngagementUpdate(BaseModel):
    """Schema for updating client engagements"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[EngagementStatus] = None
    estimated_cost: Optional[Decimal] = Field(None, ge=0)
    approved_budget: Optional[Decimal] = Field(None, ge=0)
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)
    projected_monthly_savings: Optional[Decimal] = Field(None, ge=0)
    actual_monthly_savings: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    github_repo_url: Optional[str] = None


class ClientEngagement(ClientEngagementBase):
    """Schema for client engagement responses"""
    id: UUID
    client_id: UUID
    status: EngagementStatus
    total_cost: Decimal
    progress_percentage: int = 0
    resources_discovered: int = 0
    resources_analyzed: int = 0
    optimizations_identified: int = 0
    projected_monthly_savings: Decimal = Decimal('0')
    actual_monthly_savings: Optional[Decimal] = None
    roi_percentage: Optional[Decimal] = None
    payback_months: Optional[Decimal] = None
    github_repo_url: Optional[str] = None
    github_repo_created: bool = False
    actual_completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Relationships
    items: List[EngagementItem] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ProgressEventBase(BaseModel):
    """Base schema for progress events"""
    event_type: str = Field(..., min_length=1, max_length=100)
    event_description: str = Field(..., min_length=1)
    progress_percentage: Optional[Decimal] = Field(default=None, ge=0, le=100)
    resources_processed: Optional[int] = Field(default=None, ge=0)
    cost_incurred: Decimal = Field(default=Decimal('0'), ge=0)
    savings_identified: Decimal = Field(default=Decimal('0'), ge=0)
    event_data: Optional[str] = None  # JSON string
    visible_to_client: bool = Field(default=True)


class ProgressEventCreate(ProgressEventBase):
    """Schema for creating progress events"""
    engagement_id: UUID


class ProgressEvent(ProgressEventBase):
    """Schema for progress event responses"""
    id: UUID
    engagement_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PricingCalculationRequest(BaseModel):
    """Request schema for pricing calculations"""
    service_tokens: List[Dict[str, Any]] = Field(..., description="List of service tokens with quantities")
    client_id: Optional[UUID] = None
    apply_volume_discounts: bool = Field(default=True)
    apply_pricing_rules: bool = Field(default=True)

    @field_validator('service_tokens')
    @classmethod
    def validate_service_tokens(cls, v):
        """Validate service tokens structure"""
        for token in v:
            if 'service_token_id' not in token or 'quantity' not in token:
                raise ValueError("Each service token must have 'service_token_id' and 'quantity'")
            if not isinstance(token['quantity'], int) or token['quantity'] < 1:
                raise ValueError("Quantity must be a positive integer")
        return v


class PricingCalculationResponse(BaseModel):
    """Response schema for pricing calculations"""
    total_cost: Decimal = Field(...)
    subtotal: Decimal = Field(...)
    total_discount: Decimal = Field(default=Decimal('0'))
    discount_percentage: Decimal = Field(default=Decimal('0'), ge=0, le=100)
    estimated_duration_hours: Optional[Decimal] = None
    
    # Breakdown by category
    breakdown_by_category: Dict[str, Decimal] = Field(default_factory=dict)
    
    # Individual items
    items: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Applied discounts/rules
    applied_rules: List[str] = Field(default_factory=list)
    
    # ROI calculations (if savings provided)
    projected_monthly_savings: Optional[Decimal] = None
    roi_percentage: Optional[Decimal] = None
    payback_months: Optional[Decimal] = None


class InvoiceBase(BaseModel):
    """Base schema for invoices"""
    total_amount: Decimal = Field(..., gt=0)
    tax_amount: Decimal = Field(default=Decimal('0'), ge=0)
    discount_amount: Decimal = Field(default=Decimal('0'), ge=0)
    due_date: datetime
    payment_method: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    """Schema for creating invoices"""
    engagement_id: UUID


class Invoice(InvoiceBase):
    """Schema for invoice responses"""
    id: UUID
    engagement_id: UUID
    invoice_number: str
    status: str
    issue_date: datetime
    paid_date: Optional[datetime] = None
    payment_reference: Optional[str] = None
    pdf_path: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EngagementDashboard(BaseModel):
    """Dashboard view for client engagements"""
    engagement: ClientEngagement
    recent_progress: List[ProgressEvent] = Field(default_factory=list)
    cost_breakdown: Dict[str, Decimal] = Field(default_factory=dict)
    savings_timeline: List[Dict[str, Any]] = Field(default_factory=list)
    next_milestones: List[str] = Field(default_factory=list)
    
    # Real-time metrics
    current_roi: Optional[Decimal] = None
    time_to_break_even: Optional[str] = None
    completion_eta: Optional[datetime] = None


class AdminPricingDashboard(BaseModel):
    """Admin dashboard for pricing management"""
    active_engagements: List[ClientEngagement] = Field(default_factory=list)
    monthly_revenue: Decimal = Field(default=Decimal('0'))
    ytd_revenue: Decimal = Field(default=Decimal('0'))
    average_engagement_value: Decimal = Field(default=Decimal('0'))
    total_savings_delivered: Decimal = Field(default=Decimal('0'))
    
    # Service token performance
    popular_services: List[Dict[str, Any]] = Field(default_factory=list)
    revenue_by_category: Dict[str, Decimal] = Field(default_factory=dict)
    
    # Trends
    monthly_trends: List[Dict[str, Any]] = Field(default_factory=list)
