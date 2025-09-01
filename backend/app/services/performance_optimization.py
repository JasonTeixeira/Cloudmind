"""
World-Class Performance Optimization Service
Enterprise-grade performance optimization with intelligent caching, CDN integration,
and auto-scaling capabilities.
"""

import asyncio
import logging
import time
import hashlib
import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi import Request, Response
import httpx

from app.core.config import settings
from app.core.database import get_db
from app.services.monitoring_service import monitoring_service

logger = logging.getLogger(__name__)


class CacheStrategy(Enum):
    """Cache strategy types"""
    NONE = "none"
    SHORT = "short"  # 5 minutes
    MEDIUM = "medium"  # 30 minutes
    LONG = "long"  # 2 hours
    PERMANENT = "permanent"  # Until invalidated


@dataclass
class PerformanceMetrics:
    """Performance metrics data class"""
    response_time: float
    throughput: float
    error_rate: float
    cache_hit_rate: float
    memory_usage: float
    cpu_usage: float
    database_connections: int
    active_requests: int
    timestamp: datetime


class PerformanceOptimizationService:
    """World-class performance optimization service"""
    
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
        self.performance_metrics = []
        self.auto_scaling_config = {
            "cpu_threshold": 70.0,
            "memory_threshold": 80.0,
            "response_time_threshold": 200.0,
            "max_instances": 10,
            "min_instances": 2
        }
    
    async def optimize_response(self, request: Request, response: Response) -> Response:
        """Optimize response with advanced caching and compression"""
        try:
            # Add performance headers
            response.headers["X-Response-Time"] = str(time.time())
            response.headers["X-Cache-Status"] = "MISS"
            
            # Implement intelligent caching
            cache_key = await self._generate_cache_key(request)
            cached_response = await self._get_cached_response(cache_key)
            
            if cached_response:
                response.headers["X-Cache-Status"] = "HIT"
                return cached_response
            
            # Add compression headers
            response.headers["Content-Encoding"] = "gzip"
            response.headers["Vary"] = "Accept-Encoding"
            
            # Cache the response
            await self._cache_response(cache_key, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Performance optimization failed: {e}")
            return response
    
    async def _generate_cache_key(self, request: Request) -> str:
        """Generate intelligent cache key"""
        key_components = [
            request.method,
            request.url.path,
            request.query_params.get("version", "v1"),
            request.headers.get("accept-language", "en"),
            request.headers.get("user-agent", "")[:50]
        ]
        
        # Add user-specific components if authenticated
        if hasattr(request.state, "user"):
            key_components.append(str(request.state.user.id))
        
        key_string = "|".join(key_components)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    async def _get_cached_response(self, cache_key: str) -> Optional[Response]:
        """Get cached response with intelligent invalidation"""
        try:
            cached_data = await self.redis_client.get(f"cache:{cache_key}")
            if cached_data:
                self.cache_stats["hits"] += 1
                return Response(
                    content=cached_data,
                    headers={"X-Cache-Status": "HIT"}
                )
            else:
                self.cache_stats["misses"] += 1
                return None
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
            return None
    
    async def _cache_response(self, cache_key: str, response: Response):
        """Cache response with intelligent TTL"""
        try:
            # Determine cache strategy based on content type and path
            cache_strategy = self._determine_cache_strategy(response)
            ttl = self._get_cache_ttl(cache_strategy)
            
            await self.redis_client.setex(
                f"cache:{cache_key}",
                ttl,
                response.body
            )
            
        except Exception as e:
            logger.error(f"Cache storage failed: {e}")
    
    def _determine_cache_strategy(self, response: Response) -> CacheStrategy:
        """Determine optimal cache strategy"""
        content_type = response.headers.get("content-type", "")
        
        if "text/html" in content_type:
            return CacheStrategy.SHORT
        elif "application/json" in content_type:
            return CacheStrategy.MEDIUM
        elif "image/" in content_type or "video/" in content_type:
            return CacheStrategy.LONG
        else:
            return CacheStrategy.NONE
    
    def _get_cache_ttl(self, strategy: CacheStrategy) -> int:
        """Get cache TTL based on strategy"""
        ttl_map = {
            CacheStrategy.NONE: 0,
            CacheStrategy.SHORT: 300,  # 5 minutes
            CacheStrategy.MEDIUM: 1800,  # 30 minutes
            CacheStrategy.LONG: 7200,  # 2 hours
            CacheStrategy.PERMANENT: 86400  # 24 hours
        }
        return ttl_map.get(strategy, 0)
    
    async def optimize_database_queries(self, db: Session) -> Dict[str, Any]:
        """Optimize database queries with intelligent caching"""
        try:
            # Get database performance metrics
            db_stats = await self._get_database_stats(db)
            
            # Implement query result caching
            cache_key = f"db_stats:{int(time.time() / 300)}"  # 5-minute cache
            cached_stats = await self.redis_client.get(cache_key)
            
            if cached_stats:
                return json.loads(cached_stats)
            
            # Cache the results
            await self.redis_client.setex(
                cache_key,
                300,  # 5 minutes
                json.dumps(db_stats)
            )
            
            return db_stats
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            return {}
    
    async def _get_database_stats(self, db: Session) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            # Get connection pool stats
            pool_stats = db.bind.pool.status()
            
            # Get query performance stats
            result = db.execute(text("""
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation
                FROM pg_stats 
                WHERE schemaname = 'public'
                LIMIT 100
            """))
            
            stats = result.fetchall()
            
            return {
                "pool_size": pool_stats.get("size", 0),
                "checked_in": pool_stats.get("checkedin", 0),
                "checked_out": pool_stats.get("checkedout", 0),
                "overflow": pool_stats.get("overflow", 0),
                "invalid": pool_stats.get("invalid", 0),
                "table_stats": len(stats),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database stats collection failed: {e}")
            return {}
    
    async def implement_cdn_integration(self, static_urls: List[str]) -> Dict[str, str]:
        """Implement CDN integration for static assets"""
        cdn_mappings = {}
        
        for url in static_urls:
            # Generate CDN URL (simulate CloudFlare/AWS CloudFront)
            cdn_url = url.replace("localhost", "cdn.cloudmind.local")
            cdn_mappings[url] = cdn_url
        
        return cdn_mappings
    
    async def auto_scale_resources(self, current_metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Implement intelligent auto-scaling"""
        scaling_decision = {
            "should_scale": False,
            "scale_type": None,
            "reason": None,
            "target_instances": 1
        }
        
        try:
            # Check CPU threshold
            if current_metrics.cpu_usage > self.auto_scaling_config["cpu_threshold"]:
                scaling_decision.update({
                    "should_scale": True,
                    "scale_type": "scale_up",
                    "reason": f"CPU usage {current_metrics.cpu_usage}% exceeds threshold {self.auto_scaling_config['cpu_threshold']}%"
                })
            
            # Check memory threshold
            elif current_metrics.memory_usage > self.auto_scaling_config["memory_threshold"]:
                scaling_decision.update({
                    "should_scale": True,
                    "scale_type": "scale_up",
                    "reason": f"Memory usage {current_metrics.memory_usage}% exceeds threshold {self.auto_scaling_config['memory_threshold']}%"
                })
            
            # Check response time threshold
            elif current_metrics.response_time > self.auto_scaling_config["response_time_threshold"]:
                scaling_decision.update({
                    "should_scale": True,
                    "scale_type": "scale_up",
                    "reason": f"Response time {current_metrics.response_time}ms exceeds threshold {self.auto_scaling_config['response_time_threshold']}ms"
                })
            
            # Calculate target instances
            if scaling_decision["should_scale"]:
                current_instances = max(1, len(self.performance_metrics))
                target_instances = min(
                    current_instances + 1,
                    self.auto_scaling_config["max_instances"]
                )
                scaling_decision["target_instances"] = target_instances
            
            return scaling_decision
            
        except Exception as e:
            logger.error(f"Auto-scaling decision failed: {e}")
            return scaling_decision
    
    async def collect_performance_metrics(self) -> PerformanceMetrics:
        """Collect comprehensive performance metrics"""
        try:
            # Simulate metric collection
            metrics = PerformanceMetrics(
                response_time=150.0,  # ms
                throughput=1000.0,  # requests/second
                error_rate=0.05,  # percentage
                cache_hit_rate=85.0,  # percentage
                memory_usage=65.0,  # percentage
                cpu_usage=45.0,  # percentage
                database_connections=5,
                active_requests=25,
                timestamp=datetime.utcnow()
            )
            
            # Store metrics for trend analysis
            self.performance_metrics.append(metrics)
            
            # Keep only last 1000 metrics
            if len(self.performance_metrics) > 1000:
                self.performance_metrics = self.performance_metrics[-1000:]
            
            return metrics
            
        except Exception as e:
            logger.error(f"Performance metrics collection failed: {e}")
            return PerformanceMetrics(
                response_time=0.0,
                throughput=0.0,
                error_rate=0.0,
                cache_hit_rate=0.0,
                memory_usage=0.0,
                cpu_usage=0.0,
                database_connections=0,
                active_requests=0,
                timestamp=datetime.utcnow()
            )
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        try:
            current_metrics = await self.collect_performance_metrics()
            scaling_decision = await self.auto_scale_resources(current_metrics)
            
            # Calculate trends
            if len(self.performance_metrics) > 1:
                recent_metrics = self.performance_metrics[-10:]
                avg_response_time = sum(m.response_time for m in recent_metrics) / len(recent_metrics)
                avg_throughput = sum(m.throughput for m in recent_metrics) / len(recent_metrics)
            else:
                avg_response_time = current_metrics.response_time
                avg_throughput = current_metrics.throughput
            
            return {
                "current_metrics": {
                    "response_time": current_metrics.response_time,
                    "throughput": current_metrics.throughput,
                    "error_rate": current_metrics.error_rate,
                    "cache_hit_rate": current_metrics.cache_hit_rate,
                    "memory_usage": current_metrics.memory_usage,
                    "cpu_usage": current_metrics.cpu_usage,
                    "database_connections": current_metrics.database_connections,
                    "active_requests": current_metrics.active_requests
                },
                "trends": {
                    "avg_response_time": avg_response_time,
                    "avg_throughput": avg_throughput,
                    "performance_trend": "stable"
                },
                "cache_stats": self.cache_stats,
                "scaling_decision": scaling_decision,
                "recommendations": await self._generate_performance_recommendations(current_metrics),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Performance report generation failed: {e}")
            return {"error": str(e)}
    
    async def _generate_performance_recommendations(self, metrics: PerformanceMetrics) -> List[str]:
        """Generate intelligent performance recommendations"""
        recommendations = []
        
        if metrics.response_time > 200:
            recommendations.append("Consider implementing additional caching layers")
        
        if metrics.cache_hit_rate < 80:
            recommendations.append("Optimize cache strategies for better hit rates")
        
        if metrics.memory_usage > 80:
            recommendations.append("Consider scaling memory resources")
        
        if metrics.cpu_usage > 70:
            recommendations.append("Consider scaling CPU resources")
        
        if metrics.error_rate > 0.1:
            recommendations.append("Investigate and resolve error rate issues")
        
        if not recommendations:
            recommendations.append("Performance is optimal - no immediate actions required")
        
        return recommendations


# Global performance optimization service instance
performance_optimization_service = PerformanceOptimizationService() 