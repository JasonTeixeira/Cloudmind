"""
Advanced AI Service for CloudMind
Provides sophisticated AI-powered analysis, insights, and recommendations
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
import numpy as np
from dataclasses import dataclass
from enum import Enum

from app.core.config import settings
from app.services.ai_engine.ai_providers import OpenAIProvider, AnthropicProvider, OllamaProvider

logger = logging.getLogger(__name__)


class AnalysisType(Enum):
    """Types of AI analysis"""
    COST_OPTIMIZATION = "cost_optimization"
    SECURITY_ASSESSMENT = "security_assessment"
    INFRASTRUCTURE_HEALTH = "infrastructure_health"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    COMPLIANCE_AUDIT = "compliance_audit"
    ANOMALY_DETECTION = "anomaly_detection"
    FORECASTING = "forecasting"
    COMPREHENSIVE = "comprehensive"


class InsightPriority(Enum):
    """Insight priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AIInsight:
    """AI-generated insight"""
    id: str
    title: str
    description: str
    priority: InsightPriority
    category: str
    confidence: float
    impact_score: float
    recommendations: List[str]
    metadata: Dict[str, Any]
    created_at: datetime


@dataclass
class AIRecommendation:
    """AI-generated recommendation"""
    id: str
    title: str
    description: str
    category: str
    impact_score: float
    effort_level: str
    estimated_savings: Optional[float]
    implementation_steps: List[str]
    risks: List[str]
    prerequisites: List[str]
    created_at: datetime


