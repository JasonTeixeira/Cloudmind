"""
ML-Powered Optimization System for CloudMind
Advanced cost optimization, predictive analytics, and automated recommendations
"""

import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import joblib
import json

from app.core.config import settings
from app.services.ai_engine.ensemble_ai import ensemble_ai, ConsensusMethod
from app.services.ai_engine.god_tier_ai_service import AnalysisType
from app.services.ml.ml_framework import MLModelFramework, ModelType, ModelStatus
from app.services.ml.data_pipeline import DataPipeline
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


class OptimizationType(Enum):
    """Types of optimization strategies"""
    COST_OPTIMIZATION = "cost_optimization"
    PERFORMANCE_OPTIMIZATION = "performance_optimization"
    RESOURCE_RIGHTSIZING = "resource_rightsizing"
    CAPACITY_PLANNING = "capacity_planning"
    SECURITY_OPTIMIZATION = "security_optimization"


@dataclass
class OptimizationRecommendation:
    """ML-powered optimization recommendation"""
    recommendation_id: str
    optimization_type: OptimizationType
    resource_id: str
    resource_type: str
    current_state: Dict[str, Any]
    recommended_state: Dict[str, Any]
    expected_savings: float
    confidence_score: float
    implementation_effort: str  # "low", "medium", "high"
    risk_level: str  # "low", "medium", "high"
    reasoning: str
    ml_model_used: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


@dataclass
class PredictiveAnalysis:
    """Predictive analysis results"""
    analysis_id: str
    resource_id: str
    resource_type: str
    prediction_type: str  # "cost_forecast", "usage_forecast", "performance_forecast"
    current_value: float
    predicted_value: float
    confidence_interval: Tuple[float, float]
    trend_direction: str  # "increasing", "decreasing", "stable"
    factors: List[str]
    model_accuracy: float
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)


