import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from app.services.ai_engine.ensemble_ai import (
    EnsembleAISystem, ConsensusMethod, EnsembleResponse, ProviderWeight
)
from app.services.ai_engine.god_tier_ai_service import AIProvider, AnalysisType


class TestEnsembleAISystem:
    """Test Ensemble AI System functionality"""

    @pytest.fixture
    def ensemble_ai(self):
        """Create ensemble AI instance for testing"""
        return EnsembleAISystem()

    @pytest.fixture
    def mock_provider_responses(self):
        """Create mock provider responses"""
        return {
            'openai': {
                'content': 'OpenAI response: This is a cost optimization recommendation.',
                'provider': 'openai',
                'processing_time': 2.5,
                'timestamp': '2024-01-01T00:00:00Z'
            },
            'anthropic': {
                'content': 'Anthropic response: Here is a detailed security analysis.',
                'provider': 'anthropic',
                'processing_time': 3.1,
                'timestamp': '2024-01-01T00:00:00Z'
            },
            'google_ai': {
                'content': 'Google AI response: Technical analysis with data insights.',
                'provider': 'google_ai',
                'processing_time': 1.8,
                'timestamp': '2024-01-01T00:00:00Z'
            }
        }

    def test_ensemble_ai_initialization(self, ensemble_ai):
        """Test ensemble AI system initialization"""
        assert ensemble_ai.god_tier_service is not None
        assert len(ensemble_ai.provider_weights) == 4
        assert AIProvider.OPENAI in ensemble_ai.provider_weights
        assert AIProvider.ANTHROPIC in ensemble_ai.provider_weights

    def test_provider_weights_initialization(self, ensemble_ai):
        """Test provider weights initialization"""
        openai_weight = ensemble_ai.provider_weights[AIProvider.OPENAI]
        assert openai_weight.weight == 0.35
        assert openai_weight.reliability_score == 0.92
        assert 'general_analysis' in openai_weight.specialization

        anthropic_weight = ensemble_ai.provider_weights[AIProvider.ANTHROPIC]
        assert anthropic_weight.weight == 0.35
        assert anthropic_weight.reliability_score == 0.94
        assert 'security_analysis' in anthropic_weight.specialization

    def test_select_providers_for_analysis(self, ensemble_ai):
        """Test provider selection for different analysis types"""
        # Security assessment
        security_providers = ensemble_ai._select_providers_for_analysis(AnalysisType.SECURITY_ASSESSMENT)
        assert AIProvider.ANTHROPIC in security_providers
        assert AIProvider.OPENAI in security_providers

        # Cost optimization
        cost_providers = ensemble_ai._select_providers_for_analysis(AnalysisType.COST_OPTIMIZATION)
        assert AIProvider.OPENAI in cost_providers
        assert AIProvider.GOOGLE_AI in cost_providers

        # Comprehensive
        comprehensive_providers = ensemble_ai._select_providers_for_analysis(AnalysisType.COMPREHENSIVE)
        assert AIProvider.OPENAI in comprehensive_providers
        assert AIProvider.ANTHROPIC in comprehensive_providers
        assert AIProvider.GOOGLE_AI in comprehensive_providers

    def test_confidence_weighted_consensus(self, ensemble_ai, mock_provider_responses):
        """Test confidence-weighted consensus"""
        final_response, breakdown = ensemble_ai._confidence_weighted_consensus(mock_provider_responses)
        
        assert final_response is not None
        assert 'method' in breakdown
        assert breakdown['method'] == 'confidence_weighted'
        assert 'confidence_scores' in breakdown
        assert 'selected_provider' in breakdown
        
        # Check that confidence scores are calculated
        confidence_scores = breakdown['confidence_scores']
        assert 'openai' in confidence_scores
        assert 'anthropic' in confidence_scores
        assert 'google_ai' in confidence_scores

    def test_expert_vote_consensus(self, ensemble_ai, mock_provider_responses):
        """Test expert vote consensus"""
        # Security assessment
        final_response, breakdown = ensemble_ai._expert_vote_consensus(
            mock_provider_responses, AnalysisType.SECURITY_ASSESSMENT
        )
        
        assert final_response is not None
        assert breakdown['method'] == 'expert_vote'
        assert breakdown['expert_provider'] == 'anthropic'

        # Cost optimization
        final_response, breakdown = ensemble_ai._expert_vote_consensus(
            mock_provider_responses, AnalysisType.COST_OPTIMIZATION
        )
        
        assert final_response is not None
        assert breakdown['expert_provider'] == 'openai'

    def test_calculate_confidence_score(self, ensemble_ai, mock_provider_responses):
        """Test confidence score calculation"""
        breakdown = {
            'method': 'confidence_weighted',
            'confidence_scores': {'openai': 0.85, 'anthropic': 0.92, 'google_ai': 0.78}
        }
        
        confidence = ensemble_ai._calculate_confidence_score(mock_provider_responses, breakdown)
        
        assert 0 <= confidence <= 1
        assert confidence > 0.5  # Should be reasonably high

    @pytest.mark.asyncio
    async def test_get_single_provider_response(self, ensemble_ai):
        """Test getting response from single provider"""
        with patch.object(ensemble_ai.god_tier_service, '_get_ai_response') as mock_get:
            mock_get.return_value = {
                'content': 'Test response',
                'provider': 'openai'
            }
            
            response = await ensemble_ai._get_single_provider_response(
                'test prompt', AIProvider.OPENAI, AnalysisType.COMPREHENSIVE
            )
            
            assert 'content' in response
            assert 'provider' in response
            assert 'processing_time' in response
            assert 'timestamp' in response

    @pytest.mark.asyncio
    async def test_get_provider_responses(self, ensemble_ai):
        """Test getting responses from multiple providers"""
        with patch.object(ensemble_ai, '_get_single_provider_response') as mock_get:
            mock_get.return_value = {
                'content': 'Test response',
                'provider': 'openai',
                'processing_time': 2.0,
                'timestamp': '2024-01-01T00:00:00Z'
            }
            
            responses = await ensemble_ai._get_provider_responses(
                'test prompt', AnalysisType.COMPREHENSIVE, 2
            )
            
            assert len(responses) > 0
            assert 'openai' in responses or 'anthropic' in responses

    @pytest.mark.asyncio
    async def test_apply_consensus(self, ensemble_ai, mock_provider_responses):
        """Test consensus application"""
        # Test confidence weighted
        final_response, breakdown = await ensemble_ai._apply_consensus(
            mock_provider_responses, ConsensusMethod.CONFIDENCE_WEIGHTED, AnalysisType.COMPREHENSIVE
        )
        
        assert final_response is not None
        assert breakdown['method'] == 'confidence_weighted'

        # Test expert vote
        final_response, breakdown = await ensemble_ai._apply_consensus(
            mock_provider_responses, ConsensusMethod.EXPERT_VOTE, AnalysisType.SECURITY_ASSESSMENT
        )
        
        assert final_response is not None
        assert breakdown['method'] == 'expert_vote'

    @pytest.mark.asyncio
    async def test_generate_ensemble_response(self, ensemble_ai):
        """Test complete ensemble response generation"""
        with patch.object(ensemble_ai, '_get_provider_responses') as mock_get:
            mock_get.return_value = {
                'openai': {
                    'content': 'OpenAI response',
                    'provider': 'openai',
                    'processing_time': 2.0,
                    'timestamp': '2024-01-01T00:00:00Z'
                },
                'anthropic': {
                    'content': 'Anthropic response',
                    'provider': 'anthropic',
                    'processing_time': 3.0,
                    'timestamp': '2024-01-01T00:00:00Z'
                }
            }
            
            response = await ensemble_ai.generate_ensemble_response(
                'test prompt',
                AnalysisType.COMPREHENSIVE,
                ConsensusMethod.CONFIDENCE_WEIGHTED
            )
            
            assert isinstance(response, EnsembleResponse)
            assert response.final_response is not None
            assert response.confidence_score > 0
            assert response.consensus_method == ConsensusMethod.CONFIDENCE_WEIGHTED
            assert len(response.provider_responses) == 2

    def test_ensemble_response_creation(self):
        """Test EnsembleResponse creation"""
        response = EnsembleResponse(
            final_response="Test response",
            consensus_method=ConsensusMethod.CONFIDENCE_WEIGHTED,
            confidence_score=0.85,
            provider_responses={},
            consensus_breakdown={},
            metadata={}
        )
        
        assert response.final_response == "Test response"
        assert response.confidence_score == 0.85
        assert response.consensus_method == ConsensusMethod.CONFIDENCE_WEIGHTED
        assert response.timestamp is not None

    def test_provider_weight_creation(self):
        """Test ProviderWeight creation"""
        weight = ProviderWeight(
            provider=AIProvider.OPENAI,
            weight=0.35,
            reliability_score=0.92,
            specialization=['general_analysis']
        )
        
        assert weight.provider == AIProvider.OPENAI
        assert weight.weight == 0.35
        assert weight.reliability_score == 0.92
        assert 'general_analysis' in weight.specialization

    @pytest.mark.asyncio
    async def test_ensemble_response_with_error_handling(self, ensemble_ai):
        """Test ensemble response with error handling"""
        with patch.object(ensemble_ai, '_get_provider_responses') as mock_get:
            mock_get.return_value = {}  # No responses
            
            with pytest.raises(ValueError, match="No provider responses received"):
                await ensemble_ai.generate_ensemble_response('test prompt')

    def test_consensus_methods(self):
        """Test consensus method enums"""
        assert ConsensusMethod.CONFIDENCE_WEIGHTED.value == "confidence_weighted"
        assert ConsensusMethod.EXPERT_VOTE.value == "expert_vote"
        assert ConsensusMethod.MAJORITY_VOTE.value == "majority_vote"
        assert ConsensusMethod.WEIGHTED_VOTE.value == "weighted_vote"

    @pytest.mark.asyncio
    async def test_ensemble_ai_integration(self):
        """Test ensemble AI integration with real workflow"""
        ensemble_ai = EnsembleAISystem()
        
        # Test with mock responses
        with patch.object(ensemble_ai.god_tier_service, '_get_ai_response') as mock_get:
            mock_get.return_value = {
                'content': 'Mock AI response for testing',
                'provider': 'openai'
            }
            
            response = await ensemble_ai.generate_ensemble_response(
                'Analyze this cloud infrastructure for cost optimization opportunities',
                AnalysisType.COST_OPTIMIZATION,
                ConsensusMethod.EXPERT_VOTE
            )
            
            assert isinstance(response, EnsembleResponse)
            assert response.final_response is not None
            assert response.confidence_score > 0
            assert len(ensemble_ai.consensus_history) == 1
