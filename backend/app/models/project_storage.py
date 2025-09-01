"""
Expert-Level Project Storage Models
Enterprise-grade file storage, version control, and collaboration system
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4
from sqlalchemy import Column, String, Text, BigInteger, Integer, DateTime, Boolean, ForeignKey, JSON, Index, UniqueConstraint, Float
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class ProjectFile(Base):
    """
    Expert-level file storage with version control, metadata, and collaboration
    """
    __tablename__ = "project_files"
    
    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    # File path and structure
    file_path = Column(String(2048), nullable=False)  # Full file path within project
    file_name = Column(String(255), nullable=False)   # Just the filename
    directory_path = Column(String(1024), nullable=False)  # Directory path
    
    # File metadata
    file_type = Column(String(50), nullable=False)  # Extension-based type
    mime_type = Column(String(100))  # MIME type for web serving
    file_size = Column(BigInteger, nullable=False, default=0)
    content_hash = Column(String(64), nullable=False)  # SHA-256 hash
    encoding = Column(String(20), default='utf-8')
    
    # Version control
    version = Column(Integer, default=1, nullable=False)
    parent_version_id = Column(UUID(as_uuid=True), ForeignKey("project_files.id"))
    is_latest = Column(Boolean, default=True, nullable=False)
    commit_message = Column(Text)
    commit_author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # File content and storage
    content = Column(Text)  # For text files
    binary_content = Column(JSONB)  # For binary files (chunked)
    storage_location = Column(String(500))  # S3, local, etc.
    storage_metadata = Column(JSONB)  # Storage-specific metadata
    
    # File analysis and intelligence
    language_detected = Column(String(50))  # Programming language
    complexity_score = Column(Integer)  # Code complexity
    security_scan_results = Column(JSONB)  # Security analysis
    ai_analysis = Column(JSONB)  # AI-generated insights
    
    # Collaboration and permissions
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    permissions = Column(JSONB)  # Granular permissions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_accessed = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="files")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    commit_author = relationship("User", foreign_keys=[commit_author_id])
    parent_version = relationship("ProjectFile", remote_side=[id])
    child_versions = relationship("ProjectFile", back_populates="parent_version")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_project_files_project_path', 'project_id', 'file_path'),
        Index('idx_project_files_type', 'file_type'),
        Index('idx_project_files_created_by', 'created_by'),
        Index('idx_project_files_updated_at', 'updated_at'),
        Index('idx_project_files_content_hash', 'content_hash'),
        UniqueConstraint('project_id', 'file_path', 'version', name='uq_project_file_version'),
    )


class ProjectDirectory(Base):
    """
    Directory structure management with metadata and permissions
    """
    __tablename__ = "project_directories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    # Directory structure
    directory_path = Column(String(1024), nullable=False)
    directory_name = Column(String(255), nullable=False)
    parent_directory_id = Column(UUID(as_uuid=True), ForeignKey("project_directories.id"))
    
    # Directory metadata
    total_files = Column(Integer, default=0)
    total_size = Column(BigInteger, default=0)
    file_types = Column(JSONB)  # Count of different file types
    
    # Permissions and access
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    permissions = Column(JSONB)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="directories")
    parent_directory = relationship("ProjectDirectory", remote_side=[id])
    child_directories = relationship("ProjectDirectory", back_populates="parent_directory")
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_project_directories_project_path', 'project_id', 'directory_path'),
        UniqueConstraint('project_id', 'directory_path', name='uq_project_directory'),
    )


class ProjectTemplate(Base):
    """
    Expert-level project templates with metadata, categories, and sharing
    """
    __tablename__ = "project_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Template identification
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False)  # web-app, microservice, etc.
    subcategory = Column(String(100))  # react, python, etc.
    tags = Column(JSONB)  # Array of tags
    
    # Template structure
    file_structure = Column(JSONB, nullable=False)  # Complete file tree
    template_files = Column(JSONB)  # Template file contents
    variables = Column(JSONB)  # Template variables and defaults
    dependencies = Column(JSONB)  # Required dependencies
    
    # Template metadata
    complexity_level = Column(String(20))  # beginner, intermediate, expert
    estimated_duration = Column(Integer)  # Hours to implement
    technology_stack = Column(JSONB)  # Technologies used
    architecture_pattern = Column(String(100))  # MVC, microservices, etc.
    
    # Quality and validation
    template_version = Column(String(20), default="1.0.0")
    is_validated = Column(Boolean, default=False)
    validation_results = Column(JSONB)
    test_coverage = Column(Integer)  # Percentage
    
    # Usage and popularity
    usage_count = Column(Integer, default=0)
    rating = Column(Integer)  # 1-5 stars
    reviews = Column(JSONB)  # User reviews
    
    # Sharing and collaboration
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    shared_with = Column(JSONB)  # Users with access
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    created_by_user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_project_templates_category', 'category'),
        Index('idx_project_templates_created_by', 'created_by'),
        Index('idx_project_templates_public', 'is_public'),
        Index('idx_project_templates_featured', 'is_featured'),
    )


class ProjectDocumentation(Base):
    """
    Comprehensive documentation storage with versioning and collaboration
    """
    __tablename__ = "project_documentation"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    # Documentation identification
    title = Column(String(255), nullable=False)
    doc_type = Column(String(50), nullable=False)  # README, API, ARCHITECTURE, etc.
    doc_path = Column(String(1024))  # Path within project
    
    # Content and structure
    content = Column(Text, nullable=False)
    content_format = Column(String(20), default='markdown')  # markdown, asciidoc, etc.
    table_of_contents = Column(JSONB)  # Auto-generated TOC
    doc_metadata = Column(JSONB)  # Additional metadata
    
    # Version control
    version = Column(Integer, default=1, nullable=False)
    parent_version_id = Column(UUID(as_uuid=True), ForeignKey("project_documentation.id"))
    is_latest = Column(Boolean, default=True, nullable=False)
    change_log = Column(JSONB)  # Version change history
    
    # Collaboration
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    reviewers = Column(JSONB)  # Assigned reviewers
    review_status = Column(String(20), default='draft')  # draft, review, approved
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="documentation")
    created_by_user = relationship("User", foreign_keys=[created_by])
    updated_by_user = relationship("User", foreign_keys=[updated_by])
    parent_version = relationship("ProjectDocumentation", remote_side=[id])
    
    # Indexes
    __table_args__ = (
        Index('idx_project_docs_project_type', 'project_id', 'doc_type'),
        Index('idx_project_docs_created_by', 'created_by'),
        UniqueConstraint('project_id', 'doc_path', 'version', name='uq_project_doc_version'),
    )


class FileCollaboration(Base):
    """
    Real-time collaboration and editing tracking
    """
    __tablename__ = "file_collaboration"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False)
    
    # Collaboration session
    session_id = Column(String(100), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Cursor and selection
    cursor_position = Column(Integer)
    selection_start = Column(Integer)
    selection_end = Column(Integer)
    
    # Session state
    is_active = Column(Boolean, default=True)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    file = relationship("ProjectFile")
    user = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_file_collaboration_file_session', 'file_id', 'session_id'),
        Index('idx_file_collaboration_user', 'user_id'),
        Index('idx_file_collaboration_active', 'is_active'),
    )


class FileChange(Base):
    """
    Detailed file change tracking for version control
    """
    __tablename__ = "file_changes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    file_id = Column(UUID(as_uuid=True), ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False)
    
    # Change identification
    change_type = Column(String(20), nullable=False)  # create, update, delete, rename
    change_hash = Column(String(64), nullable=False)  # Hash of the change
    
    # Change details
    old_content = Column(Text)
    new_content = Column(Text)
    diff = Column(JSONB)  # Structured diff information
    line_changes = Column(JSONB)  # Line-by-line changes
    
    # Change metadata
    change_size = Column(Integer)  # Number of lines changed
    complexity_change = Column(Integer)  # Change in complexity score
    
    # Author and context
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    commit_message = Column(Text)
    branch_name = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    file = relationship("ProjectFile")
    author = relationship("User")
    
    # Indexes
    __table_args__ = (
        Index('idx_file_changes_file_type', 'file_id', 'change_type'),
        Index('idx_file_changes_author', 'author_id'),
        Index('idx_file_changes_created_at', 'created_at'),
    )


class ProjectBackup(Base):
    """
    Automated project backup and recovery system
    """
    __tablename__ = "project_backups"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    # Backup identification
    backup_name = Column(String(255), nullable=False)
    backup_type = Column(String(20), nullable=False)  # full, incremental, differential
    backup_reason = Column(String(100))  # manual, scheduled, before_major_change
    
    # Backup content
    file_snapshots = Column(JSONB, nullable=False)  # File state at backup time
    metadata_snapshot = Column(JSONB)  # Project metadata at backup time
    
    # Storage and location
    storage_location = Column(String(500), nullable=False)
    backup_size = Column(BigInteger)
    compression_ratio = Column(Float)
    
    # Backup status
    status = Column(String(20), default='in_progress')  # in_progress, completed, failed
    error_message = Column(Text)
    
    # Retention and lifecycle
    retention_days = Column(Integer, default=30)
    is_encrypted = Column(Boolean, default=True)
    encryption_key_id = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    project = relationship("Project", back_populates="backups")
    
    # Indexes
    __table_args__ = (
        Index('idx_project_backups_project_status', 'project_id', 'status'),
        Index('idx_project_backups_created_at', 'created_at'),
    )


# Update existing Project model to include relationships
def update_project_model():
    """
    Add relationships to existing Project model
    """
    from backend.app.models.project import Project
    
    # Add relationships to Project model
    Project.files = relationship("ProjectFile", back_populates="project", cascade="all, delete-orphan")
    Project.directories = relationship("ProjectDirectory", back_populates="project", cascade="all, delete-orphan")
    Project.documentation = relationship("ProjectDocumentation", back_populates="project", cascade="all, delete-orphan")
    Project.backups = relationship("ProjectBackup", back_populates="project", cascade="all, delete-orphan")
    
    return Project
