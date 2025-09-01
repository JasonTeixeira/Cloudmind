"""
GraphQL Implementation for CloudMind
World-class GraphQL API with advanced features
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timedelta

import strawberry
from strawberry.types import Info
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.core.database import get_db
from app.models.user import User, UserRole, UserStatus
from app.models.project import Project
from app.models.cost_analysis import CostAnalysis, CostRecommendation
from app.models.security_scan import SecurityScan, Vulnerability
from app.models.infrastructure import Infrastructure, Resource
from app.models.ai_insight import AIInsight, InsightType, InsightPriority
from app.services.auth_service import AuthService
from app.services.cost_optimization import CostOptimizationService
from app.services.security_audit import SecurityAuditService
from app.services.ai_engine import AIEngineService

logger = logging.getLogger(__name__)


@strawberry.type
class UserType:
    """User GraphQL type"""
    id: str
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    status: str
    avatar_url: Optional[str]
    company: Optional[str]
    job_title: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]


@strawberry.type
class ProjectType:
    """Project GraphQL type"""
    id: str
    name: str
    description: Optional[str]
    status: str
    owner_id: str
    cloud_providers: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    cost_summary: Optional[Dict[str, Any]]
    security_score: Optional[int]


@strawberry.type
class CostAnalysisType:
    """Cost Analysis GraphQL type"""
    id: str
    project_id: str
    user_id: str
    total_cost: float
    cost_breakdown: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    created_at: datetime
    period_start: datetime
    period_end: datetime


@strawberry.type
class SecurityScanType:
    """Security Scan GraphQL type"""
    id: str
    project_id: str
    user_id: str
    scan_type: str
    status: str
    vulnerabilities_count: int
    risk_score: float
    created_at: datetime
    completed_at: Optional[datetime]


@strawberry.type
class VulnerabilityType:
    """Vulnerability GraphQL type"""
    id: str
    security_scan_id: str
    title: str
    description: str
    severity: str
    category: str
    cvss_score: float
    status: str
    remediation_steps: List[str]
    created_at: datetime


@strawberry.type
class InfrastructureType:
    """Infrastructure GraphQL type"""
    id: str
    project_id: str
    name: str
    description: Optional[str]
    cloud_provider: str
    region: str
    environment: str
    health_status: str
    resources_count: int
    total_cost: float
    created_at: datetime
    updated_at: datetime


@strawberry.type
class ResourceType:
    """Resource GraphQL type"""
    id: str
    infrastructure_id: str
    name: str
    resource_type: str
    status: str
    cost: float
    utilization: float
    region: str
    tags: List[str]
    created_at: datetime


@strawberry.type
class AIInsightType:
    """AI Insight GraphQL type"""
    id: str
    user_id: str
    project_id: Optional[str]
    insight_type: str
    title: str
    description: str
    priority: str
    confidence_score: float
    recommendations: List[str]
    created_at: datetime


@strawberry.type
class DashboardMetricsType:
    """Dashboard Metrics GraphQL type"""
    total_projects: int
    active_projects: int
    total_cost: float
    cost_savings: float
    security_score: float
    vulnerabilities_count: int
    ai_insights_count: int
    recent_activities: List[Dict[str, Any]]


@strawberry.type
class CostOptimizationType:
    """Cost Optimization GraphQL type"""
    potential_savings: float
    recommendations: List[Dict[str, Any]]
    implementation_priority: List[str]
    roi_analysis: Dict[str, Any]
    risk_assessment: Dict[str, Any]


@strawberry.type
class SecurityPostureType:
    """Security Posture GraphQL type"""
    overall_score: float
    compliance_status: Dict[str, Any]
    risk_level: str
    vulnerabilities_by_severity: Dict[str, int]
    remediation_priority: List[str]
    threat_intelligence: Dict[str, Any]


@strawberry.input
class UserInput:
    """User input for mutations"""
    email: str
    username: str
    full_name: str
    password: str
    role: Optional[str] = "viewer"
    company: Optional[str] = None
    job_title: Optional[str] = None


@strawberry.input
class ProjectInput:
    """Project input for mutations"""
    name: str
    description: Optional[str] = None
    cloud_providers: List[str]
    tags: Optional[List[str]] = None


@strawberry.input
class CostAnalysisInput:
    """Cost Analysis input for mutations"""
    project_id: str
    period_start: datetime
    period_end: datetime
    include_recommendations: bool = True


@strawberry.input
class SecurityScanInput:
    """Security Scan input for mutations"""
    project_id: str
    scan_type: str = "comprehensive"
    include_vulnerabilities: bool = True


@strawberry.type
class Query:
    """GraphQL Query type"""
    
    @strawberry.field
    async def users(self, info: Info, limit: int = 100, offset: int = 0) -> List[UserType]:
        """Get all users with pagination"""
        db: Session = info.context["db"]
        users = db.query(User).offset(offset).limit(limit).all()
        return [UserType(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
            status=user.status.value,
            avatar_url=user.avatar_url,
            company=user.company,
            job_title=user.job_title,
            created_at=user.created_at,
            last_login=user.last_login
        ) for user in users]
    
    @strawberry.field
    async def user(self, info: Info, user_id: str) -> Optional[UserType]:
        """Get user by ID"""
        db: Session = info.context["db"]
        user = db.query(User).filter(User.id == UUID(user_id)).first()
        if not user:
            return None
        
        return UserType(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
            status=user.status.value,
            avatar_url=user.avatar_url,
            company=user.company,
            job_title=user.job_title,
            created_at=user.created_at,
            last_login=user.last_login
        )
    
    @strawberry.field
    async def projects(self, info: Info, limit: int = 100, offset: int = 0) -> List[ProjectType]:
        """Get all projects with pagination"""
        db: Session = info.context["db"]
        projects = db.query(Project).offset(offset).limit(limit).all()
        return [ProjectType(
            id=str(project.id),
            name=project.name,
            description=project.description,
            status=project.status.value,
            owner_id=str(project.owner_id),
            cloud_providers=project.cloud_providers,
            tags=project.tags or [],
            created_at=project.created_at,
            updated_at=project.updated_at,
            cost_summary=project.cost_summary,
            security_score=project.security_score
        ) for project in projects]
    
    @strawberry.field
    async def project(self, info: Info, project_id: str) -> Optional[ProjectType]:
        """Get project by ID"""
        db: Session = info.context["db"]
        project = db.query(Project).filter(Project.id == UUID(project_id)).first()
        if not project:
            return None
        
        return ProjectType(
            id=str(project.id),
            name=project.name,
            description=project.description,
            status=project.status.value,
            owner_id=str(project.owner_id),
            cloud_providers=project.cloud_providers,
            tags=project.tags or [],
            created_at=project.created_at,
            updated_at=project.updated_at,
            cost_summary=project.cost_summary,
            security_score=project.security_score
        )
    
    @strawberry.field
    async def cost_analyses(self, info: Info, project_id: Optional[str] = None, limit: int = 100) -> List[CostAnalysisType]:
        """Get cost analyses with optional project filter"""
        db: Session = info.context["db"]
        query = db.query(CostAnalysis)
        
        if project_id:
            query = query.filter(CostAnalysis.project_id == UUID(project_id))
        
        analyses = query.limit(limit).all()
        return [CostAnalysisType(
            id=str(analysis.id),
            project_id=str(analysis.project_id),
            user_id=str(analysis.user_id),
            total_cost=analysis.total_cost,
            cost_breakdown=analysis.cost_breakdown,
            recommendations=analysis.recommendations,
            created_at=analysis.created_at,
            period_start=analysis.period_start,
            period_end=analysis.period_end
        ) for analysis in analyses]
    
    @strawberry.field
    async def security_scans(self, info: Info, project_id: Optional[str] = None, limit: int = 100) -> List[SecurityScanType]:
        """Get security scans with optional project filter"""
        db: Session = info.context["db"]
        query = db.query(SecurityScan)
        
        if project_id:
            query = query.filter(SecurityScan.project_id == UUID(project_id))
        
        scans = query.limit(limit).all()
        return [SecurityScanType(
            id=str(scan.id),
            project_id=str(scan.project_id),
            user_id=str(scan.user_id),
            scan_type=scan.scan_type,
            status=scan.status.value,
            vulnerabilities_count=scan.vulnerabilities_count,
            risk_score=scan.risk_score,
            created_at=scan.created_at,
            completed_at=scan.completed_at
        ) for scan in scans]
    
    @strawberry.field
    async def vulnerabilities(self, info: Info, scan_id: Optional[str] = None, severity: Optional[str] = None) -> List[VulnerabilityType]:
        """Get vulnerabilities with optional filters"""
        db: Session = info.context["db"]
        query = db.query(Vulnerability)
        
        if scan_id:
            query = query.filter(Vulnerability.security_scan_id == UUID(scan_id))
        
        if severity:
            query = query.filter(Vulnerability.severity == severity)
        
        vulnerabilities = query.all()
        return [VulnerabilityType(
            id=str(vuln.id),
            security_scan_id=str(vuln.security_scan_id),
            title=vuln.title,
            description=vuln.description,
            severity=vuln.severity,
            category=vuln.category,
            cvss_score=vuln.cvss_score,
            status=vuln.status.value,
            remediation_steps=vuln.remediation_steps,
            created_at=vuln.created_at
        ) for vuln in vulnerabilities]
    
    @strawberry.field
    async def infrastructure(self, info: Info, project_id: Optional[str] = None) -> List[InfrastructureType]:
        """Get infrastructure with optional project filter"""
        db: Session = info.context["db"]
        query = db.query(Infrastructure)
        
        if project_id:
            query = query.filter(Infrastructure.project_id == UUID(project_id))
        
        infrastructures = query.all()
        return [InfrastructureType(
            id=str(infra.id),
            project_id=str(infra.project_id),
            name=infra.name,
            description=infra.description,
            cloud_provider=infra.cloud_provider,
            region=infra.region,
            environment=infra.environment,
            health_status=infra.health_status,
            resources_count=infra.resources_count,
            total_cost=infra.total_cost,
            created_at=infra.created_at,
            updated_at=infra.updated_at
        ) for infra in infrastructures]
    
    @strawberry.field
    async def resources(self, info: Info, infrastructure_id: Optional[str] = None) -> List[ResourceType]:
        """Get resources with optional infrastructure filter"""
        db: Session = info.context["db"]
        query = db.query(Resource)
        
        if infrastructure_id:
            query = query.filter(Resource.infrastructure_id == UUID(infrastructure_id))
        
        resources = query.all()
        return [ResourceType(
            id=str(resource.id),
            infrastructure_id=str(resource.infrastructure_id),
            name=resource.name,
            resource_type=resource.resource_type,
            status=resource.status,
            cost=resource.cost,
            utilization=resource.utilization,
            region=resource.region,
            tags=resource.tags or [],
            created_at=resource.created_at
        ) for resource in resources]
    
    @strawberry.field
    async def ai_insights(self, info: Info, user_id: Optional[str] = None, project_id: Optional[str] = None, limit: int = 100) -> List[AIInsightType]:
        """Get AI insights with optional filters"""
        db: Session = info.context["db"]
        query = db.query(AIInsight)
        
        if user_id:
            query = query.filter(AIInsight.user_id == UUID(user_id))
        
        if project_id:
            query = query.filter(AIInsight.project_id == UUID(project_id))
        
        insights = query.limit(limit).all()
        return [AIInsightType(
            id=str(insight.id),
            user_id=str(insight.user_id),
            project_id=str(insight.project_id) if insight.project_id else None,
            insight_type=insight.insight_type.value,
            title=insight.title,
            description=insight.description,
            priority=insight.priority.value,
            confidence_score=insight.confidence_score,
            recommendations=insight.recommendations,
            created_at=insight.created_at
        ) for insight in insights]
    
    @strawberry.field
    async def dashboard_metrics(self, info: Info) -> DashboardMetricsType:
        """Get comprehensive dashboard metrics"""
        db: Session = info.context["db"]
        
        # Get basic counts
        total_projects = db.query(Project).count()
        active_projects = db.query(Project).filter(Project.status == "active").count()
        
        # Get cost metrics
        total_cost = db.query(func.sum(CostAnalysis.total_cost)).scalar() or 0
        
        # Get security metrics
        security_score = db.query(func.avg(SecurityScan.risk_score)).scalar() or 0
        vulnerabilities_count = db.query(Vulnerability).count()
        
        # Get AI insights count
        ai_insights_count = db.query(AIInsight).count()
        
        # Get recent activities (simplified)
        recent_activities = []
        
        return DashboardMetricsType(
            total_projects=total_projects,
            active_projects=active_projects,
            total_cost=float(total_cost),
            cost_savings=0.0,  # Would be calculated from optimization data
            security_score=float(security_score),
            vulnerabilities_count=vulnerabilities_count,
            ai_insights_count=ai_insights_count,
            recent_activities=recent_activities
        )
    
    @strawberry.field
    async def cost_optimization(self, info: Info, project_id: str) -> CostOptimizationType:
        """Get cost optimization analysis for a project"""
        db: Session = info.context["db"]
        
        # This would integrate with the CostOptimizationService
        cost_service = CostOptimizationService(db)
        optimization_data = await cost_service.analyze_project_optimization(UUID(project_id))
        
        return CostOptimizationType(
            potential_savings=optimization_data.get("potential_savings", 0.0),
            recommendations=optimization_data.get("recommendations", []),
            implementation_priority=optimization_data.get("implementation_priority", []),
            roi_analysis=optimization_data.get("roi_analysis", {}),
            risk_assessment=optimization_data.get("risk_assessment", {})
        )
    
    @strawberry.field
    async def security_posture(self, info: Info, project_id: str) -> SecurityPostureType:
        """Get security posture analysis for a project"""
        db: Session = info.context["db"]
        
        # This would integrate with the SecurityAuditService
        security_service = SecurityAuditService(db)
        posture_data = await security_service.analyze_project_security_posture(UUID(project_id))
        
        return SecurityPostureType(
            overall_score=posture_data.get("overall_score", 0.0),
            compliance_status=posture_data.get("compliance_status", {}),
            risk_level=posture_data.get("risk_level", "unknown"),
            vulnerabilities_by_severity=posture_data.get("vulnerabilities_by_severity", {}),
            remediation_priority=posture_data.get("remediation_priority", []),
            threat_intelligence=posture_data.get("threat_intelligence", {})
        )


@strawberry.type
class Mutation:
    """GraphQL Mutation type"""
    
    @strawberry.mutation
    async def create_user(self, info: Info, user_input: UserInput) -> UserType:
        """Create a new user"""
        db: Session = info.context["db"]
        auth_service = AuthService(db)
        
        # Create user logic would go here
        # This is a simplified version
        user = User(
            email=user_input.email,
            username=user_input.username,
            full_name=user_input.full_name,
            hashed_password=auth_service.get_password_hash(user_input.password),
            role=UserRole(user_input.role or "viewer"),
            company=user_input.company,
            job_title=user_input.job_title
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserType(
            id=str(user.id),
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
            status=user.status.value,
            avatar_url=user.avatar_url,
            company=user.company,
            job_title=user.job_title,
            created_at=user.created_at,
            last_login=user.last_login
        )
    
    @strawberry.mutation
    async def create_project(self, info: Info, project_input: ProjectInput, user_id: str) -> ProjectType:
        """Create a new project"""
        db: Session = info.context["db"]
        
        project = Project(
            name=project_input.name,
            description=project_input.description,
            owner_id=UUID(user_id),
            cloud_providers=project_input.cloud_providers,
            tags=project_input.tags or []
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        return ProjectType(
            id=str(project.id),
            name=project.name,
            description=project.description,
            status=project.status.value,
            owner_id=str(project.owner_id),
            cloud_providers=project.cloud_providers,
            tags=project.tags or [],
            created_at=project.created_at,
            updated_at=project.updated_at,
            cost_summary=project.cost_summary,
            security_score=project.security_score
        )
    
    @strawberry.mutation
    async def run_cost_analysis(self, info: Info, analysis_input: CostAnalysisInput) -> CostAnalysisType:
        """Run cost analysis for a project"""
        db: Session = info.context["db"]
        cost_service = CostOptimizationService(db)
        
        # Run cost analysis
        analysis_data = await cost_service.analyze_project_costs(
            UUID(analysis_input.project_id),
            analysis_input.period_start,
            analysis_input.period_end,
            include_recommendations=analysis_input.include_recommendations
        )
        
        # Create cost analysis record
        analysis = CostAnalysis(
            project_id=UUID(analysis_input.project_id),
            user_id=UUID("00000000-0000-0000-0000-000000000000"),  # Would be current user
            total_cost=analysis_data["total_cost"],
            cost_breakdown=analysis_data["cost_breakdown"],
            recommendations=analysis_data.get("recommendations", []),
            period_start=analysis_input.period_start,
            period_end=analysis_input.period_end
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return CostAnalysisType(
            id=str(analysis.id),
            project_id=str(analysis.project_id),
            user_id=str(analysis.user_id),
            total_cost=analysis.total_cost,
            cost_breakdown=analysis.cost_breakdown,
            recommendations=analysis.recommendations,
            created_at=analysis.created_at,
            period_start=analysis.period_start,
            period_end=analysis.period_end
        )
    
    @strawberry.mutation
    async def run_security_scan(self, info: Info, scan_input: SecurityScanInput) -> SecurityScanType:
        """Run security scan for a project"""
        db: Session = info.context["db"]
        security_service = SecurityAuditService(db)
        
        # Run security scan
        scan_data = await security_service.scan_project_security(
            UUID(scan_input.project_id),
            scan_type=scan_input.scan_type,
            include_vulnerabilities=scan_input.include_vulnerabilities
        )
        
        # Create security scan record
        scan = SecurityScan(
            project_id=UUID(scan_input.project_id),
            user_id=UUID("00000000-0000-0000-0000-000000000000"),  # Would be current user
            scan_type=scan_input.scan_type,
            status="completed",
            vulnerabilities_count=scan_data.get("vulnerabilities_count", 0),
            risk_score=scan_data.get("risk_score", 0.0),
            completed_at=datetime.utcnow()
        )
        
        db.add(scan)
        db.commit()
        db.refresh(scan)
        
        return SecurityScanType(
            id=str(scan.id),
            project_id=str(scan.project_id),
            user_id=str(scan.user_id),
            scan_type=scan.scan_type,
            status=scan.status.value,
            vulnerabilities_count=scan.vulnerabilities_count,
            risk_score=scan.risk_score,
            created_at=scan.created_at,
            completed_at=scan.completed_at
        )


# Create GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation) 