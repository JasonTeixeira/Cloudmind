"""
Security Scan Models
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from app.core.database import Base



class SecurityScan(Base):
    """Advanced security scan model with enterprise features"""
    __tablename__ = "security_scans"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    scan_type = Column(String(50), nullable=False)  # vulnerability, compliance, penetration, configuration
    scan_method = Column(String(50), nullable=False, default="automated")  # automated, manual, hybrid
    
    # Scan Configuration
    target_resources = Column(JSON, nullable=False, default=list)
    scan_config = Column(JSON, nullable=True)
    compliance_frameworks = Column(JSON, nullable=True)  # SOC2, HIPAA, PCI, ISO27001, etc.
    scan_rules = Column(JSON, nullable=True)
    exclusions = Column(JSON, nullable=True)
    
    # Status & Progress
    status = Column(String(20), nullable=False, default="pending")  # pending, running, completed, failed
    progress = Column(Integer, nullable=False, default=0)  # 0-100
    current_step = Column(String(100), nullable=True)
    estimated_completion = Column(DateTime, nullable=True)
    
    # Results
    vulnerabilities_count = Column(Integer, nullable=False, default=0)
    critical_count = Column(Integer, nullable=False, default=0)
    high_count = Column(Integer, nullable=False, default=0)
    medium_count = Column(Integer, nullable=False, default=0)
    low_count = Column(Integer, nullable=False, default=0)
    info_count = Column(Integer, nullable=False, default=0)
    
    # Compliance Results
    compliance_score = Column(Float, nullable=True)  # 0-100
    compliance_status = Column(String(20), nullable=True)  # compliant, non_compliant, at_risk
    controls_total = Column(Integer, nullable=True)
    controls_passed = Column(Integer, nullable=True)
    controls_failed = Column(Integer, nullable=True)
    controls_partial = Column(Integer, nullable=True)
    
    # Security Metrics
    security_score = Column(Float, nullable=True)  # 0-100
    risk_score = Column(Float, nullable=True)  # 0-100
    threat_level = Column(String(20), nullable=True)  # low, medium, high, critical
    attack_surface = Column(JSON, nullable=True)
    
    # Performance Metrics
    scan_duration = Column(Integer, nullable=True)  # Seconds
    resources_scanned = Column(Integer, nullable=True)
    scan_coverage = Column(Float, nullable=True)  # Percentage
    false_positive_rate = Column(Float, nullable=True)
    
    # Quality & Validation
    data_quality_score = Column(Float, nullable=True)
    scan_accuracy = Column(Float, nullable=True)
    validation_status = Column(String(20), nullable=True)  # pending, validated, failed
    
    # Audit Trail
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    
    # Relationships
    user = relationship("User", back_populates="security_scans")
    project = relationship("Project", back_populates="security_scans")
    vulnerabilities = relationship("Vulnerability", back_populates="security_scan", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="security_scan", cascade="all, delete-orphan")


class Vulnerability(Base):
    """Advanced vulnerability model with detailed tracking"""
    __tablename__ = "vulnerabilities"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    security_scan_id = Column(PGUUID(as_uuid=True), ForeignKey("security_scans.id"), nullable=False)
    
    # Basic Information
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    
    # Classification
    severity = Column(String(20), nullable=False)  # critical, high, medium, low, info
    category = Column(String(50), nullable=False)  # injection, authentication, authorization, etc.
    subcategory = Column(String(50), nullable=True)
    cwe_id = Column(String(20), nullable=True)  # Common Weakness Enumeration
    cve_id = Column(String(20), nullable=True)  # Common Vulnerabilities and Exposures
    
    # Technical Details
    cvss_score = Column(Float, nullable=True)  # 0-10
    cvss_vector = Column(String(100), nullable=True)
    attack_vector = Column(String(50), nullable=True)
    attack_complexity = Column(String(20), nullable=True)
    privileges_required = Column(String(20), nullable=True)
    user_interaction = Column(String(20), nullable=True)
    scope = Column(String(20), nullable=True)
    
    # Affected Resources
    affected_resource = Column(String(255), nullable=True)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(String(255), nullable=True)
    affected_services = Column(JSON, nullable=True)
    affected_regions = Column(JSON, nullable=True)
    affected_accounts = Column(JSON, nullable=True)
    
    # Evidence & Proof of Concept
    evidence = Column(Text, nullable=True)
    proof_of_concept = Column(Text, nullable=True)
    request_data = Column(Text, nullable=True)
    response_data = Column(Text, nullable=True)
    screenshots = Column(JSON, nullable=True)
    
    # Remediation
    remediation_steps = Column(JSON, nullable=True)
    remediation_effort = Column(String(20), nullable=True)  # low, medium, high
    remediation_cost = Column(Float, nullable=True)
    remediation_time = Column(Integer, nullable=True)  # Estimated hours
    rollback_plan = Column(Text, nullable=True)
    
    # References & Resources
    references = Column(JSON, nullable=True)
    external_links = Column(JSON, nullable=True)
    vendor_advisories = Column(JSON, nullable=True)
    patch_availability = Column(String(20), nullable=True)  # available, pending, unavailable
    
    # Status & Tracking
    status = Column(String(20), nullable=False, default="open")  # open, in_progress, remediated, false_positive
    is_remediated = Column(Boolean, nullable=False, default=False)
    remediated_at = Column(DateTime, nullable=True)
    remediated_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    remediation_notes = Column(Text, nullable=True)
    verification_status = Column(String(20), nullable=True)  # pending, verified, failed
    
    # Risk Assessment
    business_impact = Column(String(20), nullable=True)  # low, medium, high, critical
    likelihood = Column(String(20), nullable=True)  # low, medium, high
    risk_score = Column(Float, nullable=True)  # 0-100
    risk_level = Column(String(20), nullable=True)  # low, medium, high, critical
    
    # Compliance
    compliance_impact = Column(JSON, nullable=True)  # Affected compliance frameworks
    regulatory_requirements = Column(JSON, nullable=True)
    audit_findings = Column(JSON, nullable=True)
    
    # Monitoring
    monitoring_status = Column(String(20), nullable=True)  # active, inactive
    last_detected = Column(DateTime, nullable=True)
    detection_count = Column(Integer, nullable=False, default=1)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    security_scan = relationship("SecurityScan", back_populates="vulnerabilities")
    remediated_by_user = relationship("User")


class ComplianceCheck(Base):
    """Compliance framework checking and validation"""
    __tablename__ = "compliance_checks"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    security_scan_id = Column(PGUUID(as_uuid=True), ForeignKey("security_scans.id"), nullable=False)
    
    # Framework Information
    framework = Column(String(50), nullable=False)  # SOC2, HIPAA, PCI, ISO27001, etc.
    control_id = Column(String(100), nullable=False)
    control_name = Column(String(255), nullable=False)
    control_description = Column(Text, nullable=True)
    control_category = Column(String(100), nullable=True)
    
    # Assessment
    status = Column(String(20), nullable=False)  # passed, failed, partial, not_applicable
    compliance_score = Column(Float, nullable=True)  # 0-100
    evidence = Column(Text, nullable=True)
    findings = Column(JSON, nullable=True)
    
    # Requirements
    requirements = Column(JSON, nullable=True)
    mandatory = Column(Boolean, nullable=False, default=False)
    critical = Column(Boolean, nullable=False, default=False)
    
    # Remediation
    remediation_required = Column(Boolean, nullable=False, default=False)
    remediation_plan = Column(Text, nullable=True)
    remediation_deadline = Column(DateTime, nullable=True)
    remediation_status = Column(String(20), nullable=True)  # pending, in_progress, completed
    
    # Validation
    validated_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    validated_at = Column(DateTime, nullable=True)
    validation_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    security_scan = relationship("SecurityScan", back_populates="compliance_checks")
    validated_by_user = relationship("User")


class SecurityAlert(Base):
    """Advanced security alerts and incident tracking"""
    __tablename__ = "security_alerts"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    vulnerability_id = Column(PGUUID(as_uuid=True), ForeignKey("vulnerabilities.id"), nullable=True)
    
    # Alert Information
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), nullable=False)  # vulnerability, compliance, threat, anomaly
    severity = Column(String(20), nullable=False, default="medium")  # info, warning, error, critical
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50), nullable=True)
    
    # Threat Intelligence
    threat_level = Column(String(20), nullable=True)  # low, medium, high, critical
    threat_actors = Column(JSON, nullable=True)
    attack_vectors = Column(JSON, nullable=True)
    ioc_data = Column(JSON, nullable=True)  # Indicators of Compromise
    
    # Affected Resources
    affected_resource = Column(String(255), nullable=True)
    resource_type = Column(String(100), nullable=True)
    affected_services = Column(JSON, nullable=True)
    affected_regions = Column(JSON, nullable=True)
    affected_users = Column(JSON, nullable=True)
    
    # Impact Assessment
    business_impact = Column(String(20), nullable=True)  # low, medium, high, critical
    financial_impact = Column(Float, nullable=True)
    operational_impact = Column(String(20), nullable=True)
    reputation_impact = Column(String(20), nullable=True)
    
    # Status & Resolution
    status = Column(String(20), nullable=False, default="active")  # active, acknowledged, investigating, resolved
    priority = Column(String(20), nullable=False, default="medium")  # low, medium, high, critical
    is_resolved = Column(Boolean, nullable=False, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Escalation
    escalation_level = Column(Integer, nullable=False, default=1)
    escalated_to = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    escalation_reason = Column(Text, nullable=True)
    
    # Notification
    notification_sent = Column(Boolean, nullable=False, default=False)
    notification_channels = Column(JSON, nullable=True)  # email, slack, webhook, sms
    notification_recipients = Column(JSON, nullable=True)
    notification_sent_at = Column(DateTime, nullable=True)
    
    # Investigation
    investigation_status = Column(String(20), nullable=True)  # pending, in_progress, completed
    investigation_notes = Column(Text, nullable=True)
    evidence_collected = Column(JSON, nullable=True)
    timeline = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    vulnerability = relationship("Vulnerability")
    resolved_by_user = relationship("User", foreign_keys=[resolved_by])
    escalated_to_user = relationship("User", foreign_keys=[escalated_to])


class SecurityPolicy(Base):
    """Security policies and compliance rules"""
    __tablename__ = "security_policies"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(PGUUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    user_id = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Policy Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    policy_type = Column(String(50), nullable=False)  # access_control, data_protection, network_security, etc.
    version = Column(String(20), nullable=False, default="1.0")
    
    # Policy Rules
    rules = Column(JSON, nullable=False)
    conditions = Column(JSON, nullable=True)
    exceptions = Column(JSON, nullable=True)
    
    # Compliance
    compliance_frameworks = Column(JSON, nullable=True)
    regulatory_requirements = Column(JSON, nullable=True)
    audit_requirements = Column(JSON, nullable=True)
    
    # Enforcement
    enforcement_level = Column(String(20), nullable=False, default="medium")  # low, medium, high, strict
    auto_remediation = Column(Boolean, nullable=False, default=False)
    remediation_actions = Column(JSON, nullable=True)
    
    # Monitoring
    monitoring_enabled = Column(Boolean, nullable=False, default=True)
    alert_thresholds = Column(JSON, nullable=True)
    reporting_frequency = Column(String(20), nullable=True)  # daily, weekly, monthly
    
    # Status
    status = Column(String(20), nullable=False, default="active")  # active, inactive, draft, archived
    effective_date = Column(DateTime, nullable=False)
    expiry_date = Column(DateTime, nullable=True)
    
    # Approval
    approved_by = Column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    approval_notes = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
    user = relationship("User", foreign_keys=[user_id])
    approved_by_user = relationship("User", foreign_keys=[approved_by]) 