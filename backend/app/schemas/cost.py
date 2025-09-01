"""
Cost analysis schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class CostAnalysisBase(BaseModel):
    """Base cost analysis schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Analysis name")
    description: Optional[str] = Field(None, max_length=1000, description="Analysis description")
    project_id: Optional[UUID] = Field(None, description="Associated project ID")
    cloud_provider: str = Field(..., description="Cloud provider (AWS, Azure, GCP)")
    regions: List[str] = Field(default_factory=list, description="Target regions")
    services: List[str] = Field(default_factory=list, description="Services to analyze")
    date_from: datetime = Field(..., description="Analysis start date")
    date_to: datetime = Field(..., description="Analysis end date")
    currency: str = Field(default="USD", description="Currency for cost calculations")


class CostAnalysisCreate(CostAnalysisBase):
    """Create cost analysis schema"""
    pass


class CostAnalysisUpdate(BaseModel):
    """Update cost analysis schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    cloud_provider: Optional[str] = Field(None)
    regions: Optional[List[str]] = Field(None)
    services: Optional[List[str]] = Field(None)
    date_from: Optional[datetime] = Field(None)
    date_to: Optional[datetime] = Field(None)
    currency: Optional[str] = Field(None)


class CostAnalysisResponse(CostAnalysisBase):
    """Cost analysis response schema"""
    id: UUID
    user_id: UUID
    total_cost: float = Field(..., description="Total cost in cents")
    total_cost_formatted: str = Field(..., description="Formatted total cost")
    cost_breakdown: Dict[str, float] = Field(default_factory=dict, description="Cost breakdown by service")
    recommendations_count: int = Field(default=0, description="Number of recommendations")
    savings_potential: float = Field(default=0, description="Potential savings in cents")
    status: str = Field(..., description="Analysis status")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CostRecommendationBase(BaseModel):
    """Base cost recommendation schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Recommendation title")
    description: str = Field(..., min_length=1, max_length=2000, description="Recommendation description")
    category: str = Field(..., description="Recommendation category")
    priority: str = Field(..., description="Priority level (low, medium, high, critical)")
    estimated_savings: float = Field(..., description="Estimated savings in cents")
    implementation_effort: str = Field(..., description="Implementation effort (low, medium, high)")
    risk_level: str = Field(..., description="Risk level (low, medium, high)")


class CostRecommendationCreate(CostRecommendationBase):
    """Create cost recommendation schema"""
    cost_analysis_id: UUID = Field(..., description="Associated cost analysis ID")
    resource_id: Optional[str] = Field(None, description="Affected resource ID")
    resource_type: Optional[str] = Field(None, description="Resource type")
    current_cost: float = Field(..., description="Current cost in cents")
    recommended_cost: float = Field(..., description="Recommended cost in cents")


class CostRecommendationResponse(CostRecommendationBase):
    """Cost recommendation response schema"""
    id: UUID
    cost_analysis_id: UUID
    resource_id: Optional[str]
    resource_type: Optional[str]
    current_cost: float
    recommended_cost: float
    savings_percentage: float = Field(..., description="Savings percentage")
    is_applied: bool = Field(default=False, description="Whether recommendation was applied")
    applied_at: Optional[datetime] = Field(None, description="When recommendation was applied")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CostSummary(BaseModel):
    """Cost summary schema"""
    total_cost: float = Field(..., description="Total cost in cents")
    total_cost_formatted: str = Field(..., description="Formatted total cost")
    period_cost: float = Field(..., description="Cost for the specified period")
    period_cost_formatted: str = Field(..., description="Formatted period cost")
    cost_change: float = Field(..., description="Cost change from previous period")
    cost_change_percentage: float = Field(..., description="Cost change percentage")
    top_services: List[Dict[str, Any]] = Field(default_factory=list, description="Top cost services")
    cost_by_region: Dict[str, float] = Field(default_factory=dict, description="Cost by region")
    cost_by_service: Dict[str, float] = Field(default_factory=dict, description="Cost by service")
    recommendations_count: int = Field(default=0, description="Number of recommendations")
    potential_savings: float = Field(default=0, description="Potential savings")
    period: str = Field(..., description="Analysis period")


class CostTrend(BaseModel):
    """Cost trend schema"""
    date: datetime = Field(..., description="Trend date")
    cost: float = Field(..., description="Cost for this date")
    cost_formatted: str = Field(..., description="Formatted cost")
    change_from_previous: float = Field(..., description="Change from previous period")
    change_percentage: float = Field(..., description="Change percentage")
    services_count: int = Field(default=0, description="Number of active services")


class CostAlert(BaseModel):
    """Cost alert schema"""
    id: UUID
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    severity: str = Field(..., description="Alert severity (info, warning, error, critical)")
    category: str = Field(..., description="Alert category")
    project_id: Optional[UUID] = Field(None, description="Associated project")
    cost_threshold: Optional[float] = Field(None, description="Cost threshold that triggered alert")
    current_cost: Optional[float] = Field(None, description="Current cost")
    is_resolved: bool = Field(default=False, description="Whether alert is resolved")
    resolved_at: Optional[datetime] = Field(None, description="When alert was resolved")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CostOptimizationRequest(BaseModel):
    """Cost optimization request schema"""
    project_id: Optional[UUID] = Field(None, description="Project to optimize")
    target_savings: Optional[float] = Field(None, description="Target savings percentage")
    risk_tolerance: str = Field(default="medium", description="Risk tolerance level")
    optimization_categories: List[str] = Field(default_factory=list, description="Categories to optimize")
    exclude_services: List[str] = Field(default_factory=list, description="Services to exclude")


class CostOptimizationResponse(BaseModel):
    """Cost optimization response schema"""
    analysis_id: UUID
    recommendations: List[CostRecommendationResponse]
    total_potential_savings: float
    total_potential_savings_formatted: str
    implementation_plan: Dict[str, Any]
    estimated_timeline: str
    risk_assessment: Dict[str, Any] 