"""
RAG (Retrieval Augmented Generation) Engine for CloudMind
Provides context-aware AI responses using document retrieval and knowledge base integration
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import asyncio
from dataclasses import dataclass

from app.core.config import settings
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


# Expose AI service at module scope for test patching
try:
    from app.services.ai_engine.god_tier_ai_service import god_tier_ai_service as _god_tier_ai_service
    god_tier_ai_service = _god_tier_ai_service
except Exception:
    god_tier_ai_service = None  # Will be patched or imported lazily


@dataclass
class Document:
    """Represents a document in the knowledge base"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class SearchResult:
    """Represents a search result with relevance score"""
    document: Document
    score: float
    context: str


class RAGEngine:
    """Retrieval Augmented Generation Engine"""
    
    def __init__(self):
        self.knowledge_base: Dict[str, Document] = {}
        self.embeddings_cache: Dict[str, List[float]] = {}
        self.search_index: Dict[str, List[str]] = {}
        
    async def initialize(self):
        """Initialize the RAG engine"""
        try:
            logger.info("🔄 Initializing RAG Engine...")
            
            # Load existing knowledge base
            await self._load_knowledge_base()
            
            # Initialize embeddings (if available)
            await self._initialize_embeddings()
            
            # Build search index
            await self._build_search_index()
            
            logger.info("✅ RAG Engine initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ RAG Engine initialization failed: {e}")
            raise
    
    async def add_document(self, content: str, metadata: Dict[str, Any]) -> str:
        """Add a document to the knowledge base"""
        async def _add_doc():
            doc_id = f"doc_{len(self.knowledge_base) + 1}_{datetime.utcnow().timestamp()}"
            
            document = Document(
                id=doc_id,
                content=content,
                metadata=metadata
            )
            
            # Generate embedding if possible
            # Always attempt embedding generation; tests mock _generate_embedding
            try:
                document.embedding = await self._generate_embedding(content)
            except Exception:
                document.embedding = None
            
            self.knowledge_base[doc_id] = document
            
            # Update search index
            await self._index_document(document)
            
            logger.info(f"📄 Added document {doc_id} to knowledge base")
            return doc_id
        
        return await async_with_retries(_add_doc, attempts=3, retry_on=(TransientError,))
    
    async def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Search for relevant documents"""
        try:
            results = []
            
            # Simple keyword-based search (fallback)
            keyword_results = await self._keyword_search(query, top_k)
            results.extend(keyword_results)
            
            # Semantic search if embeddings available
            if settings.OPENAI_API_KEY and self.embeddings_cache:
                semantic_results = await self._semantic_search(query, top_k)
                results.extend(semantic_results)
            
            # Deduplicate and sort by score
            unique_results = self._deduplicate_results(results)
            sorted_results = sorted(unique_results, key=lambda x: x.score, reverse=True)
            
            return sorted_results[:top_k]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    async def generate_response(
        self, 
        query: str, 
        context_documents: List[Document],
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate a response using retrieved context"""
        try:
            if not context_documents:
                return "I don't have enough context to answer that question."
            
            # Build context from documents
            context = self._build_context(context_documents)
            
            # Create enhanced prompt
            enhanced_prompt = self._create_enhanced_prompt(query, context, system_prompt)
            
            # Generate response using AI service
            response = await self._generate_ai_response(enhanced_prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I encountered an error while generating a response."
    
    async def _load_knowledge_base(self):
        """Load existing knowledge base from storage"""
        try:
            # Load knowledge base from storage
            logger.info("📚 Loading knowledge base...")
            
            # Try to load from database first, fallback to default documents
            try:
                # In a production environment, this would load from database
                # For now, we'll use default documents as the knowledge base
                pass
            except Exception as e:
                logger.warning(f"Could not load knowledge base from storage: {e}")
            
            # Add default documents as knowledge base
            default_docs = [
                {
                    "content": "CloudMind is an enterprise cloud management platform that provides cost optimization, security scanning, and AI-powered insights.",
                    "metadata": {"type": "platform_overview", "category": "general"}
                },
                {
                    "content": "The scanner service discovers cloud resources across AWS, Azure, and GCP, providing comprehensive visibility into your infrastructure.",
                    "metadata": {"type": "scanner_info", "category": "discovery"}
                },
                {
                    "content": "Cost optimization recommendations are generated based on resource utilization patterns and pricing analysis.",
                    "metadata": {"type": "cost_info", "category": "optimization"}
                }
            ]
            
            for doc in default_docs:
                await self.add_document(doc["content"], doc["metadata"])
                
        except Exception as e:
            logger.warning(f"Failed to load knowledge base: {e}")
    
    async def _initialize_embeddings(self):
        """Initialize embeddings for existing documents"""
        try:
            if not settings.OPENAI_API_KEY:
                logger.info("⚠️ OpenAI API key not available, skipping embeddings")
                return
            
            logger.info("🧠 Initializing embeddings...")
            
            for doc_id, document in self.knowledge_base.items():
                if not document.embedding:
                    document.embedding = await self._generate_embedding(document.content)
                    self.embeddings_cache[doc_id] = document.embedding
                    
        except Exception as e:
            logger.warning(f"Failed to initialize embeddings: {e}")
    
    async def _build_search_index(self):
        """Build search index for fast retrieval"""
        try:
            logger.info("🔍 Building search index...")
            
            for doc_id, document in self.knowledge_base.items():
                await self._index_document(document)
                
        except Exception as e:
            logger.warning(f"Failed to build search index: {e}")
    
    async def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            import openai
            
            maybe_coro = openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=text
            )
            if asyncio.iscoroutine(maybe_coro):
                response = await maybe_coro
            else:
                response = maybe_coro
            
            return response['data'][0]['embedding']
            
        except Exception as e:
            logger.warning(f"Failed to generate embedding: {e}")
            return []
    
    async def _index_document(self, document: Document):
        """Index a document for search"""
        try:
            # Simple keyword indexing
            words = document.content.lower().split()
            for word in words:
                if word not in self.search_index:
                    self.search_index[word] = []
                if document.id not in self.search_index[word]:
                    self.search_index[word].append(document.id)
                    
        except Exception as e:
            logger.warning(f"Failed to index document {document.id}: {e}")
    
    async def _keyword_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Perform keyword-based search"""
        try:
            results = []
            query_words = query.lower().split()
            
            # Calculate relevance scores
            doc_scores = {}
            for word in query_words:
                if word in self.search_index:
                    for doc_id in self.search_index[word]:
                        if doc_id not in doc_scores:
                            doc_scores[doc_id] = 0
                        doc_scores[doc_id] += 1
            
            # Create search results
            for doc_id, score in doc_scores.items():
                if doc_id in self.knowledge_base:
                    document = self.knowledge_base[doc_id]
                    results.append(SearchResult(
                        document=document,
                        score=score / len(query_words),  # Normalize score
                        context=document.content[:200] + "..."
                    ))
            
            return results
            
        except Exception as e:
            logger.warning(f"Keyword search failed: {e}")
            return []
    
    async def _semantic_search(self, query: str, top_k: int) -> List[SearchResult]:
        """Perform semantic search using embeddings"""
        try:
            if not self.embeddings_cache:
                return []
            
            # Generate query embedding
            query_embedding = await self._generate_embedding(query)
            if not query_embedding:
                return []
            
            results = []
            
            # Calculate cosine similarity
            for doc_id, doc_embedding in self.embeddings_cache.items():
                if doc_id in self.knowledge_base:
                    similarity = self._cosine_similarity(query_embedding, doc_embedding)
                    document = self.knowledge_base[doc_id]
                    results.append(SearchResult(
                        document=document,
                        score=similarity,
                        context=document.content[:200] + "..."
                    ))
            
            return results
            
        except Exception as e:
            logger.warning(f"Semantic search failed: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            if len(vec1) != len(vec2):
                return 0.0
            
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except Exception:
            return 0.0
    
    def _deduplicate_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """Remove duplicate results based on document ID"""
        seen = set()
        unique_results = []
        
        for result in results:
            if result.document.id not in seen:
                seen.add(result.document.id)
                unique_results.append(result)
        
        return unique_results
    
    def _build_context(self, documents: List[Document]) -> str:
        """Build context string from documents"""
        try:
            context_parts = []
            for doc in documents:
                context_parts.append(f"Document: {doc.content}")
            
            return "\n\n".join(context_parts)
            
        except Exception as e:
            logger.warning(f"Failed to build context: {e}")
            return ""
    
    def _create_enhanced_prompt(
        self, 
        query: str, 
        context: str, 
        system_prompt: Optional[str] = None
    ) -> str:
        """Create enhanced prompt with context"""
        try:
            if system_prompt is None:
                system_prompt = "You are a helpful AI assistant for CloudMind, an enterprise cloud management platform."
            
            enhanced_prompt = f"""
{system_prompt}

Context Information:
{context}

User Question: {query}

Please provide a helpful and accurate response based on the context provided.
"""
            return enhanced_prompt.strip()
            
        except Exception as e:
            logger.warning(f"Failed to create enhanced prompt: {e}")
            return query
    
    async def _generate_ai_response(self, prompt: str) -> str:
        """Generate AI response using the configured AI service"""
        try:
            # Use module-level service (patchable in tests); lazy import if missing
            service = god_tier_ai_service
            if service is None:
                from app.services.ai_engine.god_tier_ai_service import god_tier_ai_service as _svc
                service = _svc
            response = await service.generate_response(prompt)
            return response
            
        except Exception as e:
            logger.error(f"AI response generation failed: {e}")
            return "I'm unable to generate a response at the moment."


# Global RAG engine instance
rag_engine = RAGEngine()
