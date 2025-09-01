"""
Monitoring Schemas
Comprehensive Pydantic schemas for monitoring endpoints and responses.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AlertType(str, Enum):
    """Alert types"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    COST = "cost"
    AI = "ai"
    SYSTEM = "system"


class MetricStatus(str, Enum):
    """Metric status levels"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class TrendDirection(str, Enum):
    """Trend direction"""
    UP = "up"
    DOWN = "down"
    STABLE = "stable"


# Base Response Models
class BaseResponse(BaseModel):
    """Base response model"""
    status: str = Field(..., description="Response status")
    timestamp: str = Field(..., description="Response timestamp")


# System Health Models
class SystemHealthData(BaseModel):
    """System health data"""
    overall_status: str = Field(..., description="Overall system status")
    overall_health_score: float = Field(..., description="Overall health score (0-100)")
    uptime: float = Field(..., description="System uptime percentage")
    response_time: float = Field(..., description="Average response time in ms")
    error_rate: float = Field(..., description="Error rate percentage")
    active_connections: int = Field(..., description="Active database connections")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    network_throughput: float = Field(..., description="Network throughput in Mbps")
    last_check: str = Field(..., description="Last health check timestamp")


class SystemHealthResponse(BaseResponse):
    """System health response"""
    data: SystemHealthData = Field(..., description="System health data")


# Performance Metrics Models
class PerformanceMetricsData(BaseModel):
    """Performance metrics data"""
    current_metrics: Dict[str, Any] = Field(..., description="Current performance metrics")
    trends: Dict[str, Any] = Field(..., description="Performance trends")
    cache_stats: Dict[str, Any] = Field(..., description="Cache statistics")
    scaling_decision: Dict[str, Any] = Field(..., description="Auto-scaling decisions")
    recommendations: List[str] = Field(..., description="Performance recommendations")


class PerformanceMetricsResponse(BaseResponse):
    """Performance metrics response"""
    data: PerformanceMetricsData = Field(..., description="Performance metrics data")


# Security Metrics Models
class SecurityMetricsData(BaseModel):
    """Security metrics data"""
    security_score: float = Field(..., description="Overall security score (0-100)")
    vulnerabilities: Dict[str, Any] = Field(..., description="Vulnerability information")
    security_incidents: Dict[str, Any] = Field(..., description="Security incidents")
    compliance: Dict[str, Any] = Field(..., description="Compliance status")
    threat_intelligence: Dict[str, Any] = Field(..., description="Threat intelligence data")
    last_scan: str = Field(..., description="Last security scan timestamp")


class SecurityMetricsResponse(BaseResponse):
    """Security metrics response"""
    data: SecurityMetricsData = Field(..., description="Security metrics data")


# Business Metrics Models
class BusinessMetricsData(BaseModel):
    """Business metrics data"""
    revenue: Dict[str, Any] = Field(..., description="Revenue metrics")
    users: Dict[str, Any] = Field(..., description="User metrics")
    costs: Dict[str, Any] = Field(..., description="Cost metrics")
    ai_insights: Dict[str, Any] = Field(..., description="AI insights metrics")
    business_health_score: float = Field(..., description="Business health score")


class BusinessMetricsResponse(BaseResponse):
    """Business metrics response"""
    data: BusinessMetricsData = Field(..., description="Business metrics data")


# Alert Models
class AlertResponse(BaseModel):
    """Alert response model"""
    id: str = Field(..., description="Alert ID")
    type: AlertType = Field(..., description="Alert type")
    severity: AlertSeverity = Field(..., description="Alert severity")
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    timestamp: str = Field(..., description="Alert timestamp")
    resolved: bool = Field(..., description="Whether alert is resolved")


# Real-time Metrics Models
class RealTimeMetric(BaseModel):
    """Real-time metric model"""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    unit: str = Field(..., description="Metric unit")
    trend: TrendDirection = Field(..., description="Metric trend")
    change: float = Field(..., description="Percentage change")
    status: MetricStatus = Field(..., description="Metric status")


# Executive Dashboard Models
class ExecutiveMetrics(BaseModel):
    """Executive metrics model"""
    revenue: Dict[str, Any] = Field(..., description="Revenue metrics")
    users: Dict[str, Any] = Field(..., description="User metrics")
    performance: Dict[str, Any] = Field(..., description="Performance metrics")
    security: Dict[str, Any] = Field(..., description="Security metrics")
    costs: Dict[str, Any] = Field(..., description="Cost metrics")
    ai_insights: Dict[str, Any] = Field(..., description="AI insights metrics")


class ExecutiveDashboardData(BaseModel):
    """Executive dashboard data"""
    executive_metrics: ExecutiveMetrics = Field(..., description="Executive metrics")
    real_time_metrics: List[RealTimeMetric] = Field(..., description="Real-time metrics")
    alerts: List[Dict[str, Any]] = Field(..., description="Active alerts")
    auto_healing: Dict[str, Any] = Field(..., description="Auto-healing status")
    performance_optimization: Dict[str, Any] = Field(..., description="Performance optimization data")


class ExecutiveDashboardResponse(BaseResponse):
    """Executive dashboard response"""
    data: ExecutiveDashboardData = Field(..., description="Executive dashboard data")


# Auto-healing Models
class AutoHealingData(BaseModel):
    """Auto-healing data"""
    active_issues: int = Field(..., description="Number of active issues")
    resolved_issues: int = Field(..., description="Number of resolved issues")
    health_checks: Dict[str, Any] = Field(..., description="Health check status")
    healing_stats: Dict[str, Any] = Field(..., description="Healing statistics")
    recent_issues: List[Dict[str, Any]] = Field(..., description="Recent issues")
    predictive_thresholds: Dict[str, Any] = Field(..., description="Predictive thresholds")


class AutoHealingReportResponse(BaseResponse):
    """Auto-healing report response"""
    data: AutoHealingData = Field(..., description="Auto-healing data")


# Performance Optimization Models
class PerformanceOptimizationData(BaseModel):
    """Performance optimization data"""
    current_metrics: Dict[str, Any] = Field(..., description="Current performance metrics")
    trends: Dict[str, Any] = Field(..., description="Performance trends")
    cache_stats: Dict[str, Any] = Field(..., description="Cache statistics")
    scaling_decision: Dict[str, Any] = Field(..., description="Scaling decisions")
    recommendations: List[str] = Field(..., description="Optimization recommendations")


class PerformanceOptimizationReportResponse(BaseResponse):
    """Performance optimization report response"""
    data: PerformanceOptimizationData = Field(..., description="Performance optimization data")


# Comprehensive Health Models
class HealthRecommendation(BaseModel):
    """Health recommendation model"""
    component: str = Field(..., description="Component name")
    priority: str = Field(..., description="Recommendation priority")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Recommendation description")
    action: str = Field(..., description="Recommended action")


class ComprehensiveHealthData(BaseModel):
    """Comprehensive health data"""
    overall_health_score: float = Field(..., description="Overall health score")
    health_breakdown: Dict[str, float] = Field(..., description="Health breakdown by component")
    system_health: Dict[str, Any] = Field(..., description="System health data")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    security_metrics: Dict[str, Any] = Field(..., description="Security metrics")
    business_metrics: Dict[str, Any] = Field(..., description="Business metrics")
    auto_healing_status: Dict[str, Any] = Field(..., description="Auto-healing status")
    recommendations: List[HealthRecommendation] = Field(..., description="Health recommendations")
    critical_alerts: List[Dict[str, Any]] = Field(..., description="Critical alerts")
    system_status: str = Field(..., description="Overall system status")


class ComprehensiveHealthResponse(BaseResponse):
    """Comprehensive health response"""
    data: ComprehensiveHealthData = Field(..., description="Comprehensive health data")


# Real-time Metrics Response
class RealTimeMetricsData(BaseModel):
    """Real-time metrics data"""
    performance: Dict[str, Any] = Field(..., description="Performance metrics")
    system: Dict[str, Any] = Field(..., description="System metrics")
    health: Dict[str, Any] = Field(..., description="Health metrics")


class RealTimeMetricsResponse(BaseResponse):
    """Real-time metrics response"""
    data: RealTimeMetricsData = Field(..., description="Real-time metrics data")


# Action Response Models
class ActionResponse(BaseResponse):
    """Action response model"""
    message: str = Field(..., description="Action result message")
    data: Optional[Dict[str, Any]] = Field(None, description="Action result data")


# Utility Models
class MetricThreshold(BaseModel):
    """Metric threshold model"""
    metric_name: str = Field(..., description="Metric name")
    warning_threshold: float = Field(..., description="Warning threshold")
    critical_threshold: float = Field(..., description="Critical threshold")
    unit: str = Field(..., description="Metric unit")


class HealthCheck(BaseModel):
    """Health check model"""
    component: str = Field(..., description="Component name")
    status: str = Field(..., description="Health status")
    response_time: float = Field(..., description="Response time")
    last_check: str = Field(..., description="Last check timestamp")
    metadata: Dict[str, Any] = Field(..., description="Additional metadata")


class PerformanceOptimizationAction(BaseModel):
    """Performance optimization action"""
    action_type: str = Field(..., description="Type of optimization action")
    target_component: str = Field(..., description="Target component")
    parameters: Dict[str, Any] = Field(..., description="Action parameters")
    expected_impact: str = Field(..., description="Expected impact description")
    priority: str = Field(..., description="Action priority")


class AutoHealingAction(BaseModel):
    """Auto-healing action"""
    action_type: str = Field(..., description="Type of healing action")
    target_service: str = Field(..., description="Target service")
    trigger_condition: str = Field(..., description="Trigger condition")
    recovery_strategy: str = Field(..., description="Recovery strategy")
    success_rate: float = Field(..., description="Success rate percentage") 