class MLOptimizer:
    """Advanced ML-powered optimization system"""
    
    def __init__(self):
        self.ml_framework = MLModelFramework()
        self.data_pipeline = DataPipeline()
        self.optimization_history: List[OptimizationRecommendation] = []
        self.predictive_analyses: List[PredictiveAnalysis] = []
        self.models: Dict[str, Any] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        # Expose ensemble_ai for easier testing/mocking
        try:
            from app.services.ai_engine.ensemble_ai import ensemble_ai as _ensemble
            self.ensemble_ai = _ensemble
        except Exception:
            self.ensemble_ai = None
        
        # Initialize optimization models
        self._initialize_models()
        
        logger.info("🤖 ML Optimizer initialized")
    
    def _initialize_models(self):
        """Initialize ML models for different optimization types"""
        try:
            # Cost optimization model
            self.models['cost_optimization'] = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            
            # Performance optimization model
            self.models['performance_optimization'] = RandomForestRegressor(
                n_estimators=100,
                max_depth=8,
                random_state=42
            )
            
            # Resource right-sizing model
            self.models['resource_rightsizing'] = RandomForestClassifier(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
            
            # Initialize scalers
            for model_name in self.models.keys():
                self.scalers[model_name] = StandardScaler()
                
            logger.info("✅ ML models initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize models: {e}")
    
    async def generate_optimization_recommendations(
        self,
        resources: List[Dict[str, Any]],
        optimization_type: OptimizationType = OptimizationType.COST_OPTIMIZATION,
        include_ai_analysis: bool = True
    ) -> List[OptimizationRecommendation]:
        """Generate ML-powered optimization recommendations"""
        try:
            logger.info(f"🎯 Generating {optimization_type.value} recommendations for {len(resources)} resources")
            
            recommendations = []
            
            for resource in resources:
                # Generate ML-based recommendation
                ml_recommendation = await self._generate_ml_recommendation(
                    resource, optimization_type
                )
                
                if ml_recommendation:
                    recommendations.append(ml_recommendation)
                
                # Add AI analysis if requested
                if include_ai_analysis:
                    ai_recommendation = await self._generate_ai_recommendation(
                        resource, optimization_type
                    )
                    if ai_recommendation:
                        recommendations.append(ai_recommendation)
            
            # Store recommendations
            self.optimization_history.extend(recommendations)
            
            logger.info(f"✅ Generated {len(recommendations)} optimization recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to generate optimization recommendations: {e}")
            return []
    
    async def _generate_ml_recommendation(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType
    ) -> Optional[OptimizationRecommendation]:
        """Generate ML-based optimization recommendation"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Prepare features for ML model
            features = self._extract_ml_features(resource, optimization_type)
            
            if features is None:
                return None
            
            # Get model prediction
            model_name = optimization_type.value
            if model_name not in self.models:
                logger.warning(f"Model {model_name} not available")
                return None
            
            # Make prediction
            prediction = await self._make_ml_prediction(features, model_name)
            
            if prediction is None:
                return None
            
            # Generate recommendation based on prediction
            recommendation = await self._create_ml_recommendation(
                resource, optimization_type, float(prediction), features
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to generate ML recommendation: {e}")
            return None
    
    def _extract_ml_features(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType
    ) -> Optional[np.ndarray]:
        """Extract features for ML model"""
        try:
            features = []
            
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                # Cost optimization features
                features = [
                    resource.get('cost_per_hour', 0),
                    resource.get('utilization_rate', 0),
                    resource.get('instance_size', 0),
                    resource.get('storage_gb', 0),
                    resource.get('network_bandwidth', 0),
                    resource.get('age_days', 0),
                    resource.get('region_cost_multiplier', 1.0)
                ]
            elif optimization_type == OptimizationType.PERFORMANCE_OPTIMIZATION:
                # Performance optimization features
                features = [
                    resource.get('cpu_utilization', 0),
                    resource.get('memory_utilization', 0),
                    resource.get('network_utilization', 0),
                    resource.get('disk_utilization', 0),
                    resource.get('response_time', 0),
                    resource.get('throughput', 0),
                    resource.get('error_rate', 0)
                ]
            elif optimization_type == OptimizationType.RESOURCE_RIGHTSIZING:
                # Resource right-sizing features
                features = [
                    resource.get('current_cpu', 0),
                    resource.get('current_memory', 0),
                    resource.get('current_storage', 0),
                    resource.get('peak_utilization', 0),
                    resource.get('average_utilization', 0),
                    resource.get('cost_per_hour', 0),
                    resource.get('performance_score', 0)
                ]
            
            if not features or all(f == 0 for f in features):
                return None
            # Special-case: if this is cost optimization and all informative fields are missing
            # (region_cost_multiplier defaults to 1.0), treat as no features
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                cost_per_hour, utilization_rate, instance_size, storage_gb, network_bandwidth, age_days, region_mult = features
                if (
                    float(cost_per_hour or 0) == 0.0
                    and float(utilization_rate or 0) == 0.0
                    and (instance_size in (0, None, ""))
                    and float(storage_gb or 0) == 0.0
                    and float(network_bandwidth or 0) == 0.0
                    and float(age_days or 0) == 0.0
                ):
                    return None
            
            # Ensure numeric dtype; convert strings like instance sizes to 0.0
            numeric_features: List[float] = []
            for v in features:
                if isinstance(v, (int, float, np.integer, np.floating)):
                    numeric_features.append(float(v))
                else:
                    try:
                        numeric_features.append(float(v))
                    except Exception:
                        numeric_features.append(0.0)
            return np.asarray(numeric_features, dtype=float).reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Failed to extract ML features: {e}")
            return None
    
    async def _make_ml_prediction(
        self,
        features: np.ndarray,
        model_name: str
    ) -> Optional[float]:
        """Make prediction using ML model"""
        try:
            # For now, use mock predictions since we don't have trained models
            # In production, you would load trained models and make real predictions
            
            if model_name == 'cost_optimization':
                # Mock cost optimization prediction
                current_cost = features[0][0]
                utilization = features[0][1]
                
                if utilization < 0.3:
                    return current_cost * 0.6  # 40% cost reduction for underutilized resources
                elif utilization < 0.6:
                    return current_cost * 0.8  # 20% cost reduction for moderately utilized resources
                else:
                    return current_cost * 0.95  # 5% cost reduction for well-utilized resources
                    
            elif model_name == 'performance_optimization':
                # Mock performance optimization prediction
                cpu_util = features[0][0]
                memory_util = features[0][1]
                
                if cpu_util > 0.8 or memory_util > 0.8:
                    return 0.2  # High optimization potential
                elif cpu_util > 0.6 or memory_util > 0.6:
                    return 0.1  # Medium optimization potential
                else:
                    return 0.05  # Low optimization potential
                    
            elif model_name == 'resource_rightsizing':
                # Mock resource right-sizing prediction
                current_cpu = features[0][0]
                current_memory = features[0][1]
                avg_util = features[0][4]
                
                if avg_util < 0.3:
                    return 0.8  # High right-sizing potential
                elif avg_util < 0.6:
                    return 0.5  # Medium right-sizing potential
                else:
                    return 0.2  # Low right-sizing potential
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to make ML prediction: {e}")
            return None
    
    async def _create_ml_recommendation(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType,
        prediction: float,
        features: np.ndarray
    ) -> OptimizationRecommendation:
        """Create ML-based optimization recommendation"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Calculate expected savings
            current_cost = resource.get('cost_per_hour', 0)
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                expected_savings = current_cost - prediction
            else:
                expected_savings = prediction * current_cost  # Optimization potential
            
            # Determine implementation effort and risk
            implementation_effort, risk_level = self._assess_implementation_risk(
                resource, optimization_type, prediction
            )
            
            # Generate reasoning
            reasoning = self._generate_ml_reasoning(
                resource, optimization_type, prediction, features
            )
            
            recommendation = OptimizationRecommendation(
                recommendation_id=f"ml_{resource_id}_{optimization_type.value}",
                optimization_type=optimization_type,
                resource_id=resource_id,
                resource_type=resource_type,
                current_state=resource,
                recommended_state=self._generate_recommended_state(
                    resource, optimization_type, prediction
                ),
                expected_savings=expected_savings,
                confidence_score=0.85,  # Mock confidence score
                implementation_effort=implementation_effort,
                risk_level=risk_level,
                reasoning=reasoning,
                ml_model_used=f"{optimization_type.value}_model"
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to create ML recommendation: {e}")
            raise
    
    async def _generate_ai_recommendation(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType
    ) -> Optional[OptimizationRecommendation]:
        """Generate AI-based optimization recommendation using ensemble AI"""
        try:
            # Create AI prompt for optimization analysis
            prompt = self._create_optimization_prompt(resource, optimization_type)
            
            # Get AI analysis
            analysis_type = AnalysisType.COST_OPTIMIZATION if optimization_type == OptimizationType.COST_OPTIMIZATION else AnalysisType.COMPREHENSIVE
            
            ai_client = self.ensemble_ai or ensemble_ai
            # Support both async and sync mocks in tests
            maybe_coro = ai_client.generate_ensemble_response(
                prompt=prompt,
                analysis_type=analysis_type,
                consensus_method=ConsensusMethod.EXPERT_VOTE
            )
            if asyncio.iscoroutine(maybe_coro):
                ai_response = await maybe_coro
            else:
                ai_response = maybe_coro
            
            # Parse AI response and create recommendation
            recommendation = self._parse_ai_recommendation(
                resource, optimization_type, ai_response
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to generate AI recommendation: {e}")
            return None
    
    def _create_optimization_prompt(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType
    ) -> str:
        """Create AI prompt for optimization analysis"""
        resource_type = resource.get('type', 'unknown')
        resource_id = resource.get('id', 'unknown')
        
        if optimization_type == OptimizationType.COST_OPTIMIZATION:
            return f"""
            Analyze this {resource_type} resource (ID: {resource_id}) for cost optimization opportunities:
            
            Current State:
            - Cost per hour: ${resource.get('cost_per_hour', 0):.2f}
            - Utilization rate: {resource.get('utilization_rate', 0):.1%}
            - Instance size: {resource.get('instance_size', 'unknown')}
            - Storage: {resource.get('storage_gb', 0)} GB
            - Age: {resource.get('age_days', 0)} days
            
            Provide specific cost optimization recommendations including:
            1. Potential savings
            2. Recommended actions
            3. Implementation effort
            4. Risk assessment
            5. Reasoning
            """
        else:
            return f"""
            Analyze this {resource_type} resource (ID: {resource_id}) for {optimization_type.value} opportunities:
            
            Resource Details: {json.dumps(resource, indent=2)}
            
            Provide specific optimization recommendations including:
            1. Current performance analysis
            2. Optimization opportunities
            3. Recommended actions
            4. Expected improvements
            5. Implementation guidance
            """
    
    def _parse_ai_recommendation(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType,
        ai_response: Any
    ) -> OptimizationRecommendation:
        """Parse AI response and create recommendation"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Extract information from AI response
            content = ai_response.final_response
            
            # Mock parsing - in production, you'd use more sophisticated parsing
            expected_savings = 0.0
            if "savings" in content.lower():
                # Extract savings from AI response
                expected_savings = resource.get('cost_per_hour', 0) * 0.2  # Mock 20% savings
            
            recommendation = OptimizationRecommendation(
                recommendation_id=f"ai_{resource_id}_{optimization_type.value}",
                optimization_type=optimization_type,
                resource_id=resource_id,
                resource_type=resource_type,
                current_state=resource,
                recommended_state=resource.copy(),  # Mock recommended state
                expected_savings=expected_savings,
                confidence_score=ai_response.confidence_score,
                implementation_effort="medium",
                risk_level="low",
                reasoning=content,
                ml_model_used="ensemble_ai"
            )
            
            return recommendation
            
        except Exception as e:
            logger.error(f"Failed to parse AI recommendation: {e}")
            raise
    
    async def generate_predictive_analysis(
        self,
        resources: List[Dict[str, Any]],
        prediction_type: str = "cost_forecast",
        forecast_days: int = 30
    ) -> List[PredictiveAnalysis]:
        """Generate predictive analysis for resources"""
        try:
            logger.info(f"🔮 Generating {prediction_type} predictions for {len(resources)} resources")
            
            analyses = []
            
            for resource in resources:
                analysis = await self._generate_single_prediction(
                    resource, prediction_type, forecast_days
                )
                
                if analysis:
                    analyses.append(analysis)
            
            # Store analyses
            self.predictive_analyses.extend(analyses)
            
            logger.info(f"✅ Generated {len(analyses)} predictive analyses")
            return analyses
            
        except Exception as e:
            logger.error(f"Failed to generate predictive analysis: {e}")
            return []
    
    async def _generate_single_prediction(
        self,
        resource: Dict[str, Any],
        prediction_type: str,
        forecast_days: int
    ) -> Optional[PredictiveAnalysis]:
        """Generate prediction for a single resource"""
        try:
            resource_id = resource.get('id', 'unknown')
            resource_type = resource.get('type', 'unknown')
            
            # Mock prediction logic
            if prediction_type == "cost_forecast":
                current_cost = resource.get('cost_per_hour', 0)
                predicted_cost = current_cost * (1 + np.random.normal(0, 0.1))  # Mock 10% variation
                confidence_interval = (predicted_cost * 0.9, predicted_cost * 1.1)
                trend_direction = "increasing" if predicted_cost > current_cost else "decreasing"
                
            elif prediction_type == "usage_forecast":
                current_usage = resource.get('utilization_rate', 0.5)
                predicted_usage = current_usage * (1 + np.random.normal(0, 0.2))
                confidence_interval = (max(0, predicted_usage - 0.1), min(1, predicted_usage + 0.1))
                trend_direction = "increasing" if predicted_usage > current_usage else "decreasing"
                
            else:
                return None
            
            analysis = PredictiveAnalysis(
                analysis_id=f"pred_{resource_id}_{prediction_type}",
                resource_id=resource_id,
                resource_type=resource_type,
                prediction_type=prediction_type,
                current_value=current_cost if prediction_type == "cost_forecast" else current_usage,
                predicted_value=predicted_cost if prediction_type == "cost_forecast" else predicted_usage,
                confidence_interval=confidence_interval,
                trend_direction=trend_direction,
                factors=["historical_usage", "seasonal_patterns", "growth_trends"],
                model_accuracy=0.85  # Mock accuracy
            )
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to generate single prediction: {e}")
            return None
    
    def _assess_implementation_risk(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType,
        prediction: float
    ) -> Tuple[str, str]:
        """Assess implementation effort and risk level"""
        try:
            # Mock risk assessment logic
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                if prediction < resource.get('cost_per_hour', 0) * 0.7:
                    return "high", "medium"  # High effort, medium risk
                else:
                    return "medium", "low"  # Medium effort, low risk
            else:
                return "medium", "low"  # Default assessment
                
        except Exception as e:
            logger.error(f"Failed to assess implementation risk: {e}")
            return "medium", "low"
    
    def _generate_ml_reasoning(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType,
        prediction: float,
        features: np.ndarray
    ) -> str:
        """Generate reasoning for ML recommendation"""
        try:
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                current_cost = resource.get('cost_per_hour', 0)
                utilization = resource.get('utilization_rate', 0)
                
                if utilization < 0.3:
                    return f"Resource is underutilized ({utilization:.1%}). Consider downsizing to reduce costs by ${current_cost - prediction:.2f}/hour."
                elif utilization < 0.6:
                    return f"Resource has moderate utilization ({utilization:.1%}). Optimization could save ${current_cost - prediction:.2f}/hour."
                else:
                    return f"Resource is well-utilized ({utilization:.1%}). Limited optimization potential."
                    
            elif optimization_type == OptimizationType.PERFORMANCE_OPTIMIZATION:
                return f"Performance optimization analysis suggests {prediction:.1%} improvement potential based on current resource metrics."
                
            elif optimization_type == OptimizationType.RESOURCE_RIGHTSIZING:
                return f"Resource right-sizing analysis indicates {prediction:.1%} potential for optimization based on utilization patterns."
            
            return "ML analysis completed with optimization recommendations."
            
        except Exception as e:
            logger.error(f"Failed to generate ML reasoning: {e}")
            return "ML analysis completed."
    
    def _generate_recommended_state(
        self,
        resource: Dict[str, Any],
        optimization_type: OptimizationType,
        prediction: float
    ) -> Dict[str, Any]:
        """Generate recommended state based on optimization"""
        try:
            recommended_state = resource.copy()
            
            if optimization_type == OptimizationType.COST_OPTIMIZATION:
                # Mock cost optimization recommendations
                current_cost = resource.get('cost_per_hour', 0)
                if prediction < current_cost * 0.8:
                    recommended_state['recommended_instance_size'] = 'smaller'
                    recommended_state['estimated_cost'] = prediction
                    recommended_state['savings_percentage'] = (current_cost - prediction) / current_cost
                    
            elif optimization_type == OptimizationType.PERFORMANCE_OPTIMIZATION:
                # Mock performance optimization recommendations
                recommended_state['performance_optimization_score'] = prediction
                recommended_state['recommended_actions'] = ['optimize_configuration', 'update_software']
                
            elif optimization_type == OptimizationType.RESOURCE_RIGHTSIZING:
                # Mock resource right-sizing recommendations
                recommended_state['rightsizing_potential'] = prediction
                recommended_state['recommended_cpu'] = resource.get('current_cpu', 0) * 0.8
                recommended_state['recommended_memory'] = resource.get('current_memory', 0) * 0.8
            
            return recommended_state
            
        except Exception as e:
            logger.error(f"Failed to generate recommended state: {e}")
            return resource.copy()
    
    async def get_optimization_summary(self) -> Dict[str, Any]:
        """Get summary of optimization recommendations"""
        try:
            total_recommendations = len(self.optimization_history)
            total_savings = sum(rec.expected_savings for rec in self.optimization_history)
            
            # Group by optimization type
            by_type = {}
            for rec in self.optimization_history:
                opt_type = rec.optimization_type.value
                if opt_type not in by_type:
                    by_type[opt_type] = []
                by_type[opt_type].append(rec)
            
            # Calculate confidence scores
            avg_confidence = np.mean([rec.confidence_score for rec in self.optimization_history]) if self.optimization_history else 0
            
            return {
                'total_recommendations': total_recommendations,
                'total_potential_savings': total_savings,
                'average_confidence': avg_confidence,
                'recommendations_by_type': {
                    opt_type: len(recs) for opt_type, recs in by_type.items()
                },
                'recent_recommendations': [
                    {
                        'id': rec.recommendation_id,
                        'type': rec.optimization_type.value,
                        'resource_id': rec.resource_id,
                        'expected_savings': rec.expected_savings,
                        'confidence': rec.confidence_score
                    }
                    for rec in self.optimization_history[-10:]  # Last 10 recommendations
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get optimization summary: {e}")
            return {}
    
    async def get_predictive_summary(self) -> Dict[str, Any]:
        """Get summary of predictive analyses"""
        try:
            total_analyses = len(self.predictive_analyses)
            
            # Group by prediction type
            by_type = {}
            for analysis in self.predictive_analyses:
                pred_type = analysis.prediction_type
                if pred_type not in by_type:
                    by_type[pred_type] = []
                by_type[pred_type].append(analysis)
            
            # Calculate average accuracy
            avg_accuracy = np.mean([analysis.model_accuracy for analysis in self.predictive_analyses]) if self.predictive_analyses else 0
            
            return {
                'total_analyses': total_analyses,
                'average_accuracy': avg_accuracy,
                'analyses_by_type': {
                    pred_type: len(analyses) for pred_type, analyses in by_type.items()
                },
                'recent_analyses': [
                    {
                        'id': analysis.analysis_id,
                        'type': analysis.prediction_type,
                        'resource_id': analysis.resource_id,
                        'trend': analysis.trend_direction,
                        'accuracy': analysis.model_accuracy
                    }
                    for analysis in self.predictive_analyses[-10:]  # Last 10 analyses
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get predictive summary: {e}")
            return {}


# Global ML optimizer instance
ml_optimizer = MLOptimizer()
