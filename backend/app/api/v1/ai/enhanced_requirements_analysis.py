"""
Enhanced Requirements Analysis API
Provides comprehensive requirements analysis with real-time knowledge integration
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging

from app.services.ai_engine.architecture_engine import AIArchitectureEngine
from app.services.ai_engine.enhanced_knowledge_engine import EnhancedKnowledgeEngine
from app.core.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()

class EnhancedRequirementsRequest(BaseModel):
    project_description: str
    business_goals: List[str]
    technical_constraints: List[str]
    team_size: int
    timeline: str
    budget: Optional[str] = None
    domain: Optional[str] = None
    scale: Optional[str] = "startup"
    security_level: Optional[str] = "standard"
    performance_requirements: Optional[str] = "moderate"
    compliance_frameworks: Optional[List[str]] = []

class EnhancedRequirementsResponse(BaseModel):
    requirements: List[Dict[str, Any]]
    architecture_recommendations: List[Dict[str, Any]]
    technology_recommendations: List[Dict[str, Any]]
    real_time_knowledge: Dict[str, List[Dict[str, Any]]]
    project_template: Optional[Dict[str, Any]] = None
    risk_assessment: Dict[str, Any]
    cost_estimation: Dict[str, Any]
    timeline: Dict[str, Any]
    success_metrics: Dict[str, Any]

@router.post("/enhanced-requirements-analysis", response_model=EnhancedRequirementsResponse)
async def analyze_enhanced_requirements(
    request: EnhancedRequirementsRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze project requirements with enhanced real-time knowledge integration
    """
    try:
        logger.info(f"Starting enhanced requirements analysis for user {current_user.id}")
        
        # Initialize enhanced architecture engine
        architecture_engine = AIArchitectureEngine()
        knowledge_engine = EnhancedKnowledgeEngine()
        
        # Step 1: Analyze requirements with AI
        requirements_analysis = await architecture_engine.analyze_requirements(
            project_description=request.project_description,
            business_goals=request.business_goals,
            technical_constraints=request.technical_constraints,
            team_size=request.team_size,
            timeline=request.timeline,
            budget=request.budget
        )
        
        # Step 2: Get real-time knowledge for enhanced recommendations
        real_time_knowledge = await knowledge_engine.get_comprehensive_knowledge({
            "project_description": request.project_description,
            "business_goals": request.business_goals,
            "technical_constraints": request.technical_constraints,
            "domain": request.domain,
            "scale": request.scale,
            "security_level": request.security_level,
            "performance_requirements": request.performance_requirements,
            "compliance_frameworks": request.compliance_frameworks
        })
        
        # Step 3: Generate enhanced architecture recommendations
        enhanced_architecture_recommendations = await _generate_enhanced_architecture_recommendations(
            requirements_analysis,
            real_time_knowledge,
            request
        )
        
        # Step 4: Generate enhanced technology recommendations
        enhanced_technology_recommendations = await _generate_enhanced_technology_recommendations(
            requirements_analysis,
            real_time_knowledge,
            request
        )
        
        # Step 5: Generate project template
        project_template = await _generate_project_template(
            enhanced_architecture_recommendations,
            enhanced_technology_recommendations,
            request
        )
        
        # Step 6: Generate comprehensive analysis
        risk_assessment = await _generate_risk_assessment(
            requirements_analysis,
            real_time_knowledge,
            request
        )
        
        cost_estimation = await _generate_cost_estimation(
            requirements_analysis,
            real_time_knowledge,
            request
        )
        
        timeline = await _generate_timeline(
            requirements_analysis,
            enhanced_architecture_recommendations,
            request
        )
        
        success_metrics = await _generate_success_metrics(
            requirements_analysis,
            request
        )
        
        return EnhancedRequirementsResponse(
            requirements=requirements_analysis.get("requirements", []),
            architecture_recommendations=enhanced_architecture_recommendations,
            technology_recommendations=enhanced_technology_recommendations,
            real_time_knowledge=real_time_knowledge,
            project_template=project_template,
            risk_assessment=risk_assessment,
            cost_estimation=cost_estimation,
            timeline=timeline,
            success_metrics=success_metrics
        )
        
    except Exception as e:
        logger.error(f"Enhanced requirements analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

async def _generate_enhanced_architecture_recommendations(
    requirements_analysis: Dict[str, Any],
    real_time_knowledge: Dict[str, List[Dict[str, Any]]],
    request: EnhancedRequirementsRequest
) -> List[Dict[str, Any]]:
    """Generate enhanced architecture recommendations with real-time knowledge"""
    try:
        base_recommendations = requirements_analysis.get("architecture_recommendations", [])
        enhanced_recommendations = []
        
        for recommendation in base_recommendations:
            enhanced_rec = recommendation.copy()
            
            # Add real-time insights
            enhanced_rec["real_time_insights"] = []
            
            # Add security insights from NVD/CVE data
            if "security_vulnerabilities" in real_time_knowledge:
                security_insights = []
                for entry in real_time_knowledge["security_vulnerabilities"]:
                    if entry.get("content", {}).get("severity") in ["HIGH", "CRITICAL"]:
                        security_insights.append({
                            "type": "security_vulnerability",
                            "title": entry.get("title", ""),
                            "severity": entry.get("content", {}).get("severity", ""),
                            "score": entry.get("content", {}).get("score", 0),
                            "source": entry.get("source", ""),
                            "recommendation": f"Consider security implications: {entry.get('title', '')}"
                        })
                enhanced_rec["real_time_insights"].extend(security_insights)
            
            # Add technology trend insights
            if "technology_trends" in real_time_knowledge:
                trend_insights = []
                for entry in real_time_knowledge["technology_trends"]:
                    trend_insights.append({
                        "type": "technology_trend",
                        "title": entry.get("title", ""),
                        "popularity": entry.get("content", {}).get("score", 0),
                        "source": entry.get("source", ""),
                        "recommendation": f"Consider trending technology: {entry.get('title', '')}"
                    })
                enhanced_rec["real_time_insights"].extend(trend_insights)
            
            # Add cloud cost insights
            if "cloud_services" in real_time_knowledge:
                cost_insights = []
                for entry in real_time_knowledge["cloud_services"]:
                    cost_insights.append({
                        "type": "cloud_cost",
                        "title": entry.get("title", ""),
                        "pricing": entry.get("content", {}).get("pricing", {}),
                        "source": entry.get("source", ""),
                        "recommendation": f"Consider cost implications for {entry.get('title', '')}"
                    })
                enhanced_rec["real_time_insights"].extend(cost_insights)
            
            enhanced_recommendations.append(enhanced_rec)
        
        return enhanced_recommendations
        
    except Exception as e:
        logger.error(f"Enhanced architecture recommendations failed: {e}")
        return []

async def _generate_enhanced_technology_recommendations(
    requirements_analysis: Dict[str, Any],
    real_time_knowledge: Dict[str, List[Dict[str, Any]]],
    request: EnhancedRequirementsRequest
) -> List[Dict[str, Any]]:
    """Generate enhanced technology recommendations with real-time knowledge"""
    try:
        base_recommendations = requirements_analysis.get("technology_recommendations", [])
        enhanced_recommendations = []
        
        for recommendation in base_recommendations:
            enhanced_rec = recommendation.copy()
            
            # Add real-time data
            enhanced_rec["real_time_data"] = []
            
            # Add security vulnerability data
            if "security_vulnerabilities" in real_time_knowledge:
                for entry in real_time_knowledge["security_vulnerabilities"]:
                    if recommendation["name"].lower() in entry.get("title", "").lower():
                        enhanced_rec["real_time_data"].append({
                            "type": "security_vulnerability",
                            "title": entry.get("title", ""),
                            "severity": entry.get("content", {}).get("severity", ""),
                            "score": entry.get("content", {}).get("score", 0),
                            "source": entry.get("source", ""),
                            "impact": "High security risk detected"
                        })
            
            # Add technology trend data
            if "technology_trends" in real_time_knowledge:
                for entry in real_time_knowledge["technology_trends"]:
                    if recommendation["name"].lower() in entry.get("title", "").lower():
                        enhanced_rec["real_time_data"].append({
                            "type": "technology_trend",
                            "title": entry.get("title", ""),
                            "popularity": entry.get("content", {}).get("score", 0),
                            "source": entry.get("source", ""),
                            "impact": "High community adoption"
                        })
            
            # Add performance benchmark data
            if "performance_benchmarks" in real_time_knowledge:
                for entry in real_time_knowledge["performance_benchmarks"]:
                    if recommendation["name"].lower() in entry.get("title", "").lower():
                        enhanced_rec["real_time_data"].append({
                            "type": "performance_benchmark",
                            "title": entry.get("title", ""),
                            "benchmark_data": entry.get("content", {}),
                            "source": entry.get("source", ""),
                            "impact": "Performance benchmark available"
                        })
            
            enhanced_recommendations.append(enhanced_rec)
        
        return enhanced_recommendations
        
    except Exception as e:
        logger.error(f"Enhanced technology recommendations failed: {e}")
        return []

async def _generate_project_template(
    architecture_recommendations: List[Dict[str, Any]],
    technology_recommendations: List[Dict[str, Any]],
    request: EnhancedRequirementsRequest
) -> Optional[Dict[str, Any]]:
    """Generate comprehensive project template"""
    try:
        if not architecture_recommendations:
            return None
        
        # Select the best architecture recommendation
        best_architecture = max(
            architecture_recommendations,
            key=lambda x: (x.get("scalability_score", 0) + x.get("security_score", 0)) / 2
        )
        
        # Build technology stack
        technology_stack = {}
        for tech_rec in technology_recommendations[:5]:  # Top 5 recommendations
            category = tech_rec.get("category", "other")
            if category not in technology_stack:
                technology_stack[category] = []
            technology_stack[category].append(tech_rec.get("name", ""))
        
        # Generate project structure
        project_structure = {
            "frontend": {
                "framework": technology_stack.get("framework", ["React"])[0],
                "styling": "Tailwind CSS",
                "state_management": "Zustand",
                "testing": "Jest + Testing Library"
            },
            "backend": {
                "framework": technology_stack.get("framework", ["FastAPI"])[0],
                "database": technology_stack.get("database", ["PostgreSQL"])[0],
                "cache": technology_stack.get("cache", ["Redis"])[0],
                "message_queue": technology_stack.get("message_queue", ["Celery"])[0]
            },
            "infrastructure": {
                "containerization": "Docker",
                "orchestration": "Kubernetes",
                "monitoring": "Prometheus + Grafana",
                "logging": "ELK Stack"
            },
            "security": {
                "authentication": "JWT + OAuth2",
                "authorization": "RBAC",
                "encryption": "AES-256",
                "vulnerability_scanning": "Snyk + Trivy"
            }
        }
        
        # Generate setup instructions
        setup_instructions = [
            "1. Clone the repository and navigate to the project directory",
            "2. Install dependencies: npm install && pip install -r requirements.txt",
            "3. Set up environment variables: cp .env.example .env",
            "4. Initialize database: python manage.py migrate",
            "5. Start development servers: npm run dev && python main.py",
            "6. Run tests: npm test && python -m pytest",
            "7. Build for production: npm run build && docker build -t app ."
        ]
        
        # Generate configuration files
        configuration_files = {
            "docker-compose.yml": """
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
  redis:
    image: redis:6-alpine
""",
            ".env.example": """
DATABASE_URL=postgresql://user:pass@localhost:5432/app
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
""",
            "requirements.txt": """
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
celery==5.3.4
pydantic==2.5.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.6
"""
        }
        
        return {
            "name": f"{request.domain or 'Project'} Template",
            "description": f"Generated template for {request.domain or 'project'} with {best_architecture.get('name', 'optimal')} architecture",
            "architecture_type": best_architecture.get("architecture_type", ""),
            "technology_stack": technology_stack,
            "project_structure": project_structure,
            "setup_instructions": setup_instructions,
            "configuration_files": configuration_files,
            "deployment_scripts": [
                "scripts/deploy.sh",
                "scripts/setup.sh",
                "scripts/migrate.sh"
            ],
            "testing_strategy": {
                "unit_tests": "90%+ coverage",
                "integration_tests": "API endpoint testing",
                "e2e_tests": "User workflow testing",
                "security_tests": "Vulnerability scanning"
            },
            "monitoring_setup": {
                "metrics": "Prometheus",
                "logging": "ELK Stack",
                "alerting": "Grafana Alerts",
                "tracing": "Jaeger"
            },
            "security_configuration": {
                "authentication": "JWT + OAuth2",
                "authorization": "RBAC",
                "encryption": "AES-256",
                "compliance": request.compliance_frameworks
            }
        }
        
    except Exception as e:
        logger.error(f"Project template generation failed: {e}")
        return None

async def _generate_risk_assessment(
    requirements_analysis: Dict[str, Any],
    real_time_knowledge: Dict[str, List[Dict[str, Any]]],
    request: EnhancedRequirementsRequest
) -> Dict[str, Any]:
    """Generate comprehensive risk assessment"""
    try:
        risks = []
        
        # Security risks from real-time vulnerability data
        if "security_vulnerabilities" in real_time_knowledge:
            high_severity_vulns = [
                entry for entry in real_time_knowledge["security_vulnerabilities"]
                if entry.get("content", {}).get("severity") in ["HIGH", "CRITICAL"]
            ]
            if high_severity_vulns:
                risks.append({
                    "category": "Security",
                    "risk": "High severity vulnerabilities detected",
                    "impact": "Critical",
                    "mitigation": "Implement security scanning and regular updates",
                    "source": "NVD/CVE Database"
                })
        
        # Technology risks from trends
        if "technology_trends" in real_time_knowledge:
            low_popularity_techs = [
                entry for entry in real_time_knowledge["technology_trends"]
                if entry.get("content", {}).get("score", 0) < 100
            ]
            if low_popularity_techs:
                risks.append({
                    "category": "Technology",
                    "risk": "Low community adoption",
                    "impact": "Medium",
                    "mitigation": "Consider more popular alternatives",
                    "source": "Stack Overflow/GitHub Trends"
                })
        
        # Compliance risks
        if request.compliance_frameworks:
            risks.append({
                "category": "Compliance",
                "risk": "Regulatory compliance requirements",
                "impact": "High",
                "mitigation": "Implement compliance monitoring and reporting",
                "source": "Compliance Frameworks"
            })
        
        # Performance risks
        if request.performance_requirements in ["high", "extreme"]:
            risks.append({
                "category": "Performance",
                "risk": "High performance requirements",
                "impact": "Medium",
                "mitigation": "Implement performance monitoring and optimization",
                "source": "Requirements Analysis"
            })
        
        return {
            "total_risks": len(risks),
            "risk_categories": list(set(risk["category"] for risk in risks)),
            "high_impact_risks": len([r for r in risks if r["impact"] == "Critical"]),
            "risks": risks,
            "recommendations": [
                "Implement comprehensive security scanning",
                "Establish regular vulnerability assessment",
                "Set up performance monitoring",
                "Create compliance audit procedures"
            ]
        }
        
    except Exception as e:
        logger.error(f"Risk assessment generation failed: {e}")
        return {"risks": [], "recommendations": []}

async def _generate_cost_estimation(
    requirements_analysis: Dict[str, Any],
    real_time_knowledge: Dict[str, List[Dict[str, Any]]],
    request: EnhancedRequirementsRequest
) -> Dict[str, Any]:
    """Generate cost estimation with real-time data"""
    try:
        base_cost = 50000  # Base cost for development
        
        # Adjust based on team size
        team_cost = base_cost * (request.team_size / 5)
        
        # Adjust based on timeline
        timeline_multiplier = {
            "1-3 months": 1.5,
            "3-6 months": 1.0,
            "6-12 months": 0.8,
            "12+ months": 0.7
        }.get(request.timeline, 1.0)
        
        # Adjust based on scale
        scale_multiplier = {
            "startup": 0.7,
            "small_team": 1.0,
            "enterprise": 2.0,
            "enterprise_plus": 3.0,
            "global_scale": 5.0
        }.get(request.scale, 1.0)
        
        # Adjust based on security level
        security_multiplier = {
            "basic": 1.0,
            "standard": 1.2,
            "enhanced": 1.5,
            "enterprise": 2.0,
            "government": 3.0
        }.get(request.security_level, 1.0)
        
        estimated_cost = team_cost * timeline_multiplier * scale_multiplier * security_multiplier
        
        # Add cloud costs from real-time data
        cloud_costs = 0
        if "cloud_services" in real_time_knowledge:
            for entry in real_time_knowledge["cloud_services"]:
                pricing = entry.get("content", {}).get("pricing", {})
                if pricing:
                    cloud_costs += pricing.get("monthly_cost", 0) * 12  # Annual cost
        
        return {
            "development_cost": estimated_cost,
            "cloud_infrastructure_cost": cloud_costs,
            "total_estimated_cost": estimated_cost + cloud_costs,
            "cost_breakdown": {
                "development": f"${estimated_cost:,.0f}",
                "infrastructure": f"${cloud_costs:,.0f}",
                "security": f"${estimated_cost * 0.2:,.0f}",
                "testing": f"${estimated_cost * 0.15:,.0f}",
                "deployment": f"${estimated_cost * 0.1:,.0f}"
            },
            "cost_optimization_recommendations": [
                "Use cloud-native services to reduce infrastructure costs",
                "Implement automated testing to reduce manual testing costs",
                "Consider open-source alternatives for cost-sensitive components",
                "Implement resource monitoring to optimize cloud spending"
            ]
        }
        
    except Exception as e:
        logger.error(f"Cost estimation generation failed: {e}")
        return {"total_estimated_cost": 0, "cost_breakdown": {}}

async def _generate_timeline(
    requirements_analysis: Dict[str, Any],
    architecture_recommendations: List[Dict[str, Any]],
    request: EnhancedRequirementsRequest
) -> Dict[str, Any]:
    """Generate detailed project timeline"""
    try:
        base_timeline = {
            "1-3 months": 12,
            "3-6 months": 24,
            "6-12 months": 48,
            "12+ months": 96
        }.get(request.timeline, 24)
        
        # Adjust based on complexity
        complexity_multiplier = {
            "simple": 0.8,
            "moderate": 1.0,
            "complex": 1.5,
            "enterprise": 2.0
        }.get(request.scale, 1.0)
        
        total_weeks = base_timeline * complexity_multiplier
        
        phases = [
            {
                "phase": "Planning & Requirements",
                "duration_weeks": max(2, total_weeks * 0.1),
                "tasks": [
                    "Requirements gathering and analysis",
                    "Architecture design",
                    "Technology stack selection",
                    "Project planning and estimation"
                ]
            },
            {
                "phase": "Development Setup",
                "duration_weeks": max(2, total_weeks * 0.15),
                "tasks": [
                    "Environment setup",
                    "CI/CD pipeline configuration",
                    "Database design and setup",
                    "Security framework implementation"
                ]
            },
            {
                "phase": "Core Development",
                "duration_weeks": max(8, total_weeks * 0.5),
                "tasks": [
                    "Backend API development",
                    "Frontend application development",
                    "Database implementation",
                    "Integration testing"
                ]
            },
            {
                "phase": "Testing & Quality Assurance",
                "duration_weeks": max(3, total_weeks * 0.15),
                "tasks": [
                    "Unit testing",
                    "Integration testing",
                    "Security testing",
                    "Performance testing"
                ]
            },
            {
                "phase": "Deployment & Launch",
                "duration_weeks": max(2, total_weeks * 0.1),
                "tasks": [
                    "Production deployment",
                    "Monitoring setup",
                    "Documentation completion",
                    "Team training"
                ]
            }
        ]
        
        return {
            "total_duration_weeks": total_weeks,
            "estimated_completion_date": f"{total_weeks} weeks from start",
            "phases": phases,
            "milestones": [
                {"week": 2, "milestone": "Requirements and architecture finalized"},
                {"week": 4, "milestone": "Development environment ready"},
                {"week": 12, "milestone": "Core features implemented"},
                {"week": 15, "milestone": "Testing completed"},
                {"week": 17, "milestone": "Production deployment"}
            ]
        }
        
    except Exception as e:
        logger.error(f"Timeline generation failed: {e}")
        return {"total_duration_weeks": 0, "phases": []}

async def _generate_success_metrics(
    requirements_analysis: Dict[str, Any],
    request: EnhancedRequirementsRequest
) -> Dict[str, Any]:
    """Generate success metrics and KPIs"""
    try:
        metrics = {
            "technical_metrics": {
                "code_coverage": "90%+",
                "api_response_time": "<200ms",
                "uptime": "99.9%",
                "security_score": "95/100",
                "performance_score": "90/100"
            },
            "business_metrics": {
                "time_to_market": request.timeline,
                "cost_efficiency": "Within budget",
                "user_satisfaction": "4.5/5",
                "feature_completion": "100%",
                "bug_rate": "<1%"
            },
            "quality_metrics": {
                "test_coverage": "90%+",
                "documentation_completeness": "95%+",
                "code_quality_score": "A+",
                "security_compliance": "100%",
                "performance_benchmarks": "Met"
            },
            "team_metrics": {
                "developer_productivity": "High",
                "knowledge_transfer": "Complete",
                "team_satisfaction": "4.5/5",
                "skill_development": "Enhanced"
            }
        }
        
        return {
            "overall_success_score": "95%",
            "metrics": metrics,
            "kpis": [
                "Project delivered on time and within budget",
                "All security requirements met",
                "Performance benchmarks achieved",
                "Team skills enhanced",
                "Documentation complete and accurate"
            ],
            "monitoring_recommendations": [
                "Implement real-time performance monitoring",
                "Set up automated security scanning",
                "Establish regular code quality reviews",
                "Create automated testing pipelines",
                "Monitor user satisfaction metrics"
            ]
        }
        
    except Exception as e:
        logger.error(f"Success metrics generation failed: {e}")
        return {"overall_success_score": "0%", "metrics": {}} 