"""
Security schemas
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator


class SecurityScanBase(BaseModel):
    """Base security scan schema"""
    name: str = Field(..., min_length=1, max_length=255, description="Scan name")
    description: Optional[str] = Field(None, max_length=1000, description="Scan description")
    project_id: Optional[UUID] = Field(None, description="Associated project ID")
    scan_type: str = Field(..., description="Type of security scan")
    target_resources: List[str] = Field(default_factory=list, description="Target resources to scan")
    scan_config: Dict[str, Any] = Field(default_factory=dict, description="Scan configuration")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Compliance frameworks to check")


class SecurityScanCreate(SecurityScanBase):
    """Create security scan schema"""
    pass


class SecurityScanUpdate(BaseModel):
    """Update security scan schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    scan_type: Optional[str] = Field(None)
    target_resources: Optional[List[str]] = Field(None)
    scan_config: Optional[Dict[str, Any]] = Field(None)
    compliance_frameworks: Optional[List[str]] = Field(None)


class SecurityScanResponse(SecurityScanBase):
    """Security scan response schema"""
    id: UUID
    user_id: UUID
    status: str = Field(..., description="Scan status")
    progress: int = Field(default=0, ge=0, le=100, description="Scan progress percentage")
    vulnerabilities_count: int = Field(default=0, description="Number of vulnerabilities found")
    critical_count: int = Field(default=0, description="Number of critical vulnerabilities")
    high_count: int = Field(default=0, description="Number of high severity vulnerabilities")
    medium_count: int = Field(default=0, description="Number of medium severity vulnerabilities")
    low_count: int = Field(default=0, description="Number of low severity vulnerabilities")
    compliance_score: Optional[float] = Field(None, description="Compliance score percentage")
    scan_duration: Optional[int] = Field(None, description="Scan duration in seconds")
    started_at: Optional[datetime] = Field(None, description="When scan started")
    completed_at: Optional[datetime] = Field(None, description="When scan completed")
    error_message: Optional[str] = Field(None, description="Error message if scan failed")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VulnerabilityBase(BaseModel):
    """Base vulnerability schema"""
    title: str = Field(..., min_length=1, max_length=255, description="Vulnerability title")
    description: str = Field(..., min_length=1, max_length=2000, description="Vulnerability description")
    severity: str = Field(..., description="Vulnerability severity (critical, high, medium, low)")
    category: str = Field(..., description="Vulnerability category")
    cve_id: Optional[str] = Field(None, description="CVE identifier")
    cvss_score: Optional[float] = Field(None, ge=0, le=10, description="CVSS score")
    affected_resource: Optional[str] = Field(None, description="Affected resource identifier")
    resource_type: Optional[str] = Field(None, description="Resource type")


class VulnerabilityCreate(VulnerabilityBase):
    """Create vulnerability schema"""
    security_scan_id: UUID = Field(..., description="Associated security scan ID")
    remediation_steps: List[str] = Field(default_factory=list, description="Remediation steps")
    references: List[str] = Field(default_factory=list, description="Reference links")


class VulnerabilityResponse(VulnerabilityBase):
    """Vulnerability response schema"""
    id: UUID
    security_scan_id: UUID
    status: str = Field(..., description="Vulnerability status")
    remediation_steps: List[str] = Field(default_factory=list, description="Remediation steps")
    references: List[str] = Field(default_factory=list, description="Reference links")
    is_remediated: bool = Field(default=False, description="Whether vulnerability is remediated")
    remediated_at: Optional[datetime] = Field(None, description="When vulnerability was remediated")
    remediated_by: Optional[str] = Field(None, description="Who remediated the vulnerability")
    remediation_notes: Optional[str] = Field(None, description="Remediation notes")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SecuritySummary(BaseModel):
    """Security summary schema"""
    total_scans: int = Field(..., description="Total number of scans")
    completed_scans: int = Field(..., description="Number of completed scans")
    failed_scans: int = Field(..., description="Number of failed scans")
    total_vulnerabilities: int = Field(..., description="Total number of vulnerabilities")
    critical_vulnerabilities: int = Field(..., description="Number of critical vulnerabilities")
    high_vulnerabilities: int = Field(..., description="Number of high severity vulnerabilities")
    medium_vulnerabilities: int = Field(..., description="Number of medium severity vulnerabilities")
    low_vulnerabilities: int = Field(..., description="Number of low severity vulnerabilities")
    remediated_vulnerabilities: int = Field(..., description="Number of remediated vulnerabilities")
    security_score: float = Field(..., ge=0, le=100, description="Overall security score")
    compliance_score: float = Field(..., ge=0, le=100, description="Overall compliance score")
    last_scan_date: Optional[datetime] = Field(None, description="Date of last scan")
    period: str = Field(..., description="Analysis period")


class ComplianceReport(BaseModel):
    """Compliance report schema"""
    framework: str = Field(..., description="Compliance framework")
    overall_score: float = Field(..., ge=0, le=100, description="Overall compliance score")
    status: str = Field(..., description="Compliance status")
    assessment_date: datetime = Field(..., description="Assessment date")
    controls_total: int = Field(..., description="Total number of controls")
    controls_passed: int = Field(..., description="Number of passed controls")
    controls_failed: int = Field(..., description="Number of failed controls")
    controls_partial: int = Field(..., description="Number of partially compliant controls")
    recommendations: List[str] = Field(default_factory=list, description="Compliance recommendations")
    next_assessment_date: Optional[datetime] = Field(None, description="Next assessment date")


class SecurityAlert(BaseModel):
    """Security alert schema"""
    id: UUID
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    severity: str = Field(..., description="Alert severity (info, warning, error, critical)")
    category: str = Field(..., description="Alert category")
    project_id: Optional[UUID] = Field(None, description="Associated project")
    vulnerability_id: Optional[UUID] = Field(None, description="Associated vulnerability")
    affected_resource: Optional[str] = Field(None, description="Affected resource")
    is_resolved: bool = Field(default=False, description="Whether alert is resolved")
    resolved_at: Optional[datetime] = Field(None, description="When alert was resolved")
    resolved_by: Optional[str] = Field(None, description="Who resolved the alert")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SecurityScanRequest(BaseModel):
    """Security scan request schema"""
    project_id: Optional[UUID] = Field(None, description="Project to scan")
    scan_type: str = Field(..., description="Type of scan to perform")
    target_resources: List[str] = Field(default_factory=list, description="Resources to scan")
    compliance_frameworks: List[str] = Field(default_factory=list, description="Frameworks to check")
    scan_config: Dict[str, Any] = Field(default_factory=dict, description="Scan configuration")


class SecurityScanResult(BaseModel):
    """Security scan result schema"""
    scan_id: UUID
    vulnerabilities: List[VulnerabilityResponse]
    compliance_report: Optional[ComplianceReport] = Field(None, description="Compliance report")
    security_score: float = Field(..., ge=0, le=100, description="Security score")
    scan_summary: Dict[str, Any] = Field(default_factory=dict, description="Scan summary")
    recommendations: List[str] = Field(default_factory=list, description="Security recommendations") 