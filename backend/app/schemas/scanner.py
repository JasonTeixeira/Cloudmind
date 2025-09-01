"""
Enterprise Scanner Schemas
Professional multi-cloud cost optimization scanner schemas
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class ScanType(str, Enum):
    """Scan types"""
    QUICK = "quick"
    COMPREHENSIVE = "comprehensive"
    DEEP = "deep"
    CONTINUOUS = "continuous"


class ProviderType(str, Enum):
    """Cloud provider types"""
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    ALIBABA = "alibaba"
    ORACLE = "oracle"
    IBM = "ibm"
    DIGITALOCEAN = "digitalocean"
    KUBERNETES = "kubernetes"


class ResourceType(str, Enum):
    """Resource types"""
    EC2_INSTANCE = "ec2_instance"
    RDS_INSTANCE = "rds_instance"
    S3_BUCKET = "s3_bucket"
    EBS_VOLUME = "ebs_volume"
    LAMBDA_FUNCTION = "lambda_function"
    ELASTICACHE = "elasticache"
    LOAD_BALANCER = "load_balancer"
    VIRTUAL_MACHINE = "virtual_machine"
    SQL_DATABASE = "sql_database"
    BLOB_STORAGE = "blob_storage"
    COMPUTE_INSTANCE = "compute_instance"
    CLOUD_SQL = "cloud_sql"
    CLOUD_STORAGE = "cloud_storage"
    KUBERNETES_POD = "kubernetes_pod"
    KUBERNETES_SERVICE = "kubernetes_service"


class OptimizationType(str, Enum):
    """Optimization types"""
    IMMEDIATE_WIN = "immediate_win"
    RIGHTSIZING = "rightsizing"
    RESERVED_INSTANCE = "reserved_instance"
    ARCHITECTURE = "architecture"
    STORAGE_OPTIMIZATION = "storage_optimization"
    NETWORK_OPTIMIZATION = "network_optimization"
    DATABASE_OPTIMIZATION = "database_optimization"
    CONTAINER_OPTIMIZATION = "container_optimization"


class PriorityLevel(str, Enum):
    """Priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskLevel(str, Enum):
    """Risk levels"""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ImplementationEffort(str, Enum):
    """Implementation effort levels"""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ScannerConfig(BaseModel):
    """Scanner configuration"""
    scan_type: ScanType = Field(..., description="Type of scan to perform")
    providers: List[ProviderType] = Field(..., description="Cloud providers to scan")
    regions: Optional[List[str]] = Field(None, description="Specific regions to scan")
    services: Optional[List[str]] = Field(None, description="Specific services to scan")
    deep_scan: bool = Field(default=False, description="Perform deep analysis")
    include_metrics: bool = Field(default=True, description="Include utilization metrics")
    include_costs: bool = Field(default=True, description="Include cost analysis")
    include_optimizations: bool = Field(default=True, description="Include optimization recommendations")
    safety_audit: bool = Field(default=True, description="Perform safety audit")
    parallel_scanning: bool = Field(default=True, description="Enable parallel scanning")
    rate_limiting: bool = Field(default=True, description="Enable rate limiting")
    dry_run: bool = Field(default=True, description="Perform dry run only")
    timeout_minutes: int = Field(default=30, description="Scan timeout in minutes")
    max_resources: Optional[int] = Field(None, description="Maximum resources to scan")
    filters: Optional[Dict[str, Any]] = Field(None, description="Resource filters")
    credentials: Optional[Dict[str, Any]] = Field(None, description="Cloud credentials")


