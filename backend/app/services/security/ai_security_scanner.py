"""
AI-Powered Security Scanner for CloudMind
Advanced security vulnerability detection, compliance automation, and threat intelligence
"""

import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import json
import re
import uuid

from app.core.config import settings
from app.services.ai_engine.ensemble_ai import ensemble_ai, ConsensusMethod
from app.services.ai_engine.god_tier_ai_service import AnalysisType
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


class SecuritySeverity(Enum):
    """Security vulnerability severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ComplianceFramework(Enum):
    """Compliance frameworks"""
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    NIST = "nist"
    AWS_CIS = "aws_cis"
    AZURE_CIS = "azure_cis"


class ThreatType(Enum):
    """Types of security threats"""
    MALWARE = "malware"
    PHISHING = "phishing"
    DDoS = "ddos"
    DATA_BREACH = "data_breach"
    INSIDER_THREAT = "insider_threat"
    ZERO_DAY = "zero_day"
    CONFIGURATION_ERROR = "configuration_error"
    ACCESS_CONTROL = "access_control"


@dataclass
class SecurityVulnerability:
    """Security vulnerability details"""
    vulnerability_id: str
    title: str
    description: str
    severity: SecuritySeverity
    cvss_score: float
    affected_resources: List[str]
    remediation_steps: List[str]
    references: List[str]
    discovered_at: datetime
    ai_confidence: float
    false_positive_risk: float
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class ComplianceCheck:
    """Compliance check result"""
    check_id: str
    framework: ComplianceFramework
    control_id: str
    control_name: str
    status: str  # "compliant", "non_compliant", "partial", "not_applicable"
    description: str
    evidence: List[str]
    remediation_required: bool
    remediation_steps: List[str]
    risk_level: str
    last_checked: datetime
    ai_confidence: float
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class ThreatIntelligence:
    """Threat intelligence information"""
    threat_id: str
    threat_type: ThreatType
    title: str
    description: str
    indicators: List[str]
    severity: SecuritySeverity
    affected_resources: List[str]
    mitigation_strategies: List[str]
    threat_actors: List[str]
    confidence_score: float
    source: str
    discovered_at: datetime
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class SecurityReport:
    """Comprehensive security report"""
    report_id: str
    scan_type: str
    scan_duration: float
    resources_scanned: int
    vulnerabilities_found: int
    compliance_issues: int
    threats_detected: int
    overall_security_score: float
    recommendations: List[str]
    executive_summary: str
    detailed_findings: Dict[str, Any]
    generated_at: datetime = None
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now(timezone.utc)


class AISecurityScanner:
    """Advanced AI-powered security scanner"""
    
    def __init__(self):
        self.vulnerabilities: List[SecurityVulnerability] = []
        self.compliance_checks: List[ComplianceCheck] = []
        self.threat_intelligence: List[ThreatIntelligence] = []
        self.security_reports: List[SecurityReport] = []
        
        # Initialize security patterns
        self._initialize_security_patterns()
        
        logger.info("🛡️ AI Security Scanner initialized")
    
    def _initialize_security_patterns(self):
        """Initialize security patterns and signatures"""
        try:
            # Common vulnerability patterns
            self.vulnerability_patterns = {
                'sql_injection': [
                    r"(\b(union|select|insert|update|delete|drop|create|alter)\b.*\b(from|into|where|table|database)\b)",
                    r"(\b(exec|execute|sp_executesql)\b.*\b(@|'|\"))"
                ],
                'xss': [
                    r"(\b(script|javascript|vbscript)\b.*\b(alert|confirm|prompt|eval|document\.cookie)\b)",
                    r"(\b(onload|onerror|onclick|onmouseover)\b.*\b(alert|confirm|prompt)\b)"
                ],
                'path_traversal': [
                    r"(\b(\.\.\/|\.\.\\|\.\.%2f|\.\.%5c)\b)",
                    r"(\b(etc\/passwd|windows\/system32|proc\/self)\b)"
                ]
            }
            
            # Compliance control mappings
            self.compliance_controls = {
                ComplianceFramework.SOC2: {
                    'CC1': 'Control Environment',
                    'CC2': 'Communication and Information',
                    'CC3': 'Risk Assessment',
                    'CC4': 'Monitoring Activities',
                    'CC5': 'Control Activities'
                },
                ComplianceFramework.AWS_CIS: {
                    '1.1': 'Avoid the use of the "root" account',
                    '1.2': 'Ensure MFA is enabled for the "root" account',
                    '1.3': 'Ensure credentials unused for 90 days or greater are disabled',
                    '1.4': 'Ensure access keys are rotated every 90 days or less'
                }
            }
            
            logger.info("✅ Security patterns initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize security patterns: {e}")
    
    async def scan_resources(
        self,
        resources: List[Dict[str, Any]],
        scan_type: str = "comprehensive",
        include_compliance: bool = True,
        include_threat_intelligence: bool = True
    ) -> SecurityReport:
        """Perform comprehensive security scan"""
        try:
            logger.info(f"🔍 Starting {scan_type} security scan for {len(resources)} resources")
            
            start_time = datetime.now(timezone.utc)
            
            # Initialize scan results
            vulnerabilities = []
            compliance_issues = []
            threats = []
            
            # Perform vulnerability scanning
            if scan_type in ["comprehensive", "vulnerability"]:
                vulnerabilities = await self._scan_vulnerabilities(resources)
            
            # Perform compliance checking
            if include_compliance and scan_type in ["comprehensive", "compliance"]:
                compliance_issues = await self._check_compliance(resources)
            
            # Perform threat intelligence analysis
            if include_threat_intelligence and scan_type in ["comprehensive", "threat"]:
                threats = await self._analyze_threat_intelligence(resources)
            
            # Calculate security score
            security_score = self._calculate_security_score(vulnerabilities, compliance_issues, threats)
            
            # Generate recommendations
            recommendations = await self._generate_security_recommendations(
                vulnerabilities, compliance_issues, threats
            )
            
            # Create executive summary
            executive_summary = await self._generate_executive_summary(
                vulnerabilities, compliance_issues, threats, security_score
            )
            
            # Calculate scan duration
            end_time = datetime.now(timezone.utc)
            scan_duration = (end_time - start_time).total_seconds()
            
            # Create security report
            report = SecurityReport(
                report_id=str(uuid.uuid4()),
                scan_type=scan_type,
                scan_duration=scan_duration,
                resources_scanned=len(resources),
                vulnerabilities_found=len(vulnerabilities),
                compliance_issues=len(compliance_issues),
                threats_detected=len(threats),
                overall_security_score=security_score,
                recommendations=recommendations,
                executive_summary=executive_summary,
                detailed_findings={
                    "vulnerabilities": [self._vulnerability_to_dict(v) for v in vulnerabilities],
                    "compliance_issues": [self._compliance_to_dict(c) for c in compliance_issues],
                    "threats": [self._threat_to_dict(t) for t in threats]
                }
            )
            
            # Store results
            self.vulnerabilities.extend(vulnerabilities)
            self.compliance_checks.extend(compliance_issues)
            self.threat_intelligence.extend(threats)
            self.security_reports.append(report)
            
            logger.info(f"✅ Security scan completed: {len(vulnerabilities)} vulnerabilities, {len(compliance_issues)} compliance issues, {len(threats)} threats")
            
            return report
            
        except Exception as e:
            logger.error(f"Security scan failed: {e}")
            raise
    
    async def _scan_vulnerabilities(self, resources: List[Dict[str, Any]]) -> List[SecurityVulnerability]:
        """Scan resources for vulnerabilities"""
        try:
            vulnerabilities = []
            
            for resource in resources:
                # Perform pattern-based vulnerability detection
                pattern_vulnerabilities = self._detect_pattern_vulnerabilities(resource)
                vulnerabilities.extend(pattern_vulnerabilities)
                
                # Perform AI-powered vulnerability analysis
                ai_vulnerabilities = await self._ai_vulnerability_analysis(resource)
                vulnerabilities.extend(ai_vulnerabilities)
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Vulnerability scanning failed: {e}")
            return []
    
    def _detect_pattern_vulnerabilities(self, resource: Dict[str, Any]) -> List[SecurityVulnerability]:
        """Detect vulnerabilities using pattern matching"""
        try:
            vulnerabilities = []
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Convert resource to string for pattern matching
            resource_str = json.dumps(resource, default=str).lower()
            
            for vuln_type, patterns in self.vulnerability_patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, resource_str, re.IGNORECASE)
                    if matches:
                        vulnerability = SecurityVulnerability(
                            vulnerability_id=f"{vuln_type}_{resource_id}_{len(vulnerabilities)}",
                            title=f"{vuln_type.replace('_', ' ').title()} Vulnerability",
                            description=f"Potential {vuln_type} vulnerability detected in {resource_type} resource",
                            severity=self._determine_severity(vuln_type),
                            cvss_score=self._calculate_cvss_score(vuln_type),
                            affected_resources=[resource_id],
                            remediation_steps=self._get_remediation_steps(vuln_type),
                            references=self._get_vulnerability_references(vuln_type),
                            discovered_at=datetime.now(timezone.utc),
                            ai_confidence=0.7,
                            false_positive_risk=0.3
                        )
                        vulnerabilities.append(vulnerability)
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Pattern vulnerability detection failed: {e}")
            return []
    
    async def _ai_vulnerability_analysis(self, resource: Dict[str, Any]) -> List[SecurityVulnerability]:
        """Perform AI-powered vulnerability analysis"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Create AI prompt for vulnerability analysis
            prompt = f"""
            Analyze this {resource_type} resource for security vulnerabilities:
            
            Resource Details: {json.dumps(resource, indent=2)}
            
            Identify potential security vulnerabilities including:
            1. Configuration vulnerabilities
            2. Access control issues
            3. Data exposure risks
            4. Network security issues
            5. Application security vulnerabilities
            
            For each vulnerability found, provide:
            - Vulnerability title and description
            - Severity level (critical, high, medium, low)
            - CVSS score estimate
            - Remediation steps
            - References
            
            Focus on real-world security risks and provide actionable recommendations.
            """
            
            # Get AI analysis
            ai_response = await ensemble_ai.generate_ensemble_response(
                prompt=prompt,
                analysis_type=AnalysisType.SECURITY_ASSESSMENT,
                consensus_method=ConsensusMethod.EXPERT_VOTE
            )
            
            # Parse AI response for vulnerabilities
            vulnerabilities = self._parse_ai_vulnerabilities(
                ai_response.final_response, resource_id, resource_type, ai_response.confidence_score
            )
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"AI vulnerability analysis failed: {e}")
            return []
    
    def _parse_ai_vulnerabilities(
        self,
        ai_response: str,
        resource_id: str,
        resource_type: str,
        confidence_score: float
    ) -> List[SecurityVulnerability]:
        """Parse AI response for vulnerabilities"""
        try:
            vulnerabilities = []
            
            # Mock parsing - create vulnerability based on AI response
            if "vulnerability" in ai_response.lower() or "security" in ai_response.lower():
                vulnerability = SecurityVulnerability(
                    vulnerability_id=f"ai_{resource_id}_{len(vulnerabilities)}",
                    title="AI-Detected Security Vulnerability",
                    description=f"AI analysis identified potential security issues in {resource_type} resource: {ai_response[:200]}...",
                    severity=SecuritySeverity.MEDIUM,
                    cvss_score=5.5,
                    affected_resources=[resource_id],
                    remediation_steps=[
                        "Review resource configuration",
                        "Implement security best practices",
                        "Conduct security assessment"
                    ],
                    references=["AI Security Analysis"],
                    discovered_at=datetime.now(timezone.utc),
                    ai_confidence=confidence_score,
                    false_positive_risk=0.2
                )
                vulnerabilities.append(vulnerability)
            
            return vulnerabilities
            
        except Exception as e:
            logger.error(f"Failed to parse AI vulnerabilities: {e}")
            return []
    
    async def _check_compliance(self, resources: List[Dict[str, Any]]) -> List[ComplianceCheck]:
        """Check compliance against various frameworks"""
        try:
            compliance_issues = []
            
            # Check against AWS CIS framework
            framework_issues = await self._check_framework_compliance(resources, ComplianceFramework.AWS_CIS)
            compliance_issues.extend(framework_issues)
            
            return compliance_issues
            
        except Exception as e:
            logger.error(f"Compliance checking failed: {e}")
            return []
    
    async def _check_framework_compliance(
        self,
        resources: List[Dict[str, Any]],
        framework: ComplianceFramework
    ) -> List[ComplianceCheck]:
        """Check compliance against specific framework"""
        try:
            compliance_issues = []
            controls = self.compliance_controls.get(framework, {})
            
            for control_id, control_name in controls.items():
                # Create AI prompt for compliance checking
                prompt = f"""
                Check compliance for {framework.value.upper()} control {control_id}: {control_name}
                
                Resources to check: {json.dumps(resources, indent=2)}
                
                Determine if the resources comply with this control. Consider:
                1. Control requirements and objectives
                2. Current resource configuration
                3. Security best practices
                4. Industry standards
                
                Provide:
                - Compliance status (compliant/non_compliant/partial/not_applicable)
                - Description of findings
                - Evidence supporting the assessment
                - Remediation steps if non-compliant
                - Risk level assessment
                """
                
                # Get AI compliance assessment
                ai_response = await ensemble_ai.generate_ensemble_response(
                    prompt=prompt,
                    analysis_type=AnalysisType.COMPLIANCE_AUDIT,
                    consensus_method=ConsensusMethod.EXPERT_VOTE
                )
                
                # Parse compliance result
                compliance_check = self._parse_compliance_result(
                    ai_response, framework, control_id, control_name, ai_response.confidence_score
                )
                
                if compliance_check:
                    compliance_issues.append(compliance_check)
            
            return compliance_issues
            
        except Exception as e:
            logger.error(f"Framework compliance checking failed: {e}")
            return []
    
    def _parse_compliance_result(
        self,
        ai_response: str,
        framework: ComplianceFramework,
        control_id: str,
        control_name: str,
        confidence_score: float
    ) -> Optional[ComplianceCheck]:
        """Parse AI compliance assessment result"""
        try:
            # Mock parsing - determine compliance status from AI response
            response_lower = ai_response.lower()
            
            if "compliant" in response_lower:
                status = "compliant"
            elif "non_compliant" in response_lower or "violation" in response_lower:
                status = "non_compliant"
            elif "partial" in response_lower:
                status = "partial"
            else:
                status = "not_applicable"
            
            # Only create check if there are issues
            if status in ["non_compliant", "partial"]:
                compliance_check = ComplianceCheck(
                    check_id=f"{framework.value}_{control_id}_{uuid.uuid4().hex[:8]}",
                    framework=framework,
                    control_id=control_id,
                    control_name=control_name,
                    status=status,
                    description=f"AI assessment for {control_name}: {ai_response[:200]}...",
                    evidence=[f"AI analysis: {ai_response[:100]}..."],
                    remediation_required=status == "non_compliant",
                    remediation_steps=[
                        "Review control requirements",
                        "Implement missing controls",
                        "Document compliance evidence"
                    ],
                    risk_level="medium" if status == "partial" else "high",
                    last_checked=datetime.now(timezone.utc),
                    ai_confidence=confidence_score
                )
                return compliance_check
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to parse compliance result: {e}")
            return None
    
    async def _analyze_threat_intelligence(self, resources: List[Dict[str, Any]]) -> List[ThreatIntelligence]:
        """Analyze threat intelligence for resources"""
        try:
            threats = []
            
            for resource in resources:
                # Perform AI-powered threat analysis
                ai_threats = await self._ai_threat_analysis(resource)
                threats.extend(ai_threats)
            
            return threats
            
        except Exception as e:
            logger.error(f"Threat intelligence analysis failed: {e}")
            return []
    
    async def _ai_threat_analysis(self, resource: Dict[str, Any]) -> List[ThreatIntelligence]:
        """Perform AI-powered threat analysis"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Create AI prompt for threat analysis
            prompt = f"""
            Analyze this {resource_type} resource for potential security threats:
            
            Resource Details: {json.dumps(resource, indent=2)}
            
            Identify potential security threats including:
            1. Malware and malicious activities
            2. Phishing and social engineering
            3. DDoS and network attacks
            4. Data breaches and unauthorized access
            5. Insider threats
            6. Configuration-based threats
            
            For each threat identified, provide:
            - Threat type and description
            - Indicators of compromise
            - Severity assessment
            - Mitigation strategies
            - Potential threat actors
            
            Focus on realistic threats and provide actionable intelligence.
            """
            
            # Get AI analysis
            ai_response = await ensemble_ai.generate_ensemble_response(
                prompt=prompt,
                analysis_type=AnalysisType.SECURITY_ASSESSMENT,
                consensus_method=ConsensusMethod.EXPERT_VOTE
            )
            
            # Parse AI response for threats
            threats = self._parse_ai_threats(
                ai_response.final_response, resource_id, resource_type, ai_response.confidence_score
            )
            
            return threats
            
        except Exception as e:
            logger.error(f"AI threat analysis failed: {e}")
            return []
    
    def _parse_ai_threats(
        self,
        ai_response: str,
        resource_id: str,
        resource_type: str,
        confidence_score: float
    ) -> List[ThreatIntelligence]:
        """Parse AI response for threats"""
        try:
            threats = []
            
            # Mock parsing - create threat based on AI response
            if "threat" in ai_response.lower() or "attack" in ai_response.lower():
                threat = ThreatIntelligence(
                    threat_id=f"ai_threat_{resource_id}_{len(threats)}",
                    threat_type=ThreatType.CONFIGURATION_ERROR,
                    title="AI-Detected Security Threat",
                    description=f"AI analysis identified potential security threats in {resource_type} resource: {ai_response[:200]}...",
                    indicators=["AI analysis", "Security assessment"],
                    severity=SecuritySeverity.MEDIUM,
                    affected_resources=[resource_id],
                    mitigation_strategies=[
                        "Implement security controls",
                        "Monitor for suspicious activity",
                        "Update security policies"
                    ],
                    threat_actors=["Unknown"],
                    confidence_score=confidence_score,
                    source="AI Threat Analysis",
                    discovered_at=datetime.now(timezone.utc)
                )
                threats.append(threat)
            
            return threats
            
        except Exception as e:
            logger.error(f"Failed to parse AI threats: {e}")
            return []
    
    def _calculate_security_score(
        self,
        vulnerabilities: List[SecurityVulnerability],
        compliance_issues: List[ComplianceCheck],
        threats: List[ThreatIntelligence]
    ) -> float:
        """Calculate overall security score"""
        try:
            # Base score starts at 100
            score = 100.0
            
            # Deduct points for vulnerabilities
            for vuln in vulnerabilities:
                if vuln.severity == SecuritySeverity.CRITICAL:
                    score -= 20
                elif vuln.severity == SecuritySeverity.HIGH:
                    score -= 15
                elif vuln.severity == SecuritySeverity.MEDIUM:
                    score -= 10
                elif vuln.severity == SecuritySeverity.LOW:
                    score -= 5
            
            # Deduct points for compliance issues
            for issue in compliance_issues:
                if issue.status == "non_compliant":
                    score -= 10
                elif issue.status == "partial":
                    score -= 5
            
            # Deduct points for threats
            for threat in threats:
                if threat.severity == SecuritySeverity.CRITICAL:
                    score -= 15
                elif threat.severity == SecuritySeverity.HIGH:
                    score -= 10
                elif threat.severity == SecuritySeverity.MEDIUM:
                    score -= 5
            
            # Ensure score doesn't go below 0
            return max(0.0, score)
            
        except Exception as e:
            logger.error(f"Failed to calculate security score: {e}")
            return 50.0
    
    async def _generate_security_recommendations(
        self,
        vulnerabilities: List[SecurityVulnerability],
        compliance_issues: List[ComplianceCheck],
        threats: List[ThreatIntelligence]
    ) -> List[str]:
        """Generate security recommendations"""
        try:
            recommendations = []
            
            # Add vulnerability-based recommendations
            if vulnerabilities:
                recommendations.append(f"Address {len(vulnerabilities)} identified vulnerabilities")
                recommendations.append("Implement vulnerability management program")
                recommendations.append("Conduct regular security assessments")
            
            # Add compliance-based recommendations
            if compliance_issues:
                recommendations.append(f"Resolve {len(compliance_issues)} compliance issues")
                recommendations.append("Implement compliance monitoring")
                recommendations.append("Establish compliance reporting")
            
            # Add threat-based recommendations
            if threats:
                recommendations.append(f"Mitigate {len(threats)} identified threats")
                recommendations.append("Implement threat detection and response")
                recommendations.append("Establish security monitoring")
            
            # Add general recommendations
            recommendations.extend([
                "Implement security awareness training",
                "Establish incident response procedures",
                "Conduct regular security audits",
                "Implement multi-factor authentication",
                "Establish data backup and recovery procedures"
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return ["Conduct comprehensive security review"]
    
    async def _generate_executive_summary(
        self,
        vulnerabilities: List[SecurityVulnerability],
        compliance_issues: List[ComplianceCheck],
        threats: List[ThreatIntelligence],
        security_score: float
    ) -> str:
        """Generate executive summary"""
        try:
            summary = f"""
            Security Assessment Executive Summary
            
            Overall Security Score: {security_score:.1f}/100
            
            Key Findings:
            - Vulnerabilities Found: {len(vulnerabilities)}
            - Compliance Issues: {len(compliance_issues)}
            - Threats Detected: {len(threats)}
            
            Critical Issues: {len([v for v in vulnerabilities if v.severity == SecuritySeverity.CRITICAL])}
            High Priority Issues: {len([v for v in vulnerabilities if v.severity == SecuritySeverity.HIGH])}
            
            Recommendations:
            - Immediate action required for critical vulnerabilities
            - Address compliance gaps to meet regulatory requirements
            - Implement threat detection and response capabilities
            - Establish ongoing security monitoring and assessment program
            
            Next Steps:
            1. Prioritize and remediate critical vulnerabilities
            2. Address compliance issues within 30 days
            3. Implement recommended security controls
            4. Establish regular security review schedule
            """
            
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate executive summary: {e}")
            return "Security assessment completed. Review findings and implement recommendations."
    
    def _determine_severity(self, vuln_type: str) -> SecuritySeverity:
        """Determine vulnerability severity"""
        severity_mapping = {
            'sql_injection': SecuritySeverity.CRITICAL,
            'xss': SecuritySeverity.HIGH,
            'path_traversal': SecuritySeverity.HIGH
        }
        return severity_mapping.get(vuln_type, SecuritySeverity.MEDIUM)
    
    def _calculate_cvss_score(self, vuln_type: str) -> float:
        """Calculate CVSS score for vulnerability"""
        cvss_mapping = {
            'sql_injection': 9.8,
            'xss': 6.1,
            'path_traversal': 7.5
        }
        return cvss_mapping.get(vuln_type, 5.0)
    
    def _get_remediation_steps(self, vuln_type: str) -> List[str]:
        """Get remediation steps for vulnerability"""
        remediation_mapping = {
            'sql_injection': [
                "Use parameterized queries",
                "Implement input validation",
                "Use ORM frameworks",
                "Apply principle of least privilege"
            ],
            'xss': [
                "Implement output encoding",
                "Use Content Security Policy",
                "Validate and sanitize input",
                "Use secure frameworks"
            ],
            'path_traversal': [
                "Validate file paths",
                "Use whitelist approach",
                "Implement proper access controls",
                "Use secure file handling"
            ]
        }
        return remediation_mapping.get(vuln_type, ["Review and fix security issue"])
    
    def _get_vulnerability_references(self, vuln_type: str) -> List[str]:
        """Get references for vulnerability"""
        return [
            f"OWASP Top 10 - {vuln_type.replace('_', ' ').title()}",
            "CWE Database",
            "NIST Cybersecurity Framework"
        ]
    
    def _vulnerability_to_dict(self, vuln: SecurityVulnerability) -> Dict[str, Any]:
        """Convert vulnerability to dictionary"""
        return {
            "id": vuln.vulnerability_id,
            "title": vuln.title,
            "description": vuln.description,
            "severity": vuln.severity.value,
            "cvss_score": vuln.cvss_score,
            "affected_resources": vuln.affected_resources,
            "remediation_steps": vuln.remediation_steps,
            "ai_confidence": vuln.ai_confidence,
            "discovered_at": vuln.discovered_at.isoformat()
        }
    
    def _compliance_to_dict(self, check: ComplianceCheck) -> Dict[str, Any]:
        """Convert compliance check to dictionary"""
        return {
            "id": check.check_id,
            "framework": check.framework.value,
            "control_id": check.control_id,
            "control_name": check.control_name,
            "status": check.status,
            "description": check.description,
            "remediation_required": check.remediation_required,
            "risk_level": check.risk_level,
            "ai_confidence": check.ai_confidence,
            "last_checked": check.last_checked.isoformat()
        }
    
    def _threat_to_dict(self, threat: ThreatIntelligence) -> Dict[str, Any]:
        """Convert threat to dictionary"""
        return {
            "id": threat.threat_id,
            "type": threat.threat_type.value,
            "title": threat.title,
            "description": threat.description,
            "severity": threat.severity.value,
            "indicators": threat.indicators,
            "confidence_score": threat.confidence_score,
            "source": threat.source,
            "discovered_at": threat.discovered_at.isoformat()
        }
    
    async def get_security_summary(self) -> Dict[str, Any]:
        """Get security scanning summary"""
        try:
            total_vulnerabilities = len(self.vulnerabilities)
            total_compliance_issues = len(self.compliance_checks)
            total_threats = len(self.threat_intelligence)
            total_reports = len(self.security_reports)
            
            # Calculate statistics
            critical_vulns = len([v for v in self.vulnerabilities if v.severity == SecuritySeverity.CRITICAL])
            high_vulns = len([v for v in self.vulnerabilities if v.severity == SecuritySeverity.HIGH])
            
            non_compliant = len([c for c in self.compliance_checks if c.status == "non_compliant"])
            
            return {
                "total_vulnerabilities": total_vulnerabilities,
                "critical_vulnerabilities": critical_vulns,
                "high_vulnerabilities": high_vulns,
                "total_compliance_issues": total_compliance_issues,
                "non_compliant_issues": non_compliant,
                "total_threats": total_threats,
                "total_reports": total_reports,
                "average_security_score": sum(r.overall_security_score for r in self.security_reports) / max(len(self.security_reports), 1),
                "recent_reports": [
                    {
                        "report_id": r.report_id,
                        "scan_type": r.scan_type,
                        "security_score": r.overall_security_score,
                        "vulnerabilities": r.vulnerabilities_found,
                        "compliance_issues": r.compliance_issues,
                        "threats": r.threats_detected,
                        "generated_at": r.generated_at.isoformat()
                    }
                    for r in sorted(self.security_reports, key=lambda x: x.generated_at, reverse=True)[:5]
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get security summary: {e}")
            return {}


# Global AI security scanner instance
ai_security_scanner = AISecurityScanner()
