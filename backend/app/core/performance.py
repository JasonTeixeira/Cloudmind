"""
Performance Optimization Module for CloudMind
Implements caching, connection pooling, and query optimization
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from functools import wraps
import redis
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import psutil
import time

from app.core.config import settings

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor and optimize system performance"""
    
    def __init__(self):
        # Prefer REDIS_URL parsing for consistency; fall back to discrete settings
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
        self.metrics = {}
        self.start_time = time.time()
    
    async def monitor_system_health(self) -> Dict[str, Any]:
        """Monitor overall system health"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            
            # Network I/O
            network = psutil.net_io_counters()
            
            # Database connections
            db_connections = await self._get_db_connection_count()
            
            # Redis health
            redis_health = await self._check_redis_health()
            
            health_metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "disk_usage": disk.percent,
                "disk_free": disk.free,
                "network_bytes_sent": network.bytes_sent,
                "network_bytes_recv": network.bytes_recv,
                "db_connections": db_connections,
                "redis_health": redis_health,
                "uptime": time.time() - self.start_time
            }
            
            # Store metrics in Redis for historical analysis
            await self._store_metrics(health_metrics)
            
            return health_metrics
            
        except Exception as e:
            logger.error(f"System health monitoring failed: {e}")
            return {"error": str(e)}
    
    async def _get_db_connection_count(self) -> int:
        """Get current database connection count"""
        try:
            # This would need to be implemented based on your database setup
            return 0
        except Exception as e:
            logger.error(f"Database connection count failed: {e}")
            return 0
    
    async def _check_redis_health(self) -> Dict[str, Any]:
        """Check Redis health and performance"""
        try:
            start_time = time.time()
            self.redis_client.ping()
            ping_time = (time.time() - start_time) * 1000
            
            info = self.redis_client.info()
            
            return {
                "status": "healthy",
                "ping_time_ms": ping_time,
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "total_commands_processed": info.get("total_commands_processed", 0)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def _store_metrics(self, metrics: Dict[str, Any]):
        """Store metrics in Redis for historical analysis"""
        try:
            timestamp = datetime.utcnow().isoformat()
            self.redis_client.hset(
                "system_metrics",
                timestamp,
                str(metrics)
            )
            
            # Keep only last 24 hours of metrics
            self.redis_client.expire("system_metrics", 86400)
            
        except Exception as e:
            logger.error(f"Metrics storage failed: {e}")


class CacheManager:
    """Advanced caching system with TTL and invalidation"""
    
    def __init__(self):
        try:
            self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        except Exception:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True
            )
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0
        }
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                self.cache_stats["hits"] += 1
                return value
            else:
                self.cache_stats["misses"] += 1
                return None
        except Exception as e:
            logger.error(f"Cache get failed: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        try:
            self.redis_client.setex(key, ttl, str(value))
            self.cache_stats["sets"] += 1
        except Exception as e:
            logger.error(f"Cache set failed: {e}")
    
    async def delete(self, key: str):
        """Delete value from cache"""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete failed: {e}")
    
    async def invalidate_pattern(self, pattern: str):
        """Invalidate all keys matching pattern"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache pattern invalidation failed: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.cache_stats,
            "hit_rate": hit_rate,
            "total_requests": total_requests
        }