class ResourceDiscovery(BaseModel):
    """Resource discovery results"""
    total_resources: int = Field(..., description="Total number of resources discovered")
    resources_by_provider: Dict[str, List[Dict[str, Any]]] = Field(..., description="Resources by provider")
    discovery_time: datetime = Field(..., description="Discovery completion time")
    coverage_percentage: float = Field(..., description="Coverage percentage")
    regions_scanned: List[str] = Field(default_factory=list, description="Regions scanned")
    services_discovered: List[str] = Field(default_factory=list, description="Services discovered")
    errors: List[str] = Field(default_factory=list, description="Discovery errors")
    warnings: List[str] = Field(default_factory=list, description="Discovery warnings")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CostAnalysis(BaseModel):
    """Cost analysis results"""
    total_cost: float = Field(..., description="Total monthly cost")
    cost_breakdown: Dict[str, Any] = Field(..., description="Cost breakdown by provider")
    calculation_method: str = Field(..., description="Cost calculation method")
    accuracy_score: float = Field(..., description="Cost calculation accuracy")
    validation_status: str = Field(..., description="Validation status")
    currency: str = Field(default="USD", description="Cost currency")
    period: str = Field(default="monthly", description="Cost period")
    cost_by_service: Dict[str, float] = Field(default_factory=dict, description="Cost by service")
    cost_by_region: Dict[str, float] = Field(default_factory=dict, description="Cost by region")
    cost_trends: Dict[str, Any] = Field(default_factory=dict, description="Cost trends")
    anomalies: List[Dict[str, Any]] = Field(default_factory=list, description="Cost anomalies")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class OptimizationRecommendation(BaseModel):
    """Optimization recommendation"""
    id: str = Field(..., description="Recommendation ID")
    type: OptimizationType = Field(..., description="Optimization type")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Recommendation description")
    category: str = Field(..., description="Optimization category")
    priority: PriorityLevel = Field(..., description="Priority level")
    confidence_score: float = Field(..., description="Confidence score (0-100)")
    potential_savings: float = Field(..., description="Potential monthly savings")
    implementation_effort: ImplementationEffort = Field(..., description="Implementation effort")
    risk_level: RiskLevel = Field(..., description="Risk level")
    action_required: str = Field(..., description="Action required")
    estimated_time: str = Field(..., description="Estimated implementation time")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites")
    implementation_steps: List[str] = Field(default_factory=list, description="Implementation steps")
    rollback_plan: Optional[str] = Field(None, description="Rollback plan")
    affected_resources: List[str] = Field(default_factory=list, description="Affected resources")
    tags: List[str] = Field(default_factory=list, description="Resource tags")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SafetyAudit(BaseModel):
    """Safety audit results"""
    scan_id: str = Field(..., description="Scan ID")
    permissions_verified: bool = Field(..., description="Permissions verified")
    read_only_operations: bool = Field(..., description="Read-only operations only")
    audit_trail_complete: bool = Field(..., description="Audit trail complete")
    encryption_enabled: bool = Field(..., description="Encryption enabled")
    compliance_verified: bool = Field(..., description="Compliance verified")
    risk_assessment: str = Field(..., description="Risk assessment")
    safety_score: float = Field(..., description="Safety score (0-100)")
    audit_timestamp: datetime = Field(..., description="Audit timestamp")
    api_calls_logged: int = Field(default=0, description="Number of API calls logged")
    credentials_encrypted: bool = Field(default=True, description="Credentials encrypted")
    rate_limits_respected: bool = Field(default=True, description="Rate limits respected")
    no_write_operations: bool = Field(default=True, description="No write operations performed")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks")
    security_checks: List[str] = Field(default_factory=list, description="Security checks performed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ScanReport(BaseModel):
    """Comprehensive scan report"""
    scan_id: str = Field(..., description="Scan ID")
    executive_summary: Dict[str, Any] = Field(..., description="Executive summary")
    technical_details: Dict[str, Any] = Field(..., description="Technical details")
    cost_breakdown: Dict[str, Any] = Field(..., description="Cost breakdown")
    optimization_recommendations: List[OptimizationRecommendation] = Field(..., description="Optimization recommendations")
    safety_audit: SafetyAudit = Field(..., description="Safety audit results")
    generated_at: datetime = Field(..., description="Report generation time")
    report_format: str = Field(default="json", description="Report format")
    report_url: Optional[str] = Field(None, description="Report URL")
    export_formats: List[str] = Field(default_factory=list, description="Available export formats")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ScanResult(BaseModel):
    """Complete scan result"""
    scan_id: str = Field(..., description="Scan ID")
    user_id: UUID = Field(..., description="User ID")
    config: ScannerConfig = Field(..., description="Scan configuration")
    resources: ResourceDiscovery = Field(..., description="Resource discovery results")
    metrics: Dict[str, Any] = Field(..., description="Utilization metrics")
    costs: CostAnalysis = Field(..., description="Cost analysis results")
    optimizations: List[OptimizationRecommendation] = Field(..., description="Optimization recommendations")
    safety_audit: SafetyAudit = Field(..., description="Safety audit results")
    report: ScanReport = Field(..., description="Scan report")
    scan_duration: float = Field(..., description="Scan duration in seconds")
    accuracy_score: float = Field(..., description="Overall accuracy score")
    created_at: datetime = Field(..., description="Scan start time")
    completed_at: datetime = Field(..., description="Scan completion time")
    status: str = Field(default="completed", description="Scan status")
    errors: List[str] = Field(default_factory=list, description="Scan errors")
    warnings: List[str] = Field(default_factory=list, description="Scan warnings")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class ScanRequest(BaseModel):
    """Scan request"""
    config: ScannerConfig = Field(..., description="Scan configuration")
    project_id: Optional[UUID] = Field(None, description="Project ID")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM, description="Scan priority")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled scan time")
    notifications: List[str] = Field(default_factory=list, description="Notification channels")
    tags: List[str] = Field(default_factory=list, description="Scan tags")


