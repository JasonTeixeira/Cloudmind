import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone
import numpy as np

from app.services.optimization.ml_optimizer import (
    MLOptimizer, OptimizationType, OptimizationRecommendation, PredictiveAnalysis
)
from app.services.ai_engine.ensemble_ai import ConsensusMethod
from app.services.ai_engine.god_tier_ai_service import AnalysisType


class TestMLOptimizer:
    """Test ML Optimizer functionality"""

    @pytest.fixture
    def ml_optimizer(self):
        """Create ML optimizer instance for testing"""
        return MLOptimizer()

    @pytest.fixture
    def sample_resources(self):
        """Create sample resources for testing"""
        return [
            {
                'id': 'ec2-001',
                'type': 'ec2',
                'cost_per_hour': 0.50,
                'utilization_rate': 0.25,
                'instance_size': 'm5.large',
                'storage_gb': 100,
                'network_bandwidth': 1000,
                'age_days': 30,
                'region_cost_multiplier': 1.0
            },
            {
                'id': 'rds-001',
                'type': 'rds',
                'cost_per_hour': 0.75,
                'utilization_rate': 0.60,
                'instance_size': 'db.r5.large',
                'storage_gb': 500,
                'network_bandwidth': 500,
                'age_days': 45,
                'region_cost_multiplier': 1.2
            }
        ]

    @pytest.fixture
    def performance_resources(self):
        """Create sample performance resources for testing"""
        return [
            {
                'id': 'ec2-002',
                'type': 'ec2',
                'cpu_utilization': 0.85,
                'memory_utilization': 0.70,
                'network_utilization': 0.40,
                'disk_utilization': 0.60,
                'response_time': 150,
                'throughput': 1000,
                'error_rate': 0.02
            }
        ]

    def test_ml_optimizer_initialization(self, ml_optimizer):
        """Test ML optimizer initialization"""
        assert ml_optimizer.ml_framework is not None
        assert ml_optimizer.data_pipeline is not None
        assert len(ml_optimizer.models) == 3
        assert 'cost_optimization' in ml_optimizer.models
        assert 'performance_optimization' in ml_optimizer.models
        assert 'resource_rightsizing' in ml_optimizer.models
        assert len(ml_optimizer.scalers) == 3

    def test_extract_ml_features_cost_optimization(self, ml_optimizer, sample_resources):
        """Test feature extraction for cost optimization"""
        resource = sample_resources[0]
        features = ml_optimizer._extract_ml_features(resource, OptimizationType.COST_OPTIMIZATION)
        
        assert features is not None
        assert features.shape == (1, 7)
        assert features[0][0] == 0.50  # cost_per_hour
        assert features[0][1] == 0.25  # utilization_rate

    def test_extract_ml_features_performance_optimization(self, ml_optimizer, performance_resources):
        """Test feature extraction for performance optimization"""
        resource = performance_resources[0]
        features = ml_optimizer._extract_ml_features(resource, OptimizationType.PERFORMANCE_OPTIMIZATION)
        
        assert features is not None
        assert features.shape == (1, 7)
        assert features[0][0] == 0.85  # cpu_utilization
        assert features[0][1] == 0.70  # memory_utilization

    def test_extract_ml_features_empty_resource(self, ml_optimizer):
        """Test feature extraction with empty resource"""
        empty_resource = {'id': 'empty', 'type': 'unknown'}
        features = ml_optimizer._extract_ml_features(empty_resource, OptimizationType.COST_OPTIMIZATION)
        
        assert features is None

    @pytest.mark.asyncio
    async def test_make_ml_prediction_cost_optimization(self, ml_optimizer):
        """Test ML prediction for cost optimization"""
        features = np.array([[0.50, 0.25, 2, 100, 1000, 30, 1.0]])  # Underutilized resource
        
        prediction = await ml_optimizer._make_ml_prediction(features, 'cost_optimization')
        
        assert prediction is not None
        assert prediction < 0.50  # Should suggest cost reduction for underutilized resource

    @pytest.mark.asyncio
    async def test_make_ml_prediction_performance_optimization(self, ml_optimizer):
        """Test ML prediction for performance optimization"""
        features = np.array([[0.85, 0.70, 0.40, 0.60, 150, 1000, 0.02]])  # High utilization
        
        prediction = await ml_optimizer._make_ml_prediction(features, 'performance_optimization')
        
        assert prediction is not None
        assert prediction > 0.1  # Should suggest high optimization potential

    @pytest.mark.asyncio
    async def test_make_ml_prediction_resource_rightsizing(self, ml_optimizer):
        """Test ML prediction for resource right-sizing"""
        features = np.array([[4, 8, 100, 0.80, 0.25, 0.50, 0.85]])  # Low average utilization
        
        prediction = await ml_optimizer._make_ml_prediction(features, 'resource_rightsizing')
        
        assert prediction is not None
        assert prediction > 0.5  # Should suggest high right-sizing potential

    @pytest.mark.asyncio
    async def test_create_ml_recommendation(self, ml_optimizer, sample_resources):
        """Test ML recommendation creation"""
        resource = sample_resources[0]
        features = np.array([[0.50, 0.25, 2, 100, 1000, 30, 1.0]])
        prediction = 0.30  # 40% cost reduction
        
        recommendation = await ml_optimizer._create_ml_recommendation(
            resource, OptimizationType.COST_OPTIMIZATION, prediction, features
        )
        
        assert isinstance(recommendation, OptimizationRecommendation)
        assert recommendation.optimization_type == OptimizationType.COST_OPTIMIZATION
        assert recommendation.resource_id == 'ec2-001'
        assert recommendation.expected_savings == 0.20  # 0.50 - 0.30
        assert recommendation.confidence_score == 0.85
        assert recommendation.reasoning is not None

    def test_assess_implementation_risk(self, ml_optimizer, sample_resources):
        """Test implementation risk assessment"""
        resource = sample_resources[0]
        
        # High savings scenario
        effort, risk = ml_optimizer._assess_implementation_risk(
            resource, OptimizationType.COST_OPTIMIZATION, 0.25  # 50% cost reduction
        )
        assert effort == "high"
        assert risk == "medium"
        
        # Low savings scenario
        effort, risk = ml_optimizer._assess_implementation_risk(
            resource, OptimizationType.COST_OPTIMIZATION, 0.45  # 10% cost reduction
        )
        assert effort == "medium"
        assert risk == "low"

    def test_generate_ml_reasoning(self, ml_optimizer, sample_resources):
        """Test ML reasoning generation"""
        resource = sample_resources[0]
        features = np.array([[0.50, 0.25, 2, 100, 1000, 30, 1.0]])
        
        reasoning = ml_optimizer._generate_ml_reasoning(
            resource, OptimizationType.COST_OPTIMIZATION, 0.30, features
        )
        
        assert reasoning is not None
        assert "underutilized" in reasoning.lower()
        assert "25.0%" in reasoning

    def test_generate_recommended_state(self, ml_optimizer, sample_resources):
        """Test recommended state generation"""
        resource = sample_resources[0]
        prediction = 0.30  # 40% cost reduction
        
        recommended_state = ml_optimizer._generate_recommended_state(
            resource, OptimizationType.COST_OPTIMIZATION, prediction
        )
        
        assert recommended_state is not None
        assert 'recommended_instance_size' in recommended_state
        assert 'estimated_cost' in recommended_state
        assert 'savings_percentage' in recommended_state

    @pytest.mark.asyncio
    async def test_generate_optimization_recommendations(self, ml_optimizer, sample_resources):
        """Test optimization recommendation generation"""
        with patch.object(ml_optimizer, '_generate_ai_recommendation') as mock_ai:
            mock_ai.return_value = None  # Skip AI recommendations for this test
            
            recommendations = await ml_optimizer.generate_optimization_recommendations(
                sample_resources, OptimizationType.COST_OPTIMIZATION, include_ai_analysis=False
            )
            
            assert len(recommendations) > 0
            assert all(isinstance(rec, OptimizationRecommendation) for rec in recommendations)
            assert all(rec.optimization_type == OptimizationType.COST_OPTIMIZATION for rec in recommendations)

    @pytest.mark.asyncio
    async def test_generate_ai_recommendation(self, ml_optimizer, sample_resources):
        """Test AI recommendation generation"""
        with patch.object(ml_optimizer, 'ensemble_ai') as mock_ensemble:
            mock_response = Mock()
            mock_response.final_response = "AI analysis suggests 20% cost savings through instance right-sizing."
            mock_response.confidence_score = 0.92
            
            mock_ensemble.generate_ensemble_response.return_value = mock_response
            
            recommendation = await ml_optimizer._generate_ai_recommendation(
                sample_resources[0], OptimizationType.COST_OPTIMIZATION
            )
            
            assert recommendation is not None
            assert isinstance(recommendation, OptimizationRecommendation)
            assert recommendation.ml_model_used == "ensemble_ai"
            assert recommendation.confidence_score == 0.92

    def test_create_optimization_prompt(self, ml_optimizer, sample_resources):
        """Test optimization prompt creation"""
        resource = sample_resources[0]
        
        prompt = ml_optimizer._create_optimization_prompt(
            resource, OptimizationType.COST_OPTIMIZATION
        )
        
        assert prompt is not None
        assert "ec2" in prompt.lower()
        assert "cost optimization" in prompt.lower()
        assert "0.50" in prompt  # cost_per_hour
        assert "25.0%" in prompt  # utilization_rate

    def test_parse_ai_recommendation(self, ml_optimizer, sample_resources):
        """Test AI recommendation parsing"""
        resource = sample_resources[0]
        mock_ai_response = Mock()
        mock_ai_response.final_response = "Analysis suggests 20% cost savings through optimization."
        mock_ai_response.confidence_score = 0.88
        
        recommendation = ml_optimizer._parse_ai_recommendation(
            resource, OptimizationType.COST_OPTIMIZATION, mock_ai_response
        )
        
        assert isinstance(recommendation, OptimizationRecommendation)
        assert recommendation.ml_model_used == "ensemble_ai"
        assert recommendation.confidence_score == 0.88
        assert "20% cost savings" in recommendation.reasoning

    @pytest.mark.asyncio
    async def test_generate_predictive_analysis(self, ml_optimizer, sample_resources):
        """Test predictive analysis generation"""
        analyses = await ml_optimizer.generate_predictive_analysis(
            sample_resources, "cost_forecast", 30
        )
        
        assert len(analyses) > 0
        assert all(isinstance(analysis, PredictiveAnalysis) for analysis in analyses)
        assert all(analysis.prediction_type == "cost_forecast" for analysis in analyses)

    @pytest.mark.asyncio
    async def test_generate_single_prediction(self, ml_optimizer, sample_resources):
        """Test single prediction generation"""
        analysis = await ml_optimizer._generate_single_prediction(
            sample_resources[0], "cost_forecast", 30
        )
        
        assert analysis is not None
        assert isinstance(analysis, PredictiveAnalysis)
        assert analysis.prediction_type == "cost_forecast"
        assert analysis.resource_id == "ec2-001"
        assert analysis.trend_direction in ["increasing", "decreasing"]
        assert len(analysis.confidence_interval) == 2

    @pytest.mark.asyncio
    async def test_get_optimization_summary(self, ml_optimizer, sample_resources):
        """Test optimization summary generation"""
        # First generate some recommendations
        with patch.object(ml_optimizer, '_generate_ai_recommendation') as mock_ai:
            mock_ai.return_value = None
            
            await ml_optimizer.generate_optimization_recommendations(
                sample_resources, OptimizationType.COST_OPTIMIZATION, include_ai_analysis=False
            )
        
        summary = await ml_optimizer.get_optimization_summary()
        
        assert 'total_recommendations' in summary
        assert 'total_potential_savings' in summary
        assert 'average_confidence' in summary
        assert 'recommendations_by_type' in summary
        assert 'recent_recommendations' in summary
        assert summary['total_recommendations'] > 0

    @pytest.mark.asyncio
    async def test_get_predictive_summary(self, ml_optimizer, sample_resources):
        """Test predictive summary generation"""
        # First generate some analyses
        await ml_optimizer.generate_predictive_analysis(sample_resources, "cost_forecast", 30)
        
        summary = await ml_optimizer.get_predictive_summary()
        
        assert 'total_analyses' in summary
        assert 'average_accuracy' in summary
        assert 'analyses_by_type' in summary
        assert 'recent_analyses' in summary
        assert summary['total_analyses'] > 0

    def test_optimization_recommendation_creation(self):
        """Test OptimizationRecommendation creation"""
        recommendation = OptimizationRecommendation(
            recommendation_id="test_rec_001",
            optimization_type=OptimizationType.COST_OPTIMIZATION,
            resource_id="ec2-001",
            resource_type="ec2",
            current_state={"cost": 0.50},
            recommended_state={"cost": 0.30},
            expected_savings=0.20,
            confidence_score=0.85,
            implementation_effort="medium",
            risk_level="low",
            reasoning="Test reasoning",
            ml_model_used="test_model"
        )
        
        assert recommendation.recommendation_id == "test_rec_001"
        assert recommendation.optimization_type == OptimizationType.COST_OPTIMIZATION
        assert recommendation.expected_savings == 0.20
        assert recommendation.confidence_score == 0.85
        assert recommendation.created_at is not None

    def test_predictive_analysis_creation(self):
        """Test PredictiveAnalysis creation"""
        analysis = PredictiveAnalysis(
            analysis_id="test_analysis_001",
            resource_id="ec2-001",
            resource_type="ec2",
            prediction_type="cost_forecast",
            current_value=0.50,
            predicted_value=0.55,
            confidence_interval=(0.50, 0.60),
            trend_direction="increasing",
            factors=["growth", "seasonal"],
            model_accuracy=0.85
        )
        
        assert analysis.analysis_id == "test_analysis_001"
        assert analysis.prediction_type == "cost_forecast"
        assert analysis.current_value == 0.50
        assert analysis.predicted_value == 0.55
        assert analysis.trend_direction == "increasing"
        assert analysis.model_accuracy == 0.85
        assert analysis.created_at is not None

    def test_optimization_type_enum(self):
        """Test OptimizationType enum"""
        assert OptimizationType.COST_OPTIMIZATION.value == "cost_optimization"
        assert OptimizationType.PERFORMANCE_OPTIMIZATION.value == "performance_optimization"
        assert OptimizationType.RESOURCE_RIGHTSIZING.value == "resource_rightsizing"
        assert OptimizationType.CAPACITY_PLANNING.value == "capacity_planning"
        assert OptimizationType.SECURITY_OPTIMIZATION.value == "security_optimization"

    @pytest.mark.asyncio
    async def test_ml_optimizer_integration(self):
        """Test ML optimizer integration with real workflow"""
        ml_optimizer = MLOptimizer()
        
        # Test with sample resources
        resources = [
            {
                'id': 'test-ec2-001',
                'type': 'ec2',
                'cost_per_hour': 0.75,
                'utilization_rate': 0.20,
                'instance_size': 'm5.xlarge',
                'storage_gb': 200,
                'network_bandwidth': 2000,
                'age_days': 60,
                'region_cost_multiplier': 1.1
            }
        ]
        
        with patch.object(ml_optimizer, '_generate_ai_recommendation') as mock_ai:
            mock_ai.return_value = None
            
            # Generate recommendations
            recommendations = await ml_optimizer.generate_optimization_recommendations(
                resources, OptimizationType.COST_OPTIMIZATION, include_ai_analysis=False
            )
            
            assert len(recommendations) > 0
            
            # Generate predictive analysis
            analyses = await ml_optimizer.generate_predictive_analysis(
                resources, "cost_forecast", 30
            )
            
            assert len(analyses) > 0
            
            # Get summaries
            opt_summary = await ml_optimizer.get_optimization_summary()
            pred_summary = await ml_optimizer.get_predictive_summary()
            
            assert opt_summary['total_recommendations'] > 0
            assert pred_summary['total_analyses'] > 0
