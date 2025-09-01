"""
Infrastructure models for CloudMind
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


class ResourceStatus(str, enum.Enum):
    """Resource status"""
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"
    PENDING = "pending"
    ERROR = "error"


class ResourceType(str, enum.Enum):
    """Resource types"""
    COMPUTE = "compute"
    STORAGE = "storage"
    NETWORK = "network"
    DATABASE = "database"
    CONTAINER = "container"
    LOAD_BALANCER = "load_balancer"
    CACHE = "cache"
    QUEUE = "queue"
    FUNCTION = "function"


class Infrastructure(Base):
    """Infrastructure model for managing cloud resources"""
    
    __tablename__ = "infrastructures"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    
    # Infrastructure metadata
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    environment = Column(String(50), default="production", nullable=False)  # dev, staging, prod
    
    # Cloud provider details
    cloud_provider = Column(String(50), nullable=False)  # AWS, Azure, GCP
    region = Column(String(100), nullable=False)
    account_id = Column(String(255), nullable=True)
    
    # Infrastructure configuration
    infrastructure_as_code = Column(JSON, nullable=True)  # Terraform, CloudFormation, etc.
    tags = Column(JSON, nullable=True)
    cost_center = Column(String(100), nullable=True)
    
    # Monitoring and alerts
    monitoring_enabled = Column(Boolean, default=True, nullable=False)
    alerting_enabled = Column(Boolean, default=True, nullable=False)
    health_status = Column(String(20), default="healthy", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_sync = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="infrastructures")
    resources = relationship("Resource", back_populates="infrastructure", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Infrastructure(id={self.id}, name={self.name}, cloud_provider={self.cloud_provider})>"
    
    @property
    def total_resources(self) -> int:
        """Get total number of resources"""
        return len(self.resources) if self.resources else 0
    
    @property
    def running_resources(self) -> int:
        """Get number of running resources"""
        if not self.resources:
            return 0
        return len([r for r in self.resources if r.status == ResourceStatus.RUNNING])
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost of infrastructure"""
        if not self.resources:
            return 0.0
        return sum(r.monthly_cost for r in self.resources if r.monthly_cost)
    
    def to_dict(self) -> dict:
        """Convert infrastructure to dictionary"""
        return {
            "id": str(self.id),
            "project_id": str(self.project_id),
            "name": self.name,
            "description": self.description,
            "environment": self.environment,
            "cloud_provider": self.cloud_provider,
            "region": self.region,
            "account_id": self.account_id,
            "infrastructure_as_code": self.infrastructure_as_code,
            "tags": self.tags,
            "cost_center": self.cost_center,
            "monitoring_enabled": self.monitoring_enabled,
            "alerting_enabled": self.alerting_enabled,
            "health_status": self.health_status,
            "total_resources": self.total_resources,
            "running_resources": self.running_resources,
            "total_cost": self.total_cost,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
        }


class Resource(Base):
    """Resource model for individual cloud resources"""
    
    __tablename__ = "resources"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    infrastructure_id = Column(UUID(as_uuid=True), ForeignKey("infrastructures.id"), nullable=False)
    
    # Resource identification
    resource_id = Column(String(255), nullable=False)  # Cloud provider resource ID
    name = Column(String(255), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)
    
    # Resource details
    status = Column(Enum(ResourceStatus), default=ResourceStatus.PENDING, nullable=False)
    instance_type = Column(String(100), nullable=True)  # t3.micro, etc.
    size = Column(String(100), nullable=True)  # 100GB, etc.
    
    # Location and networking
    availability_zone = Column(String(100), nullable=True)
    private_ip = Column(String(45), nullable=True)  # IPv4/IPv6
    public_ip = Column(String(45), nullable=True)
    vpc_id = Column(String(255), nullable=True)
    subnet_id = Column(String(255), nullable=True)
    
    # Cost information
    hourly_cost = Column(Float, nullable=True)
    monthly_cost = Column(Float, nullable=True)
    cost_currency = Column(String(3), default="USD", nullable=False)
    
    # Performance metrics
    cpu_utilization = Column(Float, nullable=True)
    memory_utilization = Column(Float, nullable=True)
    disk_utilization = Column(Float, nullable=True)
    network_throughput = Column(Float, nullable=True)
    
    # Configuration
    configuration = Column(JSON, nullable=True)  # Resource-specific config
    tags = Column(JSON, nullable=True)
    resource_metadata = Column(JSON, nullable=True)  # Additional metadata
    
    # Security
    security_groups = Column(JSON, nullable=True)
    encryption_enabled = Column(Boolean, default=False, nullable=False)
    backup_enabled = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_updated = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    infrastructure = relationship("Infrastructure", back_populates="resources")
    
    def __repr__(self):
        return f"<Resource(id={self.id}, name={self.name}, type={self.resource_type}, status={self.status})>"
    
    @property
    def is_running(self) -> bool:
        """Check if resource is running"""
        return self.status == ResourceStatus.RUNNING
    
    @property
    def is_stopped(self) -> bool:
        """Check if resource is stopped"""
        return self.status == ResourceStatus.STOPPED
    
    @property
    def cost_per_day(self) -> float:
        """Calculate daily cost"""
        if self.hourly_cost:
            return self.hourly_cost * 24
        return 0.0
    
    @property
    def health_status(self) -> str:
        """Get resource health status"""
        if self.status == ResourceStatus.ERROR:
            return "error"
        elif self.status == ResourceStatus.TERMINATED:
            return "terminated"
        elif self.status == ResourceStatus.STOPPED:
            return "stopped"
        elif self.status == ResourceStatus.RUNNING:
            return "healthy"
        return "unknown"
    
    def to_dict(self) -> dict:
        """Convert resource to dictionary"""
        return {
            "id": str(self.id),
            "infrastructure_id": str(self.infrastructure_id),
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type.value,
            "status": self.status.value,
            "instance_type": self.instance_type,
            "size": self.size,
            "availability_zone": self.availability_zone,
            "private_ip": self.private_ip,
            "public_ip": self.public_ip,
            "vpc_id": self.vpc_id,
            "subnet_id": self.subnet_id,
            "hourly_cost": self.hourly_cost,
            "monthly_cost": self.monthly_cost,
            "cost_currency": self.cost_currency,
            "cpu_utilization": self.cpu_utilization,
            "memory_utilization": self.memory_utilization,
            "disk_utilization": self.disk_utilization,
            "network_throughput": self.network_throughput,
            "configuration": self.configuration,
            "tags": self.tags,
            "resource_metadata": self.resource_metadata,
            "security_groups": self.security_groups,
            "encryption_enabled": self.encryption_enabled,
            "backup_enabled": self.backup_enabled,
            "is_running": self.is_running,
            "is_stopped": self.is_stopped,
            "cost_per_day": self.cost_per_day,
            "health_status": self.health_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        } 