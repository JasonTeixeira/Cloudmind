"""
Advanced Debugging System Schemas
Professional debugging with breakpoint management, variable inspection, and performance profiling
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, validator
from enum import Enum


class DebuggerStatus(str, Enum):
    """Debugger session status"""
    INITIALIZING = "initializing"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STEPPING = "stepping"
    BREAKPOINT_HIT = "breakpoint_hit"
    ERROR = "error"
    TERMINATED = "terminated"


class BreakpointType(str, Enum):
    """Breakpoint types"""
    LINE = "line"
    CONDITIONAL = "conditional"
    LOG = "log"
    EXCEPTION = "exception"
    FUNCTION = "function"
    WATCHPOINT = "watchpoint"


class BreakpointStatus(str, Enum):
    """Breakpoint status"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    PENDING = "pending"
    RESOLVED = "resolved"
    ERROR = "error"


class StepType(str, Enum):
    """Step types for debugging"""
    OVER = "over"
    INTO = "into"
    OUT = "out"
    CONTINUE = "continue"
    PAUSE = "pause"
    RESTART = "restart"


class VariableScope(str, Enum):
    """Variable scope types"""
    LOCAL = "local"
    GLOBAL = "global"
    BUILTIN = "builtin"
    CLASS = "class"
    INSTANCE = "instance"
    MODULE = "module"


class VariableType(str, Enum):
    """Variable type categories"""
    PRIMITIVE = "primitive"
    COMPLEX = "complex"
    COLLECTION = "collection"
    OBJECT = "object"
    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    UNKNOWN = "unknown"


class ProfilerType(str, Enum):
    """Profiler types"""
    CPU = "cpu"
    MEMORY = "memory"
    CALL_GRAPH = "call_graph"
    LINE_PROFILER = "line_profiler"
    MEMORY_PROFILER = "memory_profiler"


