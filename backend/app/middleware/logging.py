"""
World-Class Secure Logging Middleware
Enterprise-grade logging with encryption and security
"""

import time
import json
import hashlib
import structlog
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import settings
from app.services.encryption_service import encryption_service

logger = structlog.get_logger()

class SecureLoggingMiddleware(BaseHTTPMiddleware):
    """World-class secure logging middleware with encryption"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.sensitive_paths = [
            "/auth/login",
            "/auth/register", 
            "/auth/forgot-password",
            "/auth/reset-password",
            "/api/v1/auth/"
        ]
        self.sensitive_headers = [
            "authorization",
            "cookie",
            "x-api-key",
            "x-csrf-token"
        ]
    
    async def dispatch(self, request: Request, call_next):
        """Process request with secure logging"""
        
        # Start timing
        start_time = time.time()
        
        # Get request details
        request_id = self._generate_request_id()
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")
        
        # Log request (excluding sensitive data)
        await self._log_request(request, request_id, client_ip, user_agent)
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            await self._log_response(response, request_id, process_time, client_ip)
            
            return response
            
        except Exception as e:
            # Log error
            await self._log_error(e, request_id, client_ip)
            raise
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        return hashlib.sha256(
            f"{time.time()}{hashlib.md5().hexdigest()}".encode()
        ).hexdigest()[:16]
    
    def _get_client_ip(self, request: Request) -> str:
        """Get real client IP with proxy detection"""
        proxy_headers = [
            "CF-Connecting-IP",  # Cloudflare
            "X-Forwarded-For",
            "X-Real-IP",
            "X-Client-IP"
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
            import ipaddress
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    async def _log_request(self, request: Request, request_id: str, client_ip: str, user_agent: str):
        """Log request with sensitive data protection"""
        try:
            # Prepare request data
            request_data = {
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": client_ip,
                "user_agent": user_agent,
                "timestamp": time.time(),
                "headers": self._sanitize_headers(request.headers),
                "query_params": dict(request.query_params),
                "path_params": dict(request.path_params)
            }
            
            # Add request body for non-sensitive endpoints
            if not self._is_sensitive_path(request.url.path):
                try:
                    body = await request.body()
                    if body:
                        # Try to parse as JSON, fallback to string
                        try:
                            body_data = json.loads(body.decode('utf-8'))
                            # Sanitize sensitive fields
                            body_data = self._sanitize_body(body_data)
                            request_data["body"] = body_data
                        except (json.JSONDecodeError, UnicodeDecodeError):
                            request_data["body"] = "[BINARY_DATA]"
                except Exception:
                    request_data["body"] = "[UNAVAILABLE]"
            
            # Encrypt and log
            encrypted_data = encryption_service.encrypt_log_data(request_data)
            
            logger.info(
                "request_received",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                client_ip=client_ip,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log request: {e}")
    
    async def _log_response(self, response: Response, request_id: str, process_time: float, client_ip: str):
        """Log response with encryption"""
        try:
            # Prepare response data
            response_data = {
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time": process_time,
                "client_ip": client_ip,
                "timestamp": time.time(),
                "headers": self._sanitize_headers(response.headers)
            }
            
            # Encrypt and log
            encrypted_data = encryption_service.encrypt_log_data(response_data)
            
            logger.info(
                "response_sent",
                request_id=request_id,
                status_code=response.status_code,
                process_time=process_time,
                client_ip=client_ip,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log response: {e}")
    
    async def _log_error(self, error: Exception, request_id: str, client_ip: str):
        """Log error with encryption"""
        try:
            # Prepare error data
            error_data = {
                "request_id": request_id,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "client_ip": client_ip,
                "timestamp": time.time()
            }
            
            # Encrypt and log
            encrypted_data = encryption_service.encrypt_log_data(error_data)
            
            logger.error(
                "request_error",
                request_id=request_id,
                error_type=type(error).__name__,
                client_ip=client_ip,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log error: {e}")
    
    def _is_sensitive_path(self, path: str) -> bool:
        """Check if path contains sensitive data"""
        path_lower = path.lower()
        return any(sensitive_path in path_lower for sensitive_path in self.sensitive_paths)
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Sanitize headers to remove sensitive information"""
        sanitized = {}
        for key, value in headers.items():
            key_lower = key.lower()
            if key_lower in self.sensitive_headers:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        return sanitized
    
    def _sanitize_body(self, body_data: Any) -> Any:
        """Sanitize request body to remove sensitive fields"""
        if isinstance(body_data, dict):
            sensitive_fields = [
                "password", "token", "secret", "key", "credential",
                "authorization", "auth", "login", "signin"
            ]
            
            sanitized = {}
            for key, value in body_data.items():
                key_lower = key.lower()
                if any(sensitive in key_lower for sensitive in sensitive_fields):
                    sanitized[key] = "[REDACTED]"
                else:
                    sanitized[key] = value
            return sanitized
        return body_data

class SecurityEventLogger:
    """Specialized logger for security events"""
    
    @staticmethod
    async def log_security_event(
        event_type: str,
        severity: str,
        description: str,
        source_ip: str,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log security event with encryption"""
        try:
            event_data = {
                "event_type": event_type,
                "severity": severity,
                "description": description,
                "source_ip": source_ip,
                "user_id": user_id,
                "metadata": metadata or {},
                "timestamp": time.time()
            }
            
            # Encrypt security event data
            encrypted_data = encryption_service.encrypt_log_data(event_data)
            
            logger.warning(
                "security_event",
                event_type=event_type,
                severity=severity,
                source_ip=source_ip,
                user_id=user_id,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log security event: {e}")
    
    @staticmethod
    async def log_audit_event(
        action: str,
        resource: str,
        user_id: str,
        source_ip: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ):
        """Log audit event with encryption"""
        try:
            audit_data = {
                "action": action,
                "resource": resource,
                "user_id": user_id,
                "source_ip": source_ip,
                "success": success,
                "details": details or {},
                "timestamp": time.time()
            }
            
            # Encrypt audit data
            encrypted_data = encryption_service.encrypt_log_data(audit_data)
            
            logger.info(
                "audit_event",
                action=action,
                resource=resource,
                user_id=user_id,
                source_ip=source_ip,
                success=success,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")

class PerformanceLogger:
    """Specialized logger for performance metrics"""
    
    @staticmethod
    async def log_performance_metric(
        metric_name: str,
        value: float,
        unit: str,
        tags: Optional[Dict[str, str]] = None
    ):
        """Log performance metric with encryption"""
        try:
            metric_data = {
                "metric_name": metric_name,
                "value": value,
                "unit": unit,
                "tags": tags or {},
                "timestamp": time.time()
            }
            
            # Encrypt performance data
            encrypted_data = encryption_service.encrypt_log_data(metric_data)
            
            logger.info(
                "performance_metric",
                metric_name=metric_name,
                value=value,
                unit=unit,
                encrypted_data=encrypted_data
            )
            
        except Exception as e:
            logger.error(f"Failed to log performance metric: {e}")

# Global logger instances
security_logger = SecurityEventLogger()
performance_logger = PerformanceLogger() 