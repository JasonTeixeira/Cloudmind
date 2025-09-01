"""
Expert-Level Project Storage Schemas
Pydantic schemas for file storage, Git integration, and template management
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Optional, Any, Union
from uuid import UUID
from datetime import datetime
from enum import Enum


# File Storage Schemas

class FileUploadResponse(BaseModel):
    """Response schema for file upload"""
    success: bool
    file_id: str
    file_path: str
    file_size: int
    version: int
    message: str


class FileListResponse(BaseModel):
    """Response schema for file listing"""
    success: bool
    files: List[Dict[str, Any]]
    total_count: int
    limit: int
    offset: int


class FileDownloadResponse(BaseModel):
    """Response schema for file download metadata"""
    success: bool
    file_id: str
    file_path: str
    file_name: str
    file_type: str
    mime_type: Optional[str]
    file_size: int
    version: int
    created_at: datetime
    updated_at: datetime
    created_by: str
    commit_message: Optional[str]
    security_scan_results: Optional[Dict[str, Any]]
    ai_analysis: Optional[Dict[str, Any]]


# Git Integration Schemas

class GitCloneRequest(BaseModel):
    """Request schema for Git repository cloning"""
    repo_url: str = Field(..., description="Git repository URL")
    branch: str = Field("main", description="Branch to clone")
    credentials: Optional[Dict[str, str]] = Field(None, description="Authentication credentials")

    @field_validator('repo_url')
    def validate_repo_url(cls, v):
        if not v.startswith(('http://', 'https://', 'git://', 'ssh://')):
            raise ValueError('Invalid repository URL')
        return v


class GitCommitRequest(BaseModel):
    """Request schema for Git commit"""
    message: str = Field(..., min_length=1, max_length=500, description="Commit message")
    files: Optional[List[str]] = Field(None, description="Specific files to commit")
    author_name: Optional[str] = Field(None, description="Author name")
    author_email: Optional[str] = Field(None, description="Author email")

    @field_validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Commit message cannot be empty')
        return v.strip()


class GitPushRequest(BaseModel):
    """Request schema for Git push"""
    remote: str = Field("origin", description="Remote repository name")
    branch: Optional[str] = Field(None, description="Branch to push")


class GitPullRequest(BaseModel):
    """Request schema for Git pull"""
    remote: str = Field("origin", description="Remote repository name")
    branch: Optional[str] = Field(None, description="Branch to pull")


# Template Management Schemas

class TemplateCreateRequest(BaseModel):
    """Request schema for template creation"""
    project_id: UUID = Field(..., description="Source project ID")
    template_name: str = Field(..., min_length=1, max_length=255, description="Template name")
    description: Optional[str] = Field(None, max_length=1000, description="Template description")
    category: str = Field("custom", description="Template category")
    subcategory: Optional[str] = Field(None, description="Template subcategory")
    tags: Optional[List[str]] = Field(None, description="Template tags")
    is_public: bool = Field(False, description="Whether template is public")

    @field_validator('template_name')
    def validate_template_name(cls, v):
        if not v.strip():
            raise ValueError('Template name cannot be empty')
        return v.strip()


class TemplateApplyRequest(BaseModel):
    """Request schema for template application"""
    new_project_id: UUID = Field(..., description="Target project ID")
    variables: Optional[Dict[str, Any]] = Field(None, description="Template variables")


class TemplateListResponse(BaseModel):
    """Response schema for template listing"""
    success: bool
    templates: List[Dict[str, Any]]
    total_count: int
    limit: int
    offset: int


class TemplateDetailsResponse(BaseModel):
    """Response schema for template details"""
    success: bool
    template: Dict[str, Any]


class TemplateUpdateRequest(BaseModel):
    """Request schema for template updates"""
    updates: Dict[str, Any] = Field(..., description="Template updates")

    @field_validator('updates')
    def validate_updates(cls, v):
        allowed_fields = {
            'name', 'description', 'category', 'subcategory', 'tags',
            'complexity_level', 'estimated_duration', 'technology_stack',
            'architecture_pattern', 'is_public', 'is_featured', 'shared_with'
        }
        
        invalid_fields = set(v.keys()) - allowed_fields
        if invalid_fields:
            raise ValueError(f'Invalid update fields: {invalid_fields}')
        
        return v


class TemplateShareRequest(BaseModel):
    """Request schema for template sharing"""
    user_ids: List[UUID] = Field(..., description="User IDs to share with")

    @field_validator('user_ids')
    def validate_user_ids(cls, v):
        if not v:
            raise ValueError('At least one user ID must be provided')
        return v


# File Analysis Schemas

class FileAnalysisRequest(BaseModel):
    """Request schema for file analysis"""
    file_path: str = Field(..., description="File path to analyze")
    analysis_type: str = Field("full", description="Type of analysis to perform")


class FileAnalysisResponse(BaseModel):
    """Response schema for file analysis"""
    success: bool
    file_path: str
    language_detected: Optional[str]
    complexity_score: Optional[int]
    security_scan_results: Optional[Dict[str, Any]]
    ai_analysis: Optional[Dict[str, Any]]
    analysis_timestamp: datetime


# Directory Management Schemas

class DirectoryCreateRequest(BaseModel):
    """Request schema for directory creation"""
    directory_path: str = Field(..., description="Directory path to create")

    @field_validator('directory_path')
    def validate_directory_path(cls, v):
        if not v.strip():
            raise ValueError('Directory path cannot be empty')
        if v.startswith('/') or '..' in v:
            raise ValueError('Invalid directory path')
        return v.strip()


class DirectoryInfoResponse(BaseModel):
    """Response schema for directory information"""
    success: bool
    directory_id: str
    directory_path: str
    directory_name: str
    total_files: int
    total_size: int
    file_types: Dict[str, int]
    created_at: datetime
    created_by: str


# Search and Filter Schemas

class FileSearchRequest(BaseModel):
    """Request schema for file search"""
    query: str = Field(..., min_length=1, description="Search query")
    file_types: Optional[List[str]] = Field(None, description="File types to search")
    search_content: bool = Field(True, description="Whether to search file content")
    limit: int = Field(50, ge=1, le=100, description="Maximum results")

    @field_validator('query')
    def validate_query(cls, v):
        if not v.strip():
            raise ValueError('Search query cannot be empty')
        return v.strip()


class FileSearchResponse(BaseModel):
    """Response schema for file search"""
    success: bool
    results: List[Dict[str, Any]]
    total_count: int
    query: str
    search_time_ms: Optional[int]


# Version Control Schemas

class FileVersionInfo(BaseModel):
    """Schema for file version information"""
    version: int
    commit_hash: str
    commit_message: str
    author: str
    timestamp: datetime
    file_size: int
    change_type: str


class FileVersionHistoryResponse(BaseModel):
    """Response schema for file version history"""
    success: bool
    file_path: str
    versions: List[FileVersionInfo]
    total_versions: int


# Collaboration Schemas

class FileCollaborationRequest(BaseModel):
    """Request schema for file collaboration"""
    session_id: str = Field(..., description="Collaboration session ID")
    cursor_position: Optional[int] = Field(None, ge=0, description="Cursor position")
    selection_start: Optional[int] = Field(None, ge=0, description="Selection start")
    selection_end: Optional[int] = Field(None, ge=0, description="Selection end")


class FileCollaborationResponse(BaseModel):
    """Response schema for file collaboration"""
    success: bool
    session_id: str
    active_users: List[Dict[str, Any]]
    last_activity: datetime


# Backup and Recovery Schemas

class BackupCreateRequest(BaseModel):
    """Request schema for backup creation"""
    backup_name: str = Field(..., min_length=1, max_length=255, description="Backup name")
    backup_type: str = Field("full", description="Backup type (full, incremental, differential)")
    backup_reason: Optional[str] = Field(None, description="Reason for backup")
    retention_days: int = Field(30, ge=1, le=365, description="Retention period in days")


class BackupInfoResponse(BaseModel):
    """Response schema for backup information"""
    success: bool
    backup_id: str
    backup_name: str
    backup_type: str
    backup_size: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    retention_days: int


# Error Response Schemas

class ErrorResponse(BaseModel):
    """Standard error response schema"""
    success: bool = False
    error: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ValidationErrorResponse(BaseModel):
    """Validation error response schema"""
    success: bool = False
    error: str
    field_errors: Dict[str, List[str]]
    error_code: str = "VALIDATION_ERROR"


# Success Response Schemas

class SuccessResponse(BaseModel):
    """Standard success response schema"""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None


# Pagination Schemas

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    size: int = Field(50, ge=1, le=1000, description="Page size")
    sort_by: Optional[str] = Field(None, description="Sort field")
    sort_order: str = Field("desc", description="Sort order (asc/desc)")
    
    @field_validator('sort_order')
    def validate_sort_order(cls, v):
        if v not in ['asc', 'desc']:
            raise ValueError('Sort order must be "asc" or "desc"')
        return v


class PaginatedResponse(BaseModel):
    """Paginated response schema"""
    success: bool
    data: List[Dict[str, Any]]
    pagination: Dict[str, Any]
    total_count: int
    total_pages: int
    current_page: int
    page_size: int


# File Type Enums

class FileType(str, Enum):
    """File type enumeration"""
    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    ARCHIVE = "archive"
    DOCUMENT = "document"
    CODE = "code"
    CONFIG = "config"
    OTHER = "other"


class ComplexityLevel(str, Enum):
    """Complexity level enumeration"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class TemplateCategory(str, Enum):
    """Template category enumeration"""
    WEB_APP = "web-app"
    MICROSERVICE = "microservice"
    MOBILE_APP = "mobile-app"
    DESKTOP_APP = "desktop-app"
    API = "api"
    LIBRARY = "library"
    TOOL = "tool"
    CUSTOM = "custom"


