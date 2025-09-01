import pytest
from unittest.mock import Mock, patch, AsyncMock
from app.services.ai_engine.rag_engine import RAGEngine, Document, SearchResult


class TestRAGEngine:
    """Test RAG Engine functionality"""

    @pytest.fixture
    def rag_engine(self):
        """Create RAG engine instance for testing"""
        return RAGEngine()

    @pytest.fixture
    def sample_document(self):
        """Create a sample document for testing"""
        return Document(
            id="test_doc_1",
            content="CloudMind is an enterprise cloud management platform that provides cost optimization and security scanning.",
            metadata={"type": "platform_overview", "category": "general"}
        )

    @pytest.mark.asyncio
    async def test_rag_engine_initialization(self, rag_engine):
        """Test RAG engine initialization"""
        with patch.object(rag_engine, '_load_knowledge_base') as mock_load:
            with patch.object(rag_engine, '_initialize_embeddings') as mock_embeddings:
                with patch.object(rag_engine, '_build_search_index') as mock_index:
                    await rag_engine.initialize()
                    
                    mock_load.assert_called_once()
                    mock_embeddings.assert_called_once()
                    mock_index.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_document(self, rag_engine):
        """Test adding a document to the knowledge base"""
        content = "Test document content"
        metadata = {"type": "test", "category": "testing"}
        
        with patch.object(rag_engine, '_generate_embedding') as mock_embedding:
            mock_embedding.return_value = [0.1, 0.2, 0.3]
            
            doc_id = await rag_engine.add_document(content, metadata)
            
            assert doc_id in rag_engine.knowledge_base
            document = rag_engine.knowledge_base[doc_id]
            assert document.content == content
            assert document.metadata == metadata
            assert document.embedding == [0.1, 0.2, 0.3]

    @pytest.mark.asyncio
    async def test_add_document_without_embeddings(self, rag_engine):
        """Test adding a document when embeddings are not available"""
        content = "Test document content"
        metadata = {"type": "test", "category": "testing"}
        
        with patch.object(rag_engine, '_generate_embedding') as mock_embedding:
            mock_embedding.side_effect = Exception("No API key")
            
            doc_id = await rag_engine.add_document(content, metadata)
            
            assert doc_id in rag_engine.knowledge_base
            document = rag_engine.knowledge_base[doc_id]
            assert document.content == content
            assert document.embedding is None

    @pytest.mark.asyncio
    async def test_keyword_search(self, rag_engine):
        """Test keyword-based search"""
        # Add test documents
        doc1 = Document(
            id="doc1",
            content="CloudMind platform provides cost optimization",
            metadata={"type": "platform"}
        )
        doc2 = Document(
            id="doc2", 
            content="Security scanning features are available",
            metadata={"type": "security"}
        )
        
        rag_engine.knowledge_base["doc1"] = doc1
        rag_engine.knowledge_base["doc2"] = doc2
        
        # Index documents
        await rag_engine._index_document(doc1)
        await rag_engine._index_document(doc2)
        
        # Search for "cost"
        results = await rag_engine._keyword_search("cost", 5)
        
        assert len(results) >= 1
        assert any("cost" in result.document.content.lower() for result in results)

    @pytest.mark.asyncio
    async def test_semantic_search(self, rag_engine):
        """Test semantic search with embeddings"""
        # Mock embeddings
        rag_engine.embeddings_cache = {
            "doc1": [0.1, 0.2, 0.3],
            "doc2": [0.4, 0.5, 0.6]
        }
        
        doc1 = Document(
            id="doc1",
            content="CloudMind platform",
            metadata={"type": "platform"}
        )
        doc2 = Document(
            id="doc2",
            content="Security features",
            metadata={"type": "security"}
        )
        
        rag_engine.knowledge_base["doc1"] = doc1
        rag_engine.knowledge_base["doc2"] = doc2
        
        with patch.object(rag_engine, '_generate_embedding') as mock_embedding:
            mock_embedding.return_value = [0.1, 0.2, 0.3]  # Similar to doc1
            
            results = await rag_engine._semantic_search("cloud platform", 5)
            
            assert len(results) >= 1
            # doc1 should have higher similarity score
            if len(results) >= 2:
                assert results[0].score >= results[1].score

    def test_cosine_similarity(self, rag_engine):
        """Test cosine similarity calculation"""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [1.0, 0.0, 0.0]
        
        similarity = rag_engine._cosine_similarity(vec1, vec2)
        assert similarity == 1.0
        
        vec3 = [0.0, 1.0, 0.0]
        similarity = rag_engine._cosine_similarity(vec1, vec3)
        assert similarity == 0.0
        
        # Test with different lengths
        vec4 = [1.0, 0.0]
        similarity = rag_engine._cosine_similarity(vec1, vec4)
        assert similarity == 0.0

    def test_deduplicate_results(self, rag_engine):
        """Test result deduplication"""
        doc1 = Document(id="doc1", content="test1", metadata={})
        doc2 = Document(id="doc2", content="test2", metadata={})
        
        results = [
            SearchResult(document=doc1, score=0.8, context="test1"),
            SearchResult(document=doc1, score=0.9, context="test1"),  # Duplicate
            SearchResult(document=doc2, score=0.7, context="test2")
        ]
        
        unique_results = rag_engine._deduplicate_results(results)
        
        assert len(unique_results) == 2
        doc_ids = [r.document.id for r in unique_results]
        assert "doc1" in doc_ids
        assert "doc2" in doc_ids

    def test_build_context(self, rag_engine):
        """Test context building from documents"""
        doc1 = Document(id="doc1", content="First document", metadata={})
        doc2 = Document(id="doc2", content="Second document", metadata={})
        
        context = rag_engine._build_context([doc1, doc2])
        
        assert "First document" in context
        assert "Second document" in context
        assert "Document:" in context

    def test_create_enhanced_prompt(self, rag_engine):
        """Test enhanced prompt creation"""
        query = "What is CloudMind?"
        context = "CloudMind is a cloud management platform."
        system_prompt = "You are a helpful assistant."
        
        enhanced_prompt = rag_engine._create_enhanced_prompt(query, context, system_prompt)
        
        assert query in enhanced_prompt
        assert context in enhanced_prompt
        assert system_prompt in enhanced_prompt

    @pytest.mark.asyncio
    async def test_search_integration(self, rag_engine):
        """Test integrated search functionality"""
        # Add test documents
        await rag_engine.add_document(
            "CloudMind provides cost optimization features",
            {"type": "cost"}
        )
        await rag_engine.add_document(
            "Security scanning is available in CloudMind",
            {"type": "security"}
        )
        
        # Search
        results = await rag_engine.search("cost optimization", 5)
        
        assert len(results) >= 1
        assert any("cost" in result.document.content.lower() for result in results)

    @pytest.mark.asyncio
    async def test_generate_response(self, rag_engine):
        """Test response generation with context"""
        # Add test document
        await rag_engine.add_document(
            "CloudMind is an enterprise cloud management platform",
            {"type": "overview"}
        )
        
        # Mock AI service
        with patch('app.services.ai_engine.rag_engine.god_tier_ai_service') as mock_ai:
            mock_ai.generate_response = AsyncMock(return_value="CloudMind is a platform for cloud management.")
            
            response = await rag_engine.generate_response(
                "What is CloudMind?",
                [rag_engine.knowledge_base[list(rag_engine.knowledge_base.keys())[0]]]
            )
            
            assert "CloudMind" in response
            mock_ai.generate_response.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_response_no_context(self, rag_engine):
        """Test response generation without context"""
        response = await rag_engine.generate_response("What is CloudMind?", [])
        
        assert "don't have enough context" in response.lower()

    @pytest.mark.asyncio
    async def test_generate_embedding_success(self, rag_engine):
        """Test successful embedding generation"""
        with patch('openai.Embedding.acreate') as mock_create:
            mock_create.return_value = {
                'data': [{'embedding': [0.1, 0.2, 0.3]}]
            }
            
            embedding = await rag_engine._generate_embedding("test text")
            
            assert embedding == [0.1, 0.2, 0.3]
            mock_create.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_embedding_failure(self, rag_engine):
        """Test embedding generation failure"""
        with patch('openai.Embedding.acreate') as mock_create:
            mock_create.side_effect = Exception("API error")
            
            embedding = await rag_engine._generate_embedding("test text")
            
            assert embedding == []

    def test_document_creation(self, sample_document):
        """Test Document dataclass creation"""
        assert sample_document.id == "test_doc_1"
        assert "CloudMind" in sample_document.content
        assert sample_document.metadata["type"] == "platform_overview"
        assert sample_document.created_at is not None
        assert sample_document.updated_at is not None

    def test_search_result_creation(self, sample_document):
        """Test SearchResult dataclass creation"""
        result = SearchResult(
            document=sample_document,
            score=0.85,
            context="CloudMind is an enterprise..."
        )
        
        assert result.document == sample_document
        assert result.score == 0.85
        assert "CloudMind" in result.context
