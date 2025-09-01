"""
ML Model Framework for CloudMind
Provides model management, versioning, deployment, and inference capabilities
"""

import logging
import json
import pickle
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import asyncio
from enum import Enum

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from app.core.config import settings
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Types of ML models"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    ANOMALY_DETECTION = "anomaly_detection"
    FORECASTING = "forecasting"
    CLUSTERING = "clustering"
    RECOMMENDATION = "recommendation"


class ModelStatus(Enum):
    """Model deployment status"""
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    FAILED = "failed"


@dataclass
class ModelMetadata:
    """Model metadata and versioning information"""
    model_id: str
    name: str
    version: str
    model_type: ModelType
    description: str
    author: str
    created_at: datetime
    updated_at: datetime
    status: ModelStatus
    accuracy: Optional[float] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    training_data_size: Optional[int] = None
    features: Optional[List[str]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    dependencies: Optional[Dict[str, str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['model_type'] = self.model_type.value
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data


@dataclass
class ModelPrediction:
    """Model prediction result"""
    model_id: str
    prediction: Union[float, int, str, List[float]]
    confidence: Optional[float] = None
    features: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)


class MLModelFramework:
    """ML Model Management Framework"""
    
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.metadata: Dict[str, ModelMetadata] = {}
        self.model_registry: Dict[str, Dict[str, ModelMetadata]] = {}
        self.feature_store: Dict[str, pd.DataFrame] = {}
        self.prediction_cache: Dict[str, List[ModelPrediction]] = {}
        
        # Model storage paths
        self.model_dir = Path("storage/models")
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Load existing models
        self._load_existing_models()
        
        logger.info("🧠 ML Model Framework initialized")
    
    async def register_model(
        self,
        name: str,
        model_type: ModelType,
        description: str,
        author: str,
        model: Optional[BaseEstimator] = None,
        features: Optional[List[str]] = None,
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> str:
        """Register a new model"""
        try:
            model_id = self._generate_model_id(name, author)
            version = "1.0.0"
            
            metadata = ModelMetadata(
                model_id=model_id,
                name=name,
                version=version,
                model_type=model_type,
                description=description,
                author=author,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                status=ModelStatus.TRAINING,
                features=features,
                hyperparameters=hyperparameters
            )
            
            # Store model and metadata
            if model:
                await self._save_model(model_id, model)
                metadata.status = ModelStatus.TRAINED
            
            self.metadata[model_id] = metadata
            
            # Add to registry
            if name not in self.model_registry:
                self.model_registry[name] = {}
            self.model_registry[name][version] = metadata
            
            logger.info(f"📝 Registered model: {name} v{version} ({model_id})")
            return model_id
            
        except Exception as e:
            logger.error(f"Failed to register model: {e}")
            raise
    
    async def train_model(
        self,
        model_id: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        hyperparameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """Train a model and update metrics"""
        try:
            if model_id not in self.metadata:
                raise ValueError(f"Model {model_id} not found")
            
            metadata = self.metadata[model_id]
            metadata.status = ModelStatus.TRAINING
            metadata.training_data_size = len(X_train)
            
            # Get or create model
            model = await self._load_model(model_id)
            if not model:
                model = self._create_model(metadata.model_type, hyperparameters)
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate model
            if X_val is None or y_val is None:
                # Use a portion of training data for validation
                from sklearn.model_selection import train_test_split
                X_train_eval, X_val_eval, y_train_eval, y_val_eval = train_test_split(
                    X_train, y_train, test_size=0.2, random_state=42
                )
                # Retrain on the evaluation training set
                model.fit(X_train_eval, y_train_eval)
                metrics = await self._evaluate_model(model, X_val_eval, y_val_eval)
            else:
                metrics = await self._evaluate_model(model, X_val, y_val)
            
            # Update metadata
            metadata.accuracy = metrics.get('accuracy')
            metadata.precision = metrics.get('precision')
            metadata.recall = metrics.get('recall')
            metadata.f1_score = metrics.get('f1_score')
            metadata.status = ModelStatus.TRAINED
            metadata.updated_at = datetime.now(timezone.utc)
            
            # Save trained model
            await self._save_model(model_id, model)
            
            logger.info(f"🎯 Trained model {model_id} with accuracy: {metrics.get('accuracy', 0):.3f}")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to train model {model_id}: {e}")
            if model_id in self.metadata:
                self.metadata[model_id].status = ModelStatus.FAILED
            raise
    
    async def predict(
        self,
        model_id: str,
        features: Dict[str, Any],
        cache_result: bool = True
    ) -> ModelPrediction:
        """Make a prediction using the specified model"""
        try:
            if model_id not in self.metadata:
                raise ValueError(f"Model {model_id} not found")
            
            metadata = self.metadata[model_id]
            if metadata.status != ModelStatus.TRAINED and metadata.status != ModelStatus.DEPLOYED:
                raise ValueError(f"Model {model_id} is not ready for prediction")
            
            # Load model
            model = await self._load_model(model_id)
            if not model:
                raise ValueError(f"Model {model_id} could not be loaded")
            
            # Prepare features
            X = self._prepare_features(features, metadata.features)
            
            # Make prediction
            prediction = model.predict(X)
            confidence = self._calculate_confidence(model, X) if hasattr(model, 'predict_proba') else None
            
            # Create prediction result
            result = ModelPrediction(
                model_id=model_id,
                prediction=prediction[0] if len(prediction) == 1 else prediction.tolist(),
                confidence=confidence,
                features=features
            )
            
            # Cache result
            if cache_result:
                if model_id not in self.prediction_cache:
                    self.prediction_cache[model_id] = []
                self.prediction_cache[model_id].append(result)
                
                # Keep only recent predictions
                if len(self.prediction_cache[model_id]) > 1000:
                    self.prediction_cache[model_id] = self.prediction_cache[model_id][-1000:]
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to make prediction with model {model_id}: {e}")
            raise
    
    async def deploy_model(self, model_id: str) -> bool:
        """Deploy a trained model"""
        try:
            if model_id not in self.metadata:
                raise ValueError(f"Model {model_id} not found")
            
            metadata = self.metadata[model_id]
            if metadata.status != ModelStatus.TRAINED:
                raise ValueError(f"Model {model_id} must be trained before deployment")
            
            # Verify model can be loaded
            model = await self._load_model(model_id)
            if not model:
                raise ValueError(f"Model {model_id} could not be loaded")
            
            # Update status
            metadata.status = ModelStatus.DEPLOYED
            metadata.updated_at = datetime.now(timezone.utc)
            
            logger.info(f"🚀 Deployed model: {metadata.name} v{metadata.version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deploy model {model_id}: {e}")
            return False
    
    async def get_model_info(self, model_id: str) -> Optional[ModelMetadata]:
        """Get model information"""
        return self.metadata.get(model_id)
    
    async def list_models(self, status: Optional[ModelStatus] = None) -> List[ModelMetadata]:
        """List all models, optionally filtered by status"""
        models = list(self.metadata.values())
        if status:
            models = [m for m in models if m.status == status]
        return models
    
    async def delete_model(self, model_id: str) -> bool:
        """Delete a model"""
        try:
            if model_id not in self.metadata:
                return False
            
            metadata = self.metadata[model_id]
            
            # Remove model file
            model_path = self.model_dir / f"{model_id}.pkl"
            if model_path.exists():
                model_path.unlink()
            
            # Remove from registry
            if metadata.name in self.model_registry:
                if metadata.version in self.model_registry[metadata.name]:
                    del self.model_registry[metadata.name][metadata.version]
                if not self.model_registry[metadata.name]:
                    del self.model_registry[metadata.name]
            
            # Remove metadata and cache
            del self.metadata[model_id]
            if model_id in self.prediction_cache:
                del self.prediction_cache[model_id]
            
            logger.info(f"🗑️ Deleted model: {metadata.name} v{metadata.version}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete model {model_id}: {e}")
            return False
    
    def _generate_model_id(self, name: str, author: str) -> str:
        """Generate unique model ID"""
        timestamp = datetime.now(timezone.utc).timestamp()
        content = f"{name}_{author}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _create_model(self, model_type: ModelType, hyperparameters: Optional[Dict[str, Any]] = None) -> BaseEstimator:
        """Create a new model based on type"""
        try:
            from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
            from sklearn.linear_model import LinearRegression, LogisticRegression
            from sklearn.svm import SVC, SVR
            from sklearn.neural_network import MLPClassifier, MLPRegressor
            
            if model_type == ModelType.CLASSIFICATION:
                return RandomForestClassifier(**(hyperparameters or {}))
            elif model_type == ModelType.REGRESSION:
                return RandomForestRegressor(**(hyperparameters or {}))
            elif model_type == ModelType.ANOMALY_DETECTION:
                return IsolationForest(**(hyperparameters or {}))
            elif model_type == ModelType.FORECASTING:
                return LinearRegression(**(hyperparameters or {}))
            else:
                return RandomForestClassifier(**(hyperparameters or {}))
                
        except Exception as e:
            logger.error(f"Failed to create model: {e}")
            raise
    
    async def _save_model(self, model_id: str, model: BaseEstimator) -> None:
        """Save model to disk"""
        try:
            model_path = self.model_dir / f"{model_id}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
        except Exception as e:
            logger.error(f"Failed to save model {model_id}: {e}")
            raise
    
    async def _load_model(self, model_id: str) -> Optional[BaseEstimator]:
        """Load model from disk"""
        try:
            model_path = self.model_dir / f"{model_id}.pkl"
            if not model_path.exists():
                return None
            
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Failed to load model {model_id}: {e}")
            return None
    
    async def _evaluate_model(
        self,
        model: BaseEstimator,
        X_val: Optional[pd.DataFrame],
        y_val: Optional[pd.Series]
    ) -> Dict[str, float]:
        """Evaluate model performance"""
        try:
            if X_val is None or y_val is None:
                # Use training data for evaluation if no validation data provided
                return {}
            
            y_pred = model.predict(X_val)
            
            metrics = {}
            
            # Calculate appropriate metrics based on model type
            if hasattr(model, 'predict_proba'):
                # Classification model
                metrics['accuracy'] = accuracy_score(y_val, y_pred)
                metrics['precision'] = precision_score(y_val, y_pred, average='weighted')
                metrics['recall'] = recall_score(y_val, y_pred, average='weighted')
                metrics['f1_score'] = f1_score(y_val, y_pred, average='weighted')
            else:
                # Regression model
                from sklearn.metrics import mean_squared_error, r2_score
                metrics['mse'] = mean_squared_error(y_val, y_pred)
                metrics['rmse'] = np.sqrt(metrics['mse'])
                metrics['r2'] = r2_score(y_val, y_pred)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to evaluate model: {e}")
            return {}
    
    def _prepare_features(self, features: Dict[str, Any], expected_features: Optional[List[str]]) -> np.ndarray:
        """Prepare features for prediction"""
        try:
            def _to_numeric(value: Any) -> float:
                # Fast, deterministic encoding for non-numeric values (e.g., categorical strings)
                if isinstance(value, (int, float, np.integer, np.floating)):
                    return float(value)
                if isinstance(value, str):
                    # Stable hash to small float range
                    hashed = int(hashlib.md5(value.encode()).hexdigest()[:6], 16)
                    return float(hashed % 1000) / 1000.0
                try:
                    return float(value)
                except Exception:
                    return 0.0

            if expected_features:
                # Ensure all expected features are present
                X = []
                for feature in expected_features:
                    if feature in features:
                        X.append(_to_numeric(features[feature]))
                    else:
                        X.append(0.0)  # Default value
                return np.asarray(X, dtype=float).reshape(1, -1)
            else:
                # Use all provided features
                return np.asarray([_to_numeric(v) for v in features.values()], dtype=float).reshape(1, -1)
                
        except Exception as e:
            logger.error(f"Failed to prepare features: {e}")
            raise
    
    def _calculate_confidence(self, model: BaseEstimator, X: np.ndarray) -> Optional[float]:
        """Calculate prediction confidence"""
        try:
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)
                return float(np.max(proba))
            return None
        except Exception:
            return None
    
    def _load_existing_models(self) -> None:
        """Load existing models from disk"""
        try:
            for model_file in self.model_dir.glob("*.pkl"):
                model_id = model_file.stem
                metadata_file = self.model_dir / f"{model_id}_metadata.json"
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata_dict = json.load(f)
                    
                    # Reconstruct metadata
                    metadata = ModelMetadata(
                        model_id=metadata_dict['model_id'],
                        name=metadata_dict['name'],
                        version=metadata_dict['version'],
                        model_type=ModelType(metadata_dict['model_type']),
                        description=metadata_dict['description'],
                        author=metadata_dict['author'],
                        created_at=datetime.fromisoformat(metadata_dict['created_at']),
                        updated_at=datetime.fromisoformat(metadata_dict['updated_at']),
                        status=ModelStatus(metadata_dict['status']),
                        accuracy=metadata_dict.get('accuracy'),
                        precision=metadata_dict.get('precision'),
                        recall=metadata_dict.get('recall'),
                        f1_score=metadata_dict.get('f1_score'),
                        training_data_size=metadata_dict.get('training_data_size'),
                        features=metadata_dict.get('features'),
                        hyperparameters=metadata_dict.get('hyperparameters'),
                        dependencies=metadata_dict.get('dependencies')
                    )
                    
                    self.metadata[model_id] = metadata
                    
                    # Add to registry
                    if metadata.name not in self.model_registry:
                        self.model_registry[metadata.name] = {}
                    self.model_registry[metadata.name][metadata.version] = metadata
                    
        except Exception as e:
            logger.warning(f"Failed to load existing models: {e}")


# Global ML framework instance
ml_framework = MLModelFramework()