class ScanResponse(BaseModel):
    """Scan response"""
    scan_id: str = Field(..., description="Scan ID")
    status: str = Field(..., description="Scan status")
    message: str = Field(..., description="Response message")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in minutes")
    progress_url: Optional[str] = Field(None, description="Progress tracking URL")
    result_url: Optional[str] = Field(None, description="Result URL when complete")
    created_at: datetime = Field(..., description="Scan creation time")


class ScanStatusResponse(BaseModel):
    """Scan status response"""
    scan_id: str = Field(..., description="Scan ID")
    status: str = Field(..., description="Scan status")
    progress: float = Field(..., description="Progress percentage")
    current_step: str = Field(..., description="Current step")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    resources_discovered: int = Field(default=0, description="Resources discovered so far")
    errors: List[str] = Field(default_factory=list, description="Current errors")
    warnings: List[str] = Field(default_factory=list, description="Current warnings")
    started_at: datetime = Field(..., description="Scan start time")
    updated_at: datetime = Field(..., description="Last update time")


class ScanListResponse(BaseModel):
    """Scan list response"""
    scans: List[ScanResult] = Field(..., description="List of scans")
    total_count: int = Field(..., description="Total number of scans")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    total_pages: int = Field(..., description="Total pages")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Applied filters")


class OptimizationApplyRequest(BaseModel):
    """Optimization apply request"""
    recommendation_id: str = Field(..., description="Recommendation ID")
    dry_run: bool = Field(default=True, description="Perform dry run")
    auto_approve: bool = Field(default=False, description="Auto approve changes")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled application time")
    rollback_plan: Optional[str] = Field(None, description="Custom rollback plan")
    notifications: List[str] = Field(default_factory=list, description="Notification channels")


class OptimizationApplyResponse(BaseModel):
    """Optimization apply response"""
    recommendation_id: str = Field(..., description="Recommendation ID")
    status: str = Field(..., description="Application status")
    message: str = Field(..., description="Response message")
    applied_changes: List[Dict[str, Any]] = Field(default_factory=list, description="Applied changes")
    estimated_savings: float = Field(..., description="Estimated savings")
    implementation_time: str = Field(..., description="Implementation time")
    risk_assessment: str = Field(..., description="Risk assessment")
    rollback_available: bool = Field(default=True, description="Rollback available")
    applied_at: datetime = Field(..., description="Application time")


class ScannerHealthResponse(BaseModel):
    """Scanner health response"""
    status: str = Field(..., description="Scanner status")
    version: str = Field(..., description="Scanner version")
    supported_providers: List[ProviderType] = Field(..., description="Supported providers")
    supported_scan_types: List[ScanType] = Field(..., description="Supported scan types")
    uptime: float = Field(..., description="Scanner uptime in seconds")
    last_scan: Optional[datetime] = Field(None, description="Last scan time")
    total_scans: int = Field(default=0, description="Total scans performed")
    success_rate: float = Field(default=100.0, description="Success rate percentage")
    average_duration: float = Field(default=0.0, description="Average scan duration")
    active_scans: int = Field(default=0, description="Active scans")
    queue_size: int = Field(default=0, description="Queue size")
    system_resources: Dict[str, Any] = Field(default_factory=dict, description="System resources")
    health_checks: Dict[str, bool] = Field(default_factory=dict, description="Health checks")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ScannerConfigResponse(BaseModel):
    """Scanner configuration response"""
    default_config: ScannerConfig = Field(..., description="Default configuration")
    available_providers: List[ProviderType] = Field(..., description="Available providers")
    available_regions: Dict[str, List[str]] = Field(..., description="Available regions by provider")
    available_services: Dict[str, List[str]] = Field(..., description="Available services by provider")
    scan_limits: Dict[str, Any] = Field(..., description="Scan limits")
    rate_limits: Dict[str, Any] = Field(..., description="Rate limits")
    safety_settings: Dict[str, Any] = Field(..., description="Safety settings")
    compliance_frameworks: List[str] = Field(..., description="Compliance frameworks")
    export_formats: List[str] = Field(..., description="Available export formats")
    notification_channels: List[str] = Field(..., description="Available notification channels")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
