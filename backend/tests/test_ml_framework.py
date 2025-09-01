import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timezone

from app.services.ml.ml_framework import (
    MLModelFramework, ModelType, ModelStatus, ModelMetadata, ModelPrediction
)
from app.services.ml.data_pipeline import (
    DataPipeline, DataSource, FeatureDefinition
)


class TestMLModelFramework:
    """Test ML Model Framework functionality"""

    @pytest.fixture
    def ml_framework(self):
        """Create ML framework instance for testing"""
        return MLModelFramework()

    @pytest.fixture
    def sample_data(self):
        """Create sample training data"""
        np.random.seed(42)
        X = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'feature3': np.random.choice(['A', 'B', 'C'], 100)
        })
        y = pd.Series(np.random.choice([0, 1], 100))
        return X, y

    @pytest.mark.asyncio
    async def test_register_model(self, ml_framework):
        """Test model registration"""
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.CLASSIFICATION,
            description="Test classification model",
            author="test_user",
            features=['feature1', 'feature2', 'feature3']
        )
        
        assert model_id in ml_framework.metadata
        metadata = ml_framework.metadata[model_id]
        assert metadata.name == "test_model"
        assert metadata.model_type == ModelType.CLASSIFICATION
        assert metadata.status == ModelStatus.TRAINING

    @pytest.mark.asyncio
    async def test_train_model(self, ml_framework, sample_data):
        """Test model training"""
        X, y = sample_data
        
        # Register model
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.CLASSIFICATION,
            description="Test classification model",
            author="test_user",
            features=['feature1', 'feature2']
        )
        
        # Train model
        metrics = await ml_framework.train_model(model_id, X[['feature1', 'feature2']], y)
        
        assert 'accuracy' in metrics
        assert metrics['accuracy'] > 0
        assert ml_framework.metadata[model_id].status == ModelStatus.TRAINED

    @pytest.mark.asyncio
    async def test_predict(self, ml_framework, sample_data):
        """Test model prediction"""
        X, y = sample_data
        
        # Register and train model
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.CLASSIFICATION,
            description="Test classification model",
            author="test_user",
            features=['feature1', 'feature2']
        )
        
        await ml_framework.train_model(model_id, X[['feature1', 'feature2']], y)
        
        # Make prediction
        features = {'feature1': 0.5, 'feature2': -0.3}
        prediction = await ml_framework.predict(model_id, features)
        
        assert prediction.model_id == model_id
        assert prediction.prediction in [0, 1]
        assert prediction.features == features

    @pytest.mark.asyncio
    async def test_deploy_model(self, ml_framework, sample_data):
        """Test model deployment"""
        X, y = sample_data
        
        # Register and train model
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.CLASSIFICATION,
            description="Test classification model",
            author="test_user"
        )
        
        await ml_framework.train_model(model_id, X[['feature1', 'feature2']], y)
        
        # Deploy model
        success = await ml_framework.deploy_model(model_id)
        
        assert success
        assert ml_framework.metadata[model_id].status == ModelStatus.DEPLOYED

    @pytest.mark.asyncio
    async def test_get_model_info(self, ml_framework):
        """Test getting model information"""
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.REGRESSION,
            description="Test regression model",
            author="test_user"
        )
        
        info = await ml_framework.get_model_info(model_id)
        
        assert info is not None
        assert info.name == "test_model"
        assert info.model_type == ModelType.REGRESSION

    @pytest.mark.asyncio
    async def test_list_models(self, ml_framework):
        """Test listing models"""
        # Register multiple models
        await ml_framework.register_model(
            name="model1",
            model_type=ModelType.CLASSIFICATION,
            description="Model 1",
            author="user1"
        )
        
        await ml_framework.register_model(
            name="model2",
            model_type=ModelType.REGRESSION,
            description="Model 2",
            author="user2"
        )
        
        # List all models
        models = await ml_framework.list_models()
        assert len(models) >= 2
        
        # List only training models
        training_models = await ml_framework.list_models(ModelStatus.TRAINING)
        assert all(m.status == ModelStatus.TRAINING for m in training_models)

    @pytest.mark.asyncio
    async def test_delete_model(self, ml_framework):
        """Test model deletion"""
        model_id = await ml_framework.register_model(
            name="test_model",
            model_type=ModelType.CLASSIFICATION,
            description="Test model",
            author="test_user"
        )
        
        # Delete model
        success = await ml_framework.delete_model(model_id)
        
        assert success
        assert model_id not in ml_framework.metadata

    def test_model_metadata_creation(self):
        """Test ModelMetadata creation"""
        metadata = ModelMetadata(
            model_id="test123",
            name="test_model",
            version="1.0.0",
            model_type=ModelType.CLASSIFICATION,
            description="Test model",
            author="test_user",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            status=ModelStatus.TRAINED,
            accuracy=0.95
        )
        
        assert metadata.model_id == "test123"
        assert metadata.accuracy == 0.95
        assert metadata.status == ModelStatus.TRAINED

    def test_model_prediction_creation(self):
        """Test ModelPrediction creation"""
        prediction = ModelPrediction(
            model_id="test123",
            prediction=1,
            confidence=0.95,
            features={'feature1': 0.5}
        )
        
        assert prediction.model_id == "test123"
        assert prediction.prediction == 1
        assert prediction.confidence == 0.95
        assert prediction.timestamp is not None


