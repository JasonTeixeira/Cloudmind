"""
Final System Integration Schemas
Professional system integration with performance, security, and monitoring
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class IntegrationType(str, Enum):
    """Integration types"""
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MONITORING = "monitoring"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


class SystemStatus(str, Enum):
    """System status types"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class PerformanceLevel(str, Enum):
    """Performance levels"""
    OPTIMAL = "optimal"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"


class SecurityLevel(str, Enum):
    """Security levels"""
    ENTERPRISE = "enterprise"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BASIC = "basic"


class DeploymentType(str, Enum):
    """Deployment types"""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    CLOUD = "cloud"
    CONTAINER = "container"


class TestType(str, Enum):
    """Test types"""
    UNIT = "unit"
    INTEGRATION = "integration"
    SYSTEM = "system"
    PERFORMANCE = "performance"
    SECURITY = "security"
    LOAD = "load"
    STRESS = "stress"
    SMOKE = "smoke"
    REGRESSION = "regression"


class TestStatus(str, Enum):
    """Test status types"""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    RUNNING = "running"
    PENDING = "pending"
    ERROR = "error"


class MonitoringType(str, Enum):
    """Monitoring types"""
    SYSTEM = "system"
    APPLICATION = "application"
    DATABASE = "database"
    NETWORK = "network"
    SECURITY = "security"
    PERFORMANCE = "performance"
    USER = "user"
    BUSINESS = "business"


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SystemHealth(BaseModel):
    """System health information"""
    id: str = Field(..., description="Health check identifier")
    status: SystemStatus = Field(..., description="System status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    uptime: float = Field(..., description="System uptime in seconds")
    version: str = Field(..., description="System version")
    environment: str = Field(..., description="Environment name")
    components: Dict[str, SystemStatus] = Field(default_factory=dict, description="Component status")
    performance: Dict[str, float] = Field(default_factory=dict, description="Performance metrics")
    errors: List[str] = Field(default_factory=list, description="Error messages")
    warnings: List[str] = Field(default_factory=list, description="Warning messages")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class PerformanceMetrics(BaseModel):
    """Performance metrics"""
    id: str = Field(..., description="Metrics identifier")
    timestamp: datetime = Field(..., description="Metrics timestamp")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    network_io: Dict[str, float] = Field(default_factory=dict, description="Network I/O metrics")
    response_time: float = Field(..., description="Average response time in ms")
    throughput: float = Field(..., description="Requests per second")
    error_rate: float = Field(..., description="Error rate percentage")
    active_connections: int = Field(..., description="Active connections")
    queue_depth: int = Field(..., description="Queue depth")
    cache_hit_rate: float = Field(..., description="Cache hit rate percentage")
    database_connections: int = Field(..., description="Database connections")
    level: PerformanceLevel = Field(..., description="Performance level")
    recommendations: List[str] = Field(default_factory=list, description="Performance recommendations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SecurityAudit(BaseModel):
    """Security audit information"""
    id: str = Field(..., description="Audit identifier")
    timestamp: datetime = Field(..., description="Audit timestamp")
    level: SecurityLevel = Field(..., description="Security level")
    vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list, description="Security vulnerabilities")
    threats: List[Dict[str, Any]] = Field(default_factory=list, description="Security threats")
    compliance: Dict[str, bool] = Field(default_factory=dict, description="Compliance status")
    encryption_status: Dict[str, bool] = Field(default_factory=dict, description="Encryption status")
    authentication_status: Dict[str, bool] = Field(default_factory=dict, description="Authentication status")
    authorization_status: Dict[str, bool] = Field(default_factory=dict, description="Authorization status")
    audit_logs: List[Dict[str, Any]] = Field(default_factory=list, description="Audit logs")
    recommendations: List[str] = Field(default_factory=list, description="Security recommendations")
    risk_score: float = Field(..., description="Overall risk score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SystemIntegration(BaseModel):
    """System integration configuration"""
    id: str = Field(..., description="Integration identifier")
    name: str = Field(..., description="Integration name")
    type: IntegrationType = Field(..., description="Integration type")
    description: str = Field(..., description="Integration description")
    status: SystemStatus = Field(..., description="Integration status")
    enabled: bool = Field(default=True, description="Whether integration is enabled")
    priority: int = Field(default=0, description="Integration priority")
    dependencies: List[str] = Field(default_factory=list, description="Integration dependencies")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Integration configuration")
    health_check: Optional[str] = Field(None, description="Health check endpoint")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Integration metrics")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TestSuite(BaseModel):
    """Test suite configuration"""
    id: str = Field(..., description="Test suite identifier")
    name: str = Field(..., description="Test suite name")
    description: str = Field(..., description="Test suite description")
    type: TestType = Field(..., description="Test type")
    status: TestStatus = Field(..., description="Test status")
    enabled: bool = Field(default=True, description="Whether test suite is enabled")
    priority: int = Field(default=0, description="Test priority")
    timeout: int = Field(default=300, description="Test timeout in seconds")
    retries: int = Field(default=3, description="Number of retries")
    dependencies: List[str] = Field(default_factory=list, description="Test dependencies")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Test configuration")
    test_cases: List[Dict[str, Any]] = Field(default_factory=list, description="Test cases")
    results: Dict[str, Any] = Field(default_factory=dict, description="Test results")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TestResult(BaseModel):
    """Test result information"""
    id: str = Field(..., description="Test result identifier")
    test_suite_id: str = Field(..., description="Test suite identifier")
    test_case_id: str = Field(..., description="Test case identifier")
    status: TestStatus = Field(..., description="Test status")
    start_time: datetime = Field(..., description="Test start time")
    end_time: Optional[datetime] = Field(None, description="Test end time")
    duration: Optional[float] = Field(None, description="Test duration in seconds")
    error_message: Optional[str] = Field(None, description="Error message")
    stack_trace: Optional[str] = Field(None, description="Stack trace")
    logs: List[str] = Field(default_factory=list, description="Test logs")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Test metrics")
    artifacts: List[str] = Field(default_factory=list, description="Test artifacts")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MonitoringAlert(BaseModel):
    """Monitoring alert"""
    id: str = Field(..., description="Alert identifier")
    name: str = Field(..., description="Alert name")
    description: str = Field(..., description="Alert description")
    type: MonitoringType = Field(..., description="Monitoring type")
    severity: AlertSeverity = Field(..., description="Alert severity")
    status: str = Field(..., description="Alert status")
    timestamp: datetime = Field(..., description="Alert timestamp")
    source: str = Field(..., description="Alert source")
    metric: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    threshold: float = Field(..., description="Threshold value")
    condition: str = Field(..., description="Alert condition")
    message: str = Field(..., description="Alert message")
    actions: List[str] = Field(default_factory=list, description="Alert actions")
    acknowledged: bool = Field(default=False, description="Whether alert is acknowledged")
    acknowledged_by: Optional[str] = Field(None, description="Acknowledged by")
    acknowledged_at: Optional[datetime] = Field(None, description="Acknowledged at")
    resolved: bool = Field(default=False, description="Whether alert is resolved")
    resolved_at: Optional[datetime] = Field(None, description="Resolved at")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DeploymentConfig(BaseModel):
    """Deployment configuration"""
    id: str = Field(..., description="Deployment identifier")
    name: str = Field(..., description="Deployment name")
    type: DeploymentType = Field(..., description="Deployment type")
    environment: str = Field(..., description="Environment name")
    version: str = Field(..., description="Deployment version")
    status: str = Field(..., description="Deployment status")
    start_time: datetime = Field(..., description="Deployment start time")
    end_time: Optional[datetime] = Field(None, description="Deployment end time")
    duration: Optional[float] = Field(None, description="Deployment duration")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Deployment configuration")
    services: List[str] = Field(default_factory=list, description="Deployed services")
    health_checks: List[str] = Field(default_factory=list, description="Health check endpoints")
    rollback_plan: Optional[str] = Field(None, description="Rollback plan")
    logs: List[str] = Field(default_factory=list, description="Deployment logs")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Deployment metrics")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SystemMetrics(BaseModel):
    """System metrics summary"""
    id: str = Field(..., description="Metrics identifier")
    timestamp: datetime = Field(..., description="Metrics timestamp")
    system_health: SystemHealth = Field(..., description="System health")
    performance: PerformanceMetrics = Field(..., description="Performance metrics")
    security: SecurityAudit = Field(..., description="Security audit")
    integrations: List[SystemIntegration] = Field(default_factory=list, description="System integrations")
    test_results: List[TestResult] = Field(default_factory=list, description="Test results")
    alerts: List[MonitoringAlert] = Field(default_factory=list, description="Monitoring alerts")
    deployments: List[DeploymentConfig] = Field(default_factory=list, description="Deployments")
    overall_score: float = Field(..., description="Overall system score")
    recommendations: List[str] = Field(default_factory=list, description="System recommendations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class OptimizationConfig(BaseModel):
    """Optimization configuration"""
    id: str = Field(..., description="Optimization identifier")
    name: str = Field(..., description="Optimization name")
    description: str = Field(..., description="Optimization description")
    type: str = Field(..., description="Optimization type")
    enabled: bool = Field(default=True, description="Whether optimization is enabled")
    priority: int = Field(default=0, description="Optimization priority")
    target_metrics: List[str] = Field(default_factory=list, description="Target metrics")
    thresholds: Dict[str, float] = Field(default_factory=dict, description="Optimization thresholds")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Optimization configuration")
    schedule: Optional[str] = Field(None, description="Optimization schedule")
    last_run: Optional[datetime] = Field(None, description="Last run time")
    next_run: Optional[datetime] = Field(None, description="Next run time")
    results: Dict[str, Any] = Field(default_factory=dict, description="Optimization results")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DocumentationConfig(BaseModel):
    """Documentation configuration"""
    id: str = Field(..., description="Documentation identifier")
    name: str = Field(..., description="Documentation name")
    type: str = Field(..., description="Documentation type")
    description: str = Field(..., description="Documentation description")
    version: str = Field(..., description="Documentation version")
    status: str = Field(..., description="Documentation status")
    content: str = Field(..., description="Documentation content")
    format: str = Field(..., description="Documentation format")
    language: str = Field(..., description="Documentation language")
    tags: List[str] = Field(default_factory=list, description="Documentation tags")
    author: str = Field(..., description="Documentation author")
    reviewers: List[str] = Field(default_factory=list, description="Documentation reviewers")
    last_review: Optional[datetime] = Field(None, description="Last review time")
    next_review: Optional[datetime] = Field(None, description="Next review time")
    url: Optional[str] = Field(None, description="Documentation URL")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class SystemHealthRequest(BaseModel):
    """System health check request"""
    components: Optional[List[str]] = Field(None, description="Components to check")
    detailed: bool = Field(default=False, description="Whether to return detailed information")


class SystemHealthResponse(BaseModel):
    """System health check response"""
    health: SystemHealth = Field(..., description="System health information")
    success: bool = Field(..., description="Whether health check was successful")
    message: str = Field(..., description="Health check message")


class PerformanceOptimizationRequest(BaseModel):
    """Performance optimization request"""
    target_metrics: List[str] = Field(..., description="Target metrics to optimize")
    optimization_level: str = Field(default="balanced", description="Optimization level")
    dry_run: bool = Field(default=False, description="Whether to perform dry run")


class PerformanceOptimizationResponse(BaseModel):
    """Performance optimization response"""
    optimizations: List[OptimizationConfig] = Field(..., description="Applied optimizations")
    improvements: Dict[str, float] = Field(..., description="Performance improvements")
    success: bool = Field(..., description="Whether optimization was successful")
    message: str = Field(..., description="Optimization message")


class SecurityHardeningRequest(BaseModel):
    """Security hardening request"""
    security_level: SecurityLevel = Field(..., description="Target security level")
    components: Optional[List[str]] = Field(None, description="Components to harden")
    dry_run: bool = Field(default=False, description="Whether to perform dry run")


class SecurityHardeningResponse(BaseModel):
    """Security hardening response"""
    hardening_configs: List[Dict[str, Any]] = Field(..., description="Applied hardening configurations")
    security_improvements: Dict[str, Any] = Field(..., description="Security improvements")
    risk_reduction: float = Field(..., description="Risk reduction percentage")
    success: bool = Field(..., description="Whether hardening was successful")
    message: str = Field(..., description="Hardening message")


class TestExecutionRequest(BaseModel):
    """Test execution request"""
    test_suites: List[str] = Field(..., description="Test suites to execute")
    parallel: bool = Field(default=True, description="Whether to run tests in parallel")
    timeout: Optional[int] = Field(None, description="Test timeout in seconds")


class TestExecutionResponse(BaseModel):
    """Test execution response"""
    test_results: List[TestResult] = Field(..., description="Test results")
    summary: Dict[str, Any] = Field(..., description="Test summary")
    success: bool = Field(..., description="Whether tests were successful")
    message: str = Field(..., description="Test execution message")


class MonitoringConfigRequest(BaseModel):
    """Monitoring configuration request"""
    monitoring_types: List[MonitoringType] = Field(..., description="Monitoring types to configure")
    alert_thresholds: Dict[str, float] = Field(default_factory=dict, description="Alert thresholds")
    notification_channels: List[str] = Field(default_factory=list, description="Notification channels")


class MonitoringConfigResponse(BaseModel):
    """Monitoring configuration response"""
    monitoring_config: Dict[str, Any] = Field(..., description="Monitoring configuration")
    alerts: List[MonitoringAlert] = Field(..., description="Configured alerts")
    success: bool = Field(..., description="Whether configuration was successful")
    message: str = Field(..., description="Configuration message")


class DeploymentRequest(BaseModel):
    """Deployment request"""
    deployment_type: DeploymentType = Field(..., description="Deployment type")
    environment: str = Field(..., description="Target environment")
    version: str = Field(..., description="Deployment version")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Deployment configuration")
    rollback_on_failure: bool = Field(default=True, description="Whether to rollback on failure")


class DeploymentResponse(BaseModel):
    """Deployment response"""
    deployment: DeploymentConfig = Field(..., description="Deployment configuration")
    status: str = Field(..., description="Deployment status")
    success: bool = Field(..., description="Whether deployment was successful")
    message: str = Field(..., description="Deployment message")


class SystemIntegrationRequest(BaseModel):
    """System integration request"""
    integration_type: IntegrationType = Field(..., description="Integration type")
    configuration: Dict[str, Any] = Field(..., description="Integration configuration")
    enabled: bool = Field(default=True, description="Whether to enable integration")


class SystemIntegrationResponse(BaseModel):
    """System integration response"""
    integration: SystemIntegration = Field(..., description="System integration")
    status: str = Field(..., description="Integration status")
    success: bool = Field(..., description="Whether integration was successful")
    message: str = Field(..., description="Integration message")


class DocumentationRequest(BaseModel):
    """Documentation request"""
    documentation_type: str = Field(..., description="Documentation type")
    content: str = Field(..., description="Documentation content")
    format: str = Field(default="markdown", description="Documentation format")
    language: str = Field(default="en", description="Documentation language")


class DocumentationResponse(BaseModel):
    """Documentation response"""
    documentation: DocumentationConfig = Field(..., description="Documentation configuration")
    url: Optional[str] = Field(None, description="Documentation URL")
    success: bool = Field(..., description="Whether documentation was created successfully")
    message: str = Field(..., description="Documentation message")


class SystemMetricsRequest(BaseModel):
    """System metrics request"""
    include_details: bool = Field(default=False, description="Whether to include detailed metrics")
    time_range: Optional[str] = Field(None, description="Time range for metrics")


class SystemMetricsResponse(BaseModel):
    """System metrics response"""
    metrics: SystemMetrics = Field(..., description="System metrics")
    success: bool = Field(..., description="Whether metrics retrieval was successful")
    message: str = Field(..., description="Metrics message")


class SystemOptimizationRequest(BaseModel):
    """System optimization request"""
    optimization_types: List[str] = Field(..., description="Types of optimization to perform")
    target_score: float = Field(..., description="Target system score")
    dry_run: bool = Field(default=False, description="Whether to perform dry run")


class SystemOptimizationResponse(BaseModel):
    """System optimization response"""
    optimizations: List[OptimizationConfig] = Field(..., description="Applied optimizations")
    improvements: Dict[str, Any] = Field(..., description="System improvements")
    new_score: float = Field(..., description="New system score")
    success: bool = Field(..., description="Whether optimization was successful")
    message: str = Field(..., description="Optimization message")
