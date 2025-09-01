"""
Integrated Terminal Schemas
Professional terminal system with advanced features
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class TerminalStatus(str, Enum):
    """Terminal session status"""
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"
    KILLED = "killed"


class TerminalType(str, Enum):
    """Terminal type"""
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    POWERSHELL = "powershell"
    CMD = "cmd"
    CUSTOM = "custom"


class CommandStatus(str, Enum):
    """Command execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class OutputType(str, Enum):
    """Terminal output type"""
    STDOUT = "stdout"
    STDERR = "stderr"
    SYSTEM = "system"
    ERROR = "error"
    PROMPT = "prompt"


class TerminalSession(BaseModel):
    """Terminal session information"""
    id: str = Field(..., description="Unique session identifier")
    project_id: UUID = Field(..., description="Project identifier")
    user_id: UUID = Field(..., description="User identifier")
    name: str = Field(..., description="Session name")
    type: TerminalType = Field(..., description="Terminal type")
    status: TerminalStatus = Field(..., description="Session status")
    created_at: datetime = Field(..., description="Creation time")
    last_activity: datetime = Field(..., description="Last activity time")
    working_directory: str = Field(..., description="Current working directory")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    custom_shell: Optional[str] = Field(None, description="Custom shell path")
    theme: str = Field(default="default", description="Terminal theme")
    font_size: int = Field(default=14, description="Font size")
    columns: int = Field(default=80, description="Terminal columns")
    rows: int = Field(default=24, description="Terminal rows")
    is_active: bool = Field(default=True, description="Whether session is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TerminalTab(BaseModel):
    """Terminal tab information"""
    id: str = Field(..., description="Unique tab identifier")
    session_id: str = Field(..., description="Parent session identifier")
    name: str = Field(..., description="Tab name")
    status: TerminalStatus = Field(..., description="Tab status")
    created_at: datetime = Field(..., description="Creation time")
    last_activity: datetime = Field(..., description="Last activity time")
    working_directory: str = Field(..., description="Current working directory")
    is_active: bool = Field(default=True, description="Whether tab is active")
    order: int = Field(default=0, description="Tab order")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TerminalPane(BaseModel):
    """Terminal pane information"""
    id: str = Field(..., description="Unique pane identifier")
    tab_id: str = Field(..., description="Parent tab identifier")
    name: str = Field(..., description="Pane name")
    status: TerminalStatus = Field(..., description="Pane status")
    created_at: datetime = Field(..., description="Creation time")
    last_activity: datetime = Field(..., description="Last activity time")
    working_directory: str = Field(..., description="Current working directory")
    is_active: bool = Field(default=True, description="Whether pane is active")
    split_direction: Optional[str] = Field(None, description="Split direction (horizontal/vertical)")
    size_percentage: float = Field(default=50.0, description="Pane size percentage")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Command(BaseModel):
    """Command information"""
    id: str = Field(..., description="Unique command identifier")
    session_id: str = Field(..., description="Terminal session identifier")
    command: str = Field(..., description="Command string")
    status: CommandStatus = Field(..., description="Command status")
    started_at: datetime = Field(..., description="Start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    exit_code: Optional[int] = Field(None, description="Exit code")
    working_directory: str = Field(..., description="Working directory")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    user_id: UUID = Field(..., description="User who executed command")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CommandOutput(BaseModel):
    """Command output information"""
    id: str = Field(..., description="Unique output identifier")
    command_id: str = Field(..., description="Command identifier")
    output_type: OutputType = Field(..., description="Output type")
    content: str = Field(..., description="Output content")
    timestamp: datetime = Field(..., description="Output timestamp")
    line_number: Optional[int] = Field(None, description="Line number")
    is_error: bool = Field(default=False, description="Whether output is error")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TerminalOutput(BaseModel):
    """Terminal output with formatting"""
    session_id: str = Field(..., description="Terminal session identifier")
    output_type: OutputType = Field(..., description="Output type")
    content: str = Field(..., description="Output content")
    timestamp: datetime = Field(..., description="Output timestamp")
    line_number: Optional[int] = Field(None, description="Line number")
    is_error: bool = Field(default=False, description="Whether output is error")
    color: Optional[str] = Field(None, description="Output color")
    background_color: Optional[str] = Field(None, description="Background color")
    is_bold: bool = Field(default=False, description="Whether text is bold")
    is_italic: bool = Field(default=False, description="Whether text is italic")
    is_underline: bool = Field(default=False, description="Whether text is underlined")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CommandResult(BaseModel):
    """Command execution result"""
    command_id: str = Field(..., description="Command identifier")
    success: bool = Field(..., description="Whether command succeeded")
    exit_code: int = Field(..., description="Exit code")
    stdout: str = Field(default="", description="Standard output")
    stderr: str = Field(default="", description="Standard error")
    execution_time: float = Field(..., description="Execution time in seconds")
    started_at: datetime = Field(..., description="Start time")
    completed_at: datetime = Field(..., description="Completion time")
    working_directory: str = Field(..., description="Working directory")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Suggestion(BaseModel):
    """Command suggestion for auto-completion"""
    suggestion: str = Field(..., description="Suggested command")
    description: Optional[str] = Field(None, description="Command description")
    category: str = Field(default="command", description="Suggestion category")
    relevance_score: float = Field(default=1.0, description="Relevance score")
    usage_count: int = Field(default=0, description="Usage count")
    last_used: Optional[datetime] = Field(None, description="Last usage time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CommandContext(BaseModel):
    """Context for command suggestions"""
    current_command: str = Field(..., description="Current command being typed")
    working_directory: str = Field(..., description="Current working directory")
    recent_commands: List[str] = Field(default_factory=list, description="Recent commands")
    file_context: List[str] = Field(default_factory=list, description="Files in current directory")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TerminalTheme(BaseModel):
    """Terminal theme configuration"""
    name: str = Field(..., description="Theme name")
    description: Optional[str] = Field(None, description="Theme description")
    background_color: str = Field(default="#000000", description="Background color")
    foreground_color: str = Field(default="#FFFFFF", description="Foreground color")
    cursor_color: str = Field(default="#FFFFFF", description="Cursor color")
    selection_color: str = Field(default="#FFFFFF", description="Selection color")
    color_palette: List[str] = Field(default_factory=list, description="Color palette")
    font_family: str = Field(default="monospace", description="Font family")
    font_size: int = Field(default=14, description="Font size")
    line_height: float = Field(default=1.2, description="Line height")
    padding: int = Field(default=10, description="Padding")
    opacity: float = Field(default=1.0, description="Opacity")
    is_default: bool = Field(default=False, description="Whether theme is default")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TerminalSettings(BaseModel):
    """Terminal settings and preferences"""
    user_id: UUID = Field(..., description="User identifier")
    default_shell: TerminalType = Field(default=TerminalType.BASH, description="Default shell")
    default_theme: str = Field(default="default", description="Default theme")
    font_family: str = Field(default="monospace", description="Font family")
    font_size: int = Field(default=14, description="Font size")
    line_height: float = Field(default=1.2, description="Line height")
    columns: int = Field(default=80, description="Default columns")
    rows: int = Field(default=24, description="Default rows")
    enable_auto_completion: bool = Field(default=True, description="Enable auto-completion")
    enable_command_history: bool = Field(default=True, description="Enable command history")
    max_history_size: int = Field(default=1000, description="Maximum history size")
    enable_syntax_highlighting: bool = Field(default=True, description="Enable syntax highlighting")
    enable_bell: bool = Field(default=True, description="Enable terminal bell")
    enable_scrollback: bool = Field(default=True, description="Enable scrollback")
    scrollback_size: int = Field(default=10000, description="Scrollback size")
    enable_right_click_paste: bool = Field(default=True, description="Enable right-click paste")
    enable_copy_on_select: bool = Field(default=True, description="Enable copy on select")
    custom_environment_variables: Dict[str, str] = Field(default_factory=dict, description="Custom environment variables")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class CreateTerminalRequest(BaseModel):
    """Create terminal session request"""
    project_id: UUID = Field(..., description="Project identifier")
    name: Optional[str] = Field(None, description="Session name")
    type: TerminalType = Field(default=TerminalType.BASH, description="Terminal type")
    working_directory: Optional[str] = Field(None, description="Working directory")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    custom_shell: Optional[str] = Field(None, description="Custom shell path")
    theme: str = Field(default="default", description="Terminal theme")
    columns: int = Field(default=80, description="Terminal columns")
    rows: int = Field(default=24, description="Terminal rows")


class CreateTerminalResponse(BaseModel):
    """Create terminal session response"""
    session: TerminalSession = Field(..., description="Created terminal session")
    websocket_url: str = Field(..., description="WebSocket URL for real-time communication")


class ExecuteCommandRequest(BaseModel):
    """Execute command request"""
    command: str = Field(..., description="Command to execute")
    working_directory: Optional[str] = Field(None, description="Working directory")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    timeout: Optional[int] = Field(None, description="Command timeout in seconds")
    capture_output: bool = Field(default=True, description="Whether to capture output")


class ExecuteCommandResponse(BaseModel):
    """Execute command response"""
    command_id: str = Field(..., description="Command identifier")
    status: CommandStatus = Field(..., description="Command status")
    result: Optional[CommandResult] = Field(None, description="Command result")


class GetSuggestionsRequest(BaseModel):
    """Get command suggestions request"""
    partial_command: str = Field(..., description="Partial command")
    context: Optional[CommandContext] = Field(None, description="Command context")
    limit: int = Field(default=10, description="Maximum suggestions")


class GetSuggestionsResponse(BaseModel):
    """Get command suggestions response"""
    suggestions: List[Suggestion] = Field(..., description="Command suggestions")
    total_count: int = Field(..., description="Total suggestion count")


class TerminalInfo(BaseModel):
    """Terminal session information"""
    session: TerminalSession = Field(..., description="Terminal session")
    tabs: List[TerminalTab] = Field(default_factory=list, description="Terminal tabs")
    active_tab: Optional[TerminalTab] = Field(None, description="Active tab")
    recent_commands: List[Command] = Field(default_factory=list, description="Recent commands")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Session statistics")


class ResizeTerminalRequest(BaseModel):
    """Resize terminal request"""
    columns: int = Field(..., description="Terminal columns")
    rows: int = Field(..., description="Terminal rows")


class SendInputRequest(BaseModel):
    """Send input to terminal request"""
    input_data: str = Field(..., description="Input data")
    input_type: str = Field(default="text", description="Input type")


class WebSocketMessage(BaseModel):
    """WebSocket message for terminal communication"""
    type: str = Field(..., description="Message type")
    session_id: str = Field(..., description="Terminal session identifier")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


class TerminalStatistics(BaseModel):
    """Terminal usage statistics"""
    session_id: str = Field(..., description="Terminal session identifier")
    total_commands: int = Field(default=0, description="Total commands executed")
    successful_commands: int = Field(default=0, description="Successful commands")
    failed_commands: int = Field(default=0, description="Failed commands")
    total_execution_time: float = Field(default=0.0, description="Total execution time")
    average_execution_time: float = Field(default=0.0, description="Average execution time")
    most_used_commands: List[Dict[str, Any]] = Field(default_factory=list, description="Most used commands")
    session_duration: float = Field(default=0.0, description="Session duration")
    created_at: datetime = Field(..., description="Statistics creation time")
    updated_at: datetime = Field(..., description="Statistics update time")
