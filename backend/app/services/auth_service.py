"""
Enhanced Authentication Service with Master User Support
"""

import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.core.config import settings
from app.models.user import User, UserRole
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Enhanced authentication service"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        try:
            # Find user by email
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                return None
            
            # Verify password
            if not self.verify_password(password, user.hashed_password):
                return None
            
            # Check if user is active
            if not user.is_active:
                return None
            
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    async def create_user_tokens(self, user: User) -> Dict[str, str]:
        """Create access and refresh tokens for user"""
        try:
            # Create token data
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "is_master": user.is_master,
                "is_superuser": user.is_superuser
            }
            
            # Create tokens
            access_token = self.create_access_token(token_data)
            refresh_token = self.create_refresh_token(token_data)
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}")
            raise
    
    async def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """Refresh access token using refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token)
            if not payload or payload.get("type") != "refresh":
                return None
            
            # Get user
            user_id = payload.get("sub")
            if not user_id:
                return None
            
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                return None
            
            # Create new access token
            token_data = {
                "sub": str(user.id),
                "email": user.email,
                "username": user.username,
                "role": user.role,
                "is_master": user.is_master,
                "is_superuser": user.is_superuser
            }
            
            new_access_token = self.create_access_token(token_data)
            return new_access_token
            
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return None
    
    async def change_password(self, user_id: UUID, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            # Get user
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            # Verify current password
            if not self.verify_password(current_password, user.hashed_password):
                return False
            
            # Hash new password
            hashed_new_password = self.get_password_hash(new_password)
            
            # Update password
            user.hashed_password = hashed_new_password
            user.password_changed_at = datetime.utcnow()
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Password change error: {str(e)}")
            self.db.rollback()
            return False
    
    async def create_master_user(self, master_data: UserCreate) -> User:
        """Create master user with enhanced permissions"""
        try:
            # Check if master user already exists
            existing_master = self.db.query(User).filter(User.is_master_user == True).first()
            if existing_master:
                raise ValueError("Master user already exists")
            
            # Create master user
            hashed_password = self.get_password_hash(master_data.password)
            
            master_user = User(
                email=master_data.email,
                username=master_data.username,
                full_name=master_data.full_name,
                hashed_password=hashed_password,
                role=UserRole.MASTER,
                is_master_user=True,
                is_superuser=True,
                is_verified=True,
                is_active=True,
                company=master_data.company,
                job_title=master_data.job_title,
                phone=master_data.phone,
                location=master_data.location,
                timezone=master_data.timezone or "UTC"
            )
            
            self.db.add(master_user)
            self.db.commit()
            self.db.refresh(master_user)
            
            logger.info(f"Master user created: {master_user.email}")
            return master_user
            
        except Exception as e:
            logger.error(f"Master user creation error: {str(e)}")
            self.db.rollback()
            raise
    
    async def validate_password_strength(self, password: str) -> bool:
        """Validate password strength with enhanced requirements"""
        import re
        
        # Minimum length
        if len(password) < 12:
            return False
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
        
        # Check for lowercase letter
        if not re.search(r'[a-z]', password):
            return False
        
        # Check for digit
        if not re.search(r'\d', password):
            return False
        
        # Check for special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            return False
        
        # Check for common weak patterns
        weak_patterns = [
            'password', '123456', 'qwerty', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'master', 'football'
        ]
        
        password_lower = password.lower()
        for pattern in weak_patterns:
            if pattern in password_lower:
                return False
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            return False
        
        return True
    
    async def lock_user_account(self, user_id: UUID, duration_minutes: int = 30) -> bool:
        """Lock user account temporarily"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.locked_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Account lock error: {str(e)}")
            self.db.rollback()
            return False
    
    async def unlock_user_account(self, user_id: UUID) -> bool:
        """Unlock user account"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            user.locked_until = None
            user.failed_login_attempts = 0
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Account unlock error: {str(e)}")
            self.db.rollback()
            return False
    
    async def get_user_permissions(self, user: User) -> Dict[str, bool]:
        """Get user permissions based on role"""
        return {
            "can_access_all_projects": user.can_access_all_projects,
            "can_manage_users": user.can_manage_users,
            "can_view_reports": user.can_view_reports,
            "is_master": user.is_master,
            "can_create_projects": user.role in [UserRole.MASTER, UserRole.ADMIN, UserRole.MANAGER],
            "can_delete_projects": user.role in [UserRole.MASTER, UserRole.ADMIN],
            "can_manage_infrastructure": user.role in [UserRole.MASTER, UserRole.ADMIN, UserRole.ENGINEER],
            "can_view_analytics": user.role in [UserRole.MASTER, UserRole.ADMIN, UserRole.MANAGER]
        } 