class TestDataPipeline:
    """Test Data Pipeline functionality"""

    @pytest.fixture
    def data_pipeline(self):
        """Create data pipeline instance for testing"""
        return DataPipeline()

    @pytest.fixture
    def sample_features(self):
        """Create sample feature definitions"""
        return [
            FeatureDefinition(
                name="cpu_utilization",
                data_type="numeric",
                source="aws_metrics",
                transformation="standardize"
            ),
            FeatureDefinition(
                name="instance_type",
                data_type="categorical",
                source="aws_metrics",
                transformation="encode"
            ),
            FeatureDefinition(
                name="region",
                data_type="categorical",
                source="aws_metrics",
                transformation="encode"
            )
        ]

    @pytest.mark.asyncio
    async def test_add_data_source(self, data_pipeline):
        """Test adding data source"""
        source = DataSource(
            name="test_source",
            source_type="api",
            config={"endpoint": "https://api.example.com"},
            refresh_interval=1800
        )
        
        data_pipeline.add_data_source(source)
        
        assert "test_source" in data_pipeline.data_sources
        assert data_pipeline.data_sources["test_source"].name == "test_source"

    @pytest.mark.asyncio
    async def test_add_feature_definitions(self, data_pipeline, sample_features):
        """Test adding feature definitions"""
        data_pipeline.add_feature_definitions("test_model", sample_features)
        
        assert "test_model" in data_pipeline.feature_definitions
        assert len(data_pipeline.feature_definitions["test_model"]) == 3

    @pytest.mark.asyncio
    async def test_collect_data(self, data_pipeline):
        """Test data collection"""
        data = await data_pipeline.collect_data("aws_metrics")
        
        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert "instance_id" in data.columns

    @pytest.mark.asyncio
    async def test_prepare_features(self, data_pipeline, sample_features):
        """Test feature preparation"""
        # Add feature definitions
        data_pipeline.add_feature_definitions("test_model", sample_features)
        
        # Create sample data
        sample_data = pd.DataFrame({
            'cpu_utilization': [50, 75, 25],
            'instance_type': ['t3.micro', 'm5.large', 'c5.xlarge'],
            'region': ['us-east-1', 'us-west-2', 'eu-west-1'],
            'target': [0, 1, 0]
        })
        
        # Prepare features
        X, y = await data_pipeline.prepare_features("test_model", sample_data, "target")
        
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert len(X) == 3
        assert len(y) == 3

    @pytest.mark.asyncio
    async def test_split_data(self, data_pipeline):
        """Test data splitting"""
        # Create sample data
        X = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100)
        })
        y = pd.Series(np.random.choice([0, 1], 100))
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = await data_pipeline.split_data(X, y)
        
        assert len(X_train) > 0
        assert len(X_val) > 0
        assert len(X_test) > 0
        assert len(y_train) > 0
        assert len(y_val) > 0
        assert len(y_test) > 0

    @pytest.mark.asyncio
    async def test_create_sample_data(self, data_pipeline, sample_features):
        """Test sample data creation"""
        # Add feature definitions
        data_pipeline.add_feature_definitions("test_model", sample_features)
        
        # Create sample data
        sample_data = await data_pipeline.create_sample_data("test_model", num_samples=100)
        
        assert isinstance(sample_data, pd.DataFrame)
        assert len(sample_data) == 100
        assert "cpu_utilization" in sample_data.columns
        assert "instance_type" in sample_data.columns
        assert "region" in sample_data.columns

    @pytest.mark.asyncio
    async def test_feature_transformations(self, data_pipeline):
        """Test feature transformations"""
        # Test standardization
        data = pd.Series([1, 2, 3, 4, 5])
        standardized = await data_pipeline._standardize_feature(data, "test_feature", "test_model")
        
        assert isinstance(standardized, pd.Series)
        assert len(standardized) == 5
        
        # Test encoding
        categorical_data = pd.Series(['A', 'B', 'A', 'C'])
        encoded = await data_pipeline._encode_feature(categorical_data, "test_cat", "test_model")
        
        assert isinstance(encoded, pd.Series)
        assert len(encoded) == 4
        assert all(isinstance(x, (int, np.integer)) for x in encoded)

    def test_data_source_creation(self):
        """Test DataSource creation"""
        source = DataSource(
            name="test_source",
            source_type="aws",
            config={"region": "us-east-1"},
            refresh_interval=3600
        )
        
        assert source.name == "test_source"
        assert source.source_type == "aws"
        assert source.enabled is True

    def test_feature_definition_creation(self):
        """Test FeatureDefinition creation"""
        feature = FeatureDefinition(
            name="cpu_utilization",
            data_type="numeric",
            source="aws_metrics",
            transformation="standardize",
            required=True,
            description="CPU utilization percentage"
        )
        
        assert feature.name == "cpu_utilization"
        assert feature.data_type == "numeric"
        assert feature.transformation == "standardize"


