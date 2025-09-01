"""
Enhanced User Service with Activity Tracking and Master Dashboard
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc

from app.models.user import User, UserActivity, UserRole, UserStatus
from app.schemas.user import UserCreate, UserUpdate, UserProfileUpdate
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


class UserService:
    """Enhanced user service with activity tracking"""
    
    def __init__(self, db: Session):
        self.db = db
        self.auth_service = AuthService(db)
    
    async def get_users(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        role: Optional[UserRole] = None,
        status: Optional[UserStatus] = None
    ) -> List[User]:
        """Get users with filtering"""
        try:
            query = self.db.query(User)
            
            if role:
                query = query.filter(User.role == role)
            
            if status:
                query = query.filter(User.status == status)
            
            users = query.offset(skip).limit(limit).all()
            return users
            
        except Exception as e:
            logger.error(f"Get users error: {str(e)}")
            return []
    
    async def get_user(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            return user
            
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user
            
        except Exception as e:
            logger.error(f"Get user by email error: {str(e)}")
            return None
    
    async def create_user(self, user_data: UserCreate, created_by: UUID) -> User:
        """Create new user"""
        try:
            # Check if email already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                raise ValueError("Email already registered")
            
            # Check if username already exists
            existing_username = self.db.query(User).filter(User.username == user_data.username).first()
            if existing_username:
                raise ValueError("Username already taken")
            
            # Hash password
            hashed_password = self.auth_service.get_password_hash(user_data.password)
            
            # Create user
            user = User(
                email=user_data.email,
                username=user_data.username,
                full_name=user_data.full_name,
                hashed_password=hashed_password,
                role=user_data.role,
                is_master_user=user_data.is_master_user,
                company=user_data.company,
                job_title=user_data.job_title,
                phone=user_data.phone,
                location=user_data.location,
                timezone=user_data.timezone or "UTC",
                created_by=created_by
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User created: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Create user error: {str(e)}")
            self.db.rollback()
            raise
    
    async def update_user(self, user_id: UUID, user_data: UserUpdate, updated_by: UUID) -> Optional[User]:
        """Update user"""
        try:
            user = await self.get_user(user_id)
            if not user:
                return None
            
            # Update fields
            if user_data.email is not None:
                # Check if email is already taken by another user
                existing_user = self.db.query(User).filter(
                    and_(User.email == user_data.email, User.id != user_id)
                ).first()
                if existing_user:
                    raise ValueError("Email already taken by another user")
                user.email = user_data.email
            
            if user_data.username is not None:
                # Check if username is already taken by another user
                existing_username = self.db.query(User).filter(
                    and_(User.username == user_data.username, User.id != user_id)
                ).first()
                if existing_username:
                    raise ValueError("Username already taken by another user")
                user.username = user_data.username
            
            if user_data.full_name is not None:
                user.full_name = user_data.full_name
            
            if user_data.role is not None:
                user.role = user_data.role
            
            if user_data.status is not None:
                user.status = user_data.status
            
            if user_data.company is not None:
                user.company = user_data.company
            
            if user_data.job_title is not None:
                user.job_title = user_data.job_title
            
            if user_data.phone is not None:
                user.phone = user_data.phone
            
            if user_data.location is not None:
                user.location = user_data.location
            
            if user_data.timezone is not None:
                user.timezone = user_data.timezone
            
            if user_data.is_active is not None:
                user.is_active = user_data.is_active
            
            if user_data.is_verified is not None:
                user.is_verified = user_data.is_verified
            
            if user_data.is_master_user is not None:
                user.is_master_user = user_data.is_master_user
            
            user.updated_by = updated_by
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User updated: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Update user error: {str(e)}")
            self.db.rollback()
            raise
    
    async def update_user_profile(self, user_id: UUID, profile_data: UserProfileUpdate) -> Optional[User]:
        """Update current user profile"""
        try:
            user = await self.get_user(user_id)
            if not user:
                return None
            
            # Update profile fields
            if profile_data.full_name is not None:
                user.full_name = profile_data.full_name
            
            if profile_data.company is not None:
                user.company = profile_data.company
            
            if profile_data.job_title is not None:
                user.job_title = profile_data.job_title
            
            if profile_data.phone is not None:
                user.phone = profile_data.phone
            
            if profile_data.location is not None:
                user.location = profile_data.location
            
            if profile_data.timezone is not None:
                user.timezone = profile_data.timezone
            
            if profile_data.bio is not None:
                user.bio = profile_data.bio
            
            if profile_data.avatar_url is not None:
                user.avatar_url = profile_data.avatar_url
            
            if profile_data.preferences is not None:
                user.preferences = profile_data.preferences
            
            if profile_data.notification_settings is not None:
                user.notification_settings = profile_data.notification_settings
            
            if profile_data.ui_settings is not None:
                user.ui_settings = profile_data.ui_settings
            
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User profile updated: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Update user profile error: {str(e)}")
            self.db.rollback()
            return None
    
    async def delete_user(self, user_id: UUID, deleted_by: UUID) -> bool:
        """Delete user"""
        try:
            user = await self.get_user(user_id)
            if not user:
                return False
            
            # Prevent deletion of master user
            if user.is_master_user:
                raise ValueError("Cannot delete master user")
            
            # Soft delete by deactivating
            user.is_active = False
            user.status = UserStatus.INACTIVE
            user.updated_by = deleted_by
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            
            logger.info(f"User deactivated: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Delete user error: {str(e)}")
            self.db.rollback()
            raise
    
    async def track_user_activity(
        self, 
        user_id: UUID, 
        activity_type: str, 
        description: str, 
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserActivity:
        """Track user activity"""
        try:
            activity = UserActivity(
                user_id=user_id,
                activity_type=activity_type,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent,
                activity_metadata=metadata or {}
            )
            
            self.db.add(activity)
            self.db.commit()
            self.db.refresh(activity)
            
            return activity
            
        except Exception as e:
            logger.error(f"Track activity error: {str(e)}")
            self.db.rollback()
            raise
    
    async def track_failed_login_attempt(self, email: str, ip_address: str) -> None:
        """Track failed login attempt"""
        try:
            user = await self.get_user_by_email(email)
            if user:
                user.increment_failed_login_attempts()
                self.db.commit()
                
                # Track activity
                await self.track_user_activity(
                    user.id,
                    "failed_login",
                    f"Failed login attempt from {ip_address}",
                    ip_address,
                    metadata={"failed_attempts": user.failed_login_attempts}
                )
                
        except Exception as e:
            logger.error(f"Track failed login error: {str(e)}")
    
    async def get_user_activities(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        activity_type: Optional[str] = None
    ) -> List[UserActivity]:
        """Get user activities"""
        try:
            query = self.db.query(UserActivity).filter(UserActivity.user_id == user_id)
            
            if activity_type:
                query = query.filter(UserActivity.activity_type == activity_type)
            
            activities = query.order_by(desc(UserActivity.created_at)).offset(skip).limit(limit).all()
            return activities
            
        except Exception as e:
            logger.error(f"Get user activities error: {str(e)}")
            return []
    
    async def get_master_dashboard_data(self) -> Dict[str, Any]:
        """Get master dashboard data"""
        try:
            # Get user statistics
            total_users = self.db.query(User).count()
            active_users = self.db.query(User).filter(User.is_active == True).count()
            
            # Get user stats by role
            user_stats = {}
            for role in UserRole:
                count = self.db.query(User).filter(User.role == role).count()
                user_stats[role.value] = count
            
            # Get recent activities
            recent_activities = self.db.query(UserActivity).order_by(
                desc(UserActivity.created_at)
            ).limit(10).all()
            
            # Get system health metrics
            system_health = {
                "total_users": total_users,
                "active_users": active_users,
                "inactive_users": total_users - active_users,
                "users_by_role": user_stats,
                "recent_activities_count": len(recent_activities)
            }
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "total_projects": 0,  # Will be implemented with project service
                "total_cost_analyses": 0,  # Will be implemented with cost service
                "total_security_scans": 0,  # Will be implemented with security service
                "recent_activities": [activity.to_dict() for activity in recent_activities],
                "user_stats": user_stats,
                "system_health": system_health
            }
            
        except Exception as e:
            logger.error(f"Get master dashboard error: {str(e)}")
            return {}
    
    async def get_user_permissions(self, user: User) -> Dict[str, bool]:
        """Get user permissions"""
        return await self.auth_service.get_user_permissions(user)
    
    async def is_user_locked(self, user: User) -> bool:
        """Check if user account is locked"""
        return user.is_locked
    
    async def unlock_user_account(self, user_id: UUID) -> bool:
        """Unlock user account"""
        return await self.auth_service.unlock_user_account(user_id)
    
    async def get_active_sessions(self, user_id: UUID) -> List[Dict[str, Any]]:
        """Get active user sessions (placeholder for future implementation)"""
        # This would be implemented with a session management system
        return []
    
    async def revoke_user_session(self, user_id: UUID, session_id: str) -> bool:
        """Revoke user session (placeholder for future implementation)"""
        # This would be implemented with a session management system
        return True 