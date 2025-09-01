"""
Ensemble AI System for CloudMind
Multi-provider AI with voting/consensus mechanisms for enhanced accuracy and reliability
"""

import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np
from statistics import mean, median
from collections import Counter

from app.core.config import settings
from app.services.ai_engine.god_tier_ai_service import GodTierAIService, AIProvider, AnalysisType
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


class ConsensusMethod(Enum):
    """Consensus methods for ensemble AI"""
    MAJORITY_VOTE = "majority_vote"
    WEIGHTED_VOTE = "weighted_vote"
    CONFIDENCE_WEIGHTED = "confidence_weighted"
    EXPERT_VOTE = "expert_vote"


@dataclass
class EnsembleResponse:
    """Ensemble AI response with consensus information"""
    final_response: str
    consensus_method: ConsensusMethod
    confidence_score: float
    provider_responses: Dict[str, Dict[str, Any]]
    consensus_breakdown: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


@dataclass
class ProviderWeight:
    """Provider weight configuration for ensemble"""
    provider: AIProvider
    weight: float
    reliability_score: float
    specialization: List[str]


class EnsembleAISystem:
    """Advanced Ensemble AI System with multi-provider consensus"""
    
    def __init__(self):
        self.god_tier_service = GodTierAIService()
        self.provider_weights: Dict[AIProvider, ProviderWeight] = {}
        self.consensus_history: List[EnsembleResponse] = []
        
        # Initialize provider weights
        self._initialize_provider_weights()
        
        logger.info("🧠 Ensemble AI System initialized")
    
    def _initialize_provider_weights(self):
        """Initialize provider weights based on capabilities"""
        self.provider_weights = {
            AIProvider.OPENAI: ProviderWeight(
                provider=AIProvider.OPENAI,
                weight=0.35,
                reliability_score=0.92,
                specialization=['general_analysis', 'code_generation']
            ),
            AIProvider.ANTHROPIC: ProviderWeight(
                provider=AIProvider.ANTHROPIC,
                weight=0.35,
                reliability_score=0.94,
                specialization=['security_analysis', 'compliance_audit']
            ),
            AIProvider.GOOGLE_AI: ProviderWeight(
                provider=AIProvider.GOOGLE_AI,
                weight=0.20,
                reliability_score=0.88,
                specialization=['factual_queries', 'data_analysis']
            ),
            AIProvider.OLLAMA: ProviderWeight(
                provider=AIProvider.OLLAMA,
                weight=0.10,
                reliability_score=0.85,
                specialization=['local_processing']
            )
        }
    
    async def generate_ensemble_response(
        self,
        prompt: str,
        analysis_type: AnalysisType = AnalysisType.COMPREHENSIVE,
        consensus_method: ConsensusMethod = ConsensusMethod.CONFIDENCE_WEIGHTED,
        min_providers: int = 2
    ) -> EnsembleResponse:
        """Generate ensemble response using multiple AI providers"""
        try:
            logger.info(f"🎯 Generating ensemble response for {analysis_type.value}")
            
            # Get provider responses
            provider_responses = await self._get_provider_responses(
                prompt, analysis_type, min_providers
            )
            
            if not provider_responses:
                raise ValueError("No provider responses received")
            
            # Apply consensus method
            final_response, consensus_breakdown = await self._apply_consensus(
                provider_responses, consensus_method, analysis_type
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                provider_responses, consensus_breakdown
            )
            
            # Create ensemble response
            ensemble_response = EnsembleResponse(
                final_response=final_response,
                consensus_method=consensus_method,
                confidence_score=confidence_score,
                provider_responses=provider_responses,
                consensus_breakdown=consensus_breakdown,
                metadata={
                    'analysis_type': analysis_type.value,
                    'num_providers': len(provider_responses)
                }
            )
            
            # Store in history
            self.consensus_history.append(ensemble_response)
            
            logger.info(f"✅ Ensemble response generated with confidence: {confidence_score:.3f}")
            return ensemble_response
            
        except Exception as e:
            logger.error(f"Failed to generate ensemble response: {e}")
            raise
    
    async def _get_provider_responses(
        self,
        prompt: str,
        analysis_type: AnalysisType,
        min_providers: int
    ) -> Dict[str, Dict[str, Any]]:
        """Get responses from multiple providers"""
        try:
            # Select providers
            selected_providers = self._select_providers_for_analysis(analysis_type)
            
            # Create tasks for parallel execution
            tasks = []
            for provider in selected_providers:
                task = self._get_single_provider_response(prompt, provider, analysis_type)
                tasks.append(task)
            
            # Execute
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            responses = {}
            for i, result in enumerate(results):
                provider = selected_providers[i]
                if isinstance(result, Exception):
                    logger.warning(f"Provider {provider.value} failed: {result}")
                else:
                    responses[provider.value] = result
            
            return responses
            
        except Exception as e:
            logger.error(f"Failed to get provider responses: {e}")
            return {}
    
    async def _get_single_provider_response(
        self,
        prompt: str,
        provider: AIProvider,
        analysis_type: AnalysisType
    ) -> Dict[str, Any]:
        """Get response from a single provider"""
        try:
            start_time = datetime.now(timezone.utc)
            
            response_data = await self.god_tier_service._get_ai_response(
                prompt, analysis_type, provider
            )
            
            end_time = datetime.now(timezone.utc)
            processing_time = (end_time - start_time).total_seconds()
            
            response_data.update({
                'provider': provider.value,
                'processing_time': processing_time,
                'timestamp': start_time.isoformat()
            })
            
            return response_data
            
        except Exception as e:
            logger.error(f"Provider {provider.value} failed: {e}")
            raise
    
    def _select_providers_for_analysis(self, analysis_type: AnalysisType) -> List[AIProvider]:
        """Select best providers for specific analysis type"""
        if analysis_type == AnalysisType.SECURITY_ASSESSMENT:
            return [AIProvider.ANTHROPIC, AIProvider.OPENAI]
        elif analysis_type == AnalysisType.COST_OPTIMIZATION:
            return [AIProvider.OPENAI, AIProvider.GOOGLE_AI]
        else:
            return [AIProvider.OPENAI, AIProvider.ANTHROPIC, AIProvider.GOOGLE_AI]
    
    async def _apply_consensus(
        self,
        provider_responses: Dict[str, Dict[str, Any]],
        consensus_method: ConsensusMethod,
        analysis_type: AnalysisType
    ) -> Tuple[str, Dict[str, Any]]:
        """Apply consensus method to provider responses"""
        try:
            if consensus_method == ConsensusMethod.CONFIDENCE_WEIGHTED:
                return self._confidence_weighted_consensus(provider_responses)
            elif consensus_method == ConsensusMethod.EXPERT_VOTE:
                return self._expert_vote_consensus(provider_responses, analysis_type)
            else:
                return self._confidence_weighted_consensus(provider_responses)
                
        except Exception as e:
            logger.error(f"Failed to apply consensus: {e}")
            first_response = list(provider_responses.values())[0]
            return first_response.get('content', 'No consensus reached'), {'error': str(e)}
    
    def _confidence_weighted_consensus(
        self,
        provider_responses: Dict[str, Dict[str, Any]]
    ) -> Tuple[str, Dict[str, Any]]:
        """Apply confidence-weighted consensus"""
        try:
            confidence_scores = {}
            
            for provider_name, response in provider_responses.items():
                provider = AIProvider(provider_name)
                base_reliability = self.provider_weights.get(provider, ProviderWeight(
                    provider=provider, weight=0.1, reliability_score=0.8, specialization=[]
                )).reliability_score
                
                content = response.get('content', '')
                content_quality = min(len(content) / 200, 1.0)
                processing_time = response.get('processing_time', 10)
                time_penalty = max(0, 1 - (processing_time / 30))
                
                confidence = base_reliability * content_quality * time_penalty
                confidence_scores[provider_name] = confidence
            
            best_provider = max(confidence_scores.items(), key=lambda x: x[1])[0]
            final_response = provider_responses[best_provider].get('content', '')
            
            breakdown = {
                'method': 'confidence_weighted',
                'confidence_scores': confidence_scores,
                'selected_provider': best_provider
            }
            
            return final_response, breakdown
            
        except Exception as e:
            logger.error(f"Confidence-weighted consensus failed: {e}")
            return "Consensus failed", {'error': str(e)}
    
    def _expert_vote_consensus(
        self,
        provider_responses: Dict[str, Dict[str, Any]],
        analysis_type: AnalysisType
    ) -> Tuple[str, Dict[str, Any]]:
        """Apply expert vote consensus"""
        try:
            if analysis_type == AnalysisType.SECURITY_ASSESSMENT:
                expert_provider = AIProvider.ANTHROPIC
            elif analysis_type == AnalysisType.COST_OPTIMIZATION:
                expert_provider = AIProvider.OPENAI
            else:
                expert_provider = AIProvider.OPENAI
            
            expert_response = provider_responses.get(expert_provider.value)
            if expert_response:
                final_response = expert_response.get('content', '')
            else:
                final_response = list(provider_responses.values())[0].get('content', '')
            
            breakdown = {
                'method': 'expert_vote',
                'expert_provider': expert_provider.value
            }
            
            return final_response, breakdown
            
        except Exception as e:
            logger.error(f"Expert vote consensus failed: {e}")
            return "Consensus failed", {'error': str(e)}
    
    def _calculate_confidence_score(
        self,
        provider_responses: Dict[str, Dict[str, Any]],
        consensus_breakdown: Dict[str, Any]
    ) -> float:
        """Calculate overall confidence score"""
        try:
            method_confidence = {
                'confidence_weighted': 0.9,
                'expert_vote': 0.95
            }
            
            method = consensus_breakdown.get('method', 'confidence_weighted')
            base_confidence = method_confidence.get(method, 0.8)
            
            num_providers = len(provider_responses)
            provider_factor = min(num_providers / 3, 1.0)
            
            confidence = base_confidence * provider_factor
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Failed to calculate confidence score: {e}")
            return 0.5


# Global ensemble AI instance
ensemble_ai = EnsembleAISystem()
