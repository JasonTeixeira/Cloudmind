"""
World-Class AI Architecture & Engineering Intelligence Engine
Provides comprehensive requirements analysis, architecture design, technology selection,
and project planning capabilities with encyclopedia-level knowledge base.
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import uuid

from app.core.config import settings
from app.services.ai_engine.ai_providers import OpenAIProvider, AnthropicProvider, OllamaProvider
from app.services.ai_engine.enhanced_knowledge_engine import EnhancedKnowledgeEngine

logger = logging.getLogger(__name__)


class ArchitectureType(Enum):
    """Architecture types"""
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    CQRS = "cqrs"
    EVENT_SOURCING = "event_sourcing"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    CLEAN_ARCHITECTURE = "clean_architecture"
    DOMAIN_DRIVEN = "domain_driven"


class TechnologyCategory(Enum):
    """Technology categories"""
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CACHE = "cache"
    MESSAGE_QUEUE = "message_queue"
    CONTAINER = "container"
    ORCHESTRATION = "orchestration"
    MONITORING = "monitoring"
    SECURITY = "security"
    CLOUD_PROVIDER = "cloud_provider"
    CI_CD = "ci_cd"
    TESTING = "testing"


class ProjectScale(Enum):
    """Project scale levels"""
    STARTUP = "startup"
    SMALL_TEAM = "small_team"
    ENTERPRISE = "enterprise"
    ENTERPRISE_PLUS = "enterprise_plus"
    GLOBAL_SCALE = "global_scale"


@dataclass
class Requirement:
    """Project requirement"""
    id: str
    title: str
    description: str
    category: str
    priority: str
    complexity: str
    dependencies: List[str]
    acceptance_criteria: List[str]
    constraints: List[str]
    assumptions: List[str]


@dataclass
class ArchitectureRecommendation:
    """Architecture recommendation"""
    id: str
    name: str
    description: str
    architecture_type: ArchitectureType
    pros: List[str]
    cons: List[str]
    complexity_score: float
    scalability_score: float
    maintainability_score: float
    cost_score: float
    security_score: float
    technology_stack: Dict[str, List[str]]
    implementation_steps: List[str]
    risks: List[str]
    alternatives: List[str]


@dataclass
class TechnologyRecommendation:
    """Technology recommendation"""
    id: str
    name: str
    category: TechnologyCategory
    description: str
    pros: List[str]
    cons: List[str]
    use_cases: List[str]
    alternatives: List[str]
    learning_curve: str
    community_support: str
    enterprise_adoption: str
    cost_considerations: str
    security_features: List[str]
    performance_characteristics: Dict[str, Any]


@dataclass
class ProjectTemplate:
    """Project template"""
    id: str
    name: str
    description: str
    architecture_type: ArchitectureType
    technology_stack: Dict[str, List[str]]
    project_structure: Dict[str, Any]
    setup_instructions: List[str]
    configuration_files: Dict[str, str]
    deployment_scripts: List[str]
    testing_strategy: Dict[str, Any]
    monitoring_setup: Dict[str, Any]
    security_configuration: Dict[str, Any]


class AIArchitectureEngine:
    """World-class AI architecture and engineering intelligence engine"""
    
    def __init__(self):
        self.openai_provider = OpenAIProvider()
        self.anthropic_provider = AnthropicProvider()
        self.ollama_provider = OllamaProvider()
        
        # Initialize enhanced knowledge engine
        self.enhanced_knowledge_engine = EnhancedKnowledgeEngine()
        
        # Initialize knowledge base
        self.knowledge_base = self._initialize_knowledge_base()
        
        # Architecture patterns and best practices
        self.architecture_patterns = self._load_architecture_patterns()
        
        # Technology encyclopedia
        self.technology_encyclopedia = self._load_technology_encyclopedia()
        
        # Project templates
        self.project_templates = self._load_project_templates()
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize comprehensive knowledge base"""
        return {
            "security": {
                "frameworks": ["OWASP", "NIST", "ISO27001", "SOC2", "PCI DSS", "HIPAA"],
                "patterns": ["Zero Trust", "Defense in Depth", "Principle of Least Privilege"],
                "threats": ["SQL Injection", "XSS", "CSRF", "DDoS", "Ransomware", "APT"],
                "tools": ["SonarQube", "Snyk", "Bandit", "Semgrep", "Trivy", "Nessus"]
            },
            "cloud": {
                "providers": ["AWS", "Azure", "GCP", "DigitalOcean", "Vultr"],
                "services": ["Compute", "Storage", "Database", "Networking", "Security"],
                "patterns": ["Multi-Cloud", "Hybrid Cloud", "Cloud-Native", "Serverless"],
                "best_practices": ["Well-Architected Framework", "12-Factor App", "Cloud Security"]
            },
            "networking": {
                "protocols": ["HTTP/HTTPS", "TCP/UDP", "WebSocket", "gRPC", "GraphQL"],
                "patterns": ["API Gateway", "Load Balancer", "CDN", "Service Mesh"],
                "security": ["SSL/TLS", "VPN", "Firewall", "WAF", "DDoS Protection"]
            },
            "distributed_systems": {
                "patterns": ["Microservices", "Event Sourcing", "CQRS", "Saga Pattern"],
                "challenges": ["Consistency", "Availability", "Partition Tolerance"],
                "solutions": ["Consensus Algorithms", "Distributed Caching", "Message Queues"]
            },
            "databases": {
                "types": ["Relational", "NoSQL", "Graph", "Time-Series", "Vector"],
                "patterns": ["Sharding", "Replication", "Caching", "Read/Write Splitting"],
                "technologies": ["PostgreSQL", "MongoDB", "Redis", "Neo4j", "InfluxDB"]
            }
        }
    
    def _load_architecture_patterns(self) -> Dict[str, Any]:
        """Load comprehensive architecture patterns"""
        return {
            "microservices": {
                "description": "Distributed system with loosely coupled services",
                "use_cases": ["Large-scale applications", "Team autonomy", "Technology diversity"],
                "complexity": "high",
                "scalability": "excellent",
                "maintainability": "good",
                "technologies": ["Docker", "Kubernetes", "Service Mesh", "API Gateway"]
            },
            "monolith": {
                "description": "Single application with all functionality",
                "use_cases": ["Small teams", "Simple applications", "Rapid prototyping"],
                "complexity": "low",
                "scalability": "limited",
                "maintainability": "challenging",
                "technologies": ["Spring Boot", "Django", "Rails", "Laravel"]
            },
            "serverless": {
                "description": "Event-driven, auto-scaling functions",
                "use_cases": ["Sporadic workloads", "Event processing", "Cost optimization"],
                "complexity": "medium",
                "scalability": "excellent",
                "maintainability": "good",
                "technologies": ["AWS Lambda", "Azure Functions", "Google Cloud Functions"]
            },
            "event_driven": {
                "description": "Asynchronous communication via events",
                "use_cases": ["Real-time processing", "Data pipelines", "IoT applications"],
                "complexity": "high",
                "scalability": "excellent",
                "maintainability": "challenging",
                "technologies": ["Apache Kafka", "RabbitMQ", "AWS EventBridge", "Apache Pulsar"]
            },
            "clean_architecture": {
                "description": "Layered architecture with dependency inversion",
                "use_cases": ["Complex business logic", "Testability", "Maintainability"],
                "complexity": "medium",
                "scalability": "good",
                "maintainability": "excellent",
                "technologies": ["Domain-Driven Design", "SOLID Principles", "Dependency Injection"]
            }
        }
    
    def _load_technology_encyclopedia(self) -> Dict[str, Any]:
        """Load comprehensive technology encyclopedia"""
        return {
            "programming_languages": {
                "python": {
                    "description": "High-level, interpreted programming language",
                    "use_cases": ["Web Development", "Data Science", "AI/ML", "Automation"],
                    "pros": ["Readable syntax", "Rich ecosystem", "AI/ML libraries"],
                    "cons": ["Slower execution", "GIL limitations", "Mobile development"],
                    "frameworks": ["Django", "FastAPI", "Flask", "PyTorch", "TensorFlow"]
                },
                "javascript": {
                    "description": "Dynamic programming language for web development",
                    "use_cases": ["Frontend Development", "Backend Development", "Mobile Apps"],
                    "pros": ["Ubiquitous", "Rich ecosystem", "Real-time capabilities"],
                    "cons": ["Type safety", "Callback hell", "Browser differences"],
                    "frameworks": ["React", "Vue.js", "Angular", "Node.js", "Express"]
                },
                "java": {
                    "description": "Object-oriented programming language",
                    "use_cases": ["Enterprise Applications", "Android Development", "Big Data"],
                    "pros": ["Platform independent", "Strong typing", "Enterprise ready"],
                    "cons": ["Verbose syntax", "Memory overhead", "Slower startup"],
                    "frameworks": ["Spring Boot", "Hibernate", "Apache Kafka", "Hadoop"]
                },
                "go": {
                    "description": "Statically typed, compiled language",
                    "use_cases": ["Microservices", "Cloud Native", "System Programming"],
                    "pros": ["Fast compilation", "Concurrent programming", "Simple syntax"],
                    "cons": ["Limited ecosystem", "No generics", "Error handling"],
                    "frameworks": ["Gin", "Echo", "Fiber", "Kubernetes", "Docker"]
                }
            },
            "databases": {
                "postgresql": {
                    "description": "Advanced open-source relational database",
                    "use_cases": ["OLTP", "Data Warehousing", "Geospatial Data"],
                    "pros": ["ACID compliance", "Rich features", "Extensibility"],
                    "cons": ["Complex setup", "Resource intensive", "Limited horizontal scaling"],
                    "alternatives": ["MySQL", "Oracle", "SQL Server"]
                },
                "mongodb": {
                    "description": "Document-oriented NoSQL database",
                    "use_cases": ["Content Management", "Real-time Analytics", "IoT Data"],
                    "pros": ["Schema flexibility", "Horizontal scaling", "JSON native"],
                    "cons": ["No ACID transactions", "Memory usage", "Complex queries"],
                    "alternatives": ["CouchDB", "DynamoDB", "Firestore"]
                },
                "redis": {
                    "description": "In-memory data structure store",
                    "use_cases": ["Caching", "Session Storage", "Real-time Analytics"],
                    "pros": ["Ultra-fast", "Rich data types", "Persistence"],
                    "cons": ["Memory limited", "No complex queries", "Single-threaded"],
                    "alternatives": ["Memcached", "Hazelcast", "Apache Ignite"]
                }
            },
            "cloud_providers": {
                "aws": {
                    "description": "Leading cloud computing platform",
                    "services": ["EC2", "S3", "Lambda", "RDS", "DynamoDB"],
                    "pros": ["Market leader", "Comprehensive services", "Global presence"],
                    "cons": ["Complex pricing", "Vendor lock-in", "Learning curve"],
                    "use_cases": ["Enterprise", "Startups", "Global applications"]
                },
                "azure": {
                    "description": "Microsoft's cloud computing platform",
                    "services": ["Virtual Machines", "Blob Storage", "Functions", "SQL Database"],
                    "pros": ["Enterprise integration", "Hybrid cloud", "Windows ecosystem"],
                    "cons": ["Less mature", "Complex pricing", "Limited regions"],
                    "use_cases": ["Enterprise", "Microsoft shops", "Hybrid deployments"]
                },
                "gcp": {
                    "description": "Google's cloud computing platform",
                    "services": ["Compute Engine", "Cloud Storage", "Cloud Functions", "BigQuery"],
                    "pros": ["Strong AI/ML", "Network performance", "Innovation"],
                    "cons": ["Smaller ecosystem", "Less enterprise focus", "Limited services"],
                    "use_cases": ["AI/ML", "Data analytics", "Innovation-focused"]
                }
            }
        }
    
    def _load_project_templates(self) -> Dict[str, Any]:
        """Load project templates"""
        return {
            "microservices_api": {
                "name": "Microservices API",
                "description": "Scalable microservices architecture with API gateway",
                "architecture": ArchitectureType.MICROSERVICES,
                "technologies": {
                    "backend": ["FastAPI", "Django", "Spring Boot"],
                    "database": ["PostgreSQL", "MongoDB", "Redis"],
                    "message_queue": ["RabbitMQ", "Apache Kafka", "AWS SQS"],
                    "container": ["Docker", "Kubernetes"],
                    "monitoring": ["Prometheus", "Grafana", "Jaeger"]
                }
            },
            "serverless_app": {
                "name": "Serverless Application",
                "description": "Event-driven serverless architecture",
                "architecture": ArchitectureType.SERVERLESS,
                "technologies": {
                    "compute": ["AWS Lambda", "Azure Functions", "Google Cloud Functions"],
                    "storage": ["S3", "Blob Storage", "Cloud Storage"],
                    "database": ["DynamoDB", "Cosmos DB", "Firestore"],
                    "api": ["API Gateway", "Application Gateway", "Cloud Endpoints"]
                }
            },
            "monolith_webapp": {
                "name": "Monolithic Web Application",
                "description": "Traditional monolithic web application",
                "architecture": ArchitectureType.MONOLITH,
                "technologies": {
                    "backend": ["Django", "Rails", "Spring Boot"],
                    "frontend": ["React", "Vue.js", "Angular"],
                    "database": ["PostgreSQL", "MySQL", "SQLite"],
                    "deployment": ["Docker", "Heroku", "DigitalOcean"]
                }
            }
        }
    
    async def analyze_requirements(
        self,
        project_description: str,
        business_goals: List[str],
        technical_constraints: List[str],
        team_size: int,
        timeline: str,
        budget: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze project requirements and generate comprehensive recommendations"""
        try:
            logger.info("Starting comprehensive requirements analysis")
            
            # Create requirements analysis prompt
            prompt = self._create_requirements_analysis_prompt(
                project_description, business_goals, technical_constraints,
                team_size, timeline, budget
            )
            
            # Get AI analysis
            analysis = await self._get_ai_response(prompt, "requirements_analysis")
            
            # Parse and structure requirements
            requirements = await self._parse_requirements(analysis)
            
            # Get real-time knowledge for enhanced recommendations
            real_time_knowledge = await self.enhanced_knowledge_engine.get_comprehensive_knowledge({
                "project_description": project_description,
                "business_goals": business_goals,
                "technical_constraints": technical_constraints,
                "technologies": requirements.get("technologies", []),
                "architecture": requirements.get("architecture", ""),
                "domain": requirements.get("domain", "")
            })
            
            # Generate architecture recommendations with real-time knowledge
            architecture_recommendations = await self._generate_architecture_recommendations(requirements, real_time_knowledge)
            
            # Generate technology recommendations with real-time knowledge
            technology_recommendations = await self._generate_technology_recommendations(requirements, real_time_knowledge)
            
            # Generate project plan
            project_plan = await self._generate_project_plan(requirements, architecture_recommendations)
            
            return {
                "requirements": requirements,
                "architecture_recommendations": architecture_recommendations,
                "technology_recommendations": technology_recommendations,
                "project_plan": project_plan,
                "risk_assessment": await self._assess_risks(requirements),
                "cost_estimation": await self._estimate_costs(requirements),
                "timeline": await self._generate_timeline(requirements),
                "success_metrics": await self._define_success_metrics(requirements)
            }
            
        except Exception as e:
            logger.error(f"Requirements analysis failed: {e}")
            raise
    
    async def design_architecture(
        self,
        requirements: Dict[str, Any],
        constraints: List[str],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Design comprehensive system architecture"""
        try:
            logger.info("Starting architecture design")
            
            # Analyze requirements for architecture patterns
            architecture_patterns = await self._analyze_architecture_patterns(requirements)
            
            # Generate detailed architecture design
            architecture_design = await self._generate_architecture_design(
                requirements, architecture_patterns, constraints, preferences
            )
            
            # Create system diagrams
            system_diagrams = await self._generate_system_diagrams(architecture_design)
            
            # Generate implementation guide
            implementation_guide = await self._generate_implementation_guide(architecture_design)
            
            return {
                "architecture_design": architecture_design,
                "system_diagrams": system_diagrams,
                "implementation_guide": implementation_guide,
                "technology_stack": await self._select_technology_stack(architecture_design),
                "deployment_strategy": await self._design_deployment_strategy(architecture_design),
                "security_architecture": await self._design_security_architecture(architecture_design),
                "monitoring_strategy": await self._design_monitoring_strategy(architecture_design)
            }
            
        except Exception as e:
            logger.error(f"Architecture design failed: {e}")
            raise
    
    async def generate_project_template(
        self,
        architecture_type: ArchitectureType,
        technology_stack: Dict[str, List[str]],
        project_scale: ProjectScale
    ) -> ProjectTemplate:
        """Generate comprehensive project template"""
        try:
            logger.info(f"Generating project template for {architecture_type.value}")
            
            # Get base template
            base_template = self.project_templates.get(architecture_type.value, {})
            
            # Generate project structure
            project_structure = await self._generate_project_structure(
                architecture_type, technology_stack, project_scale
            )
            
            # Generate configuration files
            config_files = await self._generate_configuration_files(
                architecture_type, technology_stack
            )
            
            # Generate deployment scripts
            deployment_scripts = await self._generate_deployment_scripts(
                architecture_type, technology_stack
            )
            
            # Generate testing strategy
            testing_strategy = await self._generate_testing_strategy(
                architecture_type, technology_stack
            )
            
            return ProjectTemplate(
                id=str(uuid.uuid4()),
                name=f"{architecture_type.value.title()} Template",
                description=f"Comprehensive template for {architecture_type.value} architecture",
                architecture_type=architecture_type,
                technology_stack=technology_stack,
                project_structure=project_structure,
                setup_instructions=await self._generate_setup_instructions(architecture_type),
                configuration_files=config_files,
                deployment_scripts=deployment_scripts,
                testing_strategy=testing_strategy,
                monitoring_setup=await self._generate_monitoring_setup(architecture_type),
                security_configuration=await self._generate_security_configuration(architecture_type)
            )
            
        except Exception as e:
            logger.error(f"Project template generation failed: {e}")
            raise
    
    async def get_knowledge_base_entry(
        self,
        category: str,
        topic: str
    ) -> Dict[str, Any]:
        """Get encyclopedia-style knowledge base entry"""
        try:
            # Search knowledge base
            if category in self.knowledge_base:
                if topic in self.knowledge_base[category]:
                    return {
                        "category": category,
                        "topic": topic,
                        "content": self.knowledge_base[category][topic],
                        "related_topics": self._get_related_topics(category, topic),
                        "best_practices": await self._get_best_practices(category, topic),
                        "common_pitfalls": await self._get_common_pitfalls(category, topic),
                        "implementation_guide": await self._get_implementation_guide(category, topic)
                    }
            
            # If not found in local knowledge base, query AI
            return await self._query_ai_knowledge_base(category, topic)
            
        except Exception as e:
            logger.error(f"Knowledge base query failed: {e}")
            raise
    
    async def compare_technologies(
        self,
        category: TechnologyCategory,
        technologies: List[str]
    ) -> Dict[str, Any]:
        """Compare technologies in a category"""
        try:
            comparison_data = {}
            
            for tech in technologies:
                if tech in self.technology_encyclopedia.get(category.value, {}):
                    comparison_data[tech] = self.technology_encyclopedia[category.value][tech]
                else:
                    # Query AI for technology information
                    comparison_data[tech] = await self._query_ai_technology_info(tech, category)
            
            # Generate comparison matrix
            comparison_matrix = await self._generate_comparison_matrix(comparison_data)
            
            # Generate recommendations
            recommendations = await self._generate_technology_recommendations(comparison_data)
            
            return {
                "technologies": comparison_data,
                "comparison_matrix": comparison_matrix,
                "recommendations": recommendations,
                "decision_framework": await self._create_decision_framework(category)
            }
            
        except Exception as e:
            logger.error(f"Technology comparison failed: {e}")
            raise
    
    def _create_requirements_analysis_prompt(
        self,
        project_description: str,
        business_goals: List[str],
        technical_constraints: List[str],
        team_size: int,
        timeline: str,
        budget: Optional[str]
    ) -> str:
        """Create comprehensive requirements analysis prompt"""
        return f"""
        Analyze the following project requirements and provide comprehensive recommendations:

        PROJECT DESCRIPTION:
        {project_description}

        BUSINESS GOALS:
        {chr(10).join(f"- {goal}" for goal in business_goals)}

        TECHNICAL CONSTRAINTS:
        {chr(10).join(f"- {constraint}" for constraint in technical_constraints)}

        TEAM SIZE: {team_size} developers
        TIMELINE: {timeline}
        BUDGET: {budget or 'Not specified'}

        Please provide:
        1. Detailed functional and non-functional requirements
        2. Architecture recommendations with pros/cons
        3. Technology stack recommendations
        4. Risk assessment and mitigation strategies
        5. Cost estimation and budget planning
        6. Implementation timeline and milestones
        7. Success metrics and KPIs
        8. Security and compliance considerations
        9. Scalability and performance requirements
        10. Team structure and skill requirements

        Format the response as structured JSON with clear sections.
        """
    
    async def _get_ai_response(self, prompt: str, task_type: str) -> str:
        """Get AI response for architecture tasks"""
        try:
            # Use Claude for architecture and requirements analysis
            if task_type in ["requirements_analysis", "architecture_design"]:
                return await self.anthropic_provider.get_response(prompt)
            else:
                return await self.openai_provider.get_response(prompt)
        except Exception as e:
            logger.error(f"AI response failed: {e}")
            # Fallback to local model
            return await self.ollama_provider.get_response(prompt)
    
    async def _parse_requirements(self, analysis: str) -> List[Requirement]:
        """Parse AI analysis into structured requirements"""
        try:
            # Parse JSON response
            data = json.loads(analysis)
            
            requirements = []
            for req_data in data.get("requirements", []):
                requirement = Requirement(
                    id=str(uuid.uuid4()),
                    title=req_data.get("title", ""),
                    description=req_data.get("description", ""),
                    category=req_data.get("category", ""),
                    priority=req_data.get("priority", "medium"),
                    complexity=req_data.get("complexity", "medium"),
                    dependencies=req_data.get("dependencies", []),
                    acceptance_criteria=req_data.get("acceptance_criteria", []),
                    constraints=req_data.get("constraints", []),
                    assumptions=req_data.get("assumptions", [])
                )
                requirements.append(requirement)
            
            return requirements
            
        except Exception as e:
            logger.error(f"Requirements parsing failed: {e}")
            return []
    
    async def _generate_architecture_recommendations(
        self,
        requirements: List[Requirement]
    ) -> List[ArchitectureRecommendation]:
        """Generate architecture recommendations based on requirements"""
        try:
            recommendations = []
            
            # Analyze requirements for architecture patterns
            for pattern_name, pattern_data in self.architecture_patterns.items():
                score = await self._calculate_architecture_fit(requirements, pattern_data)
                
                if score > 0.7:  # Only recommend if good fit
                    recommendation = ArchitectureRecommendation(
                        id=str(uuid.uuid4()),
                        name=pattern_name.replace("_", " ").title(),
                        description=pattern_data["description"],
                        architecture_type=ArchitectureType(pattern_name),
                        pros=pattern_data.get("pros", []),
                        cons=pattern_data.get("cons", []),
                        complexity_score=pattern_data.get("complexity_score", 0.5),
                        scalability_score=pattern_data.get("scalability_score", 0.5),
                        maintainability_score=pattern_data.get("maintainability_score", 0.5),
                        cost_score=pattern_data.get("cost_score", 0.5),
                        security_score=pattern_data.get("security_score", 0.5),
                        technology_stack=pattern_data.get("technologies", {}),
                        implementation_steps=await self._generate_implementation_steps(pattern_name),
                        risks=await self._identify_architecture_risks(pattern_name),
                        alternatives=await self._find_architecture_alternatives(pattern_name)
                    )
                    recommendations.append(recommendation)
            
            return sorted(recommendations, key=lambda x: x.complexity_score, reverse=True)
            
        except Exception as e:
            logger.error(f"Architecture recommendations failed: {e}")
            return []
    
    async def _calculate_architecture_fit(
        self,
        requirements: List[Requirement],
        pattern_data: Dict[str, Any]
    ) -> float:
        """Calculate how well an architecture pattern fits the requirements"""
        try:
            # Simple scoring algorithm
            score = 0.0
            total_factors = 0
            
            # Team size factor
            if "team_size" in pattern_data:
                score += 0.2
                total_factors += 1
            
            # Complexity factor
            if "complexity" in pattern_data:
                score += 0.2
                total_factors += 1
            
            # Scalability factor
            if "scalability" in pattern_data:
                score += 0.2
                total_factors += 1
            
            # Use case matching
            use_cases = pattern_data.get("use_cases", [])
            for req in requirements:
                if any(use_case.lower() in req.description.lower() for use_case in use_cases):
                    score += 0.1
                    total_factors += 1
            
            return score / total_factors if total_factors > 0 else 0.0
            
        except Exception as e:
            logger.error(f"Architecture fit calculation failed: {e}")
            return 0.0


# Global architecture engine instance
ai_architecture_engine = AIArchitectureEngine() 