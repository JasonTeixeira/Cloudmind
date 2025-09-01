"""
File Explorer Schemas
Professional file management with advanced features
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class FileType(str, Enum):
    """File type enumeration"""
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    UNKNOWN = "unknown"


class GitStatus(str, Enum):
    """Git status enumeration"""
    UNTRACKED = "untracked"
    MODIFIED = "modified"
    STAGED = "staged"
    COMMITTED = "committed"
    IGNORED = "ignored"
    CONFLICT = "conflict"


class FileNode(BaseModel):
    """File tree node"""
    id: str = Field(..., description="Unique file identifier")
    name: str = Field(..., description="File or directory name")
    path: str = Field(..., description="Full file path")
    type: FileType = Field(..., description="File type")
    size: Optional[int] = Field(None, description="File size in bytes")
    modified_at: Optional[datetime] = Field(None, description="Last modification time")
    created_at: Optional[datetime] = Field(None, description="Creation time")
    is_hidden: bool = Field(default=False, description="Whether file is hidden")
    permissions: Optional[str] = Field(None, description="File permissions")
    owner: Optional[str] = Field(None, description="File owner")
    group: Optional[str] = Field(None, description="File group")
    git_status: Optional[GitStatus] = Field(None, description="Git status")
    mime_type: Optional[str] = Field(None, description="MIME type")
    extension: Optional[str] = Field(None, description="File extension")
    children: Optional[List['FileNode']] = Field(default=None, description="Child nodes for directories")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class FileTree(BaseModel):
    """File tree structure"""
    root: FileNode = Field(..., description="Root node")
    total_files: int = Field(..., description="Total number of files")
    total_directories: int = Field(..., description="Total number of directories")
    total_size: int = Field(..., description="Total size in bytes")
    last_updated: datetime = Field(..., description="Last tree update time")
    path: str = Field(..., description="Current path")


class FileFilters(BaseModel):
    """File search filters"""
    file_types: List[str] = Field(default_factory=list, description="File types to include")
    min_size: int = Field(default=0, description="Minimum file size")
    max_size: Optional[int] = Field(None, description="Maximum file size")
    modified_after: Optional[datetime] = Field(None, description="Modified after date")
    modified_before: Optional[datetime] = Field(None, description="Modified before date")
    git_status: List[GitStatus] = Field(default_factory=list, description="Git status filters")
    is_hidden: Optional[bool] = Field(None, description="Include hidden files")
    owner: str = Field(default="", description="File owner filter")
    group: str = Field(default="", description="File group filter")


class FileResult(BaseModel):
    """File search result"""
    id: str = Field(..., description="File identifier")
    name: str = Field(..., description="File name")
    path: str = Field(..., description="File path")
    type: FileType = Field(..., description="File type")
    size: Optional[int] = Field(None, description="File size")
    modified_at: Optional[datetime] = Field(None, description="Last modified")
    git_status: Optional[GitStatus] = Field(None, description="Git status")
    relevance_score: float = Field(..., description="Search relevance score")
    highlight_matches: List[str] = Field(default_factory=list, description="Highlighted search matches")


class FilePreview(BaseModel):
    """File preview with content"""
    path: str = Field(..., description="File path")
    content: str = Field(..., description="File content preview")
    content_type: str = Field(..., description="Content type")
    encoding: str = Field(..., description="File encoding")
    language: Optional[str] = Field(None, description="Programming language")
    syntax_highlighted: bool = Field(default=False, description="Whether content is syntax highlighted")
    truncated: bool = Field(default=False, description="Whether content was truncated")
    max_size: int = Field(default=10000, description="Maximum preview size")


class FileMetadata(BaseModel):
    """Detailed file metadata"""
    path: str = Field(..., description="File path")
    name: str = Field(..., description="File name")
    type: FileType = Field(..., description="File type")
    size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(..., description="Creation time")
    modified_at: datetime = Field(..., description="Last modification time")
    accessed_at: datetime = Field(..., description="Last access time")
    permissions: str = Field(..., description="File permissions")
    owner: str = Field(..., description="File owner")
    group: str = Field(..., description="File group")
    mime_type: str = Field(..., description="MIME type")
    extension: Optional[str] = Field(None, description="File extension")
    is_hidden: bool = Field(..., description="Whether file is hidden")
    is_symlink: bool = Field(..., description="Whether file is a symlink")
    symlink_target: Optional[str] = Field(None, description="Symlink target")
    git_status: Optional[GitStatus] = Field(None, description="Git status")
    git_commit: Optional[str] = Field(None, description="Last git commit")
    git_author: Optional[str] = Field(None, description="Last git author")
    checksum: Optional[str] = Field(None, description="File checksum")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")


class FileOperation(str, Enum):
    """File operation types"""
    COPY = "copy"
    MOVE = "move"
    DELETE = "delete"
    RENAME = "rename"
    CREATE_DIRECTORY = "create_directory"
    DUPLICATE = "duplicate"
    COMPRESS = "compress"
    EXTRACT = "extract"


class OperationResult(BaseModel):
    """File operation result"""
    success: bool = Field(..., description="Operation success status")
    operation: FileOperation = Field(..., description="Operation type")
    affected_files: List[str] = Field(default_factory=list, description="Affected file paths")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    operation_id: str = Field(..., description="Unique operation identifier")
    timestamp: datetime = Field(..., description="Operation timestamp")
    user_id: UUID = Field(..., description="User who performed operation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional operation metadata")


# Request/Response Models
class FileTreeResponse(BaseModel):
    """File tree response"""
    project_id: str = Field(..., description="Project identifier")
    path: str = Field(..., description="Current path")
    root_node: FileNode = Field(..., description="Root file node")
    total_files: int = Field(..., description="Total files count")
    total_directories: int = Field(..., description="Total directories count")
    total_size: int = Field(..., description="Total size in bytes")
    last_updated: datetime = Field(..., description="Last update time")


class FileSearchRequest(BaseModel):
    """File search request"""
    query: str = Field(..., description="Search query")
    filters: Optional[FileFilters] = Field(None, description="Search filters")
    limit: int = Field(default=100, description="Maximum results")
    offset: int = Field(default=0, description="Result offset")
    sort_by: str = Field(default="relevance", description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order")


class FileSearchResponse(BaseModel):
    """File search response"""
    project_id: str = Field(..., description="Project identifier")
    query: str = Field(..., description="Search query")
    results: List[FileResult] = Field(..., description="Search results")
    total_count: int = Field(..., description="Total result count")
    has_more: bool = Field(..., description="Whether more results exist")
    search_time_ms: int = Field(..., description="Search execution time")


class FilePreviewRequest(BaseModel):
    """File preview request"""
    file_path: str = Field(..., description="File path")
    max_size: int = Field(default=10000, description="Maximum preview size")
    include_syntax_highlighting: bool = Field(default=True, description="Include syntax highlighting")


class FilePreviewResponse(BaseModel):
    """File preview response"""
    preview: FilePreview = Field(..., description="File preview")
    metadata: FileMetadata = Field(..., description="File metadata")


class FileOperationRequest(BaseModel):
    """File operation request"""
    operation: FileOperation = Field(..., description="Operation type")
    source_paths: List[str] = Field(..., description="Source file paths")
    destination: Optional[str] = Field(None, description="Destination path")
    overwrite: bool = Field(default=False, description="Overwrite existing files")
    create_backup: bool = Field(default=True, description="Create backup before operation")


class FileOperationResponse(BaseModel):
    """File operation response"""
    result: OperationResult = Field(..., description="Operation result")
    affected_files: List[str] = Field(..., description="Affected file paths")
    backup_paths: Optional[List[str]] = Field(None, description="Backup file paths")


class FileMetadataResponse(BaseModel):
    """File metadata response"""
    metadata: FileMetadata = Field(..., description="File metadata")
    git_info: Optional[Dict[str, Any]] = Field(None, description="Git information")
    custom_metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom metadata")


class GitStatusResponse(BaseModel):
    """Git status response"""
    project_id: str = Field(..., description="Project identifier")
    file_statuses: Dict[str, GitStatus] = Field(..., description="File git statuses")
    branch: str = Field(..., description="Current branch")
    last_commit: Optional[str] = Field(None, description="Last commit hash")
    last_commit_message: Optional[str] = Field(None, description="Last commit message")
    last_commit_author: Optional[str] = Field(None, description="Last commit author")
    last_commit_date: Optional[datetime] = Field(None, description="Last commit date")
    has_uncommitted_changes: bool = Field(..., description="Has uncommitted changes")
    has_untracked_files: bool = Field(..., description="Has untracked files")


class FileFiltersRequest(BaseModel):
    """File filters request"""
    filters: FileFilters = Field(..., description="File filters")
    apply_to_tree: bool = Field(default=True, description="Apply filters to file tree")
    apply_to_search: bool = Field(default=True, description="Apply filters to search")


# Update forward references
FileNode.model_rebuild()
