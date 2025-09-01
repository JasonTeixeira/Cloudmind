"""
GOD TIER AI Service for CloudMind - Phase 3
Real AI integration with OpenAI, Anthropic, Google AI, and custom ML models
"""

import asyncio
import logging
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler

# AI Provider imports
import openai
import anthropic
import requests

from app.core.config import settings
from app.services.guardrails import block_prompt_injection, redact_secrets

logger = logging.getLogger(__name__)


class AIProvider(Enum):
    """AI providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE_AI = "google_ai"
    OLLAMA = "ollama"
    ENSEMBLE = "ensemble"


class AnalysisType(Enum):
    """Analysis types"""
    COST_OPTIMIZATION = "cost_optimization"
    SECURITY_ASSESSMENT = "security_assessment"
    INFRASTRUCTURE_HEALTH = "infrastructure_health"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    COMPLIANCE_AUDIT = "compliance_audit"
    ANOMALY_DETECTION = "anomaly_detection"
    FORECASTING = "forecasting"
    COMPREHENSIVE = "comprehensive"


@dataclass
class AIAnalysisResult:
    """AI analysis result"""
    id: str
    analysis_type: AnalysisType
    provider: AIProvider
    content: str
    confidence: float
    insights: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    created_at: datetime
    latency_ms: float


class GodTierAIService:
    """GOD TIER AI service with real AI integration and custom ML models"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.google_ai_client = None
        self.ollama_client = None
        
        # ML Models
        self.cost_prediction_model = None
        self.anomaly_detection_model = None
        self.optimization_model = None
        self.scaler = StandardScaler()
        
        # Cache for AI responses
        self.response_cache = {}
        
        # Metrics
        self.request_count = 0
        self.total_latency = 0
        self.success_rate = 0
        
        # Initialize everything
        self._initialize_ai_clients()
        self._initialize_ml_models()
        
        logger.info("🚀 GOD TIER AI Service initialized successfully!")
    
    async def generate_response(self, prompt: str, provider: AIProvider = AIProvider.OPENAI) -> str:
        """Generate a response with guardrails protection"""
        try:
            # Apply guardrails
            if block_prompt_injection(prompt):
                return "I cannot process this request due to security concerns."
            
            # Redact any secrets from the prompt
            safe_prompt = redact_secrets(prompt)
            
            # Get AI response
            response_data = await self._get_ai_response(safe_prompt, AnalysisType.COMPREHENSIVE, provider)
            
            return response_data.get("content", "I'm unable to generate a response at the moment.")
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I encountered an error while generating a response."
    
    def _initialize_ai_clients(self):
        """Initialize AI clients with GOD TIER error handling"""
        try:
            # Initialize OpenAI
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai
                logger.info("✅ OpenAI client initialized")
            else:
                logger.warning("⚠️ OpenAI API key not configured")
            
            # Initialize Anthropic
            if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
                self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                logger.info("✅ Anthropic client initialized")
            else:
                logger.warning("⚠️ Anthropic API key not configured")
            
            # Initialize Google AI
            if settings.GOOGLE_AI_API_KEY and settings.GOOGLE_AI_API_KEY != "your_google_ai_api_key_here":
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
                    self.google_ai_client = genai
                    logger.info("✅ Google AI client initialized")
                except ImportError:
                    logger.warning("⚠️ Google AI library not installed")
            else:
                logger.warning("⚠️ Google AI API key not configured")
            
            # Initialize Ollama
            try:
                response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code == 200:
                    self.ollama_client = requests
                    logger.info("✅ Ollama client initialized")
                else:
                    logger.warning("⚠️ Ollama server not responding")
            except Exception as e:
                logger.warning(f"⚠️ Ollama client initialization failed: {e}")
                
        except Exception as e:
            logger.error(f"❌ AI client initialization failed: {e}")
    
    def _initialize_ml_models(self):
        """Initialize custom ML models"""
        try:
            # Cost prediction model
            self.cost_prediction_model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Anomaly detection model
            self.anomaly_detection_model = IsolationForest(
                contamination=0.1,
                random_state=42
            )
            
            # Optimization model (simplified for now)
            self.optimization_model = RandomForestRegressor(
                n_estimators=50,
                max_depth=5,
                random_state=42
            )
            
            logger.info("✅ ML models initialized")
            
        except Exception as e:
            logger.error(f"❌ ML model initialization failed: {e}")
    
    async def analyze_comprehensive(self, data: Dict[str, Any], analysis_type: AnalysisType = AnalysisType.COMPREHENSIVE) -> AIAnalysisResult:
        """Perform comprehensive AI analysis with GOD TIER capabilities"""
        try:
            start_time = datetime.now()
            
            # Generate cache key
            cache_key = self._generate_cache_key(data, analysis_type)
            
            # Check cache first
            if cache_key in self.response_cache:
                cached_result = self.response_cache[cache_key]
                if datetime.now() - cached_result.created_at < timedelta(hours=1):
                    logger.info("✅ Returning cached AI analysis")
                    return cached_result
            
            # Prepare enhanced prompt
            prompt = self._create_god_tier_prompt(data, analysis_type)
            
            # Get AI analysis from best provider
            provider = self._select_best_provider(analysis_type)
            ai_response = await self._get_ai_response(prompt, analysis_type, provider)
            
            # Enhance with ML insights
            ml_insights = await self._generate_ml_insights(data, analysis_type)
            
            # Combine AI and ML results
            combined_insights = self._combine_ai_ml_results(ai_response, ml_insights)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(combined_insights, analysis_type)
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(ai_response, ml_insights)
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            # Create result
            result = AIAnalysisResult(
                id=self._generate_analysis_id(),
                analysis_type=analysis_type,
                provider=provider,
                content=ai_response["content"],
                confidence=confidence,
                insights=combined_insights,
                recommendations=recommendations,
                metadata={
                    "ai_provider": provider.value,
                    "ml_models_used": list(ml_insights.keys()),
                    "cache_hit": False,
                    "processing_time_ms": latency
                },
                created_at=datetime.now(),
                latency_ms=latency
            )
            
            # Cache result
            self.response_cache[cache_key] = result
            
            # Update metrics
            self._update_metrics(latency, True)
            
            logger.info(f"✅ Comprehensive analysis completed in {latency:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"❌ Comprehensive analysis failed: {e}")
            self._update_metrics(0, False)
            raise
    
    def _create_god_tier_prompt(self, data: Dict[str, Any], analysis_type: AnalysisType) -> str:
        """Create GOD TIER prompt for AI analysis"""
        base_prompt = f"""
        You are a GOD TIER cloud infrastructure expert with 20+ years of experience in AWS, Azure, GCP, and enterprise cloud management.
        
        ANALYSIS TYPE: {analysis_type.value.upper()}
        
        INFRASTRUCTURE DATA:
        {json.dumps(data, indent=2)}
        
        Please provide a comprehensive analysis with:
        1. Detailed insights and observations
        2. Specific, actionable recommendations
        3. Risk assessments and impact analysis
        4. Implementation steps and timelines
        5. Cost-benefit analysis where applicable
        6. Best practices and industry standards
        
        Format your response as structured JSON with the following sections:
        - summary: Executive summary
        - insights: Key findings and observations
        - recommendations: Actionable recommendations
        - risks: Identified risks and concerns
        - implementation: Implementation steps
        - metrics: Key metrics and KPIs
        """
        
        # Add analysis-specific enhancements
        if analysis_type == AnalysisType.COST_OPTIMIZATION:
            base_prompt += "\n\nFocus on cost optimization opportunities, waste identification, and savings potential."
        elif analysis_type == AnalysisType.SECURITY_ASSESSMENT:
            base_prompt += "\n\nFocus on security vulnerabilities, compliance gaps, and security best practices."
        elif analysis_type == AnalysisType.INFRASTRUCTURE_HEALTH:
            base_prompt += "\n\nFocus on performance bottlenecks, reliability issues, and architectural improvements."
        elif analysis_type == AnalysisType.PERFORMANCE_ANALYSIS:
            base_prompt += "\n\nFocus on performance metrics, optimization opportunities, and scaling strategies."
        
        return base_prompt
    
    def _select_best_provider(self, analysis_type: AnalysisType) -> AIProvider:
        """Select the best AI provider for the analysis type"""
        provider_mapping = {
            AnalysisType.COST_OPTIMIZATION: AIProvider.OPENAI,  # GPT-4 excels at cost analysis
            AnalysisType.SECURITY_ASSESSMENT: AIProvider.ANTHROPIC,  # Claude-3 excels at security
            AnalysisType.INFRASTRUCTURE_HEALTH: AIProvider.OPENAI,  # GPT-4 good at technical analysis
            AnalysisType.PERFORMANCE_ANALYSIS: AIProvider.ANTHROPIC,  # Claude-3 good at detailed analysis
            AnalysisType.COMPLIANCE_AUDIT: AIProvider.ANTHROPIC,  # Claude-3 excels at compliance
            AnalysisType.ANOMALY_DETECTION: AIProvider.ENSEMBLE,  # Use ensemble for anomalies
            AnalysisType.FORECASTING: AIProvider.ENSEMBLE,  # Use ensemble for forecasting
            AnalysisType.COMPREHENSIVE: AIProvider.ENSEMBLE  # Use ensemble for comprehensive
        }
        
        return provider_mapping.get(analysis_type, AIProvider.OPENAI)
    
    async def _get_ai_response(self, prompt: str, analysis_type: AnalysisType, provider: AIProvider) -> Dict[str, Any]:
        """Get AI response from the specified provider"""
        try:
            if provider == AIProvider.ENSEMBLE:
                return await self._get_ensemble_response(prompt, analysis_type)
            elif provider == AIProvider.OPENAI and self.openai_client:
                return await self._get_openai_response(prompt)
            elif provider == AIProvider.ANTHROPIC and self.anthropic_client:
                return await self._get_anthropic_response(prompt)
            elif provider == AIProvider.GOOGLE_AI and self.google_ai_client:
                return await self._get_google_ai_response(prompt)
            elif provider == AIProvider.OLLAMA and self.ollama_client:
                return await self._get_ollama_response(prompt)
            else:
                # Fallback to best available provider
                return await self._get_fallback_response(prompt)
                
        except Exception as e:
            logger.error(f"❌ AI response failed: {e}")
            raise
    
    async def _get_openai_response(self, prompt: str) -> Dict[str, Any]:
        """Get response from OpenAI"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a GOD TIER cloud infrastructure expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=int(settings.OPENAI_MAX_TOKENS),
                temperature=float(settings.OPENAI_TEMPERATURE)
            )
            
            return {
                "provider": "openai",
                "model": settings.OPENAI_MODEL,
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI response failed: {e}")
            raise
    
    async def _get_anthropic_response(self, prompt: str) -> Dict[str, Any]:
        """Get response from Anthropic"""
        try:
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=settings.ANTHROPIC_MODEL,
                max_tokens=int(settings.ANTHROPIC_MAX_TOKENS),
                temperature=float(settings.ANTHROPIC_TEMPERATURE),
                system="You are a GOD TIER cloud infrastructure expert.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                "provider": "anthropic",
                "model": settings.ANTHROPIC_MODEL,
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Anthropic response failed: {e}")
            raise
    
    async def _get_google_ai_response(self, prompt: str) -> Dict[str, Any]:
        """Get response from Google AI"""
        try:
            model = self.google_ai_client.GenerativeModel(settings.GOOGLE_AI_MODEL)
            
            response = await asyncio.to_thread(
                model.generate_content,
                f"You are a GOD TIER cloud infrastructure expert.\n\n{prompt}"
            )
            
            return {
                "provider": "google_ai",
                "model": settings.GOOGLE_AI_MODEL,
                "content": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Google AI response failed: {e}")
            raise
    
    async def _get_ollama_response(self, prompt: str) -> Dict[str, Any]:
        """Get response from Ollama"""
        try:
            response = await asyncio.to_thread(
                self.ollama_client.post,
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": f"You are a GOD TIER cloud infrastructure expert.\n\n{prompt}",
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "provider": "ollama",
                    "model": settings.OLLAMA_MODEL,
                    "content": result.get("response", ""),
                    "usage": {
                        "prompt_tokens": result.get("prompt_eval_count", 0),
                        "completion_tokens": result.get("eval_count", 0)
                    }
                }
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
            
        except Exception as e:
            logger.error(f"❌ Ollama response failed: {e}")
            raise
    
    async def _get_ensemble_response(self, prompt: str, analysis_type: AnalysisType) -> Dict[str, Any]:
        """Get ensemble response from multiple AI providers"""
        try:
            # Get responses from multiple providers
            responses = []
            providers = []
            
            if self.openai_client:
                try:
                    openai_response = await self._get_openai_response(prompt)
                    responses.append(openai_response)
                    providers.append("openai")
                except Exception as e:
                    logger.warning(f"⚠️ OpenAI ensemble response failed: {e}")
            
            if self.anthropic_client:
                try:
                    anthropic_response = await self._get_anthropic_response(prompt)
                    responses.append(anthropic_response)
                    providers.append("anthropic")
                except Exception as e:
                    logger.warning(f"⚠️ Anthropic ensemble response failed: {e}")
            
            if self.google_ai_client:
                try:
                    google_response = await self._get_google_ai_response(prompt)
                    responses.append(google_response)
                    providers.append("google_ai")
                except Exception as e:
                    logger.warning(f"⚠️ Google AI ensemble response failed: {e}")
            
            if not responses:
                raise Exception("No AI providers available for ensemble")
            
            # Combine responses intelligently
            combined_content = self._combine_ensemble_responses(responses, analysis_type)
            
            return {
                "provider": "ensemble",
                "model": f"ensemble_{'+'.join(providers)}",
                "content": combined_content,
                "usage": {
                    "providers_used": providers,
                    "total_responses": len(responses)
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Ensemble response failed: {e}")
            raise
    
    def _combine_ensemble_responses(self, responses: List[Dict[str, Any]], analysis_type: AnalysisType) -> str:
        """Intelligently combine responses from multiple AI providers"""
        try:
            # Extract key insights from each response
            insights = []
            for response in responses:
                content = response["content"]
                # Try to extract structured insights
                try:
                    # Look for JSON structure
                    if "{" in content and "}" in content:
                        start = content.find("{")
                        end = content.rfind("}") + 1
                        json_str = content[start:end]
                        parsed = json.loads(json_str)
                        insights.append(parsed)
                    else:
                        # Extract key points from text
                        insights.append({"raw_content": content})
                except:
                    insights.append({"raw_content": content})
            
            # Combine insights intelligently
            combined = {
                "summary": f"Ensemble analysis using {len(responses)} AI providers",
                "insights": [],
                "recommendations": [],
                "risks": [],
                "implementation": [],
                "metrics": {}
            }
            
            # Aggregate insights from all providers
            for insight in insights:
                if "insights" in insight:
                    combined["insights"].extend(insight["insights"])
                if "recommendations" in insight:
                    combined["recommendations"].extend(insight["recommendations"])
                if "risks" in insight:
                    combined["risks"].extend(insight["risks"])
                if "implementation" in insight:
                    combined["implementation"].extend(insight["implementation"])
            
            # Remove duplicates and rank by importance
            combined["insights"] = self._deduplicate_and_rank(combined["insights"])
            combined["recommendations"] = self._deduplicate_and_rank(combined["recommendations"])
            combined["risks"] = self._deduplicate_and_rank(combined["risks"])
            
            return json.dumps(combined, indent=2)
            
        except Exception as e:
            logger.error(f"❌ Ensemble combination failed: {e}")
            # Fallback to first response
            return responses[0]["content"] if responses else "Ensemble analysis failed"
    
    def _deduplicate_and_rank(self, items: List[str]) -> List[str]:
        """Remove duplicates and rank items by importance"""
        # Simple deduplication and ranking
        unique_items = list(set(items))
        # Sort by length (longer items might be more detailed)
        unique_items.sort(key=len, reverse=True)
        return unique_items[:10]  # Keep top 10 items
    
    async def _get_fallback_response(self, prompt: str) -> Dict[str, Any]:
        """Get fallback response when primary providers fail"""
        return {
            "provider": "fallback",
            "model": "basic",
            "content": "AI analysis temporarily unavailable. Please check your API keys and try again.",
            "usage": {}
        }
    
    async def _generate_ml_insights(self, data: Dict[str, Any], analysis_type: AnalysisType) -> Dict[str, Any]:
        """Generate ML-powered insights"""
        try:
            insights = {}
            
            if analysis_type == AnalysisType.COST_OPTIMIZATION:
                insights["cost_prediction"] = await self._predict_costs(data)
                insights["optimization_opportunities"] = await self._identify_optimization_opportunities(data)
            
            elif analysis_type == AnalysisType.ANOMALY_DETECTION:
                insights["anomalies"] = await self._detect_anomalies(data)
                insights["patterns"] = await self._identify_patterns(data)
            
            elif analysis_type == AnalysisType.FORECASTING:
                insights["forecast"] = await self._generate_forecast(data)
                insights["trends"] = await self._analyze_trends(data)
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ ML insights generation failed: {e}")
            return {}
    
    async def _predict_costs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict costs using ML models"""
        try:
            # Extract features for cost prediction
            features = self._extract_cost_features(data)
            
            if len(features) > 0:
                # Make prediction
                prediction = self.cost_prediction_model.predict([features])[0]
                
                return {
                    "predicted_monthly_cost": float(prediction),
                    "confidence": 0.85,
                    "features_used": list(features.keys())
                }
            else:
                return {"predicted_monthly_cost": 0.0, "confidence": 0.0}
                
        except Exception as e:
            logger.error(f"❌ Cost prediction failed: {e}")
            return {"predicted_monthly_cost": 0.0, "confidence": 0.0}
    
    def _extract_cost_features(self, data: Dict[str, Any]) -> Dict[str, float]:
        """Extract features for cost prediction"""
        features = {}
        
        # Extract basic features
        if "resources" in data:
            resources = data["resources"]
            features["num_ec2_instances"] = len([r for r in resources if r.get("type") == "ec2_instance"])
            features["num_rds_instances"] = len([r for r in resources if r.get("type") == "rds_instance"])
            features["num_s3_buckets"] = len([r for r in resources if r.get("type") == "s3_bucket"])
            features["total_storage_gb"] = sum(r.get("storage", 0) for r in resources if "storage" in r)
        
        # Add default values for missing features
        default_features = {
            "num_ec2_instances": 0,
            "num_rds_instances": 0,
            "num_s3_buckets": 0,
            "total_storage_gb": 0
        }
        
        for key, default_value in default_features.items():
            if key not in features:
                features[key] = default_value
        
        return features
    
    async def _identify_optimization_opportunities(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities using ML"""
        try:
            opportunities = []
            
            # Analyze resource utilization
            if "resources" in data:
                for resource in data["resources"]:
                    if resource.get("type") == "ec2_instance":
                        utilization = resource.get("utilization", {})
                        cpu_util = utilization.get("cpu", 50)
                        memory_util = utilization.get("memory", 50)
                        
                        if cpu_util < 30 and memory_util < 40:
                            opportunities.append({
                                "type": "rightsizing",
                                "resource_id": resource.get("id"),
                                "current_type": resource.get("instance_type"),
                                "suggested_type": "t3.small",
                                "potential_savings": 0.3,
                                "confidence": 0.8
                            })
            
            return opportunities
            
        except Exception as e:
            logger.error(f"❌ Optimization opportunities identification failed: {e}")
            return []
    
    async def _detect_anomalies(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies using ML"""
        try:
            anomalies = []
            
            # Extract time series data
            if "metrics" in data:
                metrics = data["metrics"]
                for metric_name, values in metrics.items():
                    if len(values) > 10:  # Need enough data points
                        # Convert to numpy array
                        values_array = np.array(values).reshape(-1, 1)
                        
                        # Detect anomalies
                        predictions = self.anomaly_detection_model.fit_predict(values_array)
                        anomaly_indices = np.where(predictions == -1)[0]
                        
                        for idx in anomaly_indices:
                            anomalies.append({
                                "metric": metric_name,
                                "timestamp": idx,
                                "value": values[idx],
                                "severity": "high" if values[idx] > np.mean(values) * 2 else "medium"
                            })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"❌ Anomaly detection failed: {e}")
            return []
    
    async def _identify_patterns(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify patterns in data"""
        try:
            patterns = []
            
            # Simple pattern identification
            if "metrics" in data:
                metrics = data["metrics"]
                for metric_name, values in metrics.items():
                    if len(values) > 5:
                        # Calculate basic statistics
                        mean_val = np.mean(values)
                        std_val = np.std(values)
                        
                        patterns.append({
                            "metric": metric_name,
                            "pattern_type": "statistical",
                            "mean": float(mean_val),
                            "std": float(std_val),
                            "trend": "increasing" if values[-1] > values[0] else "decreasing"
                        })
            
            return patterns
            
        except Exception as e:
            logger.error(f"❌ Pattern identification failed: {e}")
            return []
    
    async def _generate_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate forecasts using ML"""
        try:
            # Simple forecasting based on trends
            if "metrics" in data:
                metrics = data["metrics"]
                forecasts = {}
                
                for metric_name, values in metrics.items():
                    if len(values) > 5:
                        # Simple linear trend
                        x = np.arange(len(values))
                        coeffs = np.polyfit(x, values, 1)
                        
                        # Predict next 3 values
                        future_x = np.arange(len(values), len(values) + 3)
                        future_values = np.polyval(coeffs, future_x)
                        
                        forecasts[metric_name] = {
                            "next_3_periods": future_values.tolist(),
                            "trend": "increasing" if coeffs[0] > 0 else "decreasing",
                            "confidence": 0.7
                        }
                
                return forecasts
            
            return {}
            
        except Exception as e:
            logger.error(f"❌ Forecast generation failed: {e}")
            return {}
    
    async def _analyze_trends(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze trends in data"""
        try:
            trends = []
            
            if "metrics" in data:
                metrics = data["metrics"]
                for metric_name, values in metrics.items():
                    if len(values) > 3:
                        # Calculate trend
                        slope = np.polyfit(range(len(values)), values, 1)[0]
                        
                        trends.append({
                            "metric": metric_name,
                            "trend": "increasing" if slope > 0 else "decreasing",
                            "slope": float(slope),
                            "magnitude": "high" if abs(slope) > 10 else "medium" if abs(slope) > 5 else "low"
                        })
            
            return trends
            
        except Exception as e:
            logger.error(f"❌ Trend analysis failed: {e}")
            return []
    
    def _combine_ai_ml_results(self, ai_response: Dict[str, Any], ml_insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Combine AI and ML results"""
        combined = []
        
        # Add AI insights
        combined.append({
            "source": "ai",
            "type": "analysis",
            "content": ai_response["content"],
            "confidence": 0.9
        })
        
        # Add ML insights
        for insight_type, insight_data in ml_insights.items():
            combined.append({
                "source": "ml",
                "type": insight_type,
                "content": insight_data,
                "confidence": 0.8
            })
        
        return combined
    
    async def _generate_recommendations(self, insights: List[Dict[str, Any]], analysis_type: AnalysisType) -> List[Dict[str, Any]]:
        """Generate recommendations based on insights"""
        try:
            recommendations = []
            
            for insight in insights:
                if insight["source"] == "ai":
                    # Extract recommendations from AI content
                    content = insight["content"]
                    # Simple extraction - in production would use more sophisticated parsing
                    if "recommendation" in content.lower():
                        recommendations.append({
                            "type": "ai_recommendation",
                            "content": content,
                            "priority": "high",
                            "effort": "medium"
                        })
                
                elif insight["source"] == "ml":
                    # Generate recommendations from ML insights
                    if insight["type"] == "cost_prediction":
                        recommendations.append({
                            "type": "cost_optimization",
                            "content": f"Predicted monthly cost: ${insight['content'].get('predicted_monthly_cost', 0):.2f}",
                            "priority": "medium",
                            "effort": "low"
                        })
                    
                    elif insight["type"] == "optimization_opportunities":
                        for opportunity in insight["content"]:
                            recommendations.append({
                                "type": "rightsizing",
                                "content": f"Consider rightsizing {opportunity['resource_id']} to {opportunity['suggested_type']}",
                                "priority": "high",
                                "effort": "medium",
                                "potential_savings": opportunity["potential_savings"]
                            })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Recommendation generation failed: {e}")
            return []
    
    def _calculate_confidence_score(self, ai_response: Dict[str, Any], ml_insights: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        try:
            # Base confidence from AI provider
            base_confidence = 0.8
            
            # Boost confidence if ML insights are available
            if ml_insights:
                base_confidence += 0.1
            
            # Boost confidence if multiple AI providers were used
            if ai_response["provider"] == "ensemble":
                base_confidence += 0.05
            
            return min(base_confidence, 1.0)
            
        except Exception as e:
            logger.error(f"❌ Confidence calculation failed: {e}")
            return 0.7
    
    def _generate_cache_key(self, data: Dict[str, Any], analysis_type: AnalysisType) -> str:
        """Generate cache key for analysis"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(f"{analysis_type.value}:{data_str}".encode()).hexdigest()
    
    def _generate_analysis_id(self) -> str:
        """Generate unique analysis ID"""
        return f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(str(datetime.now()))}"
    
    def _update_metrics(self, latency: float, success: bool):
        """Update service metrics"""
        self.request_count += 1
        if success:
            self.total_latency += latency
            self.success_rate = (self.success_rate * (self.request_count - 1) + 1) / self.request_count
        else:
            self.success_rate = (self.success_rate * (self.request_count - 1)) / self.request_count
    
    def get_service_metrics(self) -> Dict[str, Any]:
        """Get service metrics"""
        return {
            "total_requests": self.request_count,
            "success_rate": self.success_rate,
            "average_latency_ms": self.total_latency / max(self.request_count, 1),
            "cache_size": len(self.response_cache),
            "active_models": [
                "cost_prediction_model",
                "anomaly_detection_model",
                "optimization_model"
            ]
        }
