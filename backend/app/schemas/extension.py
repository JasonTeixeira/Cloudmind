"""
Advanced Extension System Schemas
Professional extension system with plugin architecture, marketplace, and security sandboxing
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class ExtensionStatus(str, Enum):
    """Extension status"""
    INSTALLING = "installing"
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    UPDATING = "updating"
    ERROR = "error"
    UNINSTALLING = "uninstalling"
    UNINSTALLED = "uninstalled"


class ExtensionType(str, Enum):
    """Extension types"""
    LANGUAGE = "language"
    THEME = "theme"
    SNIPPET = "snippet"
    LINTER = "linter"
    FORMATTER = "formatter"
    DEBUGGER = "debugger"
    PROFILER = "profiler"
    GIT = "git"
    DATABASE = "database"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    UTILITY = "utility"
    CUSTOM = "custom"


class ExtensionCategory(str, Enum):
    """Extension categories"""
    PROGRAMMING_LANGUAGES = "programming_languages"
    THEMES = "themes"
    SNIPPETS = "snippets"
    LINTING_FORMATTING = "linting_formatting"
    DEBUGGING = "debugging"
    TESTING = "testing"
    VERSION_CONTROL = "version_control"
    DATABASES = "databases"
    DEPLOYMENT = "deployment"
    DOCUMENTATION = "documentation"
    PRODUCTIVITY = "productivity"
    OTHER = "other"


class ExtensionPermission(str, Enum):
    """Extension permissions"""
    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    EXECUTE_COMMANDS = "execute_commands"
    ACCESS_TERMINAL = "access_terminal"
    ACCESS_DEBUGGER = "access_debugger"
    ACCESS_PROFILER = "access_profiler"
    ACCESS_DATABASE = "access_database"
    ACCESS_NETWORK = "access_network"
    ACCESS_SYSTEM = "access_system"
    MODIFY_UI = "modify_ui"
    SEND_NOTIFICATIONS = "send_notifications"
    READ_USER_DATA = "read_user_data"
    WRITE_USER_DATA = "write_user_data"


class ExtensionCompatibility(str, Enum):
    """Extension compatibility levels"""
    COMPATIBLE = "compatible"
    PARTIALLY_COMPATIBLE = "partially_compatible"
    INCOMPATIBLE = "incompatible"
    UNKNOWN = "unknown"


class ExtensionRating(str, Enum):
    """Extension rating levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    POOR = "poor"
    UNRATED = "unrated"


