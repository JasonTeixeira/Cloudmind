"""
Project Member Model for CloudMind
Handles project collaboration and team management
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ProjectRole(str, Enum):
    """Project member roles with permissions"""
    OWNER = "owner"           # Full access, can delete project
    ADMIN = "admin"           # Can manage members, settings
    EDITOR = "editor"         # Can edit project content
    VIEWER = "viewer"         # Read-only access
    GUEST = "guest"           # Limited access


class ProjectMember(Base):
    """Project Member model for team collaboration"""
    
    __tablename__ = "project_members"
    
    # Primary key
    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    project_id = Column(PostgresUUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    invited_by = Column(PostgresUUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Member details
    role = Column(String(20), default=ProjectRole.VIEWER, nullable=False)
    permissions = Column(Text, nullable=True)  # JSON string of specific permissions
    
    # Status and timestamps
    is_active = Column(Boolean, default=True, nullable=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_active = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Invitation details
    invitation_token = Column(String(255), nullable=True, unique=True)
    invitation_expires_at = Column(DateTime(timezone=True), nullable=True)
    invitation_accepted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="members")
    user = relationship("User", foreign_keys=[user_id], back_populates="project_memberships")
    inviter = relationship("User", foreign_keys=[invited_by])
    
    def __repr__(self):
        return f"<ProjectMember(id={self.id}, project_id={self.project_id}, user_id={self.user_id}, role={self.role})>"
    
    @property
    def is_owner(self) -> bool:
        """Check if member is project owner"""
        return self.role == ProjectRole.OWNER
    
    @property
    def is_admin(self) -> bool:
        """Check if member is project admin"""
        return self.role in [ProjectRole.OWNER, ProjectRole.ADMIN]
    
    @property
    def can_edit(self) -> bool:
        """Check if member can edit project"""
        return self.role in [ProjectRole.OWNER, ProjectRole.ADMIN, ProjectRole.EDITOR]
    
    @property
    def can_manage_members(self) -> bool:
        """Check if member can manage other members"""
        return self.role in [ProjectRole.OWNER, ProjectRole.ADMIN]
    
    @property
    def is_invitation_pending(self) -> bool:
        """Check if invitation is still pending"""
        return (
            self.invitation_token is not None and 
            self.invitation_expires_at and 
            self.invitation_expires_at > datetime.utcnow() and
            self.invitation_accepted_at is None
        )
    
    def accept_invitation(self) -> None:
        """Accept the project invitation"""
        self.invitation_accepted_at = datetime.utcnow()
        self.invitation_token = None
        self.invitation_expires_at = None
        self.is_active = True
    
    def update_last_active(self) -> None:
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
    
    def has_permission(self, permission: str) -> bool:
        """Check if member has specific permission"""
        if self.role == ProjectRole.OWNER:
            return True
        
        if not self.permissions:
            return False
        
        # Parse permissions JSON and check
        import json
        try:
            user_permissions = json.loads(self.permissions)
            return permission in user_permissions
        except (json.JSONDecodeError, TypeError):
            return False 