class TestMLIntegration:
    """Test ML framework and data pipeline integration"""

    @pytest.mark.asyncio
    async def test_end_to_end_ml_workflow(self):
        """Test complete ML workflow"""
        # Initialize components
        ml_framework = MLModelFramework()
        data_pipeline = DataPipeline()
        
        # Define features
        features = [
            FeatureDefinition(
                name="cpu_utilization",
                data_type="numeric",
                source="aws_metrics",
                transformation="standardize"
            ),
            FeatureDefinition(
                name="memory_utilization",
                data_type="numeric",
                source="aws_metrics",
                transformation="standardize"
            ),
            FeatureDefinition(
                name="instance_type",
                data_type="categorical",
                source="aws_metrics",
                transformation="encode"
            )
        ]
        
        data_pipeline.add_feature_definitions("cost_optimization", features)
        
        # Create sample data
        sample_data = await data_pipeline.create_sample_data("cost_optimization", num_samples=200)
        sample_data['optimization_target'] = np.random.choice([0, 1], 200)
        
        # Prepare features
        X, y = await data_pipeline.prepare_features("cost_optimization", sample_data, "optimization_target")
        
        # Split data
        X_train, X_val, X_test, y_train, y_val, y_test = await data_pipeline.split_data(X, y)
        
        # Register and train model
        model_id = await ml_framework.register_model(
            name="cost_optimization_model",
            model_type=ModelType.CLASSIFICATION,
            description="Model for cost optimization recommendations",
            author="ml_engineer",
            features=['cpu_utilization', 'memory_utilization', 'instance_type']
        )
        
        # Train model
        metrics = await ml_framework.train_model(model_id, X_train, y_train, X_val, y_val)
        
        assert 'accuracy' in metrics
        assert metrics['accuracy'] > 0
        
        # Deploy model
        success = await ml_framework.deploy_model(model_id)
        assert success
        
        # Make prediction
        features = {
            'cpu_utilization': 75.0,
            'memory_utilization': 60.0,
            'instance_type': 'm5.large'
        }
        
        prediction = await ml_framework.predict(model_id, features)
        
        assert prediction.model_id == model_id
        assert prediction.prediction in [0, 1]
        assert prediction.features == features
