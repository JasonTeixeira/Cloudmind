"""
Infrastructure schemas for CloudMind API
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field

from app.models.infrastructure import ResourceType, ResourceStatus


class InfrastructureBase(BaseModel):
    """Base infrastructure schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Infrastructure name")
    description: Optional[str] = Field(None, max_length=1000, description="Infrastructure description")
    environment: str = Field(default="production", description="Environment (dev, staging, prod)")
    cloud_provider: str = Field(..., description="Cloud provider (AWS, Azure, GCP)")
    region: str = Field(..., description="Cloud region")
    account_id: Optional[str] = Field(None, description="Cloud account ID")
    cost_center: Optional[str] = Field(None, description="Cost center for billing")


class InfrastructureCreate(InfrastructureBase):
    """Schema for creating infrastructure"""
    project_id: UUID = Field(..., description="Project ID")
    infrastructure_as_code: Optional[Dict[str, Any]] = Field(None, description="IaC configuration")
    tags: Optional[Dict[str, str]] = Field(None, description="Resource tags")


class InfrastructureUpdate(BaseModel):
    """Schema for updating infrastructure"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    environment: Optional[str] = Field(None)
    cloud_provider: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
    account_id: Optional[str] = Field(None)
    cost_center: Optional[str] = Field(None)
    infrastructure_as_code: Optional[Dict[str, Any]] = Field(None)
    tags: Optional[Dict[str, str]] = Field(None)
    monitoring_enabled: Optional[bool] = Field(None)
    alerting_enabled: Optional[bool] = Field(None)


class InfrastructureResponse(InfrastructureBase):
    """Schema for infrastructure response"""
    id: UUID = Field(..., description="Infrastructure ID")
    project_id: UUID = Field(..., description="Project ID")
    infrastructure_as_code: Optional[Dict[str, Any]] = Field(None)
    tags: Optional[Dict[str, str]] = Field(None)
    monitoring_enabled: bool = Field(..., description="Monitoring status")
    alerting_enabled: bool = Field(..., description="Alerting status")
    health_status: str = Field(..., description="Health status")
    total_resources: int = Field(..., description="Total number of resources")
    running_resources: int = Field(..., description="Number of running resources")
    total_cost: float = Field(..., description="Total monthly cost")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_sync: Optional[datetime] = Field(None, description="Last sync timestamp")

    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    """Base resource schema"""
    resource_id: str = Field(..., description="Cloud provider resource ID")
    name: str = Field(..., min_length=1, max_length=255, description="Resource name")
    resource_type: ResourceType = Field(..., description="Resource type")
    instance_type: Optional[str] = Field(None, description="Instance type")
    size: Optional[str] = Field(None, description="Resource size")
    availability_zone: Optional[str] = Field(None, description="Availability zone")
    private_ip: Optional[str] = Field(None, description="Private IP address")
    public_ip: Optional[str] = Field(None, description="Public IP address")
    vpc_id: Optional[str] = Field(None, description="VPC ID")
    subnet_id: Optional[str] = Field(None, description="Subnet ID")
    hourly_cost: Optional[float] = Field(None, description="Hourly cost")
    monthly_cost: Optional[float] = Field(None, description="Monthly cost")
    cost_currency: str = Field(default="USD", description="Cost currency")
    cpu_utilization: Optional[float] = Field(None, description="CPU utilization percentage")
    memory_utilization: Optional[float] = Field(None, description="Memory utilization percentage")
    disk_utilization: Optional[float] = Field(None, description="Disk utilization percentage")
    network_throughput: Optional[float] = Field(None, description="Network throughput")
    configuration: Optional[Dict[str, Any]] = Field(None, description="Resource configuration")
    tags: Optional[Dict[str, str]] = Field(None, description="Resource tags")
    resource_metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    security_groups: Optional[List[str]] = Field(None, description="Security groups")
    encryption_enabled: bool = Field(default=False, description="Encryption status")
    backup_enabled: bool = Field(default=False, description="Backup status")


class ResourceCreate(ResourceBase):
    """Schema for creating resource"""
    infrastructure_id: UUID = Field(..., description="Infrastructure ID")


class ResourceUpdate(BaseModel):
    """Schema for updating resource"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    resource_type: Optional[ResourceType] = Field(None)
    instance_type: Optional[str] = Field(None)
    size: Optional[str] = Field(None)
    availability_zone: Optional[str] = Field(None)
    private_ip: Optional[str] = Field(None)
    public_ip: Optional[str] = Field(None)
    vpc_id: Optional[str] = Field(None)
    subnet_id: Optional[str] = Field(None)
    hourly_cost: Optional[float] = Field(None)
    monthly_cost: Optional[float] = Field(None)
    cost_currency: Optional[str] = Field(None)
    cpu_utilization: Optional[float] = Field(None)
    memory_utilization: Optional[float] = Field(None)
    disk_utilization: Optional[float] = Field(None)
    network_throughput: Optional[float] = Field(None)
    configuration: Optional[Dict[str, Any]] = Field(None)
    tags: Optional[Dict[str, str]] = Field(None)
    resource_metadata: Optional[Dict[str, Any]] = Field(None)
    security_groups: Optional[List[str]] = Field(None)
    encryption_enabled: Optional[bool] = Field(None)
    backup_enabled: Optional[bool] = Field(None)


class ResourceResponse(ResourceBase):
    """Schema for resource response"""
    id: UUID = Field(..., description="Resource ID")
    infrastructure_id: UUID = Field(..., description="Infrastructure ID")
    status: ResourceStatus = Field(..., description="Resource status")
    is_running: bool = Field(..., description="Running status")
    is_stopped: bool = Field(..., description="Stopped status")
    cost_per_day: float = Field(..., description="Daily cost")
    health_status: str = Field(..., description="Health status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    last_updated: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class InfrastructureSummary(BaseModel):
    """Schema for infrastructure summary"""
    total_infrastructures: int = Field(..., description="Total number of infrastructures")
    active_infrastructures: int = Field(..., description="Number of active infrastructures")
    total_resources: int = Field(..., description="Total number of resources")
    running_resources: int = Field(..., description="Number of running resources")
    total_monthly_cost: float = Field(..., description="Total monthly cost")
    health_score: float = Field(..., description="Overall health score")
    resources_by_type: Dict[str, int] = Field(..., description="Resources by type")
    resources_by_status: Dict[str, int] = Field(..., description="Resources by status")


class InfrastructureHealth(BaseModel):
    """Schema for infrastructure health"""
    infrastructure_id: UUID = Field(..., description="Infrastructure ID")
    health_status: str = Field(..., description="Health status")
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="Health issues")
    recommendations: List[Dict[str, Any]] = Field(default_factory=list, description="Recommendations")
    last_check: datetime = Field(..., description="Last health check timestamp")


class ResourceMetrics(BaseModel):
    """Schema for resource metrics"""
    resource_id: UUID = Field(..., description="Resource ID")
    cpu_utilization: float = Field(..., description="CPU utilization")
    memory_utilization: float = Field(..., description="Memory utilization")
    disk_utilization: float = Field(..., description="Disk utilization")
    network_throughput: float = Field(..., description="Network throughput")
    cost_per_hour: float = Field(..., description="Cost per hour")
    timestamp: datetime = Field(..., description="Metrics timestamp") 