"""
Data Seeding Script - Professional Implementation
Populates database with realistic, comprehensive data for development and testing
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from uuid import uuid4
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.cost_analysis import CostAnalysis, CostRecommendation
from app.models.security_scan import SecurityScan, Vulnerability
from app.models.infrastructure import Infrastructure, Resource
from app.models.ai_insight import AIInsight, AIModel, InsightType, InsightPriority
from app.core.auth import get_password_hash

logger = logging.getLogger(__name__)


class DataSeeder:
    """Professional data seeder for CloudMind"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def seed_all_data(self):
        """Seed all data in the correct order"""
        logger.info("🌱 Starting comprehensive data seeding...")
        
        try:
            # Seed in dependency order
            await self._seed_users()
            await self._seed_projects()
            await self._seed_cost_analyses()
            await self._seed_security_scans()
            await self._seed_infrastructure()
            await self._seed_ai_insights()
            
            logger.info("✅ All data seeded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error seeding data: {str(e)}")
            raise
    
    async def _seed_users(self):
        """Seed realistic users"""
        logger.info("👥 Seeding users...")
        
        users_data = [
            {
                "email": "admin@cloudmind.local",
                "username": "admin",
                "full_name": "System Administrator",
                "is_superuser": True,
                "is_verified": True
            },
            {
                "email": "john.doe@acme.com",
                "username": "john.doe",
                "full_name": "John Doe",
                "is_superuser": False,
                "is_verified": True
            },
            {
                "email": "sarah.smith@techcorp.com",
                "username": "sarah.smith",
                "full_name": "Sarah Smith",
                "is_superuser": False,
                "is_verified": True
            },
            {
                "email": "mike.johnson@startup.io",
                "username": "mike.johnson",
                "full_name": "Mike Johnson",
                "is_superuser": False,
                "is_verified": True
            },
            {
                "email": "demo@cloudmind.local",
                "username": "demo",
                "full_name": "Demo User",
                "is_superuser": False,
                "is_verified": True
            }
        ]
        
        for user_data in users_data:
            existing = self.db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    id=uuid4(),
                    email=user_data["email"],
                    username=user_data["username"],
                    full_name=user_data["full_name"],
                    hashed_password=get_password_hash("password123"),
                    is_superuser=user_data["is_superuser"],
                    is_verified=user_data["is_verified"],
                    is_active=True,
                    preferences={
                        "theme": "light",
                        "notifications": True,
                        "timezone": "UTC"
                    }
                )
                self.db.add(user)
        
        self.db.commit()
        logger.info(f"✅ Seeded {len(users_data)} users")
    
    async def _seed_projects(self):
        """Seed realistic projects"""
        logger.info("📁 Seeding projects...")
        
        users = self.db.query(User).all()
        
        projects_data = [
            {
                "name": "E-commerce Platform",
                "description": "High-traffic e-commerce application with microservices architecture",
                "cloud_providers": ["aws", "azure"],
                "environments": ["production", "staging", "development"],
                "team_size": 15,
                "monthly_budget": 25000
            },
            {
                "name": "Mobile App Backend",
                "description": "RESTful API backend for mobile applications",
                "cloud_providers": ["aws"],
                "environments": ["production", "staging"],
                "team_size": 8,
                "monthly_budget": 8000
            },
            {
                "name": "Data Analytics Platform",
                "description": "Big data processing and analytics infrastructure",
                "cloud_providers": ["aws", "gcp"],
                "environments": ["production", "development"],
                "team_size": 12,
                "monthly_budget": 15000
            },
            {
                "name": "SaaS Application",
                "description": "Multi-tenant SaaS platform with Kubernetes",
                "cloud_providers": ["aws", "azure", "gcp"],
                "environments": ["production", "staging", "development", "testing"],
                "team_size": 25,
                "monthly_budget": 35000
            },
            {
                "name": "Legacy Migration",
                "description": "On-premises to cloud migration project",
                "cloud_providers": ["aws"],
                "environments": ["migration", "testing"],
                "team_size": 10,
                "monthly_budget": 12000
            }
        ]
        
        for i, project_data in enumerate(projects_data):
            user = users[i % len(users)]
            existing = self.db.query(Project).filter(
                Project.name == project_data["name"],
                Project.owner_id == user.id
            ).first()
            
            if not existing:
                project = Project(
                    id=uuid4(),
                    name=project_data["name"],
                    description=project_data["description"],
                    owner_id=user.id,
                    cloud_providers=project_data["cloud_providers"],
                    environments=project_data["environments"],
                    team_size=project_data["team_size"],
                    monthly_budget=project_data["monthly_budget"],
                    status="active",
                    settings={
                        "cost_alerts": True,
                        "security_scanning": True,
                        "backup_enabled": True,
                        "monitoring_enabled": True
                    }
                )
                self.db.add(project)
        
        self.db.commit()
        logger.info(f"✅ Seeded {len(projects_data)} projects")
    
    async def _seed_cost_analyses(self):
        """Seed realistic cost analyses"""
        logger.info("💰 Seeding cost analyses...")
        
        users = self.db.query(User).all()
        projects = self.db.query(Project).all()
        
        # Generate 6 months of cost data for each project
        for project in projects:
            base_cost = project.monthly_budget
            for month in range(6):
                # Generate realistic cost variations
                variation = random.uniform(0.8, 1.3)  # ±30% variation
                actual_cost = base_cost * variation
                
                # Create cost analysis
                analysis = CostAnalysis(
                    id=uuid4(),
                    user_id=project.owner_id,
                    project_id=project.id,
                    name=f"Cost Analysis - {datetime.now().strftime('%B %Y')}",
                    description=f"Monthly cost analysis for {project.name}",
                    cloud_provider=random.choice(project.cloud_providers),
                    regions=["us-east-1", "us-west-2", "eu-west-1"],
                    services=["ec2", "rds", "s3", "lambda", "cloudfront"],
                    date_from=datetime.now() - timedelta(days=30 * (6 - month)),
                    date_to=datetime.now() - timedelta(days=30 * (5 - month)),
                    currency="USD",
                    total_cost=actual_cost,
                    breakdown={
                        "compute": actual_cost * 0.4,
                        "storage": actual_cost * 0.2,
                        "network": actual_cost * 0.15,
                        "database": actual_cost * 0.15,
                        "other": actual_cost * 0.1
                    },
                    status="completed"
                )
                self.db.add(analysis)
                
                # Create cost recommendations
                if variation > 1.1:  # If cost is high
                    recommendation = CostRecommendation(
                        id=uuid4(),
                        analysis_id=analysis.id,
                        title="Optimize Compute Resources",
                        description="Consider using reserved instances for predictable workloads",
                        category="compute",
                        priority="high",
                        potential_savings=actual_cost * 0.15,
                        effort_level="medium",
                        implementation_steps=[
                            "Analyze current usage patterns",
                            "Identify suitable instances for reservation",
                            "Implement auto-scaling policies"
                        ]
                    )
                    self.db.add(recommendation)
        
        self.db.commit()
        logger.info("✅ Seeded cost analyses and recommendations")
    
    async def _seed_security_scans(self):
        """Seed realistic security scans"""
        logger.info("🔒 Seeding security scans...")
        
        users = self.db.query(User).all()
        projects = self.db.query(Project).all()
        
        vulnerability_types = [
            {"name": "SQL Injection", "severity": "high", "category": "web"},
            {"name": "XSS Vulnerability", "severity": "medium", "category": "web"},
            {"name": "Weak Password Policy", "severity": "medium", "category": "auth"},
            {"name": "Missing SSL/TLS", "severity": "high", "category": "network"},
            {"name": "Open Ports", "severity": "low", "category": "network"},
            {"name": "Outdated Software", "severity": "medium", "category": "system"},
            {"name": "Insufficient Logging", "severity": "low", "category": "monitoring"},
            {"name": "Weak Encryption", "severity": "high", "category": "crypto"}
        ]
        
        for project in projects:
            # Create security scan
            scan = SecurityScan(
                id=uuid4(),
                user_id=project.owner_id,
                project_id=project.id,
                name=f"Security Scan - {project.name}",
                description=f"Comprehensive security assessment for {project.name}",
                scan_type="comprehensive",
                status="completed",
                scan_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                compliance_frameworks=["SOC2", "HIPAA", "PCI"],
                risk_score=random.randint(20, 80),
                summary={
                    "total_vulnerabilities": random.randint(5, 25),
                    "critical_issues": random.randint(0, 3),
                    "high_issues": random.randint(2, 8),
                    "medium_issues": random.randint(3, 12),
                    "low_issues": random.randint(5, 15)
                }
            )
            self.db.add(scan)
            
            # Create vulnerabilities
            num_vulns = random.randint(5, 15)
            for _ in range(num_vulns):
                vuln_type = random.choice(vulnerability_types)
                vulnerability = Vulnerability(
                    id=uuid4(),
                    scan_id=scan.id,
                    name=vuln_type["name"],
                    description=f"Detailed description of {vuln_type['name'].lower()} vulnerability",
                    severity=vuln_type["severity"],
                    category=vuln_type["category"],
                    cve_id=f"CVE-2024-{random.randint(1000, 9999)}",
                    affected_resources=["web-server-1", "database-1"],
                    remediation_steps=[
                        "Update affected software",
                        "Implement security patches",
                        "Review access controls"
                    ],
                    risk_score=random.randint(1, 10)
                )
                self.db.add(vulnerability)
        
        self.db.commit()
        logger.info("✅ Seeded security scans and vulnerabilities")
    
    async def _seed_infrastructure(self):
        """Seed realistic infrastructure data"""
        logger.info("🏗️ Seeding infrastructure...")
        
        users = self.db.query(User).all()
        projects = self.db.query(Project).all()
        
        resource_types = [
            {"type": "ec2", "name": "Web Server", "instance_type": "t3.medium"},
            {"type": "ec2", "name": "Application Server", "instance_type": "t3.large"},
            {"type": "rds", "name": "Database", "instance_type": "db.t3.medium"},
            {"type": "s3", "name": "Storage Bucket", "instance_type": "standard"},
            {"type": "lambda", "name": "API Function", "instance_type": "serverless"},
            {"type": "cloudfront", "name": "CDN", "instance_type": "global"},
            {"type": "elasticache", "name": "Redis Cache", "instance_type": "cache.t3.micro"},
            {"type": "loadbalancer", "name": "Load Balancer", "instance_type": "application"}
        ]
        
        for project in projects:
            infrastructure = Infrastructure(
                id=uuid4(),
                user_id=project.owner_id,
                project_id=project.id,
                name=f"Infrastructure - {project.name}",
                description=f"Cloud infrastructure for {project.name}",
                cloud_provider=random.choice(project.cloud_providers),
                regions=["us-east-1", "us-west-2"],
                status="active",
                total_resources=len(resource_types),
                monthly_cost=project.monthly_budget * 0.8
            )
            self.db.add(infrastructure)
            
            # Create resources
            for resource_type in resource_types:
                resource = Resource(
                    id=uuid4(),
                    infrastructure_id=infrastructure.id,
                    name=resource_type["name"],
                    resource_type=resource_type["type"],
                    instance_type=resource_type["instance_type"],
                    region="us-east-1",
                    status="running",
                    utilization_rate=random.uniform(0.2, 0.9),
                    monthly_cost=random.uniform(50, 500),
                    tags={
                        "environment": "production",
                        "project": project.name,
                        "managed_by": "terraform"
                    },
                    metrics={
                        "cpu_usage": random.uniform(20, 80),
                        "memory_usage": random.uniform(30, 85),
                        "network_io": random.uniform(100, 1000),
                        "disk_usage": random.uniform(40, 90)
                    }
                )
                self.db.add(resource)
        
        self.db.commit()
        logger.info("✅ Seeded infrastructure and resources")
    
    async def _seed_ai_insights(self):
        """Seed realistic AI insights"""
        logger.info("🤖 Seeding AI insights...")
        
        users = self.db.query(User).all()
        projects = self.db.query(Project).all()
        
        insight_templates = [
            {
                "title": "Cost Optimization Opportunity",
                "description": "Your compute costs are 25% higher than industry benchmarks. Consider implementing auto-scaling and reserved instances.",
                "insight_type": InsightType.COST_OPTIMIZATION,
                "priority": InsightPriority.HIGH,
                "recommendations": [
                    "Implement auto-scaling policies",
                    "Purchase reserved instances for predictable workloads",
                    "Use spot instances for non-critical workloads"
                ],
                "impact_analysis": {
                    "potential_savings": "$2,500/month",
                    "effort_level": "Medium",
                    "time_to_implement": "2-3 weeks"
                }
            },
            {
                "title": "Security Posture Improvement",
                "description": "Found 12 vulnerabilities across your infrastructure. Implement comprehensive security measures.",
                "insight_type": InsightType.SECURITY,
                "priority": InsightPriority.MEDIUM,
                "recommendations": [
                    "Implement automated vulnerability scanning",
                    "Establish security baselines",
                    "Create incident response procedures"
                ],
                "impact_analysis": {
                    "risk_level": "Medium",
                    "effort_level": "Medium",
                    "time_to_implement": "4-6 weeks"
                }
            },
            {
                "title": "Performance Optimization",
                "description": "Database queries are taking 3x longer than optimal. Consider query optimization and indexing.",
                "insight_type": InsightType.PERFORMANCE,
                "priority": InsightPriority.MEDIUM,
                "recommendations": [
                    "Optimize database queries",
                    "Add appropriate indexes",
                    "Implement connection pooling"
                ],
                "impact_analysis": {
                    "performance_improvement": "60%",
                    "effort_level": "Medium",
                    "time_to_implement": "1-2 weeks"
                }
            },
            {
                "title": "Resource Utilization",
                "description": "30% of your resources are underutilized. Consider rightsizing or consolidation.",
                "insight_type": InsightType.INFRASTRUCTURE,
                "priority": InsightPriority.LOW,
                "recommendations": [
                    "Review resource sizing",
                    "Implement auto-scaling",
                    "Consider spot instances"
                ],
                "impact_analysis": {
                    "potential_savings": "$1,200/month",
                    "effort_level": "Low",
                    "time_to_implement": "1-2 weeks"
                }
            }
        ]
        
        for project in projects:
            # Create 2-4 insights per project
            num_insights = random.randint(2, 4)
            selected_insights = random.sample(insight_templates, num_insights)
            
            for insight_template in selected_insights:
                insight = AIInsight(
                    id=uuid4(),
                    user_id=project.owner_id,
                    project_id=project.id,
                    title=insight_template["title"],
                    description=insight_template["description"],
                    insight_type=insight_template["insight_type"],
                    priority=insight_template["priority"],
                    confidence_score=random.uniform(0.8, 0.95),
                    recommendations=insight_template["recommendations"],
                    impact_analysis=insight_template["impact_analysis"],
                    is_acknowledged=random.choice([True, False]),
                    is_implemented=random.choice([True, False]),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                self.db.add(insight)
        
        self.db.commit()
        logger.info("✅ Seeded AI insights")


async def main():
    """Main seeding function"""
    db = next(get_db())
    seeder = DataSeeder(db)
    await seeder.seed_all_data()


if __name__ == "__main__":
    asyncio.run(main()) 