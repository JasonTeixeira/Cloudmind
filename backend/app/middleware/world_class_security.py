"""
World-Class Security Middleware
Enterprise-grade security with comprehensive protection
"""

import logging
import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from fastapi import Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response as StarletteResponse
import ipaddress

logger = logging.getLogger(__name__)

class WorldClassSecurityMiddleware(BaseHTTPMiddleware):
    """World-class security middleware with comprehensive protection"""
    
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_store: Dict[str, List[float]] = {}
        self.blocked_ips: Dict[str, datetime] = {}
        self.suspicious_ips: Dict[str, int] = {}
        self.request_log: List[Dict[str, Any]] = []
        
        # Security configuration
        self.max_requests_per_minute = 100
        self.max_requests_per_hour = 1000
        self.max_failed_attempts = 10
        self.block_duration_minutes = 30
        self.suspicious_threshold = 5
        
        # Security headers
        self.security_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
            "X-Permitted-Cross-Domain-Policies": "none",
            "X-Download-Options": "noopen",
            "X-DNS-Prefetch-Control": "off",
            "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        }
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Process request with comprehensive security checks"""
        start_time = time.time()
        
        try:
            # Get client information
            client_ip = self._get_real_ip(request)
            user_agent = request.headers.get("user-agent", "")
            request_id = self._generate_request_id()
            
            # Log request
            self._log_request(request, client_ip, user_agent, request_id)
            
            # Security checks
            await self._perform_security_checks(request, client_ip, user_agent)
            
            # Rate limiting
            await self._check_rate_limit(client_ip)
            
            # Process request
            response = await call_next(request)
            
            # Add security headers
            self._add_security_headers(response)
            
            # Log response
            self._log_response(response, start_time, request_id)
            
            return response
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Security middleware error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
    
    def _get_real_ip(self, request: Request) -> str:
        """Get real client IP with proxy detection"""
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
        
        return request.client.host if request.client else "unknown"
    
    def _is_valid_ip(self, ip: str) -> bool:
        """Validate IP address"""
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        return hashlib.sha256(f"{time.time()}{secrets.token_hex(8)}".encode()).hexdigest()[:16]
    
    def _log_request(self, request: Request, client_ip: str, user_agent: str, request_id: str):
        """Log request details"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": client_ip,
            "user_agent": user_agent,
            "headers": dict(request.headers),
            "query_params": dict(request.query_params)
        }
        
        self.request_log.append(log_entry)
        
        # Keep only last 1000 requests
        if len(self.request_log) > 1000:
            self.request_log.pop(0)
    
    def _log_response(self, response: Response, start_time: float, request_id: str):
        """Log response details"""
        duration = time.time() - start_time
        
        # Find corresponding request log entry
        for entry in self.request_log:
            if entry.get("request_id") == request_id:
                entry["response_status"] = response.status_code
                entry["response_time"] = duration
                break
    
    async def _perform_security_checks(self, request: Request, client_ip: str, user_agent: str):
        """Perform comprehensive security checks"""
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            block_until = self.blocked_ips[client_ip]
            if datetime.utcnow() < block_until:
                remaining_time = (block_until - datetime.utcnow()).total_seconds() / 60
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail=f"IP address blocked. Try again in {int(remaining_time)} minutes"
                )
            else:
                # Unblock IP
                del self.blocked_ips[client_ip]
        
        # Check for suspicious patterns
        await self._check_suspicious_patterns(request, client_ip, user_agent)
        
        # Validate request headers
        await self._validate_request_headers(request)
        
        # Check for SQL injection patterns
        await self._check_sql_injection(request)
        
        # Check for XSS patterns
        await self._check_xss_patterns(request)
        
        # Check for path traversal
        await self._check_path_traversal(request)
    
    async def _check_suspicious_patterns(self, request: Request, client_ip: str, user_agent: str):
        """Check for suspicious request patterns"""
        suspicious_patterns = [
            "/admin", "/wp-admin", "/phpmyadmin", "/mysql",
            "/.env", "/config", "/backup", "/.git",
            "union select", "drop table", "insert into",
            "script>", "javascript:", "onload=", "onerror="
        ]
        
        url = str(request.url).lower()
        query_string = str(request.query_params).lower()
        
        for pattern in suspicious_patterns:
            if pattern in url or pattern in query_string:
                await self._record_suspicious_activity(client_ip, f"Suspicious pattern: {pattern}")
                break
    
    async def _validate_request_headers(self, request: Request):
        """Validate request headers for security"""
        required_headers = ["host", "user-agent"]
        
        for header in required_headers:
            if header not in request.headers:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required header: {header}"
                )
        
        # Check for suspicious headers
        suspicious_headers = [
            "x-forwarded-host", "x-forwarded-proto", "x-forwarded-for",
            "x-real-ip", "x-client-ip", "x-cluster-client-ip"
        ]
        
        for header in suspicious_headers:
            if header in request.headers:
                # Log suspicious header
                logger.warning(f"Suspicious header detected: {header}")
    
    async def _check_sql_injection(self, request: Request):
        """Check for SQL injection patterns"""
        sql_patterns = [
            "union select", "drop table", "insert into", "delete from",
            "update set", "alter table", "create table", "drop database",
            "exec(", "execute(", "eval(", "system("
        ]
        
        url = str(request.url).lower()
        query_string = str(request.query_params).lower()
        
        for pattern in sql_patterns:
            if pattern in url or pattern in query_string:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request detected"
                )
    
    async def _check_xss_patterns(self, request: Request):
        """Check for XSS patterns"""
        xss_patterns = [
            "<script", "javascript:", "onload=", "onerror=", "onclick=",
            "onmouseover=", "onfocus=", "onblur=", "onchange="
        ]
        
        url = str(request.url).lower()
        query_string = str(request.query_params).lower()
        
        for pattern in xss_patterns:
            if pattern in url or pattern in query_string:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request detected"
                )
    
    async def _check_path_traversal(self, request: Request):
        """Check for path traversal attempts"""
        path_traversal_patterns = [
            "../", "..\\", "..%2f", "..%5c", "%2e%2e%2f",
            "....//", "....\\\\", "..%252f", "..%255c"
        ]
        
        url = str(request.url).lower()
        
        for pattern in path_traversal_patterns:
            if pattern in url:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request detected"
                )
    
    async def _record_suspicious_activity(self, client_ip: str, reason: str):
        """Record suspicious activity"""
        if client_ip not in self.suspicious_ips:
            self.suspicious_ips[client_ip] = 0
        
        self.suspicious_ips[client_ip] += 1
        
        if self.suspicious_ips[client_ip] >= self.suspicious_threshold:
            # Block IP
            self.blocked_ips[client_ip] = datetime.utcnow() + timedelta(minutes=self.block_duration_minutes)
            logger.warning(f"IP {client_ip} blocked due to suspicious activity: {reason}")
    
    async def _check_rate_limit(self, client_ip: str):
        """Check rate limiting"""
        current_time = time.time()
        
        if client_ip not in self.rate_limit_store:
            self.rate_limit_store[client_ip] = []
        
        # Remove old requests
        cutoff_time = current_time - 60  # 1 minute
        self.rate_limit_store[client_ip] = [
            req_time for req_time in self.rate_limit_store[client_ip]
            if req_time > cutoff_time
        ]
        
        # Check per-minute limit
        if len(self.rate_limit_store[client_ip]) >= self.max_requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later."
            )
        
        # Add current request
        self.rate_limit_store[client_ip].append(current_time)
        
        # Check per-hour limit (simplified)
        hour_cutoff = current_time - 3600  # 1 hour
        hourly_requests = [
            req_time for req_time in self.rate_limit_store[client_ip]
            if req_time > hour_cutoff
        ]
        
        if len(hourly_requests) >= self.max_requests_per_hour:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Hourly rate limit exceeded. Try again later."
            )
    
    def _add_security_headers(self, response: Response):
        """Add comprehensive security headers"""
        for header, value in self.security_headers.items():
            response.headers[header] = value
        
        # Add custom security headers
        response.headers["X-Request-ID"] = self._generate_request_id()
        response.headers["X-Runtime"] = str(time.time())
    
    def get_security_stats(self) -> Dict[str, Any]:
        """Get security statistics"""
        current_time = datetime.utcnow()
        
        # Calculate blocked IPs
        active_blocks = {
            ip: (block_until - current_time).total_seconds() / 60
            for ip, block_until in self.blocked_ips.items()
            if block_until > current_time
        }
        
        # Calculate suspicious IPs
        suspicious_ips = {
            ip: count for ip, count in self.suspicious_ips.items()
            if count > 0
        }
        
        return {
            "blocked_ips": len(active_blocks),
            "suspicious_ips": len(suspicious_ips),
            "total_requests": len(self.request_log),
            "rate_limited_ips": len(self.rate_limit_store),
            "security_score": self._calculate_security_score()
        }
    
    def _calculate_security_score(self) -> int:
        """Calculate overall security score"""
        score = 100
        
        # Deduct points for blocked IPs
        score -= len(self.blocked_ips) * 2
        
        # Deduct points for suspicious IPs
        score -= len(self.suspicious_ips) * 1
        
        # Deduct points for high request volume
        if len(self.request_log) > 500:
            score -= 10
        
        return max(0, score) 