"""
AI Providers Service - Secure Integration with OpenAI and Anthropic
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
import anthropic
from pydantic import BaseModel

from app.core.config import settings

logger = logging.getLogger(__name__)


class AIProviderConfig(BaseModel):
    """Configuration for AI providers"""
    provider: str
    model: str
    max_tokens: int
    temperature: float
    api_key: str


class AIResponse(BaseModel):
    """Standardized AI response"""
    provider: str
    model: str
    content: str
    usage: Dict[str, Any]
    latency_ms: float
    timestamp: datetime


class AIProvidersService:
    """GOD TIER AI providers service with OpenAI, Anthropic, Google AI, and Ollama integration"""
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.google_ai_client = None
        self.ollama_client = None
        self.cache = {}
        self.request_count = 0
        self.total_latency = 0
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AI clients with GOD TIER error handling"""
        try:
            # Initialize OpenAI client
            if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your_openai_api_key_here":
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai
                logger.info("✅ OpenAI client initialized successfully")
            else:
                logger.warning("⚠️ OpenAI API key not configured")
            
            # Initialize Anthropic client
            if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
                self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                logger.info("✅ Anthropic client initialized successfully")
            else:
                logger.warning("⚠️ Anthropic API key not configured")
            
            # Initialize Google AI client
            if settings.GOOGLE_AI_API_KEY and settings.GOOGLE_AI_API_KEY != "your_google_ai_api_key_here":
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
                    self.google_ai_client = genai
                    logger.info("✅ Google AI client initialized successfully")
                except ImportError:
                    logger.warning("⚠️ Google AI library not installed")
            else:
                logger.warning("⚠️ Google AI API key not configured")
            
            # Initialize Ollama client
            try:
                import requests
                self.ollama_client = requests
                # Test Ollama connection
                response = requests.get(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=5)
                if response.status_code == 200:
                    logger.info("✅ Ollama client initialized successfully")
                else:
                    logger.warning("⚠️ Ollama server not responding")
            except Exception as e:
                logger.warning(f"⚠️ Ollama client initialization failed: {e}")
                
        except Exception as e:
            logger.error(f"❌ Error initializing AI clients: {str(e)}")
    
    async def get_ai_analysis(self, prompt: str, analysis_type: str = "general", provider: str = "auto") -> AIResponse:
        """Get AI analysis with GOD TIER provider selection and fallback"""
        try:
            start_time = datetime.now()
            
            # Determine best provider for analysis type
            if provider == "auto":
                provider = self._select_best_provider(analysis_type)
            
            # Get response from selected provider
            if provider == "openai" and self.openai_client:
                response = await self._get_openai_response(prompt, analysis_type)
            elif provider == "anthropic" and self.anthropic_client:
                response = await self._get_anthropic_response(prompt, analysis_type)
            elif provider == "google" and self.google_ai_client:
                response = await self._get_google_ai_response(prompt, analysis_type)
            elif provider == "ollama" and self.ollama_client:
                response = await self._get_ollama_response(prompt, analysis_type)
            else:
                # Fallback to best available provider
                response = await self._get_fallback_response(prompt, analysis_type)
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            # Update metrics
            self.request_count += 1
            self.total_latency += latency
            
            return AIResponse(
                provider=response["provider"],
                model=response["model"],
                content=response["content"],
                usage=response.get("usage", {}),
                latency_ms=latency,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {e}")
            return await self._get_error_response(prompt, analysis_type, str(e))
    
    def _select_best_provider(self, analysis_type: str) -> str:
        """Select the best AI provider for the analysis type"""
        provider_mapping = {
            "cost_optimization": "openai",  # GPT-4 excels at cost analysis
            "security_assessment": "anthropic",  # Claude-3 excels at security
            "infrastructure_health": "openai",  # GPT-4 good at technical analysis
            "performance_analysis": "anthropic",  # Claude-3 good at detailed analysis
            "compliance_audit": "anthropic",  # Claude-3 excels at compliance
            "anomaly_detection": "openai",  # GPT-4 good at pattern recognition
            "forecasting": "openai",  # GPT-4 good at predictions
            "comprehensive": "anthropic",  # Claude-3 good at comprehensive analysis
            "general": "openai"  # Default to OpenAI
        }
        
        return provider_mapping.get(analysis_type, "openai")
    
    async def _get_openai_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get response from OpenAI with GOD TIER prompt engineering"""
        try:
            # Enhanced prompt engineering for different analysis types
            enhanced_prompt = self._enhance_prompt_for_analysis(prompt, analysis_type, "openai")
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(analysis_type)},
                    {"role": "user", "content": enhanced_prompt}
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
    
    async def _get_anthropic_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get response from Anthropic with GOD TIER prompt engineering"""
        try:
            # Enhanced prompt engineering for different analysis types
            enhanced_prompt = self._enhance_prompt_for_analysis(prompt, analysis_type, "anthropic")
            
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=settings.ANTHROPIC_MODEL,
                max_tokens=int(settings.ANTHROPIC_MAX_TOKENS),
                temperature=float(settings.ANTHROPIC_TEMPERATURE),
                system=self._get_system_prompt(analysis_type),
                messages=[
                    {"role": "user", "content": enhanced_prompt}
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
    
    async def _get_google_ai_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get response from Google AI with GOD TIER prompt engineering"""
        try:
            # Enhanced prompt engineering for different analysis types
            enhanced_prompt = self._enhance_prompt_for_analysis(prompt, analysis_type, "google")
            
            model = self.google_ai_client.GenerativeModel(settings.GOOGLE_AI_MODEL)
            
            response = await asyncio.to_thread(
                model.generate_content,
                f"{self._get_system_prompt(analysis_type)}\n\n{enhanced_prompt}"
            )
            
            return {
                "provider": "google",
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
    
    async def _get_ollama_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get response from Ollama with GOD TIER prompt engineering"""
        try:
            # Enhanced prompt engineering for different analysis types
            enhanced_prompt = self._enhance_prompt_for_analysis(prompt, analysis_type, "ollama")
            
            response = await asyncio.to_thread(
                self.ollama_client.post,
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": f"{self._get_system_prompt(analysis_type)}\n\n{enhanced_prompt}",
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
    
    def _enhance_prompt_for_analysis(self, prompt: str, analysis_type: str, provider: str) -> str:
        """Enhance prompt with GOD TIER engineering for specific analysis types"""
        base_prompt = prompt
        
        # Add analysis-specific enhancements
        if analysis_type == "cost_optimization":
            base_prompt += "\n\nPlease provide detailed cost optimization recommendations with specific dollar amounts and implementation steps."
        elif analysis_type == "security_assessment":
            base_prompt += "\n\nPlease provide a comprehensive security assessment with risk levels, vulnerabilities, and remediation steps."
        elif analysis_type == "infrastructure_health":
            base_prompt += "\n\nPlease provide infrastructure health analysis with performance metrics, bottlenecks, and improvement recommendations."
        elif analysis_type == "performance_analysis":
            base_prompt += "\n\nPlease provide detailed performance analysis with metrics, benchmarks, and optimization strategies."
        elif analysis_type == "compliance_audit":
            base_prompt += "\n\nPlease provide compliance audit results with regulatory requirements, gaps, and remediation plans."
        elif analysis_type == "anomaly_detection":
            base_prompt += "\n\nPlease identify anomalies with confidence scores, impact assessment, and recommended actions."
        elif analysis_type == "forecasting":
            base_prompt += "\n\nPlease provide forecasting analysis with predictions, confidence intervals, and trend analysis."
        
        # Add provider-specific enhancements
        if provider == "openai":
            base_prompt += "\n\nProvide a structured response with clear sections and actionable insights."
        elif provider == "anthropic":
            base_prompt += "\n\nProvide a detailed analysis with step-by-step reasoning and comprehensive recommendations."
        elif provider == "google":
            base_prompt += "\n\nProvide a concise but comprehensive analysis with key insights and recommendations."
        elif provider == "ollama":
            base_prompt += "\n\nProvide a clear and actionable analysis with practical recommendations."
        
        return base_prompt
    
    def _get_system_prompt(self, analysis_type: str) -> str:
        """Get GOD TIER system prompt for analysis type"""
        system_prompts = {
            "cost_optimization": """You are an expert cloud cost optimization specialist with 15+ years of experience. You analyze cloud infrastructure and provide detailed, actionable cost optimization recommendations. Focus on identifying waste, rightsizing opportunities, and architectural improvements that can save money while maintaining performance and reliability.""",
            
            "security_assessment": """You are a senior cloud security architect with 20+ years of experience in cybersecurity. You conduct comprehensive security assessments and identify vulnerabilities, compliance gaps, and security risks. Provide detailed remediation steps and security best practices.""",
            
            "infrastructure_health": """You are a cloud infrastructure expert with deep knowledge of AWS, Azure, and GCP. You analyze infrastructure health, performance bottlenecks, and architectural issues. Provide detailed recommendations for improving reliability, performance, and scalability.""",
            
            "performance_analysis": """You are a performance engineering specialist with expertise in cloud performance optimization. You analyze performance metrics, identify bottlenecks, and provide optimization strategies. Focus on improving response times, throughput, and resource utilization.""",
            
            "compliance_audit": """You are a compliance expert with deep knowledge of SOC2, HIPAA, GDPR, PCI-DSS, and other regulatory frameworks. You conduct comprehensive compliance audits and identify gaps, risks, and remediation requirements.""",
            
            "anomaly_detection": """You are a data scientist specializing in anomaly detection and machine learning. You analyze patterns, identify anomalies, and provide insights into unusual behavior. Focus on detecting security threats, performance issues, and cost anomalies.""",
            
            "forecasting": """You are a forecasting expert with expertise in time series analysis and predictive modeling. You analyze trends, make predictions, and provide insights into future resource needs and costs.""",
            
            "comprehensive": """You are a senior cloud architect with comprehensive expertise in cloud infrastructure, security, performance, and cost optimization. You provide holistic analysis and recommendations across all aspects of cloud management.""",
            
            "general": """You are an expert cloud consultant with deep knowledge of cloud infrastructure, security, performance, and cost optimization. You provide insightful analysis and actionable recommendations."""
        }
        
        return system_prompts.get(analysis_type, system_prompts["general"])
    
    async def _get_fallback_response(self, prompt: str, analysis_type: str) -> Dict[str, Any]:
        """Get fallback response when primary providers fail"""
        try:
            # Try providers in order of preference
            providers = ["openai", "anthropic", "google", "ollama"]
            
            for provider in providers:
                try:
                    if provider == "openai" and self.openai_client:
                        return await self._get_openai_response(prompt, analysis_type)
                    elif provider == "anthropic" and self.anthropic_client:
                        return await self._get_anthropic_response(prompt, analysis_type)
                    elif provider == "google" and self.google_ai_client:
                        return await self._get_google_ai_response(prompt, analysis_type)
                    elif provider == "ollama" and self.ollama_client:
                        return await self._get_ollama_response(prompt, analysis_type)
                except Exception as e:
                    logger.warning(f"⚠️ {provider} fallback failed: {e}")
                    continue
            
            # If all providers fail, return a basic response
            return {
                "provider": "fallback",
                "model": "basic",
                "content": f"Analysis for {analysis_type}: Unable to process request due to AI provider issues. Please check your API keys and try again.",
                "usage": {}
            }
            
        except Exception as e:
            logger.error(f"❌ Fallback response failed: {e}")
            raise
    
    async def _get_error_response(self, prompt: str, analysis_type: str, error: str) -> AIResponse:
        """Get error response when all providers fail"""
        return AIResponse(
            provider="error",
            model="none",
            content=f"Error performing {analysis_type} analysis: {error}",
            usage={},
            latency_ms=0,
            timestamp=datetime.now()
        )
    
    async def test_openai_connection(self) -> Dict[str, Any]:
        """Test OpenAI API connection"""
        if not self.openai_client:
            return {
                "status": "error",
                "message": "OpenAI client not initialized - API key not configured",
                "provider": "openai"
            }
        
        try:
            start_time = datetime.now()
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello! Please respond with 'OpenAI connection successful'."}
                ],
                max_tokens=50,
                temperature=0.1
            )
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            return {
                "status": "success",
                "message": "OpenAI connection successful",
                "provider": "openai",
                "model": settings.OPENAI_MODEL,
                "response": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "latency_ms": latency
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": f"OpenAI connection failed: {str(e)}",
                "provider": "openai"
            }
    
    async def test_anthropic_connection(self) -> Dict[str, Any]:
        """Test Anthropic API connection"""
        if not self.anthropic_client:
            return {
                "status": "error",
                "message": "Anthropic client not initialized - API key not configured",
                "provider": "anthropic"
            }
        
        try:
            start_time = datetime.now()
            
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=settings.ANTHROPIC_MODEL,
                max_tokens=50,
                temperature=0.1,
                messages=[
                    {"role": "user", "content": "Hello! Please respond with 'Anthropic connection successful'."}
                ]
            )
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            return {
                "status": "success",
                "message": "Anthropic connection successful",
                "provider": "anthropic",
                "model": settings.ANTHROPIC_MODEL,
                "response": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "latency_ms": latency
            }
            
        except Exception as e:
            logger.error(f"❌ Anthropic connection test failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Anthropic connection failed: {str(e)}",
                "provider": "anthropic"
            }
    
    async def analyze_cost_data(self, cost_data: Dict[str, Any], provider: str = "openai") -> AIResponse:
        """Analyze cost data using AI"""
        prompt = self._create_cost_analysis_prompt(cost_data)
        
        if provider == "openai":
            return await self._call_openai(prompt, "cost_analysis")
        elif provider == "anthropic":
            return await self._call_anthropic(prompt, "cost_analysis")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def analyze_security_data(self, security_data: Dict[str, Any], provider: str = "anthropic") -> AIResponse:
        """Analyze security data using AI"""
        prompt = self._create_security_analysis_prompt(security_data)
        
        if provider == "openai":
            return await self._call_openai(prompt, "security_analysis")
        elif provider == "anthropic":
            return await self._call_anthropic(prompt, "security_analysis")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def generate_optimization_recommendations(self, data: Dict[str, Any], provider: str = "anthropic") -> AIResponse:
        """Generate optimization recommendations using AI"""
        prompt = self._create_optimization_prompt(data)
        
        if provider == "openai":
            return await self._call_openai(prompt, "optimization")
        elif provider == "anthropic":
            return await self._call_anthropic(prompt, "optimization")
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    async def _call_openai(self, prompt: str, task_type: str) -> AIResponse:
        """Call OpenAI API with proper error handling"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        try:
            start_time = datetime.now()
            
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(task_type)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE
            )
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            return AIResponse(
                provider="openai",
                model=settings.OPENAI_MODEL,
                content=response.choices[0].message.content,
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                latency_ms=latency,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"❌ OpenAI API call failed: {str(e)}")
            raise
    
    async def _call_anthropic(self, prompt: str, task_type: str) -> AIResponse:
        """Call Anthropic API with proper error handling"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        try:
            start_time = datetime.now()
            
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=settings.ANTHROPIC_MODEL,
                max_tokens=settings.ANTHROPIC_MAX_TOKENS,
                temperature=settings.ANTHROPIC_TEMPERATURE,
                messages=[
                    {"role": "user", "content": f"{self._get_system_prompt(task_type)}\n\n{prompt}"}
                ]
            )
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            
            return AIResponse(
                provider="anthropic",
                model=settings.ANTHROPIC_MODEL,
                content=response.content[0].text,
                usage={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                latency_ms=latency,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"❌ Anthropic API call failed: {str(e)}")
            raise
    
    def _get_system_prompt(self, task_type: str) -> str:
        """Get system prompt for different task types"""
        prompts = {
            "cost_analysis": """You are an expert cloud cost optimization analyst. Analyze the provided cost data and provide actionable insights for cost reduction and optimization. Focus on specific recommendations with potential savings estimates.""",
            
            "security_analysis": """You are an expert cloud security analyst. Analyze the provided security data and identify potential vulnerabilities, compliance issues, and security recommendations. Provide specific actionable steps for remediation.""",
            
            "optimization": """You are an expert cloud infrastructure optimization specialist. Analyze the provided data and generate specific, actionable recommendations for performance improvement, cost optimization, and best practices implementation."""
        }
        
        return prompts.get(task_type, "You are a helpful cloud engineering assistant.")
    
    def _create_cost_analysis_prompt(self, cost_data: Dict[str, Any]) -> str:
        """Create cost analysis prompt"""
        return f"""
Please analyze the following cloud cost data and provide detailed insights:

Cost Data:
{self._format_cost_data(cost_data)}

Please provide:
1. Key cost trends and patterns
2. Specific optimization opportunities
3. Estimated potential savings
4. Actionable recommendations
5. Risk assessment for proposed changes

Format your response as a structured analysis with clear sections.
"""
    
    def _create_security_analysis_prompt(self, security_data: Dict[str, Any]) -> str:
        """Create security analysis prompt"""
        return f"""
Please analyze the following security scan data and provide comprehensive security insights:

Security Data:
{self._format_security_data(security_data)}

Please provide:
1. Critical vulnerabilities identified
2. Compliance assessment
3. Security risk scoring
4. Remediation priorities
5. Security best practices recommendations

Format your response as a structured security analysis with clear sections.
"""
    
    def _create_optimization_prompt(self, data: Dict[str, Any]) -> str:
        """Create optimization prompt"""
        return f"""
Please analyze the following infrastructure and performance data to generate optimization recommendations:

Data:
{self._format_optimization_data(data)}

Please provide:
1. Performance bottlenecks identified
2. Resource optimization opportunities
3. Cost reduction strategies
4. Best practices implementation
5. Risk assessment for changes

Format your response as a structured optimization plan with clear sections.
"""
    
    def _format_cost_data(self, data: Dict[str, Any]) -> str:
        """Format cost data for AI analysis"""
        return str(data)  # Simplified for now
    
    def _format_security_data(self, data: Dict[str, Any]) -> str:
        """Format security data for AI analysis"""
        return str(data)  # Simplified for now
    
    def _format_optimization_data(self, data: Dict[str, Any]) -> str:
        """Format optimization data for AI analysis"""
        return str(data)  # Simplified for now
    
    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all AI providers"""
        status = {
            "openai": {
                "configured": bool(self.openai_client),
                "model": settings.OPENAI_MODEL if self.openai_client else None
            },
            "anthropic": {
                "configured": bool(self.anthropic_client),
                "model": settings.ANTHROPIC_MODEL if self.anthropic_client else None
            }
        }
        
        return status 