class QueryOptimizer:
    """Database query optimization and monitoring"""
    
    def __init__(self):
        self.slow_query_threshold = 1.0  # seconds
        self.query_stats = {}
    
    def monitor_query(self, query_name: str):
        """Decorator to monitor query performance"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    
                    # Record query stats
                    if query_name not in self.query_stats:
                        self.query_stats[query_name] = {
                            "count": 0,
                            "total_time": 0,
                            "avg_time": 0,
                            "min_time": float('inf'),
                            "max_time": 0,
                            "slow_queries": 0
                        }
                    
                    stats = self.query_stats[query_name]
                    stats["count"] += 1
                    stats["total_time"] += execution_time
                    stats["avg_time"] = stats["total_time"] / stats["count"]
                    stats["min_time"] = min(stats["min_time"], execution_time)
                    stats["max_time"] = max(stats["max_time"], execution_time)
                    
                    if execution_time > self.slow_query_threshold:
                        stats["slow_queries"] += 1
                        logger.warning(f"Slow query detected: {query_name} took {execution_time:.2f}s")
                    
                    return result
                    
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"Query {query_name} failed after {execution_time:.2f}s: {e}")
                    raise
                    
            return wrapper
        return decorator
    
    def get_query_stats(self) -> Dict[str, Any]:
        """Get query performance statistics"""
        return self.query_stats


class ConnectionPool:
    """Database connection pooling with health checks"""
    
    def __init__(self):
        self.engine = create_engine(
            settings.DATABASE_URL,
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
    
    def get_session(self):
        """Get database session from pool"""
        return self.SessionLocal()
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database connection pool health"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
            
            pool_info = self.engine.pool.status()
            
            return {
                "status": "healthy",
                "pool_size": pool_info["pool_size"],
                "checked_in": pool_info["checked_in"],
                "checked_out": pool_info["checked_out"],
                "overflow": pool_info["overflow"],
                "invalid": pool_info["invalid"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }


class AsyncTaskQueue:
    """Asynchronous task queue for background processing"""
    
    def __init__(self):
        self.tasks = {}
        self.max_concurrent = 10
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
    
    async def submit_task(self, task_id: str, coro, priority: int = 0):
        """Submit task to queue"""
        async with self.semaphore:
            try:
                task = asyncio.create_task(coro)
                self.tasks[task_id] = {
                    "task": task,
                    "priority": priority,
                    "status": "running",
                    "start_time": time.time()
                }
                
                result = await task
                
                self.tasks[task_id]["status"] = "completed"
                self.tasks[task_id]["end_time"] = time.time()
                self.tasks[task_id]["result"] = result
                
                return result
                
            except Exception as e:
                self.tasks[task_id]["status"] = "failed"
                self.tasks[task_id]["error"] = str(e)
                self.tasks[task_id]["end_time"] = time.time()
                raise
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all task statuses"""
        return self.tasks.copy()


# Global instances
performance_monitor = PerformanceMonitor()
cache_manager = CacheManager()
query_optimizer = QueryOptimizer()
connection_pool = ConnectionPool()
task_queue = AsyncTaskQueue()


async def optimize_performance():
    """Main performance optimization function"""
    try:
        # Monitor system health
        health_metrics = await performance_monitor.monitor_system_health()
        
        # Check cache performance
        cache_stats = cache_manager.get_stats()
        
        # Check database health
        db_health = await connection_pool.health_check()
        
        # Get query statistics
        query_stats = query_optimizer.get_query_stats()
        
        # Generate optimization recommendations
        recommendations = await generate_optimization_recommendations(
            health_metrics, cache_stats, db_health, query_stats
        )
        
        return {
            "health_metrics": health_metrics,
            "cache_stats": cache_stats,
            "db_health": db_health,
            "query_stats": query_stats,
            "recommendations": recommendations
        }
        
    except Exception as e:
        logger.error(f"Performance optimization failed: {e}")
        return {"error": str(e)}


async def generate_optimization_recommendations(
    health_metrics: Dict[str, Any],
    cache_stats: Dict[str, Any],
    db_health: Dict[str, Any],
    query_stats: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Generate performance optimization recommendations"""
    recommendations = []
    
    # CPU optimization
    if health_metrics.get("cpu_usage", 0) > 80:
        recommendations.append({
            "type": "cpu_optimization",
            "priority": "high",
            "description": "CPU usage is high. Consider scaling up or optimizing code.",
            "action": "Monitor CPU-intensive operations and consider async processing"
        })
    
    # Memory optimization
    if health_metrics.get("memory_usage", 0) > 85:
        recommendations.append({
            "type": "memory_optimization",
            "priority": "high",
            "description": "Memory usage is high. Consider memory optimization.",
            "action": "Review memory usage patterns and implement caching"
        })
    
    # Cache optimization
    if cache_stats.get("hit_rate", 0) < 70:
        recommendations.append({
            "type": "cache_optimization",
            "priority": "medium",
            "description": "Cache hit rate is low. Consider cache optimization.",
            "action": "Review cache keys and TTL settings"
        })
    
    # Database optimization
    if db_health.get("status") != "healthy":
        recommendations.append({
            "type": "database_optimization",
            "priority": "critical",
            "description": "Database health issues detected.",
            "action": "Check database connections and query performance"
        })
    
    # Query optimization
    slow_queries = sum(stats.get("slow_queries", 0) for stats in query_stats.values())
    if slow_queries > 0:
        recommendations.append({
            "type": "query_optimization",
            "priority": "medium",
            "description": f"{slow_queries} slow queries detected.",
            "action": "Review and optimize slow queries"
        })
    
    return recommendations 