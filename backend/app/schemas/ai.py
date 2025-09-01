"""
AI Engine schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class AIInsightBase(BaseModel):
    """Base AI insight schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Insight title")
    description: str = Field(..., min_length=1, max_length=2000, description="Insight description")
    category: str = Field(..., description="Insight category")
    priority: str = Field(..., description="Priority level (low, medium, high, critical)")
    confidence_score: float = Field(..., ge=0, le=100, description="AI confidence score")
    impact_score: float = Field(..., ge=0, le=100, description="Business impact score")
    data_sources: List[str] = Field(default_factory=list, description="Data sources used")
    tags: List[str] = Field(default_factory=list, description="Insight tags")


class AIInsightCreate(AIInsightBase):
    """Create AI insight schema"""
    project_id: Optional[UUID] = Field(None, description="Associated project ID")
    analysis_type: str = Field(..., description="Type of analysis performed")
    ai_model_version: str = Field(..., description="AI model version used")


class AIInsightResponse(AIInsightBase):
    """AI insight response schema"""
    id: UUID
    user_id: UUID
    project_id: Optional[UUID]
    analysis_type: str
    ai_model_version: str
    is_actionable: bool = Field(default=False, description="Whether insight is actionable")
    is_implemented: bool = Field(default=False, description="Whether insight was implemented")
    implementation_notes: Optional[str] = Field(None, description="Implementation notes")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIRecommendationBase(BaseModel):
    """Base AI recommendation schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Recommendation title")
    description: str = Field(..., min_length=1, max_length=2000, description="Recommendation description")
    category: str = Field(..., description="Recommendation category")
    priority: str = Field(..., description="Priority level (low, medium, high, critical)")
    estimated_impact: str = Field(..., description="Estimated business impact")
    implementation_effort: str = Field(..., description="Implementation effort (low, medium, high)")
    confidence_score: float = Field(..., ge=0, le=100, description="AI confidence score")
    reasoning: str = Field(..., description="AI reasoning for recommendation")


class AIRecommendationResponse(AIRecommendationBase):
    """AI recommendation response schema"""
    id: UUID
    user_id: UUID
    project_id: Optional[UUID]
    is_implemented: bool = Field(default=False, description="Whether recommendation was implemented")
    implementation_date: Optional[datetime] = Field(None, description="When recommendation was implemented")
    implementation_notes: Optional[str] = Field(None, description="Implementation notes")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AIAnalysisRequest(BaseModel):
    """AI analysis request schema"""
    project_id: Optional[UUID] = Field(None, description="Project to analyze")
    analysis_type: str = Field(..., description="Type of analysis to perform")
    data_sources: List[str] = Field(default_factory=list, description="Data sources to include")
    analysis_period: str = Field(default="30d", description="Analysis period")
    include_recommendations: bool = Field(default=True, description="Include recommendations")
    include_predictions: bool = Field(default=False, description="Include predictions")
    custom_parameters: Dict[str, Any] = Field(default_factory=dict, description="Custom analysis parameters")


class AIAnalysisResponse(BaseModel):
    """AI analysis response schema"""
    id: UUID
    user_id: UUID
    project_id: Optional[UUID]
    analysis_type: str
    status: str = Field(..., description="Analysis status")
    insights: List[AIInsightResponse] = Field(default_factory=list, description="Generated insights")
    recommendations: List[AIRecommendationResponse] = Field(default_factory=list, description="Generated recommendations")
    predictions: Dict[str, Any] = Field(default_factory=dict, description="AI predictions")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Analysis summary")
    ai_model_metadata: Dict[str, Any] = Field(default_factory=dict, description="Model metadata")
    created_at: datetime
    completed_at: Optional[datetime] = Field(None, description="When analysis completed")

    class Config:
        from_attributes = True


class AIInsightSummary(BaseModel):
    """AI insight summary schema"""
    total_insights: int = Field(..., description="Total number of insights")
    actionable_insights: int = Field(..., description="Number of actionable insights")
    implemented_insights: int = Field(..., description="Number of implemented insights")
    average_confidence: float = Field(..., description="Average confidence score")
    average_impact: float = Field(..., description="Average impact score")
    top_categories: List[Dict[str, Any]] = Field(default_factory=list, description="Top insight categories")
    insights_by_priority: Dict[str, int] = Field(default_factory=dict, description="Insights by priority")
    period: str = Field(..., description="Analysis period")


class AIOptimizationRequest(BaseModel):
    """AI optimization request schema"""
    project_id: UUID = Field(..., description="Project to optimize")
    optimization_type: str = Field(..., description="Type of optimization")
    target_metrics: List[str] = Field(default_factory=list, description="Target metrics to optimize")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Optimization constraints")
    budget_limit: Optional[float] = Field(None, description="Budget limit for optimization")


class AIOptimizationResponse(BaseModel):
    """AI optimization response schema"""
    optimization_id: UUID
    project_id: UUID
    optimization_type: str
    status: str = Field(..., description="Optimization status")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Optimization recommendations")
    estimated_savings: float = Field(..., description="Estimated savings")
    implementation_plan: Dict[str, Any] = Field(default_factory=dict, description="Implementation plan")
    risk_assessment: Dict[str, Any] = Field(default_factory=dict, description="Risk assessment")
    created_at: datetime


class AIPredictionRequest(BaseModel):
    """AI prediction request schema"""
    project_id: UUID = Field(..., description="Project to analyze")
    prediction_type: str = Field(..., description="Type of prediction")
    prediction_period: str = Field(..., description="Prediction period")
    include_confidence_intervals: bool = Field(default=True, description="Include confidence intervals")
    custom_parameters: Dict[str, Any] = Field(default_factory=dict, description="Custom prediction parameters")


class AIPredictionResponse(BaseModel):
    """AI prediction response schema"""
    prediction_id: UUID
    project_id: UUID
    prediction_type: str
    prediction_period: str
    predictions: Dict[str, Any] = Field(default_factory=dict, description="Prediction results")
    confidence_intervals: Dict[str, Any] = Field(default_factory=dict, description="Confidence intervals")
    ai_model_accuracy: float = Field(..., description="Model accuracy score")
    factors: List[str] = Field(default_factory=list, description="Key factors influencing predictions")
    created_at: datetime


class AIAnomalyDetectionRequest(BaseModel):
    """AI anomaly detection request schema"""
    project_id: UUID = Field(..., description="Project to analyze")
    detection_period: str = Field(default="30d", description="Detection period")
    sensitivity_level: str = Field(default="medium", description="Detection sensitivity level")
    include_recommendations: bool = Field(default=True, description="Include recommendations")


class AIAnomalyDetectionResponse(BaseModel):
    """AI anomaly detection response schema"""
    detection_id: UUID
    project_id: UUID
    anomalies_detected: int = Field(..., description="Number of anomalies detected")
    anomalies: List[Dict[str, Any]] = Field(default_factory=list, description="Detected anomalies")
    severity_distribution: Dict[str, int] = Field(default_factory=dict, description="Anomaly severity distribution")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Anomaly response recommendations")
    ai_model_performance: Dict[str, Any] = Field(default_factory=dict, description="Model performance metrics")
    created_at: datetime 