class DebugSession(BaseModel):
    """Debug session information"""
    id: str = Field(..., description="Unique session identifier")
    project_id: UUID = Field(..., description="Project identifier")
    user_id: UUID = Field(..., description="User identifier")
    name: str = Field(..., description="Session name")
    status: DebuggerStatus = Field(..., description="Debugger status")
    created_at: datetime = Field(..., description="Creation time")
    last_activity: datetime = Field(..., description="Last activity time")
    target_file: str = Field(..., description="Target file to debug")
    working_directory: str = Field(..., description="Working directory")
    language: str = Field(..., description="Programming language")
    debugger_type: str = Field(..., description="Debugger type (pdb, gdb, etc.)")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    command_line_args: List[str] = Field(default_factory=list, description="Command line arguments")
    is_active: bool = Field(default=True, description="Whether session is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Breakpoint(BaseModel):
    """Breakpoint information"""
    id: str = Field(..., description="Unique breakpoint identifier")
    session_id: str = Field(..., description="Debug session identifier")
    type: BreakpointType = Field(..., description="Breakpoint type")
    status: BreakpointStatus = Field(..., description="Breakpoint status")
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., description="Line number")
    column: Optional[int] = Field(None, description="Column number")
    condition: Optional[str] = Field(None, description="Conditional expression")
    hit_count: int = Field(default=0, description="Number of times hit")
    last_hit: Optional[datetime] = Field(None, description="Last hit time")
    enabled: bool = Field(default=True, description="Whether breakpoint is enabled")
    ignore_count: int = Field(default=0, description="Number of hits to ignore")
    log_message: Optional[str] = Field(None, description="Log message for log breakpoints")
    function_name: Optional[str] = Field(None, description="Function name for function breakpoints")
    exception_type: Optional[str] = Field(None, description="Exception type for exception breakpoints")
    variable_name: Optional[str] = Field(None, description="Variable name for watchpoints")
    created_at: datetime = Field(..., description="Creation time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Variable(BaseModel):
    """Variable information"""
    id: str = Field(..., description="Unique variable identifier")
    session_id: str = Field(..., description="Debug session identifier")
    name: str = Field(..., description="Variable name")
    value: str = Field(..., description="Variable value as string")
    type: str = Field(..., description="Variable type")
    type_category: VariableType = Field(..., description="Type category")
    scope: VariableScope = Field(..., description="Variable scope")
    line_number: Optional[int] = Field(None, description="Line where variable is defined")
    is_constant: bool = Field(default=False, description="Whether variable is constant")
    is_modified: bool = Field(default=False, description="Whether variable was modified")
    size: Optional[int] = Field(None, description="Variable size in bytes")
    reference_count: Optional[int] = Field(None, description="Reference count")
    children: List['Variable'] = Field(default_factory=list, description="Child variables")
    has_children: bool = Field(default=False, description="Whether variable has children")
    is_expanded: bool = Field(default=False, description="Whether variable is expanded in UI")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class StackFrame(BaseModel):
    """Stack frame information"""
    id: str = Field(..., description="Unique frame identifier")
    session_id: str = Field(..., description="Debug session identifier")
    level: int = Field(..., description="Stack frame level")
    function_name: str = Field(..., description="Function name")
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., description="Line number")
    column: Optional[int] = Field(None, description="Column number")
    is_current: bool = Field(default=False, description="Whether this is the current frame")
    variables: List[Variable] = Field(default_factory=list, description="Local variables")
    arguments: List[Variable] = Field(default_factory=list, description="Function arguments")
    return_value: Optional[Variable] = Field(None, description="Return value")
    exception_info: Optional[Dict[str, Any]] = Field(None, description="Exception information")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class WatchExpression(BaseModel):
    """Watch expression information"""
    id: str = Field(..., description="Unique watch expression identifier")
    session_id: str = Field(..., description="Debug session identifier")
    expression: str = Field(..., description="Expression to watch")
    name: str = Field(..., description="Display name")
    value: Optional[str] = Field(None, description="Current value")
    type: Optional[str] = Field(None, description="Value type")
    is_valid: bool = Field(default=True, description="Whether expression is valid")
    error_message: Optional[str] = Field(None, description="Error message if invalid")
    is_enabled: bool = Field(default=True, description="Whether watch is enabled")
    created_at: datetime = Field(..., description="Creation time")
    last_updated: datetime = Field(..., description="Last update time")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DebugState(BaseModel):
    """Current debug state"""
    session_id: str = Field(..., description="Debug session identifier")
    status: DebuggerStatus = Field(..., description="Current status")
    current_frame: Optional[StackFrame] = Field(None, description="Current stack frame")
    breakpoint_hit: Optional[Breakpoint] = Field(None, description="Breakpoint that was hit")
    exception_info: Optional[Dict[str, Any]] = Field(None, description="Exception information")
    call_stack: List[StackFrame] = Field(default_factory=list, description="Call stack")
    variables: List[Variable] = Field(default_factory=list, description="Current variables")
    watch_expressions: List[WatchExpression] = Field(default_factory=list, description="Watch expressions")
    thread_id: Optional[int] = Field(None, description="Current thread ID")
    timestamp: datetime = Field(..., description="State timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class EvaluationResult(BaseModel):
    """Expression evaluation result"""
    session_id: str = Field(..., description="Debug session identifier")
    expression: str = Field(..., description="Evaluated expression")
    result: str = Field(..., description="Evaluation result")
    type: str = Field(..., description="Result type")
    is_error: bool = Field(default=False, description="Whether evaluation resulted in error")
    error_message: Optional[str] = Field(None, description="Error message")
    execution_time: float = Field(..., description="Execution time in seconds")
    timestamp: datetime = Field(..., description="Evaluation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ProfileSession(BaseModel):
    """Profiling session information"""
    id: str = Field(..., description="Unique profiling session identifier")
    debug_session_id: str = Field(..., description="Associated debug session")
    profiler_type: ProfilerType = Field(..., description="Profiler type")
    status: str = Field(..., description="Profiling status")
    created_at: datetime = Field(..., description="Creation time")
    started_at: Optional[datetime] = Field(None, description="Start time")
    stopped_at: Optional[datetime] = Field(None, description="Stop time")
    duration: Optional[float] = Field(None, description="Profiling duration")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Profiler configuration")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ProfileData(BaseModel):
    """Profiling data"""
    session_id: str = Field(..., description="Profiling session identifier")
    profiler_type: ProfilerType = Field(..., description="Profiler type")
    data: Dict[str, Any] = Field(..., description="Profiling data")
    summary: Dict[str, Any] = Field(..., description="Data summary")
    timestamp: datetime = Field(..., description="Data timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class PerformanceAnalysis(BaseModel):
    """Performance analysis results"""
    session_id: str = Field(..., description="Profiling session identifier")
    analysis_type: str = Field(..., description="Analysis type")
    bottlenecks: List[Dict[str, Any]] = Field(default_factory=list, description="Identified bottlenecks")
    recommendations: List[str] = Field(default_factory=list, description="Optimization recommendations")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    generated_at: datetime = Field(..., description="Analysis timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MemoryUsage(BaseModel):
    """Memory usage information"""
    session_id: str = Field(..., description="Debug session identifier")
    total_memory: int = Field(..., description="Total memory usage in bytes")
    heap_memory: int = Field(..., description="Heap memory usage in bytes")
    stack_memory: int = Field(..., description="Stack memory usage in bytes")
    object_count: int = Field(..., description="Number of objects")
    garbage_collections: int = Field(..., description="Number of garbage collections")
    memory_leaks: List[Dict[str, Any]] = Field(default_factory=list, description="Potential memory leaks")
    timestamp: datetime = Field(..., description="Memory snapshot timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# Request/Response Models
class StartDebugSessionRequest(BaseModel):
    """Start debug session request"""
    project_id: UUID = Field(..., description="Project identifier")
    target_file: str = Field(..., description="Target file to debug")
    working_directory: Optional[str] = Field(None, description="Working directory")
    language: str = Field(..., description="Programming language")
    debugger_type: str = Field(default="auto", description="Debugger type")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    command_line_args: List[str] = Field(default_factory=list, description="Command line arguments")
    breakpoints: List[Dict[str, Any]] = Field(default_factory=list, description="Initial breakpoints")


class StartDebugSessionResponse(BaseModel):
    """Start debug session response"""
    session: DebugSession = Field(..., description="Created debug session")
    websocket_url: str = Field(..., description="WebSocket URL for real-time communication")


class SetBreakpointRequest(BaseModel):
    """Set breakpoint request"""
    file_path: str = Field(..., description="File path")
    line_number: int = Field(..., description="Line number")
    column: Optional[int] = Field(None, description="Column number")
    type: BreakpointType = Field(default=BreakpointType.LINE, description="Breakpoint type")
    condition: Optional[str] = Field(None, description="Conditional expression")
    ignore_count: int = Field(default=0, description="Number of hits to ignore")
    log_message: Optional[str] = Field(None, description="Log message")
    function_name: Optional[str] = Field(None, description="Function name")
    exception_type: Optional[str] = Field(None, description="Exception type")
    variable_name: Optional[str] = Field(None, description="Variable name")


class StepRequest(BaseModel):
    """Step request"""
    step_type: StepType = Field(..., description="Step type")
    count: int = Field(default=1, description="Number of steps")


class EvaluateExpressionRequest(BaseModel):
    """Evaluate expression request"""
    expression: str = Field(..., description="Expression to evaluate")
    frame_level: Optional[int] = Field(None, description="Stack frame level")
    timeout: Optional[int] = Field(None, description="Evaluation timeout")


class AddWatchExpressionRequest(BaseModel):
    """Add watch expression request"""
    expression: str = Field(..., description="Expression to watch")
    name: Optional[str] = Field(None, description="Display name")


class StartProfilingRequest(BaseModel):
    """Start profiling request"""
    profiler_type: ProfilerType = Field(..., description="Profiler type")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Profiler configuration")


class DebugInfo(BaseModel):
    """Debug session information"""
    session: DebugSession = Field(..., description="Debug session")
    current_state: Optional[DebugState] = Field(None, description="Current debug state")
    breakpoints: List[Breakpoint] = Field(default_factory=list, description="All breakpoints")
    watch_expressions: List[WatchExpression] = Field(default_factory=list, description="Watch expressions")
    profile_sessions: List[ProfileSession] = Field(default_factory=list, description="Profiling sessions")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Session statistics")


class WebSocketDebugMessage(BaseModel):
    """WebSocket message for debug communication"""
    type: str = Field(..., description="Message type")
    session_id: str = Field(..., description="Debug session identifier")
    data: Dict[str, Any] = Field(..., description="Message data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")


# Update forward references
Variable.model_rebuild()
