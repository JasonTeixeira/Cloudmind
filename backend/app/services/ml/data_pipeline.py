"""
Data Pipeline for CloudMind ML Models
Provides data collection, preprocessing, feature engineering, and validation
"""

import logging
import asyncio
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import json

from app.core.config import settings
from app.utils.retry import async_with_retries, TransientError

logger = logging.getLogger(__name__)


@dataclass
class DataSource:
    """Data source configuration"""
    name: str
    source_type: str  # 'aws', 'azure', 'gcp', 'database', 'api'
    config: Dict[str, Any]
    refresh_interval: int = 3600  # seconds
    last_refresh: Optional[datetime] = None
    enabled: bool = True


@dataclass
class FeatureDefinition:
    """Feature definition for ML models"""
    name: str
    data_type: str  # 'numeric', 'categorical', 'datetime', 'text'
    source: str
    transformation: Optional[str] = None
    required: bool = True
    default_value: Optional[Any] = None
    description: Optional[str] = None


class DataPipeline:
    """Data Pipeline for ML model training and inference"""
    
    def __init__(self):
        self.data_sources: Dict[str, DataSource] = {}
        self.feature_definitions: Dict[str, List[FeatureDefinition]] = {}
        self.scalers: Dict[str, StandardScaler] = {}
        self.encoders: Dict[str, LabelEncoder] = {}
        self.imputers: Dict[str, SimpleImputer] = {}
        self.data_cache: Dict[str, pd.DataFrame] = {}
        self.cache_ttl: Dict[str, datetime] = {}
        
        # Initialize default data sources
        self._initialize_default_sources()
        
        logger.info("📊 Data Pipeline initialized")
    
    def add_data_source(self, source: DataSource) -> None:
        """Add a data source to the pipeline"""
        self.data_sources[source.name] = source
        logger.info(f"📥 Added data source: {source.name}")
    
    def add_feature_definitions(self, model_name: str, features: List[FeatureDefinition]) -> None:
        """Add feature definitions for a model"""
        self.feature_definitions[model_name] = features
        logger.info(f"🔧 Added {len(features)} feature definitions for {model_name}")
    
    async def collect_data(self, source_name: str, force_refresh: bool = False) -> pd.DataFrame:
        """Collect data from a specific source"""
        try:
            if source_name not in self.data_sources:
                raise ValueError(f"Data source {source_name} not found")
            
            source = self.data_sources[source_name]
            
            # Check cache
            if not force_refresh and source_name in self.data_cache:
                if source_name in self.cache_ttl:
                    if datetime.now(timezone.utc) < self.cache_ttl[source_name]:
                        logger.info(f"📋 Using cached data for {source_name}")
                        return self.data_cache[source_name]
            
            # Collect data based on source type
            if source.source_type == 'aws':
                data = await self._collect_aws_data(source)
            elif source.source_type == 'azure':
                data = await self._collect_azure_data(source)
            elif source.source_type == 'gcp':
                data = await self._collect_gcp_data(source)
            elif source.source_type == 'database':
                data = await self._collect_database_data(source)
            elif source.source_type == 'api':
                data = await self._collect_api_data(source)
            else:
                raise ValueError(f"Unsupported source type: {source.source_type}")
            
            # Cache data
            self.data_cache[source_name] = data
            self.cache_ttl[source_name] = datetime.now(timezone.utc) + timedelta(seconds=source.refresh_interval)
            
            # Update last refresh
            source.last_refresh = datetime.now(timezone.utc)
            
            logger.info(f"📥 Collected {len(data)} records from {source_name}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to collect data from {source_name}: {e}")
            raise
    
    async def prepare_features(
        self,
        model_name: str,
        data: pd.DataFrame,
        target_column: Optional[str] = None
    ) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """Prepare features for ML model training/inference"""
        try:
            if model_name not in self.feature_definitions:
                raise ValueError(f"No feature definitions found for {model_name}")
            
            features = self.feature_definitions[model_name]
            processed_data = pd.DataFrame()
            target = None
            
            for feature in features:
                if feature.name in data.columns:
                    # Apply transformations
                    processed_value = await self._apply_transformation(
                        data[feature.name], feature, model_name
                    )
                    processed_data[feature.name] = processed_value
                elif feature.required:
                    if feature.default_value is not None:
                        processed_data[feature.name] = feature.default_value
                    else:
                        raise ValueError(f"Required feature {feature.name} not found in data")
                else:
                    # Optional feature not present
                    continue
            
            # Extract target if specified
            if target_column and target_column in data.columns:
                target = data[target_column]
            
            logger.info(f"🔧 Prepared {len(processed_data.columns)} features for {model_name}")
            return processed_data, target
            
        except Exception as e:
            logger.error(f"Failed to prepare features for {model_name}: {e}")
            raise
    
    async def split_data(
        self,
        X: pd.DataFrame,
        y: Optional[pd.Series] = None,
        test_size: float = 0.2,
        val_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Optional[pd.Series], Optional[pd.Series], Optional[pd.Series]]:
        """Split data into train/validation/test sets"""
        try:
            if y is not None:
                # Split into train and temp
                X_train, X_temp, y_train, y_temp = train_test_split(
                    X, y, test_size=test_size + val_size, random_state=random_state, stratify=y
                )
                
                # Split temp into validation and test
                val_ratio = val_size / (test_size + val_size)
                X_val, X_test, y_val, y_test = train_test_split(
                    X_temp, y_temp, test_size=1 - val_ratio, random_state=random_state, stratify=y_temp
                )
                
                return X_train, X_val, X_test, y_train, y_val, y_test
            else:
                # No target variable
                X_train, X_temp = train_test_split(X, test_size=test_size + val_size, random_state=random_state)
                val_ratio = val_size / (test_size + val_size)
                X_val, X_test = train_test_split(X_temp, test_size=1 - val_ratio, random_state=random_state)
                
                return X_train, X_val, X_test, None, None, None
                
        except Exception as e:
            logger.error(f"Failed to split data: {e}")
            raise
    
    async def create_sample_data(self, model_name: str, num_samples: int = 1000) -> pd.DataFrame:
        """Create sample data for testing and development"""
        try:
            if model_name not in self.feature_definitions:
                raise ValueError(f"No feature definitions found for {model_name}")
            
            features = self.feature_definitions[model_name]
            sample_data = pd.DataFrame()
            
            for feature in features:
                if feature.data_type == 'numeric':
                    # Generate random numeric data
                    if 'cost' in feature.name.lower():
                        sample_data[feature.name] = np.random.uniform(10, 1000, num_samples)
                    elif 'cpu' in feature.name.lower():
                        sample_data[feature.name] = np.random.uniform(0, 100, num_samples)
                    elif 'memory' in feature.name.lower():
                        sample_data[feature.name] = np.random.uniform(1, 64, num_samples)
                    else:
                        sample_data[feature.name] = np.random.normal(0, 1, num_samples)
                
                elif feature.data_type == 'categorical':
                    # Generate random categorical data
                    if 'region' in feature.name.lower():
                        categories = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
                    elif 'instance_type' in feature.name.lower():
                        categories = ['t3.micro', 't3.small', 'm5.large', 'c5.xlarge']
                    elif 'status' in feature.name.lower():
                        categories = ['running', 'stopped', 'terminated']
                    else:
                        categories = ['A', 'B', 'C', 'D']
                    
                    sample_data[feature.name] = np.random.choice(categories, num_samples)
                
                elif feature.data_type == 'datetime':
                    # Generate random datetime data
                    start_date = datetime.now(timezone.utc) - timedelta(days=30)
                    end_date = datetime.now(timezone.utc)
                    sample_data[feature.name] = pd.date_range(start_date, end_date, periods=num_samples)
                
                else:
                    # Default to numeric
                    sample_data[feature.name] = np.random.normal(0, 1, num_samples)
            
            logger.info(f"🎲 Created {num_samples} sample records for {model_name}")
            return sample_data
            
        except Exception as e:
            logger.error(f"Failed to create sample data for {model_name}: {e}")
            raise
    
    async def _apply_transformation(
        self,
        data: pd.Series,
        feature: FeatureDefinition,
        model_name: str
    ) -> pd.Series:
        """Apply transformation to a feature"""
        try:
            if feature.transformation:
                if feature.transformation == 'standardize':
                    return await self._standardize_feature(data, feature.name, model_name)
                elif feature.transformation == 'normalize':
                    return await self._normalize_feature(data, feature.name, model_name)
                elif feature.transformation == 'encode':
                    return await self._encode_feature(data, feature.name, model_name)
                elif feature.transformation == 'impute':
                    return await self._impute_feature(data, feature.name, model_name)
                else:
                    logger.warning(f"Unknown transformation: {feature.transformation}")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to apply transformation {feature.transformation} to {feature.name}: {e}")
            return data
    
    async def _standardize_feature(self, data: pd.Series, feature_name: str, model_name: str) -> pd.Series:
        """Standardize a numeric feature"""
        try:
            scaler_key = f"{model_name}_{feature_name}_scaler"
            
            if scaler_key not in self.scalers:
                self.scalers[scaler_key] = StandardScaler()
                # Fit on non-null data
                non_null_data = data.dropna()
                if len(non_null_data) > 0:
                    self.scalers[scaler_key].fit(non_null_data.values.reshape(-1, 1))
            
            # Transform data
            transformed = self.scalers[scaler_key].transform(data.values.reshape(-1, 1))
            return pd.Series(transformed.flatten(), index=data.index)
            
        except Exception as e:
            logger.error(f"Failed to standardize {feature_name}: {e}")
            return data
    
    async def _normalize_feature(self, data: pd.Series, feature_name: str, model_name: str) -> pd.Series:
        """Normalize a numeric feature"""
        try:
            scaler_key = f"{model_name}_{feature_name}_normalizer"
            
            if scaler_key not in self.scalers:
                self.scalers[scaler_key] = MinMaxScaler()
                # Fit on non-null data
                non_null_data = data.dropna()
                if len(non_null_data) > 0:
                    self.scalers[scaler_key].fit(non_null_data.values.reshape(-1, 1))
            
            # Transform data
            transformed = self.scalers[scaler_key].transform(data.values.reshape(-1, 1))
            return pd.Series(transformed.flatten(), index=data.index)
            
        except Exception as e:
            logger.error(f"Failed to normalize {feature_name}: {e}")
            return data
    
    async def _encode_feature(self, data: pd.Series, feature_name: str, model_name: str) -> pd.Series:
        """Encode a categorical feature"""
        try:
            encoder_key = f"{model_name}_{feature_name}_encoder"
            
            if encoder_key not in self.encoders:
                self.encoders[encoder_key] = LabelEncoder()
                # Fit on non-null data
                non_null_data = data.dropna()
                if len(non_null_data) > 0:
                    self.encoders[encoder_key].fit(non_null_data)
            
            # Transform data
            encoded = self.encoders[encoder_key].transform(data.fillna('UNKNOWN'))
            return pd.Series(encoded, index=data.index)
            
        except Exception as e:
            logger.error(f"Failed to encode {feature_name}: {e}")
            return data
    
    async def _impute_feature(self, data: pd.Series, feature_name: str, model_name: str) -> pd.Series:
        """Impute missing values in a feature"""
        try:
            imputer_key = f"{model_name}_{feature_name}_imputer"
            
            if imputer_key not in self.imputers:
                self.imputers[imputer_key] = SimpleImputer(strategy='mean')
                # Fit on non-null data
                non_null_data = data.dropna()
                if len(non_null_data) > 0:
                    self.imputers[imputer_key].fit(non_null_data.values.reshape(-1, 1))
            
            # Transform data
            imputed = self.imputers[imputer_key].transform(data.values.reshape(-1, 1))
            return pd.Series(imputed.flatten(), index=data.index)
            
        except Exception as e:
            logger.error(f"Failed to impute {feature_name}: {e}")
            return data
    
    async def _collect_aws_data(self, source: DataSource) -> pd.DataFrame:
        """Collect data from AWS"""
        try:
            # Mock AWS data collection
            # In production, this would use boto3 to collect real data
            data = {
                'instance_id': [f'i-{i:08x}' for i in range(100)],
                'instance_type': np.random.choice(['t3.micro', 't3.small', 'm5.large'], 100),
                'region': np.random.choice(['us-east-1', 'us-west-2', 'eu-west-1'], 100),
                'cpu_utilization': np.random.uniform(0, 100, 100),
                'memory_utilization': np.random.uniform(0, 100, 100),
                'network_io': np.random.uniform(0, 1000, 100),
                'cost_per_hour': np.random.uniform(0.01, 2.0, 100),
                'status': np.random.choice(['running', 'stopped'], 100),
                'launch_time': pd.date_range(start='2024-01-01', periods=100, freq='D')
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Failed to collect AWS data: {e}")
            raise
    
    async def _collect_azure_data(self, source: DataSource) -> pd.DataFrame:
        """Collect data from Azure"""
        try:
            # Mock Azure data collection
            data = {
                'vm_id': [f'vm-{i:08x}' for i in range(100)],
                'vm_size': np.random.choice(['Standard_B1s', 'Standard_B2s', 'Standard_D2s_v3'], 100),
                'location': np.random.choice(['eastus', 'westus2', 'westeurope'], 100),
                'cpu_percent': np.random.uniform(0, 100, 100),
                'memory_percent': np.random.uniform(0, 100, 100),
                'network_bytes': np.random.uniform(0, 1000, 100),
                'cost_per_hour': np.random.uniform(0.01, 2.0, 100),
                'power_state': np.random.choice(['running', 'deallocated'], 100),
                'created_time': pd.date_range(start='2024-01-01', periods=100, freq='D')
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Failed to collect Azure data: {e}")
            raise
    
    async def _collect_gcp_data(self, source: DataSource) -> pd.DataFrame:
        """Collect data from GCP"""
        try:
            # Mock GCP data collection
            data = {
                'instance_id': [f'gcp-{i:08x}' for i in range(100)],
                'machine_type': np.random.choice(['e2-micro', 'e2-small', 'n1-standard-1'], 100),
                'zone': np.random.choice(['us-central1-a', 'us-west1-b', 'europe-west1-c'], 100),
                'cpu_usage': np.random.uniform(0, 100, 100),
                'memory_usage': np.random.uniform(0, 100, 100),
                'network_usage': np.random.uniform(0, 1000, 100),
                'cost_per_hour': np.random.uniform(0.01, 2.0, 100),
                'status': np.random.choice(['RUNNING', 'STOPPED'], 100),
                'creation_timestamp': pd.date_range(start='2024-01-01', periods=100, freq='D')
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Failed to collect GCP data: {e}")
            raise
    
    async def _collect_database_data(self, source: DataSource) -> pd.DataFrame:
        """Collect data from database"""
        try:
            # Mock database data collection
            data = {
                'id': range(100),
                'name': [f'resource_{i}' for i in range(100)],
                'type': np.random.choice(['compute', 'storage', 'network'], 100),
                'value': np.random.uniform(0, 1000, 100),
                'category': np.random.choice(['A', 'B', 'C'], 100),
                'created_at': pd.date_range(start='2024-01-01', periods=100, freq='D')
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Failed to collect database data: {e}")
            raise
    
    async def _collect_api_data(self, source: DataSource) -> pd.DataFrame:
        """Collect data from API"""
        try:
            # Mock API data collection
            data = {
                'api_id': [f'api-{i:08x}' for i in range(100)],
                'endpoint': [f'/api/v{i}/data' for i in range(100)],
                'response_time': np.random.uniform(0, 5000, 100),
                'status_code': np.random.choice([200, 400, 500], 100),
                'requests_per_minute': np.random.uniform(0, 1000, 100),
                'error_rate': np.random.uniform(0, 0.1, 100),
                'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='D')
            }
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f"Failed to collect API data: {e}")
            raise
    
    def _initialize_default_sources(self) -> None:
        """Initialize default data sources"""
        try:
            # AWS data source
            aws_source = DataSource(
                name="aws_metrics",
                source_type="aws",
                config={
                    "regions": ["us-east-1", "us-west-2"],
                    "services": ["ec2", "rds", "s3"]
                },
                refresh_interval=3600
            )
            self.add_data_source(aws_source)
            
            # Azure data source
            azure_source = DataSource(
                name="azure_metrics",
                source_type="azure",
                config={
                    "subscriptions": ["default"],
                    "services": ["compute", "storage"]
                },
                refresh_interval=3600
            )
            self.add_data_source(azure_source)
            
            # GCP data source
            gcp_source = DataSource(
                name="gcp_metrics",
                source_type="gcp",
                config={
                    "projects": ["default"],
                    "services": ["compute", "storage"]
                },
                refresh_interval=3600
            )
            self.add_data_source(gcp_source)
            
        except Exception as e:
            logger.warning(f"Failed to initialize default sources: {e}")


# Global data pipeline instance
data_pipeline = DataPipeline()