class AdvancedAIService:
    """Advanced AI service with multiple models and sophisticated analysis"""
    
    def __init__(self):
        self.openai_provider = OpenAIProvider()
        self.anthropic_provider = AnthropicProvider()
        self.ollama_provider = OllamaProvider()
        
        # Model configurations for different tasks
        self.model_configs = {
            AnalysisType.COST_OPTIMIZATION: {
                "primary": "gpt-4",
                "fallback": "claude-3-sonnet",
                "local": "llama2:70b"
            },
            AnalysisType.SECURITY_ASSESSMENT: {
                "primary": "claude-3-sonnet",
                "fallback": "gpt-4",
                "local": "llama2:70b"
            },
            AnalysisType.INFRASTRUCTURE_HEALTH: {
                "primary": "gpt-4",
                "fallback": "claude-3-sonnet",
                "local": "llama2:70b"
            },
            AnalysisType.PERFORMANCE_ANALYSIS: {
                "primary": "claude-3-sonnet",
                "fallback": "gpt-4",
                "local": "llama2:70b"
            },
            AnalysisType.COMPLIANCE_AUDIT: {
                "primary": "claude-3-sonnet",
                "fallback": "gpt-4",
                "local": "llama2:70b"
            },
            AnalysisType.ANOMALY_DETECTION: {
                "primary": "gpt-4",
                "fallback": "claude-3-sonnet",
                "local": "llama2:70b"
            },
            AnalysisType.FORECASTING: {
                "primary": "gpt-4",
                "fallback": "claude-3-sonnet",
                "local": "llama2:70b"
            },
            AnalysisType.COMPREHENSIVE: {
                "primary": "claude-3-sonnet",
                "fallback": "gpt-4",
                "local": "llama2:70b"
            }
        }
    
    async def analyze_comprehensive(
        self,
        project_data: Dict[str, Any],
        include_cost: bool = True,
        include_security: bool = True,
        include_infrastructure: bool = True,
        include_performance: bool = True,
        include_compliance: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis across all domains
        
        Args:
            project_data: Complete project data including costs, security, infrastructure
            include_cost: Whether to include cost analysis
            include_security: Whether to include security analysis
            include_infrastructure: Whether to include infrastructure analysis
            include_performance: Whether to include performance analysis
            include_compliance: Whether to include compliance analysis
            
        Returns:
            Comprehensive analysis results with insights and recommendations
        """
        try:
            logger.info("Starting comprehensive AI analysis")
            
            # Prepare analysis tasks
            tasks = []
            
            if include_cost:
                tasks.append(self._analyze_cost_optimization(project_data))
            
            if include_security:
                tasks.append(self._analyze_security_assessment(project_data))
            
            if include_infrastructure:
                tasks.append(self._analyze_infrastructure_health(project_data))
            
            if include_performance:
                tasks.append(self._analyze_performance(project_data))
            
            if include_compliance:
                tasks.append(self._analyze_compliance(project_data))
            
            # Execute all analyses concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            analysis_results = {}
            all_insights = []
            all_recommendations = []
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(f"Analysis task {i} failed: {result}")
                    continue
                
                analysis_results[f"analysis_{i}"] = result
                all_insights.extend(result.get("insights", []))
                all_recommendations.extend(result.get("recommendations", []))
            
            # Generate cross-domain insights
            cross_domain_insights = await self._generate_cross_domain_insights(
                project_data, all_insights
            )
            
            # Prioritize recommendations
            prioritized_recommendations = await self._prioritize_recommendations(
                all_recommendations
            )
            
            # Generate executive summary
            executive_summary = await self._generate_executive_summary(
                project_data, all_insights, prioritized_recommendations
            )
            
            return {
                "success": True,
                "analysis_type": "comprehensive",
                "timestamp": datetime.utcnow().isoformat(),
                "executive_summary": executive_summary,
                "insights": all_insights + cross_domain_insights,
                "recommendations": prioritized_recommendations,
                "analysis_results": analysis_results,
                "metadata": {
                    "total_insights": len(all_insights) + len(cross_domain_insights),
                    "total_recommendations": len(prioritized_recommendations),
                    "analysis_domains": len(tasks)
                }
            }
            
        except Exception as e:
            logger.error(f"Comprehensive analysis failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    async def _analyze_cost_optimization(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cost optimization opportunities"""
        try:
            cost_data = project_data.get("cost_data", {})
            
            prompt = f"""
            Analyze the following cloud cost data and provide optimization recommendations:
            
            Cost Data: {json.dumps(cost_data, indent=2)}
            
            Please provide:
            1. Cost optimization insights with confidence scores
            2. Specific recommendations with estimated savings
            3. Implementation steps for each recommendation
            4. Risk assessment for each recommendation
            5. Priority ranking based on impact and effort
            
            Format the response as JSON with the following structure:
            {{
                "insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "string",
                        "recommendations": ["string"],
                        "metadata": {{}}
                    }}
                ],
                "recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "string",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "estimated_savings": 0.0,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"]
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.COST_OPTIMIZATION
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Cost optimization analysis failed: {e}")
            return {"insights": [], "recommendations": []}
    
    async def _analyze_security_assessment(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security posture and vulnerabilities"""
        try:
            security_data = project_data.get("security_data", {})
            
            prompt = f"""
            Analyze the following security data and provide security assessment:
            
            Security Data: {json.dumps(security_data, indent=2)}
            
            Please provide:
            1. Security insights with risk levels
            2. Vulnerability assessment with severity
            3. Compliance status and gaps
            4. Security improvement recommendations
            5. Threat modeling and risk assessment
            
            Format the response as JSON with the following structure:
            {{
                "insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "security",
                        "recommendations": ["string"],
                        "metadata": {{
                            "risk_level": "string",
                            "vulnerability_type": "string",
                            "compliance_framework": "string"
                        }}
                    }}
                ],
                "recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "security",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "estimated_savings": null,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"]
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.SECURITY_ASSESSMENT
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Security assessment failed: {e}")
            return {"insights": [], "recommendations": []}
    
    async def _analyze_infrastructure_health(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze infrastructure health and optimization"""
        try:
            infrastructure_data = project_data.get("infrastructure_data", {})
            
            prompt = f"""
            Analyze the following infrastructure data and provide health assessment:
            
            Infrastructure Data: {json.dumps(infrastructure_data, indent=2)}
            
            Please provide:
            1. Infrastructure health insights
            2. Performance optimization opportunities
            3. Resource utilization analysis
            4. Scalability recommendations
            5. Reliability and availability improvements
            
            Format the response as JSON with the following structure:
            {{
                "insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "infrastructure",
                        "recommendations": ["string"],
                        "metadata": {{
                            "health_score": 0.0-1.0,
                            "utilization_level": "string",
                            "performance_metric": "string"
                        }}
                    }}
                ],
                "recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "infrastructure",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "estimated_savings": 0.0,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"]
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.INFRASTRUCTURE_HEALTH
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Infrastructure health analysis failed: {e}")
            return {"insights": [], "recommendations": []}
    
    async def _analyze_performance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics and bottlenecks"""
        try:
            performance_data = project_data.get("performance_data", {})
            
            prompt = f"""
            Analyze the following performance data and provide performance insights:
            
            Performance Data: {json.dumps(performance_data, indent=2)}
            
            Please provide:
            1. Performance bottleneck identification
            2. Optimization opportunities
            3. Capacity planning recommendations
            4. Performance monitoring improvements
            5. Scalability analysis
            
            Format the response as JSON with the following structure:
            {{
                "insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "performance",
                        "recommendations": ["string"],
                        "metadata": {{
                            "performance_metric": "string",
                            "bottleneck_type": "string",
                            "impact_level": "string"
                        }}
                    }}
                ],
                "recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "performance",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "estimated_savings": 0.0,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"]
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.PERFORMANCE_ANALYSIS
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Performance analysis failed: {e}")
            return {"insights": [], "recommendations": []}
    
    async def _analyze_compliance(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compliance status and gaps"""
        try:
            compliance_data = project_data.get("compliance_data", {})
            
            prompt = f"""
            Analyze the following compliance data and provide compliance assessment:
            
            Compliance Data: {json.dumps(compliance_data, indent=2)}
            
            Please provide:
            1. Compliance status assessment
            2. Gap analysis for each framework
            3. Remediation recommendations
            4. Risk assessment for non-compliance
            5. Compliance monitoring improvements
            
            Format the response as JSON with the following structure:
            {{
                "insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "compliance",
                        "recommendations": ["string"],
                        "metadata": {{
                            "compliance_framework": "string",
                            "compliance_status": "string",
                            "gap_severity": "string"
                        }}
                    }}
                ],
                "recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "compliance",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "estimated_savings": null,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"]
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.COMPLIANCE_AUDIT
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Compliance analysis failed: {e}")
            return {"insights": [], "recommendations": []}
    
    async def _generate_cross_domain_insights(
        self, 
        project_data: Dict[str, Any], 
        existing_insights: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate insights that span multiple domains"""
        try:
            prompt = f"""
            Analyze the following insights from different domains and identify cross-domain patterns:
            
            Existing Insights: {json.dumps(existing_insights, indent=2)}
            Project Data: {json.dumps(project_data, indent=2)}
            
            Please identify:
            1. Patterns that span multiple domains (cost, security, infrastructure, performance)
            2. Synergistic opportunities across domains
            3. Potential conflicts between recommendations
            4. Holistic optimization strategies
            5. Root cause analysis for multi-domain issues
            
            Format the response as JSON with cross-domain insights:
            {{
                "cross_domain_insights": [
                    {{
                        "title": "string",
                        "description": "string",
                        "priority": "critical|high|medium|low",
                        "confidence": 0.0-1.0,
                        "impact_score": 0.0-1.0,
                        "category": "cross_domain",
                        "recommendations": ["string"],
                        "metadata": {{
                            "affected_domains": ["string"],
                            "synergy_type": "string",
                            "root_cause": "string"
                        }}
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.COMPREHENSIVE
            )
            
            result = json.loads(response)
            return result.get("cross_domain_insights", [])
            
        except Exception as e:
            logger.error(f"Cross-domain insights generation failed: {e}")
            return []
    
    async def _prioritize_recommendations(
        self, 
        recommendations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Prioritize recommendations based on impact and effort"""
        try:
            prompt = f"""
            Prioritize the following recommendations based on impact, effort, and strategic value:
            
            Recommendations: {json.dumps(recommendations, indent=2)}
            
            Please:
            1. Score each recommendation on impact (0-1) and effort (0-1)
            2. Calculate ROI score (impact/effort)
            3. Consider dependencies between recommendations
            4. Group recommendations by implementation phase
            5. Identify quick wins vs strategic initiatives
            
            Format the response as JSON with prioritized recommendations:
            {{
                "prioritized_recommendations": [
                    {{
                        "title": "string",
                        "description": "string",
                        "category": "string",
                        "impact_score": 0.0-1.0,
                        "effort_level": "low|medium|high",
                        "roi_score": 0.0-1.0,
                        "implementation_phase": "immediate|short_term|long_term",
                        "estimated_savings": 0.0,
                        "implementation_steps": ["string"],
                        "risks": ["string"],
                        "prerequisites": ["string"],
                        "dependencies": ["string"],
                        "priority_rank": 1
                    }}
                ]
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.COMPREHENSIVE
            )
            
            result = json.loads(response)
            return result.get("prioritized_recommendations", [])
            
        except Exception as e:
            logger.error(f"Recommendation prioritization failed: {e}")
            return recommendations
    
    async def _generate_executive_summary(
        self,
        project_data: Dict[str, Any],
        insights: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate executive summary of analysis results"""
        try:
            prompt = f"""
            Generate an executive summary of the AI analysis results:
            
            Project Data: {json.dumps(project_data, indent=2)}
            Insights: {json.dumps(insights, indent=2)}
            Recommendations: {json.dumps(recommendations, indent=2)}
            
            Please provide:
            1. Executive summary (2-3 paragraphs)
            2. Key findings and insights
            3. Top 3-5 recommendations
            4. Expected business impact
            5. Implementation roadmap
            6. Risk assessment
            
            Format the response as JSON:
            {{
                "executive_summary": "string",
                "key_findings": ["string"],
                "top_recommendations": ["string"],
                "business_impact": {{
                    "cost_savings": 0.0,
                    "security_improvement": "string",
                    "performance_gains": "string",
                    "compliance_status": "string"
                }},
                "implementation_roadmap": {{
                    "immediate_actions": ["string"],
                    "short_term_goals": ["string"],
                    "long_term_strategy": ["string"]
                }},
                "risk_assessment": {{
                    "high_risks": ["string"],
                    "mitigation_strategies": ["string"]
                }}
            }}
            """
            
            response = await self._get_ai_response(
                prompt, AnalysisType.COMPREHENSIVE
            )
            
            return json.loads(response)
            
        except Exception as e:
            logger.error(f"Executive summary generation failed: {e}")
            return {
                "executive_summary": "Analysis completed with some errors.",
                "key_findings": [],
                "top_recommendations": [],
                "business_impact": {},
                "implementation_roadmap": {},
                "risk_assessment": {}
            }
    
    async def _get_ai_response(
        self, 
        prompt: str, 
        analysis_type: AnalysisType
    ) -> str:
        """Get AI response using the best available model"""
        try:
            config = self.model_configs[analysis_type]
            
            # Try primary model first
            try:
                if config["primary"] == "gpt-4":
                    return await self.openai_provider.generate_response(prompt)
                elif config["primary"] == "claude-3-sonnet":
                    return await self.anthropic_provider.generate_response(prompt)
                elif config["primary"] == "llama2:70b":
                    return await self.ollama_provider.generate_response(prompt)
            except Exception as e:
                logger.warning(f"Primary model failed: {e}")
            
            # Try fallback model
            try:
                if config["fallback"] == "gpt-4":
                    return await self.openai_provider.generate_response(prompt)
                elif config["fallback"] == "claude-3-sonnet":
                    return await self.anthropic_provider.generate_response(prompt)
            except Exception as e:
                logger.warning(f"Fallback model failed: {e}")
            
            # Try local model as last resort
            try:
                return await self.ollama_provider.generate_response(prompt)
            except Exception as e:
                logger.error(f"All AI models failed: {e}")
                raise e
                
        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            raise e
    
    async def detect_anomalies(
        self, 
        time_series_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Detect anomalies in time series data"""
        try:
            # Convert to numerical data for analysis
            values = [point.get("value", 0) for point in time_series_data]
            
            if len(values) < 3:
                return []
            
            # Calculate statistical measures
            mean = np.mean(values)
            std = np.std(values)
            
            # Detect anomalies (values beyond 2 standard deviations)
            anomalies = []
            for i, point in enumerate(time_series_data):
                value = point.get("value", 0)
                z_score = abs((value - mean) / std) if std > 0 else 0
                
                if z_score > 2.0:  # Anomaly threshold
                    anomalies.append({
                        "timestamp": point.get("timestamp"),
                        "value": value,
                        "z_score": z_score,
                        "severity": "high" if z_score > 3.0 else "medium",
                        "description": f"Anomaly detected: {value} (z-score: {z_score:.2f})"
                    })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return []
    
    async def forecast_trends(
        self, 
        historical_data: List[Dict[str, Any]], 
        forecast_periods: int = 12
    ) -> Dict[str, Any]:
        """Forecast trends based on historical data"""
        try:
            # Simple linear regression for forecasting
            values = [point.get("value", 0) for point in historical_data]
            
            if len(values) < 2:
                return {"forecast": [], "confidence": 0.0}
            
            # Calculate trend
            x = np.arange(len(values))
            slope, intercept = np.polyfit(x, values, 1)
            
            # Generate forecast
            forecast_x = np.arange(len(values), len(values) + forecast_periods)
            forecast_values = slope * forecast_x + intercept
            
            # Calculate confidence based on R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((values - y_pred) ** 2)
            ss_tot = np.sum((values - np.mean(values)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            forecast = []
            for i, value in enumerate(forecast_values):
                forecast.append({
                    "period": len(values) + i + 1,
                    "value": max(0, value),  # Ensure non-negative
                    "confidence": r_squared
                })
            
            return {
                "forecast": forecast,
                "confidence": r_squared,
                "trend": "increasing" if slope > 0 else "decreasing",
                "slope": slope
            }
            
        except Exception as e:
            logger.error(f"Trend forecasting failed: {e}")
            return {"forecast": [], "confidence": 0.0} 