class Extension(BaseModel):
    """Extension information"""
    id: str = Field(..., description="Unique extension identifier")
    name: str = Field(..., description="Extension name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Extension description")
    version: str = Field(..., description="Extension version")
    author: str = Field(..., description="Extension author")
    publisher: str = Field(..., description="Extension publisher")
    type: ExtensionType = Field(..., description="Extension type")
    category: ExtensionCategory = Field(..., description="Extension category")
    status: ExtensionStatus = Field(..., description="Extension status")
    installed_at: Optional[datetime] = Field(None, description="Installation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    enabled_at: Optional[datetime] = Field(None, description="Last enabled time")
    icon_url: Optional[str] = Field(None, description="Extension icon URL")
    repository_url: Optional[str] = Field(None, description="Repository URL")
    homepage_url: Optional[str] = Field(None, description="Homepage URL")
    license: Optional[str] = Field(None, description="License information")
    tags: List[str] = Field(default_factory=list, description="Extension tags")
    permissions: List[ExtensionPermission] = Field(default_factory=list, description="Required permissions")
    dependencies: List[str] = Field(default_factory=list, description="Extension dependencies")
    conflicts: List[str] = Field(default_factory=list, description="Conflicting extensions")
    compatibility: ExtensionCompatibility = Field(default=ExtensionCompatibility.UNKNOWN, description="Compatibility status")
    rating: ExtensionRating = Field(default=ExtensionRating.UNRATED, description="Extension rating")
    download_count: int = Field(default=0, description="Download count")
    review_count: int = Field(default=0, description="Review count")
    average_rating: float = Field(default=0.0, description="Average rating")
    size: int = Field(default=0, description="Extension size in bytes")
    is_preview: bool = Field(default=False, description="Whether extension is in preview")
    is_verified: bool = Field(default=False, description="Whether extension is verified")
    is_featured: bool = Field(default=False, description="Whether extension is featured")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionManifest(BaseModel):
    """Extension manifest information"""
    id: str = Field(..., description="Extension identifier")
    name: str = Field(..., description="Extension name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Extension description")
    version: str = Field(..., description="Extension version")
    author: str = Field(..., description="Extension author")
    publisher: str = Field(..., description="Extension publisher")
    type: ExtensionType = Field(..., description="Extension type")
    category: ExtensionCategory = Field(..., description="Extension category")
    main: str = Field(..., description="Main entry point")
    activation_events: List[str] = Field(default_factory=list, description="Activation events")
    contributes: Dict[str, Any] = Field(default_factory=dict, description="Contribution points")
    permissions: List[ExtensionPermission] = Field(default_factory=list, description="Required permissions")
    dependencies: List[str] = Field(default_factory=list, description="Extension dependencies")
    conflicts: List[str] = Field(default_factory=list, description="Conflicting extensions")
    engines: Dict[str, str] = Field(default_factory=dict, description="Engine requirements")
    scripts: Dict[str, str] = Field(default_factory=dict, description="Script definitions")
    commands: List[Dict[str, Any]] = Field(default_factory=list, description="Command definitions")
    keybindings: List[Dict[str, Any]] = Field(default_factory=list, description="Keybinding definitions")
    menus: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="Menu definitions")
    views: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict, description="View definitions")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Configuration schema")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionInstallation(BaseModel):
    """Extension installation information"""
    id: str = Field(..., description="Installation identifier")
    extension_id: str = Field(..., description="Extension identifier")
    user_id: UUID = Field(..., description="User identifier")
    project_id: Optional[UUID] = Field(None, description="Project identifier")
    status: ExtensionStatus = Field(..., description="Installation status")
    installed_at: datetime = Field(..., description="Installation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    enabled_at: Optional[datetime] = Field(None, description="Last enabled time")
    disabled_at: Optional[datetime] = Field(None, description="Last disabled time")
    installation_path: str = Field(..., description="Installation path")
    version: str = Field(..., description="Installed version")
    is_enabled: bool = Field(default=True, description="Whether extension is enabled")
    is_auto_update: bool = Field(default=True, description="Whether auto-update is enabled")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Extension settings")
    permissions_granted: List[ExtensionPermission] = Field(default_factory=list, description="Granted permissions")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionMarketplace(BaseModel):
    """Extension marketplace information"""
    id: str = Field(..., description="Marketplace identifier")
    name: str = Field(..., description="Marketplace name")
    description: str = Field(..., description="Marketplace description")
    url: str = Field(..., description="Marketplace URL")
    api_url: str = Field(..., description="API URL")
    is_official: bool = Field(default=False, description="Whether marketplace is official")
    is_enabled: bool = Field(default=True, description="Whether marketplace is enabled")
    extension_count: int = Field(default=0, description="Number of extensions")
    last_sync: Optional[datetime] = Field(None, description="Last sync time")
    sync_interval: int = Field(default=3600, description="Sync interval in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionReview(BaseModel):
    """Extension review information"""
    id: str = Field(..., description="Review identifier")
    extension_id: str = Field(..., description="Extension identifier")
    user_id: UUID = Field(..., description="User identifier")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5)")
    title: str = Field(..., description="Review title")
    content: str = Field(..., description="Review content")
    created_at: datetime = Field(..., description="Review creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    is_verified: bool = Field(default=False, description="Whether review is verified")
    helpful_count: int = Field(default=0, description="Helpful votes count")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionUpdate(BaseModel):
    """Extension update information"""
    id: str = Field(..., description="Update identifier")
    extension_id: str = Field(..., description="Extension identifier")
    current_version: str = Field(..., description="Current version")
    new_version: str = Field(..., description="New version")
    release_notes: str = Field(..., description="Release notes")
    download_url: str = Field(..., description="Download URL")
    size: int = Field(..., description="Update size in bytes")
    is_major: bool = Field(default=False, description="Whether update is major")
    is_security: bool = Field(default=False, description="Whether update is security-related")
    is_breaking: bool = Field(default=False, description="Whether update is breaking")
    published_at: datetime = Field(..., description="Publication time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionSandbox(BaseModel):
    """Extension sandbox information"""
    id: str = Field(..., description="Sandbox identifier")
    extension_id: str = Field(..., description="Extension identifier")
    user_id: UUID = Field(..., description="User identifier")
    is_enabled: bool = Field(default=True, description="Whether sandbox is enabled")
    permissions: List[ExtensionPermission] = Field(default_factory=list, description="Allowed permissions")
    restricted_apis: List[str] = Field(default_factory=list, description="Restricted APIs")
    memory_limit: int = Field(default=100 * 1024 * 1024, description="Memory limit in bytes")
    cpu_limit: float = Field(default=1.0, description="CPU limit (cores)")
    network_access: bool = Field(default=False, description="Whether network access is allowed")
    file_access: bool = Field(default=False, description="Whether file access is allowed")
    system_access: bool = Field(default=False, description="Whether system access is allowed")
    created_at: datetime = Field(..., description="Sandbox creation time")
    updated_at: datetime = Field(..., description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionHook(BaseModel):
    """Extension hook information"""
    id: str = Field(..., description="Hook identifier")
    extension_id: str = Field(..., description="Extension identifier")
    hook_type: str = Field(..., description="Hook type")
    hook_name: str = Field(..., description="Hook name")
    callback: str = Field(..., description="Callback function")
    priority: int = Field(default=0, description="Hook priority")
    is_enabled: bool = Field(default=True, description="Whether hook is enabled")
    created_at: datetime = Field(..., description="Hook creation time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionCommand(BaseModel):
    """Extension command information"""
    id: str = Field(..., description="Command identifier")
    extension_id: str = Field(..., description="Extension identifier")
    command: str = Field(..., description="Command name")
    title: str = Field(..., description="Command title")
    description: str = Field(..., description="Command description")
    category: str = Field(..., description="Command category")
    icon: Optional[str] = Field(None, description="Command icon")
    keybinding: Optional[str] = Field(None, description="Keybinding")
    is_enabled: bool = Field(default=True, description="Whether command is enabled")
    created_at: datetime = Field(..., description="Command creation time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExtensionAPI(BaseModel):
    """Extension API information"""
    id: str = Field(..., description="API identifier")
    extension_id: str = Field(..., description="Extension identifier")
    api_name: str = Field(..., description="API name")
    api_version: str = Field(..., description="API version")
    endpoints: List[Dict[str, Any]] = Field(default_factory=list, description="API endpoints")
    authentication: Dict[str, Any] = Field(default_factory=dict, description="Authentication configuration")
    rate_limiting: Dict[str, Any] = Field(default_factory=dict, description="Rate limiting configuration")
    is_enabled: bool = Field(default=True, description="Whether API is enabled")
    created_at: datetime = Field(..., description="API creation time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class InstallExtensionRequest(BaseModel):
    """Install extension request"""
    extension_id: str = Field(..., description="Extension identifier")
    version: Optional[str] = Field(None, description="Specific version to install")
    auto_enable: bool = Field(default=True, description="Whether to enable after installation")
    grant_permissions: List[ExtensionPermission] = Field(default_factory=list, description="Permissions to grant")


class InstallExtensionResponse(BaseModel):
    """Install extension response"""
    installation: ExtensionInstallation = Field(..., description="Installation information")
    success: bool = Field(..., description="Whether installation was successful")
    message: str = Field(..., description="Installation message")


class UpdateExtensionRequest(BaseModel):
    """Update extension request"""
    extension_id: str = Field(..., description="Extension identifier")
    version: Optional[str] = Field(None, description="Specific version to update to")
    backup_settings: bool = Field(default=True, description="Whether to backup settings")


class UpdateExtensionResponse(BaseModel):
    """Update extension response"""
    installation: ExtensionInstallation = Field(..., description="Updated installation")
    success: bool = Field(..., description="Whether update was successful")
    message: str = Field(..., description="Update message")


class UninstallExtensionRequest(BaseModel):
    """Uninstall extension request"""
    extension_id: str = Field(..., description="Extension identifier")
    remove_settings: bool = Field(default=False, description="Whether to remove settings")
    remove_data: bool = Field(default=False, description="Whether to remove data")


class UninstallExtensionResponse(BaseModel):
    """Uninstall extension response"""
    success: bool = Field(..., description="Whether uninstallation was successful")
    message: str = Field(..., description="Uninstallation message")


class EnableExtensionRequest(BaseModel):
    """Enable extension request"""
    extension_id: str = Field(..., description="Extension identifier")
    enable_dependencies: bool = Field(default=True, description="Whether to enable dependencies")


class EnableExtensionResponse(BaseModel):
    """Enable extension response"""
    installation: ExtensionInstallation = Field(..., description="Updated installation")
    success: bool = Field(..., description="Whether enable was successful")
    message: str = Field(..., description="Enable message")


class DisableExtensionRequest(BaseModel):
    """Disable extension request"""
    extension_id: str = Field(..., description="Extension identifier")
    disable_dependents: bool = Field(default=False, description="Whether to disable dependents")


class DisableExtensionResponse(BaseModel):
    """Disable extension response"""
    installation: ExtensionInstallation = Field(..., description="Updated installation")
    success: bool = Field(..., description="Whether disable was successful")
    message: str = Field(..., description="Disable message")


class SearchExtensionsRequest(BaseModel):
    """Search extensions request"""
    query: str = Field(..., description="Search query")
    category: Optional[ExtensionCategory] = Field(None, description="Category filter")
    type: Optional[ExtensionType] = Field(None, description="Type filter")
    rating: Optional[ExtensionRating] = Field(None, description="Rating filter")
    is_verified: Optional[bool] = Field(None, description="Verified filter")
    is_featured: Optional[bool] = Field(None, description="Featured filter")
    sort_by: str = Field(default="relevance", description="Sort field")
    sort_order: str = Field(default="desc", description="Sort order")
    page: int = Field(default=1, description="Page number")
    page_size: int = Field(default=20, description="Page size")


class SearchExtensionsResponse(BaseModel):
    """Search extensions response"""
    extensions: List[Extension] = Field(..., description="Found extensions")
    total_count: int = Field(..., description="Total count")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")
    has_more: bool = Field(..., description="Whether more results exist")


class ExtensionDetails(BaseModel):
    """Extension details information"""
    extension: Extension = Field(..., description="Extension information")
    installation: Optional[ExtensionInstallation] = Field(None, description="Installation information")
    reviews: List[ExtensionReview] = Field(default_factory=list, description="Extension reviews")
    updates: List[ExtensionUpdate] = Field(default_factory=list, description="Available updates")
    sandbox: Optional[ExtensionSandbox] = Field(None, description="Sandbox configuration")
    hooks: List[ExtensionHook] = Field(default_factory=list, description="Extension hooks")
    commands: List[ExtensionCommand] = Field(default_factory=list, description="Extension commands")
    api: Optional[ExtensionAPI] = Field(None, description="Extension API")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Extension statistics")


class ExtensionMarketplaceInfo(BaseModel):
    """Extension marketplace information"""
    marketplace: ExtensionMarketplace = Field(..., description="Marketplace information")
    extensions: List[Extension] = Field(default_factory=list, description="Featured extensions")
    categories: List[ExtensionCategory] = Field(default_factory=list, description="Available categories")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Marketplace statistics")


class ExtensionDevelopmentInfo(BaseModel):
    """Extension development information"""
    extension_id: str = Field(..., description="Extension identifier")
    development_mode: bool = Field(default=False, description="Whether in development mode")
    hot_reload: bool = Field(default=True, description="Whether hot reload is enabled")
    debug_mode: bool = Field(default=False, description="Whether debug mode is enabled")
    log_level: str = Field(default="info", description="Log level")
    development_path: str = Field(..., description="Development path")
    build_output: str = Field(..., description="Build output path")
    watch_patterns: List[str] = Field(default_factory=list, description="Watch patterns")
    build_scripts: Dict[str, str] = Field(default_factory=dict, description="Build scripts")
    test_scripts: Dict[str, str] = Field(default_factory=dict, description="Test scripts")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
