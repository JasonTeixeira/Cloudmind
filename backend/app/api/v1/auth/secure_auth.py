"""
World-Class Secure Authentication System
Enterprise-grade authentication with httpOnly cookies and enhanced security
"""

import logging
import secrets
import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.core.auth import verify_password, get_password_hash

logger = logging.getLogger(__name__)

# Enhanced password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=14
)

# JWT Bearer token for API access
security = HTTPBearer()

class SecureAuthManager:
    """World-class secure authentication manager"""
    
    def __init__(self):
        self.session_store = {}  # Fallback store
        self.failed_attempts = {}
        self.locked_accounts = {}
        self.blacklisted_tokens: set[str] = set()  # Fallback blacklist
        # Lazy Redis client
        self._redis = None

    def _get_redis(self):
        if self._redis is None:
            try:
                import redis
                self._redis = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True,
                    retry_on_timeout=True,
                    health_check_interval=30,
                    max_connections=20,
                )
                # Test
                self._redis.ping()
            except Exception as e:
                logger.warning(f"Redis not available for auth sessions/blacklist: {e}")
                self._redis = None
        return self._redis
    
    def create_secure_tokens(self, user: User) -> Dict[str, Any]:
        """Create secure JWT tokens with enhanced security"""
        try:
            # Generate secure token IDs
            access_token_id = secrets.token_urlsafe(32)
            refresh_token_id = secrets.token_urlsafe(32)
            
            # Create access token (short-lived)
            access_token_expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token_payload = {
                "sub": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "permissions": user.permissions,
                "exp": access_token_expires,
                "iat": datetime.utcnow(),
                "iss": settings.JWT_ISSUER,
                "aud": settings.JWT_AUDIENCE,
                "type": "access",
                "jti": access_token_id,
                "fingerprint": self._generate_token_fingerprint(user)
            }
            
            # Create refresh token (longer-lived)
            refresh_token_expires = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            refresh_token_payload = {
                "sub": str(user.id),
                "exp": refresh_token_expires,
                "iat": datetime.utcnow(),
                "iss": settings.JWT_ISSUER,
                "aud": settings.JWT_AUDIENCE,
                "type": "refresh",
                "jti": refresh_token_id,
                "fingerprint": self._generate_token_fingerprint(user)
            }
            
            # Sign tokens
            access_token = jwt.encode(
                access_token_payload,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
                headers={"kid": "cloudmind-access-key-1"}
            )
            
            refresh_token = jwt.encode(
                refresh_token_payload,
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
                headers={"kid": "cloudmind-refresh-key-1"}
            )
            
            # Store refresh token hash for validation (Redis if available)
            refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
            session_payload = {
                "user_id": str(user.id),
                "expires": int(refresh_token_expires.timestamp()),
                "fingerprint": self._generate_token_fingerprint(user),
            }
            try:
                r = self._get_redis()
                if r is not None:
                    ttl = int((refresh_token_expires - datetime.utcnow()).total_seconds())
                    r.setex(f"auth:session:{refresh_token_hash}", ttl, json.dumps(session_payload))
                else:
                    self.session_store[refresh_token_hash] = session_payload
            except Exception:
                self.session_store[refresh_token_hash] = session_payload
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "username": user.username,
                    "role": user.role,
                    "is_active": user.is_active
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to create secure tokens: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create authentication tokens"
            )
    
    def _generate_token_fingerprint(self, user: User) -> str:
        """Generate secure token fingerprint"""
        fingerprint_data = f"{user.id}:{user.email}:{user.last_login}:{settings.SECRET_KEY}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def verify_secure_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify secure JWT token with enhanced validation"""
        try:
            # Reject blacklisted tokens (Redis first)
            try:
                r = self._get_redis()
                if r is not None:
                    # Prefer jti blacklist, but we only have token string here; check both
                    token_hash = hashlib.sha256(token.encode()).hexdigest()
                    if r.exists(f"auth:blacklist:token:{token_hash}"):
                        logger.warning("Token is blacklisted (redis)")
                        return None
                elif token in self.blacklisted_tokens:
                    logger.warning("Token is blacklisted")
                    return None
            except Exception:
                if token in self.blacklisted_tokens:
                    logger.warning("Token is blacklisted (fallback)")
                    return None
            # Decode token
            # Note: python-jose's jwt.decode does not accept 'leeway' kwarg
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                audience=settings.JWT_AUDIENCE,
                issuer=settings.JWT_ISSUER
            )
            
            # Validate token type
            token_type = payload.get("type")
            if token_type not in ["access", "refresh"]:
                logger.warning(f"Invalid token type: {token_type}")
                return None
            
            # Validate token ID
            token_id = payload.get("jti")
            if not token_id:
                logger.warning("Missing token ID")
                return None
            
            # For refresh tokens, validate against session store
            if token_type == "refresh":
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                session_data: Optional[Dict[str, Any]] = None
                try:
                    r = self._get_redis()
                    if r is not None:
                        raw = r.get(f"auth:session:{token_hash}")
                        if raw:
                            session_data = json.loads(raw)
                    else:
                        session_data = self.session_store.get(token_hash)
                except Exception:
                    session_data = self.session_store.get(token_hash)
                if not session_data:
                    logger.warning("Refresh token not found in session store")
                    return None
                now_ts = int(datetime.utcnow().timestamp())
                if now_ts > int(session_data.get("expires", 0)):
                    logger.warning("Refresh token expired")
                    try:
                        if r is not None:
                            r.delete(f"auth:session:{token_hash}")
                        else:
                            self.session_store.pop(token_hash, None)
                    except Exception:
                        pass
                    return None
            
            return payload
            
        except JWTError as e:
            logger.warning(f"JWT verification failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return None

    def blacklist_token(self, token: str) -> None:
        """Blacklist a token (used on logout)"""
        try:
            # Blacklist both token hash and jti for safety
            token_hash = hashlib.sha256(token.encode()).hexdigest()
            r = self._get_redis()
            # Determine TTL from token exp if possible
            ttl = 60 * 60
            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=[settings.ALGORITHM],
                    options={"verify_aud": False, "verify_iss": False},
                )
                exp = payload.get("exp")
                if isinstance(exp, (int, float)):
                    ttl = max(1, int(exp - datetime.utcnow().timestamp()))
                jti = payload.get("jti")
            except Exception:
                jti = None
            if r is not None:
                r.setex(f"auth:blacklist:token:{token_hash}", ttl, "1")
                if jti:
                    r.setex(f"auth:blacklist:jti:{jti}", ttl, "1")
            else:
                self.blacklisted_tokens.add(token)
        except Exception:
            try:
                self.blacklisted_tokens.add(token)
            except Exception:
                pass
    
    async def authenticate_user_secure(
        self,
        db: Session,
        email: str,
        password: str,
        request: Request
    ) -> Optional[User]:
        """Authenticate user with enhanced security"""
        try:
            # Check for account lockout
            client_ip = self._get_client_ip(request)
            if self._is_account_locked(email, client_ip):
                logger.warning(f"Account locked for user {email} from IP {client_ip}")
                raise HTTPException(
                    status_code=status.HTTP_423_LOCKED,
                    detail="Account temporarily locked due to multiple failed attempts"
                )
            
            # Get user
            user = db.query(User).filter(User.email == email).first()
            if not user:
                self._record_failed_attempt(email, client_ip)
                return None
            
            # Verify password with timing attack protection
            if not verify_password(password, user.hashed_password):
                self._record_failed_attempt(email, client_ip)
                
                # Update user failed attempts
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    logger.warning(f"Account locked for user {email}")
                
                db.commit()
                return None
            
            # Successful authentication
            self._clear_failed_attempts(email, client_ip)
            user.failed_login_attempts = 0
            user.locked_until = None
            user.last_login = datetime.utcnow()
            user.last_activity = datetime.utcnow()
            db.commit()
            
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
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
    
    def _record_failed_attempt(self, email: str, client_ip: str):
        """Record failed login attempt"""
        key = f"{email}:{client_ip}"
        if key not in self.failed_attempts:
            self.failed_attempts[key] = []
        
        self.failed_attempts[key].append(datetime.utcnow())
        
        # Keep only recent attempts (last 15 minutes)
        cutoff_time = datetime.utcnow() - timedelta(minutes=15)
        self.failed_attempts[key] = [
            attempt for attempt in self.failed_attempts[key]
            if attempt > cutoff_time
        ]
    
    def _clear_failed_attempts(self, email: str, client_ip: str):
        """Clear failed login attempts"""
        key = f"{email}:{client_ip}"
        if key in self.failed_attempts:
            del self.failed_attempts[key]
    
    def _is_account_locked(self, email: str, client_ip: str) -> bool:
        """Check if account is locked"""
        key = f"{email}:{client_ip}"
        if key not in self.failed_attempts:
            return False
        
        # Check if too many recent attempts
        recent_attempts = [
            attempt for attempt in self.failed_attempts[key]
            if datetime.utcnow() - attempt < timedelta(minutes=15)
        ]
        
        return len(recent_attempts) >= 5
    
    def set_secure_cookies(self, response: Response, tokens: Dict[str, Any]):
        """Set secure httpOnly cookies"""
        try:
            # Set access token as httpOnly cookie
            response.set_cookie(
                key="access_token",
                value=tokens["access_token"],
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                httponly=True,
                secure=True,  # HTTPS only
                samesite="strict",
                path="/",
                domain=None  # Current domain
            )
            
            # Set refresh token as httpOnly cookie
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh_token"],
                max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
                httponly=True,
                secure=True,  # HTTPS only
                samesite="strict",
                path="/",
                domain=None  # Current domain
            )
            
            # Set CSRF token
            csrf_token = secrets.token_urlsafe(32)
            response.set_cookie(
                key="csrf_token",
                value=csrf_token,
                max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                httponly=False,  # Accessible to JavaScript for CSRF protection
                secure=True,
                samesite="strict",
                path="/"
            )
            
        except Exception as e:
            logger.error(f"Failed to set secure cookies: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to set authentication cookies"
            )
    
    def clear_secure_cookies(self, response: Response):
        """Clear secure cookies on logout"""
        try:
            # Clear all authentication cookies
            response.delete_cookie("access_token", path="/")
            response.delete_cookie("refresh_token", path="/")
            response.delete_cookie("csrf_token", path="/")
            
        except Exception as e:
            logger.error(f"Failed to clear secure cookies: {e}")
    
    def get_token_from_cookies(self, request: Request) -> Optional[str]:
        """Get access token from httpOnly cookies"""
        return request.cookies.get("access_token")
    
    def validate_csrf_token(self, request: Request) -> bool:
        """Validate CSRF token"""
        try:
            # Get CSRF token from cookie
            csrf_cookie = request.cookies.get("csrf_token")
            if not csrf_cookie:
                return False
            
            # Get CSRF token from header
            csrf_header = request.headers.get("X-CSRF-Token")
            if not csrf_header:
                return False
            
            # Compare tokens
            return csrf_cookie == csrf_header
            
        except Exception as e:
            logger.error(f"CSRF validation error: {e}")
            return False

# Global secure auth manager
secure_auth_manager = SecureAuthManager() 