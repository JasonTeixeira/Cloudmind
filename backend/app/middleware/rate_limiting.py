"""
Redis-based Rate Limiting Middleware for CloudMind API
"""

import time
import json
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp
import redis.asyncio as redis
import hashlib

from app.core.config import settings


class RedisRateLimitingMiddleware(BaseHTTPMiddleware):
    """Production-grade Redis-based rate limiting middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.redis_client: Optional[redis.Redis] = None
        self.rate_limit_cache = {}  # Fallback cache
        self.cleanup_interval = 60
        self.last_cleanup = time.time()
    
    async def get_redis_client(self) -> redis.Redis:
        """Get Redis client with connection pooling"""
        if self.redis_client is None:
            try:
                self.redis_client = redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True,
                    max_connections=20,
                    retry_on_timeout=True,
                    health_check_interval=30
                )
                # Test connection
                await self.redis_client.ping()
            except Exception as e:
                print(f"Redis connection failed: {e}, using fallback cache")
                self.redis_client = None
        
        return self.redis_client
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Process request with Redis-based rate limiting"""
        
        # Get client identifier
        client_id = self._get_client_id(request)
        
        # Check rate limit
        rate_limit_result = await self._check_rate_limit(client_id, request)
        if not rate_limit_result["allowed"]:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests",
                    "retry_after": rate_limit_result["retry_after"],
                    "limit": rate_limit_result["limit"],
                    "remaining": rate_limit_result["remaining"]
                },
                headers={
                    "Retry-After": str(rate_limit_result["retry_after"]),
                    "X-RateLimit-Limit": str(rate_limit_result["limit"]),
                    "X-RateLimit-Remaining": str(rate_limit_result["remaining"]),
                    "X-RateLimit-Reset": str(rate_limit_result["reset_time"])
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers
        self._add_rate_limit_headers(response, rate_limit_result)
        
        return response
    
    def _get_client_id(self, request: Request) -> str:
        """Get unique client identifier with enhanced fingerprinting"""
        # Get real IP
        client_ip = self._get_client_ip(request)
        
        # Get user agent
        user_agent = request.headers.get("User-Agent", "")
        
        # Get API key if present
        api_key = request.headers.get("X-API-Key", "")
        
        # Get user ID if authenticated
        user_id = ""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from app.core.auth import verify_token
                token = auth_header.split(" ")[1]
                payload = verify_token(token)
                if payload:
                    user_id = payload.get("sub", "")
            except:
                pass
        
        # Create fingerprint
        fingerprint_parts = [client_ip]
        if user_agent:
            fingerprint_parts.append(user_agent[:100])
        if api_key:
            fingerprint_parts.append(api_key[:50])
        if user_id:
            fingerprint_parts.append(user_id)
        
        # Create hash for consistent identification
        fingerprint = "|".join(fingerprint_parts)
        return hashlib.sha256(fingerprint.encode()).hexdigest()[:32]
    
    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP considering all proxy headers"""
        # Check various proxy headers in order of reliability
        proxy_headers = [
            "CF-Connecting-IP",  # Cloudflare
            "X-Forwarded-For",
            "X-Real-IP",
            "X-Client-IP",
            "X-Forwarded",
            "Forwarded-For",
            "Forwarded"
        ]
        
        for header in proxy_headers:
            if header in request.headers:
                ip = request.headers[header].split(",")[0].strip()
                if self._is_valid_ip(ip):
                    return ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address format"""
        import re
        ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        ipv6_pattern = r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        
        return bool(re.match(ipv4_pattern, ip) or re.match(ipv6_pattern, ip))
    
    async def _check_rate_limit(self, client_id: str, request: Request) -> Dict[str, Any]:
        """Check rate limits using Redis with fallback"""
        current_time = int(time.time())
        
        # Get rate limits based on endpoint
        endpoint = request.url.path
        method = request.method
        
        # Different limits for different endpoints
        if "/auth/login" in endpoint:
            limit_per_minute = 5
            limit_per_hour = 20
            limit_per_day = 100
        elif "/api/v1/" in endpoint:
            limit_per_minute = settings.RATE_LIMIT_PER_MINUTE
            limit_per_hour = settings.RATE_LIMIT_PER_HOUR
            limit_per_day = 10000
        else:
            limit_per_minute = 100
            limit_per_hour = 1000
            limit_per_day = 50000
        
        try:
            redis_client = await self.get_redis_client()
            if redis_client:
                return await self._check_redis_rate_limit(
                    redis_client, client_id, current_time, 
                    limit_per_minute, limit_per_hour, limit_per_day
                )
        except Exception as e:
            print(f"Redis rate limiting failed: {e}")
        
        # Fallback to in-memory rate limiting
        return self._check_memory_rate_limit(
            client_id, current_time, 
            limit_per_minute, limit_per_hour, limit_per_day
        )
    
    async def _check_redis_rate_limit(
        self, redis_client: redis.Redis, client_id: str, current_time: int,
        limit_per_minute: int, limit_per_hour: int, limit_per_day: int
    ) -> Dict[str, Any]:
        """Check rate limits using Redis"""
        
        # Use Redis sorted sets for efficient rate limiting
        minute_key = f"rate_limit:{client_id}:minute"
        hour_key = f"rate_limit:{client_id}:hour"
        day_key = f"rate_limit:{client_id}:day"
        
        # Use pipeline for atomic operations
        async with redis_client.pipeline() as pipe:
            # Add current request to all time windows
            pipe.zadd(minute_key, {str(current_time): current_time})
            pipe.zadd(hour_key, {str(current_time): current_time})
            pipe.zadd(day_key, {str(current_time): current_time})
            
            # Set expiration for keys
            pipe.expire(minute_key, 60)
            pipe.expire(hour_key, 3600)
            pipe.expire(day_key, 86400)
            
            # Count requests in each window
            pipe.zcount(minute_key, current_time - 60, current_time)
            pipe.zcount(hour_key, current_time - 3600, current_time)
            pipe.zcount(day_key, current_time - 86400, current_time)
            
            # Execute pipeline
            results = await pipe.execute()
        
        # Extract counts (results[3], results[4], results[5] are the counts)
        minute_count = results[3]
        hour_count = results[4]
        day_count = results[5]
        
        # Check limits
        if minute_count > limit_per_minute:
            return {
                "allowed": False,
                "retry_after": 60,
                "limit": limit_per_minute,
                "remaining": 0,
                "reset_time": current_time + 60
            }
        
        if hour_count > limit_per_hour:
            return {
                "allowed": False,
                "retry_after": 3600,
                "limit": limit_per_hour,
                "remaining": 0,
                "reset_time": current_time + 3600
            }
        
        if day_count > limit_per_day:
            return {
                "allowed": False,
                "retry_after": 86400,
                "limit": limit_per_day,
                "remaining": 0,
                "reset_time": current_time + 86400
            }
        
        # Calculate remaining requests (use the most restrictive limit)
        remaining = min(
            limit_per_minute - minute_count,
            limit_per_hour - hour_count,
            limit_per_day - day_count
        )
        
        return {
            "allowed": True,
            "retry_after": 0,
            "limit": limit_per_minute,
            "remaining": max(0, remaining),
            "reset_time": current_time + 60
        }
    
    def _check_memory_rate_limit(
        self, client_id: str, current_time: int,
        limit_per_minute: int, limit_per_hour: int, limit_per_day: int
    ) -> Dict[str, Any]:
        """Fallback memory-based rate limiting"""
        
        if client_id not in self.rate_limit_cache:
            self.rate_limit_cache[client_id] = {
                "requests": [],
                "blocked_until": 0
            }
        
        client_data = self.rate_limit_cache[client_id]
        
        # Check if blocked
        if current_time < client_data["blocked_until"]:
            return {
                "allowed": False,
                "retry_after": client_data["blocked_until"] - current_time,
                "limit": limit_per_minute,
                "remaining": 0,
                "reset_time": client_data["blocked_until"]
            }
        
        # Remove old requests
        client_data["requests"] = [
            req_time for req_time in client_data["requests"]
            if current_time - req_time < 86400  # Keep last 24 hours
        ]
        
        # Count requests in different windows
        minute_requests = len([r for r in client_data["requests"] if current_time - r < 60])
        hour_requests = len([r for r in client_data["requests"] if current_time - r < 3600])
        day_requests = len([r for r in client_data["requests"] if current_time - r < 86400])
        
        # Check limits
        if minute_requests >= limit_per_minute:
            client_data["blocked_until"] = current_time + 60
            return {
                "allowed": False,
                "retry_after": 60,
                "limit": limit_per_minute,
                "remaining": 0,
                "reset_time": current_time + 60
            }
        
        if hour_requests >= limit_per_hour:
            client_data["blocked_until"] = current_time + 3600
            return {
                "allowed": False,
                "retry_after": 3600,
                "limit": limit_per_hour,
                "remaining": 0,
                "reset_time": current_time + 3600
            }
        
        if day_requests >= limit_per_day:
            client_data["blocked_until"] = current_time + 86400
            return {
                "allowed": False,
                "retry_after": 86400,
                "limit": limit_per_day,
                "remaining": 0,
                "reset_time": current_time + 86400
            }
        
        # Add current request
        client_data["requests"].append(current_time)
        
        # Calculate remaining
        remaining = min(
            limit_per_minute - minute_requests,
            limit_per_hour - hour_requests,
            limit_per_day - day_requests
        )
        
        return {
            "allowed": True,
            "retry_after": 0,
            "limit": limit_per_minute,
            "remaining": max(0, remaining),
            "reset_time": current_time + 60
        }
    
    def _add_rate_limit_headers(self, response: Response, rate_limit_result: Dict[str, Any]):
        """Add rate limit headers to response"""
        response.headers["X-RateLimit-Limit"] = str(rate_limit_result["limit"])
        response.headers["X-RateLimit-Remaining"] = str(rate_limit_result["remaining"])
        response.headers["X-RateLimit-Reset"] = str(rate_limit_result["reset_time"])
    
    async def get_rate_limit_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics"""
        try:
            redis_client = await self.get_redis_client()
            if redis_client:
                # Get Redis stats
                info = await redis_client.info()
                return {
                    "redis_connected": True,
                    "redis_memory_used": info.get("used_memory_human", "unknown"),
                    "redis_connected_clients": info.get("connected_clients", 0),
                    "fallback_cache_size": len(self.rate_limit_cache)
                }
        except Exception as e:
            return {
                "redis_connected": False,
                "error": str(e),
                "fallback_cache_size": len(self.rate_limit_cache)
            } 