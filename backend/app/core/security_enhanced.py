"""
Enhanced Security Module for CloudMind
Implements advanced security features, threat detection, and compliance monitoring
"""

import asyncio
import logging
import hashlib
import secrets
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

from app.core.config import settings

logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    """Security levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(Enum):
    """Types of security threats"""
    BRUTE_FORCE = "brute_force"
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    CSRF = "csrf"
    RATE_LIMIT = "rate_limit"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    DATA_BREACH = "data_breach"
    MALWARE = "malware"


@dataclass
class SecurityEvent:
    """Security event record"""
    id: str
    timestamp: datetime
    event_type: str
    severity: SecurityLevel
    source_ip: str
    user_id: Optional[str]
    description: str
    metadata: Dict[str, Any]
    action_taken: str


class EnhancedSecurityManager:
    """Enhanced security manager with advanced threat detection"""
    
    def __init__(self):
        self.security_events = []
        self.blocked_ips = set()
        self.suspicious_patterns = self._load_suspicious_patterns()
        self.rate_limit_store = {}
        self.encryption_key = self._generate_encryption_key()
        self.fernet = Fernet(self.encryption_key)
        
    def _load_suspicious_patterns(self) -> Dict[str, List[str]]:
        """Load suspicious patterns for threat detection"""
        return {
            "sql_injection": [
                r"(\b(union|select|insert|update|delete|drop|create|alter)\b)",
                r"(\b(or|and)\b\s+\d+\s*=\s*\d+)",
                r"(--|#|\/\*|\*\/)",
                r"(\b(exec|execute|executing)\b)",
                r"(\b(xp_|sp_)\b)"
            ],
            "xss": [
                r"(<script[^>]*>.*?</script>)",
                r"(javascript:)",
                r"(on\w+\s*=)",
                r"(<iframe[^>]*>)",
                r"(<object[^>]*>)"
            ],
            "path_traversal": [
                r"(\.\.\/|\.\.\\)",
                r"(\/etc\/|\/var\/|\/proc\/)",
                r"(c:\\|d:\\)"
            ],
            "command_injection": [
                r"(\b(cat|ls|pwd|whoami|id|uname)\b)",
                r"(\b(rm|del|format|fdisk)\b)",
                r"(\b(netcat|nc|telnet|ssh)\b)"
            ]
        }
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key"""
        return Fernet.generate_key()
    
    async def analyze_request_security(
        self,
        request_data: Dict[str, Any],
        source_ip: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze request for security threats"""
        try:
            threats = []
            risk_score = 0
            
            # Check for suspicious patterns in request data
            request_str = str(request_data).lower()
            
            for threat_type, patterns in self.suspicious_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, request_str, re.IGNORECASE):
                        threats.append({
                            "type": threat_type,
                            "pattern": pattern,
                            "severity": SecurityLevel.HIGH
                        })
                        risk_score += 25
            
            # Check rate limiting
            rate_limit_result = await self._check_rate_limit(source_ip)
            if rate_limit_result["blocked"]:
                threats.append({
                    "type": ThreatType.RATE_LIMIT,
                    "severity": SecurityLevel.MEDIUM,
                    "description": "Rate limit exceeded"
                })
                risk_score += 15
            
            # Check for brute force attempts
            brute_force_result = await self._check_brute_force(source_ip, user_id)
            if brute_force_result["detected"]:
                threats.append({
                    "type": ThreatType.BRUTE_FORCE,
                    "severity": SecurityLevel.CRITICAL,
                    "description": "Brute force attempt detected"
                })
                risk_score += 50
            
            # Check IP reputation
            ip_reputation = await self._check_ip_reputation(source_ip)
            if ip_reputation["suspicious"]:
                threats.append({
                    "type": ThreatType.SUSPICIOUS_ACTIVITY,
                    "severity": SecurityLevel.HIGH,
                    "description": "Suspicious IP address"
                })
                risk_score += 20
            
            # Determine overall security level
            security_level = self._calculate_security_level(risk_score)
            
            # Record security event
            if threats:
                await self._record_security_event(
                    source_ip, user_id, threats, security_level
                )
            
            return {
                "secure": len(threats) == 0,
                "risk_score": risk_score,
                "security_level": security_level,
                "threats": threats,
                "recommendations": self._generate_security_recommendations(threats)
            }
            
        except Exception as e:
            logger.error(f"Security analysis failed: {e}")
            return {
                "secure": False,
                "risk_score": 100,
                "security_level": SecurityLevel.CRITICAL,
                "error": str(e)
            }
    
    async def _check_rate_limit(self, source_ip: str) -> Dict[str, Any]:
        """Check rate limiting for IP address"""
        current_time = datetime.utcnow()
        
        if source_ip not in self.rate_limit_store:
            self.rate_limit_store[source_ip] = {
                "requests": [],
                "blocked_until": None
            }
        
        ip_data = self.rate_limit_store[source_ip]
        
        # Check if IP is currently blocked
        if ip_data["blocked_until"] and current_time < ip_data["blocked_until"]:
            return {"blocked": True, "remaining_block": (ip_data["blocked_until"] - current_time).seconds}
        
        # Clean old requests
        ip_data["requests"] = [
            req_time for req_time in ip_data["requests"]
            if current_time - req_time < timedelta(minutes=1)
        ]
        
        # Add current request
        ip_data["requests"].append(current_time)
        
        # Check rate limit (100 requests per minute)
        if len(ip_data["requests"]) > 100:
            ip_data["blocked_until"] = current_time + timedelta(minutes=5)
            return {"blocked": True, "remaining_block": 300}
        
        return {"blocked": False}
    
    async def _check_brute_force(self, source_ip: str, user_id: Optional[str]) -> Dict[str, Any]:
        """Check for brute force attempts"""
        current_time = datetime.utcnow()
        key = f"brute_force:{source_ip}:{user_id or 'anonymous'}"
        
        if key not in self.rate_limit_store:
            self.rate_limit_store[key] = {
                "failed_attempts": [],
                "blocked_until": None
            }
        
        brute_data = self.rate_limit_store[key]
        
        # Check if currently blocked
        if brute_data["blocked_until"] and current_time < brute_data["blocked_until"]:
            return {"detected": True, "blocked": True}
        
        # Clean old attempts
        brute_data["failed_attempts"] = [
            attempt for attempt in brute_data["failed_attempts"]
            if current_time - attempt < timedelta(minutes=15)
        ]
        
        # Simulate failed login attempt (in real implementation, this would be triggered by actual failed login)
        # For demonstration, we'll assume this is called when a login fails
        brute_data["failed_attempts"].append(current_time)
        
        # Check for brute force (5 failed attempts in 15 minutes)
        if len(brute_data["failed_attempts"]) >= 5:
            brute_data["blocked_until"] = current_time + timedelta(minutes=30)
            return {"detected": True, "blocked": True}
        
        return {"detected": False, "blocked": False}
    
    async def _check_ip_reputation(self, source_ip: str) -> Dict[str, Any]:
        """Check IP reputation (simplified implementation)"""
        # In a real implementation, this would query external IP reputation services
        suspicious_ips = [
            "192.168.1.100",  # Example suspicious IP
            "10.0.0.50"       # Example suspicious IP
        ]
        
        return {
            "suspicious": source_ip in suspicious_ips,
            "reputation_score": 50 if source_ip in suspicious_ips else 90
        }
    
    def _calculate_security_level(self, risk_score: int) -> SecurityLevel:
        """Calculate security level based on risk score"""
        if risk_score >= 80:
            return SecurityLevel.CRITICAL
        elif risk_score >= 60:
            return SecurityLevel.HIGH
        elif risk_score >= 40:
            return SecurityLevel.MEDIUM
        else:
            return SecurityLevel.LOW
    
    async def _record_security_event(
        self,
        source_ip: str,
        user_id: Optional[str],
        threats: List[Dict[str, Any]],
        security_level: SecurityLevel
    ):
        """Record security event"""
        event = SecurityEvent(
            id=secrets.token_urlsafe(16),
            timestamp=datetime.utcnow(),
            event_type="threat_detected",
            severity=security_level,
            source_ip=source_ip,
            user_id=user_id,
            description=f"Detected {len(threats)} security threats",
            metadata={"threats": threats},
            action_taken="logged"
        )
        
        self.security_events.append(event)
        logger.warning(f"Security threat detected: {event.description}")
    
    def _generate_security_recommendations(self, threats: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on threats"""
        recommendations = []
        
        for threat in threats:
            if threat["type"] == "sql_injection":
                recommendations.append("Implement parameterized queries and input validation")
            elif threat["type"] == "xss":
                recommendations.append("Sanitize user input and implement CSP headers")
            elif threat["type"] == "brute_force":
                recommendations.append("Implement account lockout and CAPTCHA")
            elif threat["type"] == "rate_limit":
                recommendations.append("Implement proper rate limiting and monitoring")
        
        return recommendations
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(decoded_data)
            return decrypted_data.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise
    
    def generate_secure_token(self, user_id: str, expires_in: int = 3600) -> str:
        """Generate secure JWT token"""
        try:
            payload = {
                "user_id": user_id,
                "exp": datetime.utcnow() + timedelta(seconds=expires_in),
                "iat": datetime.utcnow(),
                "jti": secrets.token_urlsafe(16)
            }
            
            return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        except Exception as e:
            logger.error(f"Token generation failed: {e}")
            raise
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def hash_password(self, password: str) -> str:
        """Hash password using secure algorithm"""
        try:
            salt = secrets.token_hex(16)
            hash_obj = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000  # iterations
            )
            return f"{salt}${hash_obj.hex()}"
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_hex = hashed_password.split('$')
            hash_obj = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000  # iterations
            )
            return hash_obj.hex() == hash_hex
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Character variety checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Include lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Include uppercase letters")
        
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Include numbers")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("Include special characters")
        
        # Strength assessment
        if score >= 5:
            strength = "strong"
        elif score >= 3:
            strength = "medium"
        else:
            strength = "weak"
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback,
            "valid": score >= 3
        }
    
    async def get_security_report(self) -> Dict[str, Any]:
        """Generate security report"""
        try:
            current_time = datetime.utcnow()
            
            # Filter recent events (last 24 hours)
            recent_events = [
                event for event in self.security_events
                if current_time - event.timestamp < timedelta(hours=24)
            ]
            
            # Calculate statistics
            threat_counts = {}
            severity_counts = {}
            
            for event in recent_events:
                # Count by threat type
                for threat in event.metadata.get("threats", []):
                    threat_type = threat.get("type", "unknown")
                    threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
                
                # Count by severity
                severity = event.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            return {
                "total_events": len(recent_events),
                "threat_counts": threat_counts,
                "severity_counts": severity_counts,
                "blocked_ips": len(self.blocked_ips),
                "rate_limited_ips": len([
                    ip for ip, data in self.rate_limit_store.items()
                    if data.get("blocked_until") and current_time < data["blocked_until"]
                ]),
                "security_score": self._calculate_security_score(recent_events)
            }
            
        except Exception as e:
            logger.error(f"Security report generation failed: {e}")
            return {"error": str(e)}
    
    def _calculate_security_score(self, events: List[SecurityEvent]) -> int:
        """Calculate overall security score"""
        if not events:
            return 100
        
        # Penalize based on number and severity of events
        penalty = 0
        for event in events:
            if event.severity == SecurityLevel.CRITICAL:
                penalty += 20
            elif event.severity == SecurityLevel.HIGH:
                penalty += 10
            elif event.severity == SecurityLevel.MEDIUM:
                penalty += 5
            else:
                penalty += 1
        
        return max(0, 100 - penalty)


# Global security manager instance
security_manager = EnhancedSecurityManager()


async def init_security() -> None:
    """Initialize enhanced security (compat shim)."""
    # Placeholder for any async initialization needed in the future
    return None