"""
Advanced UI System Schemas
Professional UI system with themes, layouts, shortcuts, and customization
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class ThemeType(str, Enum):
    """Theme types"""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    CUSTOM = "custom"


class ColorScheme(str, Enum):
    """Color scheme types"""
    MONOKAI = "monokai"
    DRACULA = "dracula"
    SOLARIZED = "solarized"
    GITHUB = "github"
    VSCODE = "vscode"
    INTELLIJ = "intellij"
    CUSTOM = "custom"


class LayoutType(str, Enum):
    """Layout types"""
    DEFAULT = "default"
    COMPACT = "compact"
    SPACIOUS = "spacious"
    MINIMAL = "minimal"
    FULLSCREEN = "fullscreen"
    CUSTOM = "custom"


class PanelPosition(str, Enum):
    """Panel positions"""
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"
    CENTER = "center"
    FLOATING = "floating"


class ViewType(str, Enum):
    """View types"""
    EDITOR = "editor"
    TERMINAL = "terminal"
    EXPLORER = "explorer"
    DEBUG = "debug"
    OUTPUT = "output"
    PROBLEMS = "problems"
    SEARCH = "search"
    GIT = "git"
    EXTENSIONS = "extensions"
    SETTINGS = "settings"
    HELP = "help"


class ShortcutCategory(str, Enum):
    """Shortcut categories"""
    FILE = "file"
    EDIT = "edit"
    VIEW = "view"
    NAVIGATION = "navigation"
    SEARCH = "search"
    DEBUG = "debug"
    TERMINAL = "terminal"
    GIT = "git"
    EXTENSIONS = "extensions"
    CUSTOM = "custom"


class FontFamily(str, Enum):
    """Font families"""
    MONACO = "Monaco"
    CONSOLAS = "Consolas"
    COURIER_NEW = "Courier New"
    FIRA_CODE = "Fira Code"
    JETBRAINS_MONO = "JetBrains Mono"
    SOURCE_CODE_PRO = "Source Code Pro"
    CASCADIA_CODE = "Cascadia Code"
    CUSTOM = "custom"


class FontWeight(str, Enum):
    """Font weights"""
    NORMAL = "normal"
    BOLD = "bold"
    LIGHT = "light"
    MEDIUM = "medium"
    SEMIBOLD = "semibold"


class FontStyle(str, Enum):
    """Font styles"""
    NORMAL = "normal"
    ITALIC = "italic"


class CursorStyle(str, Enum):
    """Cursor styles"""
    LINE = "line"
    BLOCK = "block"
    UNDERLINE = "underline"
    BEAM = "beam"


class AnimationType(str, Enum):
    """Animation types"""
    NONE = "none"
    SMOOTH = "smooth"
    FAST = "fast"
    CUSTOM = "custom"


class Theme(BaseModel):
    """Theme configuration"""
    id: str = Field(..., description="Theme identifier")
    name: str = Field(..., description="Theme name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Theme description")
    type: ThemeType = Field(..., description="Theme type")
    color_scheme: ColorScheme = Field(..., description="Color scheme")
    author: str = Field(..., description="Theme author")
    version: str = Field(..., description="Theme version")
    is_default: bool = Field(default=False, description="Whether theme is default")
    is_custom: bool = Field(default=False, description="Whether theme is custom")
    colors: Dict[str, str] = Field(default_factory=dict, description="Color definitions")
    token_colors: List[Dict[str, Any]] = Field(default_factory=list, description="Token colors")
    semantic_token_colors: Dict[str, Any] = Field(default_factory=dict, description="Semantic token colors")
    ui_colors: Dict[str, str] = Field(default_factory=dict, description="UI colors")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Layout(BaseModel):
    """Layout configuration"""
    id: str = Field(..., description="Layout identifier")
    name: str = Field(..., description="Layout name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Layout description")
    type: LayoutType = Field(..., description="Layout type")
    is_default: bool = Field(default=False, description="Whether layout is default")
    is_custom: bool = Field(default=False, description="Whether layout is custom")
    panels: List[Dict[str, Any]] = Field(default_factory=list, description="Panel configurations")
    views: List[Dict[str, Any]] = Field(default_factory=list, description="View configurations")
    splits: List[Dict[str, Any]] = Field(default_factory=list, description="Split configurations")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Panel(BaseModel):
    """Panel configuration"""
    id: str = Field(..., description="Panel identifier")
    name: str = Field(..., description="Panel name")
    type: ViewType = Field(..., description="Panel type")
    position: PanelPosition = Field(..., description="Panel position")
    size: int = Field(..., description="Panel size")
    is_visible: bool = Field(default=True, description="Whether panel is visible")
    is_resizable: bool = Field(default=True, description="Whether panel is resizable")
    is_draggable: bool = Field(default=True, description="Whether panel is draggable")
    is_collapsible: bool = Field(default=True, description="Whether panel is collapsible")
    is_pinned: bool = Field(default=False, description="Whether panel is pinned")
    order: int = Field(default=0, description="Panel order")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Panel settings")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class View(BaseModel):
    """View configuration"""
    id: str = Field(..., description="View identifier")
    name: str = Field(..., description="View name")
    type: ViewType = Field(..., description="View type")
    panel_id: str = Field(..., description="Parent panel identifier")
    is_active: bool = Field(default=False, description="Whether view is active")
    is_visible: bool = Field(default=True, description="Whether view is visible")
    is_pinned: bool = Field(default=False, description="Whether view is pinned")
    order: int = Field(default=0, description="View order")
    settings: Dict[str, Any] = Field(default_factory=dict, description="View settings")
    data: Dict[str, Any] = Field(default_factory=dict, description="View data")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Split(BaseModel):
    """Split configuration"""
    id: str = Field(..., description="Split identifier")
    name: str = Field(..., description="Split name")
    direction: str = Field(..., description="Split direction (horizontal/vertical)")
    size: float = Field(..., description="Split size ratio")
    is_resizable: bool = Field(default=True, description="Whether split is resizable")
    children: List[str] = Field(default_factory=list, description="Child split/panel IDs")
    parent_id: Optional[str] = Field(None, description="Parent split identifier")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Shortcut(BaseModel):
    """Keyboard shortcut configuration"""
    id: str = Field(..., description="Shortcut identifier")
    name: str = Field(..., description="Shortcut name")
    description: str = Field(..., description="Shortcut description")
    category: ShortcutCategory = Field(..., description="Shortcut category")
    key: str = Field(..., description="Key combination")
    command: str = Field(..., description="Command to execute")
    context: Optional[str] = Field(None, description="Context where shortcut is active")
    is_enabled: bool = Field(default=True, description="Whether shortcut is enabled")
    is_global: bool = Field(default=False, description="Whether shortcut is global")
    is_custom: bool = Field(default=False, description="Whether shortcut is custom")
    order: int = Field(default=0, description="Shortcut order")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class FontSettings(BaseModel):
    """Font settings configuration"""
    family: FontFamily = Field(default=FontFamily.JETBRAINS_MONO, description="Font family")
    size: int = Field(default=14, ge=8, le=72, description="Font size")
    weight: FontWeight = Field(default=FontWeight.NORMAL, description="Font weight")
    style: FontStyle = Field(default=FontStyle.NORMAL, description="Font style")
    line_height: float = Field(default=1.4, ge=0.5, le=3.0, description="Line height")
    letter_spacing: float = Field(default=0.0, ge=-2.0, le=5.0, description="Letter spacing")
    ligatures: bool = Field(default=True, description="Whether ligatures are enabled")
    custom_font_path: Optional[str] = Field(None, description="Custom font file path")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class EditorSettings(BaseModel):
    """Editor settings configuration"""
    tab_size: int = Field(default=4, ge=1, le=8, description="Tab size")
    insert_spaces: bool = Field(default=True, description="Whether to insert spaces instead of tabs")
    word_wrap: bool = Field(default=False, description="Whether to enable word wrap")
    line_numbers: bool = Field(default=True, description="Whether to show line numbers")
    minimap: bool = Field(default=True, description="Whether to show minimap")
    scroll_beyond_last_line: bool = Field(default=False, description="Whether to scroll beyond last line")
    smooth_scrolling: bool = Field(default=True, description="Whether to enable smooth scrolling")
    cursor_style: CursorStyle = Field(default=CursorStyle.LINE, description="Cursor style")
    cursor_blinking: bool = Field(default=True, description="Whether cursor blinks")
    cursor_width: int = Field(default=2, ge=1, le=10, description="Cursor width")
    bracket_pair_colorization: bool = Field(default=True, description="Whether to colorize bracket pairs")
    guides: Dict[str, bool] = Field(default_factory=dict, description="Editor guides")
    rulers: List[int] = Field(default_factory=list, description="Editor rulers")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AnimationSettings(BaseModel):
    """Animation settings configuration"""
    type: AnimationType = Field(default=AnimationType.SMOOTH, description="Animation type")
    duration: float = Field(default=0.3, ge=0.0, le=2.0, description="Animation duration")
    easing: str = Field(default="ease-in-out", description="Animation easing")
    enabled: bool = Field(default=True, description="Whether animations are enabled")
    reduced_motion: bool = Field(default=False, description="Whether to respect reduced motion preference")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class UISettings(BaseModel):
    """Complete UI settings configuration"""
    id: str = Field(..., description="Settings identifier")
    user_id: UUID = Field(..., description="User identifier")
    theme_id: str = Field(..., description="Active theme identifier")
    layout_id: str = Field(..., description="Active layout identifier")
    font_settings: FontSettings = Field(..., description="Font settings")
    editor_settings: EditorSettings = Field(..., description="Editor settings")
    animation_settings: AnimationSettings = Field(..., description="Animation settings")
    panels: List[Panel] = Field(default_factory=list, description="Panel configurations")
    views: List[View] = Field(default_factory=list, description="View configurations")
    splits: List[Split] = Field(default_factory=list, description="Split configurations")
    shortcuts: List[Shortcut] = Field(default_factory=list, description="Keyboard shortcuts")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    custom_js: Optional[str] = Field(None, description="Custom JavaScript")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: datetime = Field(..., description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ColorPalette(BaseModel):
    """Color palette configuration"""
    id: str = Field(..., description="Palette identifier")
    name: str = Field(..., description="Palette name")
    description: str = Field(..., description="Palette description")
    colors: Dict[str, str] = Field(..., description="Color definitions")
    is_custom: bool = Field(default=False, description="Whether palette is custom")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class IconTheme(BaseModel):
    """Icon theme configuration"""
    id: str = Field(..., description="Icon theme identifier")
    name: str = Field(..., description="Icon theme name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Icon theme description")
    is_default: bool = Field(default=False, description="Whether icon theme is default")
    is_custom: bool = Field(default=False, description="Whether icon theme is custom")
    icons: Dict[str, str] = Field(default_factory=dict, description="Icon definitions")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AccessibilitySettings(BaseModel):
    """Accessibility settings configuration"""
    high_contrast: bool = Field(default=False, description="Whether to enable high contrast")
    reduced_motion: bool = Field(default=False, description="Whether to respect reduced motion")
    screen_reader_support: bool = Field(default=True, description="Whether to enable screen reader support")
    keyboard_navigation: bool = Field(default=True, description="Whether to enable keyboard navigation")
    focus_indicators: bool = Field(default=True, description="Whether to show focus indicators")
    color_blind_support: bool = Field(default=False, description="Whether to enable color blind support")
    font_scaling: float = Field(default=1.0, ge=0.5, le=3.0, description="Font scaling factor")
    created_at: datetime = Field(..., description="Creation time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class ApplyThemeRequest(BaseModel):
    """Apply theme request"""
    theme_id: str = Field(..., description="Theme identifier")
    preview: bool = Field(default=False, description="Whether to preview theme")


class ApplyThemeResponse(BaseModel):
    """Apply theme response"""
    theme: Theme = Field(..., description="Applied theme")
    success: bool = Field(..., description="Whether theme was applied successfully")
    message: str = Field(..., description="Application message")


class CreateThemeRequest(BaseModel):
    """Create theme request"""
    name: str = Field(..., description="Theme name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Theme description")
    type: ThemeType = Field(..., description="Theme type")
    color_scheme: ColorScheme = Field(..., description="Color scheme")
    colors: Dict[str, str] = Field(default_factory=dict, description="Color definitions")
    token_colors: List[Dict[str, Any]] = Field(default_factory=list, description="Token colors")
    semantic_token_colors: Dict[str, Any] = Field(default_factory=dict, description="Semantic token colors")
    ui_colors: Dict[str, str] = Field(default_factory=dict, description="UI colors")


class CreateThemeResponse(BaseModel):
    """Create theme response"""
    theme: Theme = Field(..., description="Created theme")
    success: bool = Field(..., description="Whether theme was created successfully")
    message: str = Field(..., description="Creation message")


class ApplyLayoutRequest(BaseModel):
    """Apply layout request"""
    layout_id: str = Field(..., description="Layout identifier")
    preview: bool = Field(default=False, description="Whether to preview layout")


class ApplyLayoutResponse(BaseModel):
    """Apply layout response"""
    layout: Layout = Field(..., description="Applied layout")
    success: bool = Field(..., description="Whether layout was applied successfully")
    message: str = Field(..., description="Application message")


class CreateLayoutRequest(BaseModel):
    """Create layout request"""
    name: str = Field(..., description="Layout name")
    display_name: str = Field(..., description="Display name")
    description: str = Field(..., description="Layout description")
    type: LayoutType = Field(..., description="Layout type")
    panels: List[Dict[str, Any]] = Field(default_factory=list, description="Panel configurations")
    views: List[Dict[str, Any]] = Field(default_factory=list, description="View configurations")
    splits: List[Dict[str, Any]] = Field(default_factory=list, description="Split configurations")


class CreateLayoutResponse(BaseModel):
    """Create layout response"""
    layout: Layout = Field(..., description="Created layout")
    success: bool = Field(..., description="Whether layout was created successfully")
    message: str = Field(..., description="Creation message")


class UpdateUISettingsRequest(BaseModel):
    """Update UI settings request"""
    theme_id: Optional[str] = Field(None, description="Theme identifier")
    layout_id: Optional[str] = Field(None, description="Layout identifier")
    font_settings: Optional[FontSettings] = Field(None, description="Font settings")
    editor_settings: Optional[EditorSettings] = Field(None, description="Editor settings")
    animation_settings: Optional[AnimationSettings] = Field(None, description="Animation settings")
    panels: Optional[List[Panel]] = Field(None, description="Panel configurations")
    views: Optional[List[View]] = Field(None, description="View configurations")
    splits: Optional[List[Split]] = Field(None, description="Split configurations")
    shortcuts: Optional[List[Shortcut]] = Field(None, description="Keyboard shortcuts")
    custom_css: Optional[str] = Field(None, description="Custom CSS")
    custom_js: Optional[str] = Field(None, description="Custom JavaScript")


class UpdateUISettingsResponse(BaseModel):
    """Update UI settings response"""
    settings: UISettings = Field(..., description="Updated settings")
    success: bool = Field(..., description="Whether settings were updated successfully")
    message: str = Field(..., description="Update message")


class AddShortcutRequest(BaseModel):
    """Add shortcut request"""
    name: str = Field(..., description="Shortcut name")
    description: str = Field(..., description="Shortcut description")
    category: ShortcutCategory = Field(..., description="Shortcut category")
    key: str = Field(..., description="Key combination")
    command: str = Field(..., description="Command to execute")
    context: Optional[str] = Field(None, description="Context where shortcut is active")
    is_global: bool = Field(default=False, description="Whether shortcut is global")


class AddShortcutResponse(BaseModel):
    """Add shortcut response"""
    shortcut: Shortcut = Field(..., description="Added shortcut")
    success: bool = Field(..., description="Whether shortcut was added successfully")
    message: str = Field(..., description="Addition message")


class UIPreview(BaseModel):
    """UI preview information"""
    theme: Theme = Field(..., description="Preview theme")
    layout: Layout = Field(..., description="Preview layout")
    font_settings: FontSettings = Field(..., description="Preview font settings")
    editor_settings: EditorSettings = Field(..., description="Preview editor settings")
    animation_settings: AnimationSettings = Field(..., description="Preview animation settings")
    preview_url: str = Field(..., description="Preview URL")
    expires_at: datetime = Field(..., description="Preview expiration time")


class UIStatistics(BaseModel):
    """UI statistics information"""
    total_themes: int = Field(..., description="Total number of themes")
    total_layouts: int = Field(..., description="Total number of layouts")
    total_shortcuts: int = Field(..., description="Total number of shortcuts")
    active_theme: str = Field(..., description="Active theme name")
    active_layout: str = Field(..., description="Active layout name")
    custom_themes: int = Field(..., description="Number of custom themes")
    custom_layouts: int = Field(..., description="Number of custom layouts")
    custom_shortcuts: int = Field(..., description="Number of custom shortcuts")
    created_at: datetime = Field(..., description="Statistics creation time")
