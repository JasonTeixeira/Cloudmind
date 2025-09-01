"""
Input validation middleware for CloudMind API
"""

import re
import html
from typing import Callable, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.types import ASGIApp

from app.core.config import settings


class InputValidationMiddleware(BaseHTTPMiddleware):
    """Enhanced input validation middleware"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Process request with input validation"""
        
        # Validate and sanitize query parameters
        if request.query_params:
            sanitized_params = self._sanitize_query_params(request.query_params)
            # Update request with sanitized params
            request._query_params = sanitized_params
        
        # Validate and sanitize path parameters
        if request.path_params:
            sanitized_path_params = self._sanitize_path_params(request.path_params)
            request._path_params = sanitized_path_params
        
        # Validate headers
        if not self._validate_headers(request.headers):
            return JSONResponse(
                status_code=400,
                content={"detail": "Invalid headers detected"}
            )
        
        # Process request
        response = await call_next(request)
        return response
    
    def _sanitize_query_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize query parameters"""
        sanitized = {}
        
        for key, value in params.items():
            # Validate key
            if not self._is_valid_param_name(key):
                continue
            
            # Sanitize value
            if isinstance(value, str):
                sanitized_value = self._sanitize_string(value)
                if sanitized_value:
                    sanitized[key] = sanitized_value
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _sanitize_path_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize path parameters"""
        sanitized = {}
        
        for key, value in params.items():
            # Validate key
            if not self._is_valid_param_name(key):
                continue
            
            # Sanitize value
            if isinstance(value, str):
                sanitized_value = self._sanitize_string(value)
                if sanitized_value:
                    sanitized[key] = sanitized_value
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _sanitize_string(self, value: str) -> str:
        """Sanitize string value"""
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # HTML escape
        value = html.escape(value)
        
        # Remove potentially dangerous characters
        value = re.sub(r'[<>"\']', '', value)
        
        # Limit length
        if len(value) > 1000:
            value = value[:1000]
        
        return value.strip()
    
    def _is_valid_param_name(self, name: str) -> bool:
        """Validate parameter name"""
        # Check for valid characters
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            return False
        
        # Check length
        if len(name) > 50:
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'script', 'javascript', 'vbscript', 'expression', 'onload',
            'onerror', 'onclick', 'onmouseover', 'onfocus', 'onblur'
        ]
        
        name_lower = name.lower()
        for pattern in suspicious_patterns:
            if pattern in name_lower:
                return False
        
        return True
    
    def _validate_headers(self, headers: Dict[str, str]) -> bool:
        """Validate request headers"""
        # Check for suspicious headers
        suspicious_headers = [
            'x-forwarded-host', 'x-forwarded-proto', 'x-real-ip',
            'x-forwarded-for', 'x-original-url', 'x-rewrite-url'
        ]
        
        for header_name in headers.keys():
            header_lower = header_name.lower()
            
            # Check for suspicious headers
            if any(suspicious in header_lower for suspicious in suspicious_headers):
                # Only allow from trusted sources
                if not self._is_trusted_source(headers):
                    return False
            
            # Check header value length
            if len(headers[header_name]) > 1000:
                return False
        
        return True
    
    def _is_trusted_source(self, headers: Dict[str, str]) -> bool:
        """Check if request is from a trusted source"""
        # In production, implement proper IP whitelisting
        # For now, we'll allow all sources but log suspicious activity
        return True 