# Advanced Filter Schemas

class FileFilterRequest(BaseModel):
    """Advanced file filtering request"""
    file_types: Optional[List[FileType]] = Field(None, description="File types to include")
    min_size: Optional[int] = Field(None, ge=0, description="Minimum file size")
    max_size: Optional[int] = Field(None, ge=0, description="Maximum file size")
    created_after: Optional[datetime] = Field(None, description="Created after date")
    created_before: Optional[datetime] = Field(None, description="Created before date")
    modified_after: Optional[datetime] = Field(None, description="Modified after date")
    modified_before: Optional[datetime] = Field(None, description="Modified before date")
    created_by: Optional[UUID] = Field(None, description="Created by user")
    has_security_issues: Optional[bool] = Field(None, description="Has security issues")
    complexity_min: Optional[int] = Field(None, ge=0, le=100, description="Minimum complexity score")
    complexity_max: Optional[int] = Field(None, ge=0, le=100, description="Maximum complexity score")

    @model_validator(mode='after')
    def _validate_size_range(self):
        try:
            if self.max_size and self.min_size and self.max_size < self.min_size:
                raise ValueError('max_size must be greater than min_size')
        except Exception:
            pass
        return self

    @model_validator(mode='after')
    def _validate_complexity_range(self):
        try:
            if self.complexity_max and self.complexity_min and self.complexity_max < self.complexity_min:
                raise ValueError('complexity_max must be greater than complexity_min')
        except Exception:
            pass
        return self


class TemplateFilterRequest(BaseModel):
    """Advanced template filtering request"""
    categories: Optional[List[TemplateCategory]] = Field(None, description="Template categories")
    complexity_levels: Optional[List[ComplexityLevel]] = Field(None, description="Complexity levels")
    tags: Optional[List[str]] = Field(None, description="Required tags")
    min_rating: Optional[int] = Field(None, ge=1, le=5, description="Minimum rating")
    max_rating: Optional[int] = Field(None, ge=1, le=5, description="Maximum rating")
    min_usage_count: Optional[int] = Field(None, ge=0, description="Minimum usage count")
    created_after: Optional[datetime] = Field(None, description="Created after date")
    created_before: Optional[datetime] = Field(None, description="Created before date")
    is_featured: Optional[bool] = Field(None, description="Featured templates only")
    technology_stack: Optional[List[str]] = Field(None, description="Required technology stack")

    @model_validator(mode='after')
    def _validate_rating_range(self):
        try:
            if self.max_rating and self.min_rating and self.max_rating < self.min_rating:
                raise ValueError('max_rating must be greater than min_rating')
        except Exception:
            pass
        return self
