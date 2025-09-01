"""
Cost Analysis Models
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from app.core.database import Base



class CostAnalysis(Base):
    """Advanced cost analysis model with FinOps features"""
    __tablename__ = "cost_analyses"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    analysis_type = Column(String(50), nullable=False, default="comprehensive")  # comprehensive, quick, detailed
    status = Column(String(20), nullable=False, default="pending")  # pending, running, completed, failed
    
    # Cloud Provider Details
    cloud_provider = Column(String(50), nullable=False)  # AWS, Azure, GCP, multi-cloud
    regions = Column(JSON, nullable=False, default=list)
    services = Column(JSON, nullable=False, default=list)
    accounts = Column(JSON, nullable=True)  # Multiple account support
    
    # Time Period
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime, nullable=False)
    analysis_period = Column(String(20), nullable=False, default="30d")  # 7d, 30d, 90d, 1y, custom
    
    # Cost Data
    total_cost = Column(Float, nullable=False, default=0.0)  # In cents
    total_cost_formatted = Column(String(50), nullable=True)
    cost_breakdown = Column(JSON, nullable=True)  # Detailed cost breakdown
    cost_by_service = Column(JSON, nullable=True)
    cost_by_region = Column(JSON, nullable=True)
    cost_by_account = Column(JSON, nullable=True)
    cost_by_tag = Column(JSON, nullable=True)
    
    # FinOps Metrics
    unit_economics = Column(JSON, nullable=True)  # Cost per user, transaction, etc.
    cost_efficiency_score = Column(Float, nullable=True)
    cost_optimization_potential = Column(Float, nullable=True)
    budget_variance = Column(Float, nullable=True)
    forecast_accuracy = Column(Float, nullable=True)
    
    # Advanced Analytics
    cost_trends = Column(JSON, nullable=True)
    anomaly_detection = Column(JSON, nullable=True)
    seasonal_patterns = Column(JSON, nullable=True)
    growth_projections = Column(JSON, nullable=True)
    
    # Recommendations
    recommendations_count = Column(Integer, nullable=False, default=0)
    savings_potential = Column(Float, nullable=False, default=0.0)
    implemented_savings = Column(Float, nullable=False, default=0.0)
    
    # Quality & Validation
    data_quality_score = Column(Float, nullable=True)
    data_completeness = Column(Float, nullable=True)
    last_data_refresh = Column(DateTime, nullable=True)
    data_sources = Column(JSON, nullable=True)
    
    # Audit Trail
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="cost_analyses")
    project = relationship("Project", back_populates="cost_analyses")
    recommendations = relationship("CostRecommendation", back_populates="cost_analysis", cascade="all, delete-orphan")
    alerts = relationship("CostAlert", back_populates="cost_analysis", cascade="all, delete-orphan")


class CostRecommendation(Base):
    """Advanced cost optimization recommendations"""
    __tablename__ = "cost_recommendations"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cost_analysis_id = Column(PGUUID(as_uuid=True), ForeignKey("cost_analyses.id"), nullable=False)
    
    # Basic Information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # compute, storage, network, database, etc.
    subcategory = Column(String(50), nullable=True)  # rightsizing, reservations, spot_instances, etc.
    
    # Priority & Impact
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    impact_score = Column(Float, nullable=False, default=0.0)  # 0-100
    urgency_score = Column(Float, nullable=False, default=0.0)  # 0-100
    
    # Financial Impact
    estimated_savings = Column(Float, nullable=False, default=0.0)  # In cents
    estimated_savings_percentage = Column(Float, nullable=True)
    payback_period = Column(Integer, nullable=True)  # Days to recover investment
    roi_score = Column(Float, nullable=True)  # Return on investment
    
    # Implementation Details
    implementation_effort = Column(String(20), nullable=False, default="medium")  # low, medium, high
    implementation_time = Column(Integer, nullable=True)  # Estimated hours
    risk_level = Column(String(20), nullable=False, default="low")  # low, medium, high
    technical_complexity = Column(String(20), nullable=False, default="medium")
    
    # Resource Information
    resource_id = Column(String(255), nullable=True)
    resource_type = Column(String(100), nullable=True)
    resource_name = Column(String(255), nullable=True)
    affected_services = Column(JSON, nullable=True)
    affected_regions = Column(JSON, nullable=True)
    
    # Cost Details
    current_cost = Column(Float, nullable=False, default=0.0)
    recommended_cost = Column(Float, nullable=False, default=0.0)
    savings_percentage = Column(Float, nullable=True)
    
    # Implementation Steps
    implementation_steps = Column(JSON, nullable=True)
    prerequisites = Column(JSON, nullable=True)
    rollback_plan = Column(Text, nullable=True)
    
    # Status & Tracking
    status = Column(String(20), nullable=False, default="pending")  # pending, approved, implemented, rejected
    is_applied = Column(Boolean, nullable=False, default=False)
    applied_at = Column(DateTime, nullable=True)
    applied_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    implementation_notes = Column(Text, nullable=True)
    
    # Validation & Monitoring
    validation_status = Column(String(20), nullable=True)  # pending, validated, failed
    actual_savings = Column(Float, nullable=True)
    actual_savings_percentage = Column(Float, nullable=True)
    monitoring_period = Column(Integer, nullable=True)  # Days to monitor after implementation
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cost_analysis = relationship("CostAnalysis", back_populates="recommendations")
    applied_by_user = relationship("User")


class CostAlert(Base):
    """Advanced cost alerts and notifications"""
    __tablename__ = "cost_alerts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cost_analysis_id = Column(PGUUID(as_uuid=True), ForeignKey("cost_analyses.id"), nullable=True)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    # Alert Information
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), nullable=False)  # threshold, anomaly, trend, budget, forecast
    severity = Column(String(20), nullable=False, default="medium")  # info, warning, error, critical
    category = Column(String(50), nullable=False)  # cost_spike, budget_exceeded, unused_resource, etc.
    
    # Threshold & Conditions
    threshold_value = Column(Float, nullable=True)
    threshold_type = Column(String(20), nullable=True)  # percentage, absolute, trend
    condition_operator = Column(String(10), nullable=True)  # >, <, >=, <=, ==
    trigger_value = Column(Float, nullable=True)
    
    # Resource Information
    affected_resource = Column(String(255), nullable=True)
    resource_type = Column(String(100), nullable=True)
    affected_services = Column(JSON, nullable=True)
    affected_regions = Column(JSON, nullable=True)
    
    # Financial Impact
    cost_impact = Column(Float, nullable=True)
    cost_impact_percentage = Column(Float, nullable=True)
    projected_cost = Column(Float, nullable=True)
    
    # Status & Resolution
    status = Column(String(20), nullable=False, default="active")  # active, acknowledged, resolved, dismissed
    is_resolved = Column(Boolean, nullable=False, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Notification
    notification_sent = Column(Boolean, nullable=False, default=False)
    notification_channels = Column(JSON, nullable=True)  # email, slack, webhook, etc.
    escalation_level = Column(Integer, nullable=False, default=1)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cost_analysis = relationship("CostAnalysis", back_populates="alerts")
    project = relationship("Project")
    resolved_by_user = relationship("User")


class CostBudget(Base):
    """Budget management and tracking"""
    __tablename__ = "cost_budgets"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Budget Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    budget_type = Column(String(50), nullable=False)  # monthly, quarterly, yearly, custom
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    
    # Financial Details
    budget_amount = Column(Float, nullable=False)  # In cents
    currency = Column(String(3), nullable=False, default="USD")
    allocated_amount = Column(Float, nullable=False, default=0.0)
    spent_amount = Column(Float, nullable=False, default=0.0)
    remaining_amount = Column(Float, nullable=False, default=0.0)
    
    # Tracking
    spending_rate = Column(Float, nullable=True)  # Daily spending rate
    projected_spend = Column(Float, nullable=True)
    variance_percentage = Column(Float, nullable=True)
    is_over_budget = Column(Boolean, nullable=False, default=False)
    
    # Alerts & Notifications
    alert_thresholds = Column(JSON, nullable=True)  # 50%, 75%, 90%, 100%
    notification_recipients = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(20), nullable=False, default="active")  # active, paused, completed, archived
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    user = relationship("User")


class CostForecast(Base):
    """Cost forecasting and predictions"""
    __tablename__ = "cost_forecasts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Forecast Information
    forecast_type = Column(String(50), nullable=False)  # linear, seasonal, ml_based, custom
    forecast_period = Column(String(20), nullable=False)  # 30d, 90d, 180d, 1y
    confidence_level = Column(Float, nullable=False, default=0.95)
    
    # Predictions
    predicted_costs = Column(JSON, nullable=False)  # Daily/monthly predictions
    confidence_intervals = Column(JSON, nullable=True)
    trend_analysis = Column(JSON, nullable=True)
    seasonal_factors = Column(JSON, nullable=True)
    
    # Model Information
    ai_model_version = Column(String(50), nullable=True)
    ai_model_accuracy = Column(Float, nullable=True)
    training_data_period = Column(String(20), nullable=True)
    last_training_date = Column(DateTime, nullable=True)
    
    # Factors & Variables
    influencing_factors = Column(JSON, nullable=True)
    assumptions = Column(JSON, nullable=True)
    risk_factors = Column(JSON, nullable=True)
    
    # Status
    status = Column(String(20), nullable=False, default="active")  # active, archived, invalidated
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    user = relationship("User") 