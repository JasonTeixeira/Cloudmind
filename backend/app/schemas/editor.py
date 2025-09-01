"""
Code Editor Schemas
Pydantic models for code editor API endpoints
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime, timezone
from enum import Enum


class EditorOpenRequest(BaseModel):
    """Request to open file in editor"""
    file_path: str = Field(..., description="Path to the file to open")
    
    @field_validator('file_path')
    def validate_file_path(cls, v):
        if not v or v.strip() == "":
            raise ValueError('File path cannot be empty')
        return v


class EditorSaveRequest(BaseModel):
    """Request to save file from editor"""
    session_id: str = Field(..., description="Editor session ID")
    content: str = Field(..., description="File content to save")
    
    @field_validator('session_id')
    def validate_session_id(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Session ID cannot be empty')
        return v


class EditorSessionResponse(BaseModel):
    """Response for editor session"""
    session_id: str
    file_path: str
    content: str
    language: str
    created_at: datetime
    last_modified: datetime
    collaborators: List[UUID]
    
    class Config:
        from_attributes = True


class AutocompleteRequest(BaseModel):
    """Request for autocomplete suggestions"""
    content: str = Field(..., description="File content")
    cursor_pos: int = Field(..., description="Cursor position in content")
    language: str = Field(..., description="Programming language")
    
    @field_validator('cursor_pos')
    def validate_cursor_pos(cls, v):
        if v < 0:
            raise ValueError('Cursor position must be non-negative')
        return v


class AutocompleteSuggestion(BaseModel):
    """Autocomplete suggestion"""
    text: str = Field(..., description="Suggestion text")
    type: str = Field(..., description="Suggestion type (keyword, function, class, etc.)")
    description: str = Field("", description="Suggestion description")
    detail: str = Field("", description="Additional details")


class AutocompleteResponse(BaseModel):
    """Response for autocomplete suggestions"""
    suggestions: List[AutocompleteSuggestion]


class ValidationRequest(BaseModel):
    """Request for syntax validation"""
    content: str = Field(..., description="File content to validate")
    language: str = Field(..., description="Programming language")


class Diagnostic(BaseModel):
    """Code diagnostic/error"""
    message: str = Field(..., description="Diagnostic message")
    severity: str = Field(..., description="Severity level (error, warning, info, hint)")
    line: int = Field(..., description="Line number (1-based)")
    column: int = Field(..., description="Column number (1-based)")
    end_line: Optional[int] = Field(None, description="End line number")
    end_column: Optional[int] = Field(None, description="End column number")
    
    @field_validator('severity')
    def validate_severity(cls, v):
        valid_severities = ['error', 'warning', 'info', 'hint']
        if v not in valid_severities:
            raise ValueError(f'Severity must be one of: {valid_severities}')
        return v
    
    @field_validator('line', 'column')
    def validate_line_column(cls, v):
        if v < 1:
            raise ValueError('Line and column numbers must be 1-based')
        return v


class ValidationResponse(BaseModel):
    """Response for syntax validation"""
    diagnostics: List[Diagnostic]


class SyntaxHighlightingRequest(BaseModel):
    """Request for syntax highlighting"""
    content: str = Field(..., description="File content to highlight")
    language: str = Field(..., description="Programming language")


class Token(BaseModel):
    """Syntax highlighting token"""
    type: str = Field(..., description="Token type")
    value: str = Field(..., description="Token value")
    start: int = Field(..., description="Start position in content")
    end: int = Field(..., description="End position in content")
    line: int = Field(..., description="Line number")
    
    @field_validator('start', 'end')
    def validate_positions(cls, v):
        if v < 0:
            raise ValueError('Position must be non-negative')
        return v

    @model_validator(mode='after')
    def _validate_token_ranges(self):
        if hasattr(self, 'end') and hasattr(self, 'start'):
            if self.end < self.start:
                raise ValueError('End position must be after start position')
        return self


class SyntaxHighlightingResponse(BaseModel):
    """Response for syntax highlighting"""
    tokens: List[Token]


class CollaborationJoinRequest(BaseModel):
    """Request to join collaboration session"""
    session_id: str = Field(..., description="Editor session ID")
    
    @field_validator('session_id')
    def validate_session_id(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Session ID cannot be empty')
        return v


class CollaborationLeaveRequest(BaseModel):
    """Request to leave collaboration session"""
    session_id: str = Field(..., description="Editor session ID")
    
    @field_validator('session_id')
    def validate_session_id(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Session ID cannot be empty')
        return v


class TextChangeRequest(BaseModel):
    """Request for text change in collaboration"""
    session_id: str = Field(..., description="Editor session ID")
    change_type: str = Field(..., description="Type of change (insert, delete, replace)")
    position: int = Field(..., description="Position in content")
    text: str = Field("", description="Text to insert")
    deleted_text: str = Field("", description="Text being deleted")
    
    @field_validator('change_type')
    def validate_change_type(cls, v):
        valid_types = ['insert', 'delete', 'replace']
        if v not in valid_types:
            raise ValueError(f'Change type must be one of: {valid_types}')
        return v
    
    @field_validator('position')
    def validate_position(cls, v):
        if v < 0:
            raise ValueError('Position must be non-negative')
        return v


class CursorPositionRequest(BaseModel):
    """Request to update cursor position"""
    session_id: str = Field(..., description="Editor session ID")
    line: int = Field(..., description="Line number (1-based)")
    column: int = Field(..., description="Column number (1-based)")
    
    @field_validator('line', 'column')
    def validate_line_column(cls, v):
        if v < 1:
            raise ValueError('Line and column numbers must be 1-based')
        return v


class TextSelectionRequest(BaseModel):
    """Request to update text selection"""
    session_id: str = Field(..., description="Editor session ID")
    start_line: int = Field(..., description="Start line number (1-based)")
    start_column: int = Field(..., description="Start column number (1-based)")
    end_line: int = Field(..., description="End line number (1-based)")
    end_column: int = Field(..., description="End column number (1-based)")
    
    @field_validator('start_line', 'start_column', 'end_line', 'end_column')
    def validate_line_column(cls, v):
        if v < 1:
            raise ValueError('Line and column numbers must be 1-based')
        return v

    @model_validator(mode='after')
    def _validate_selection_ranges(self):
        try:
            if (self.end_line < self.start_line) or (self.end_line == self.start_line and self.end_column < self.start_column):
                raise ValueError('End position must be after start position')
        except Exception:
            pass
        return self


class EditorSettings(BaseModel):
    """Editor settings"""
    theme: str = Field("vs-dark", description="Editor theme")
    font_size: int = Field(14, description="Font size")
    tab_size: int = Field(4, description="Tab size")
    insert_spaces: bool = Field(True, description="Use spaces instead of tabs")
    word_wrap: bool = Field(False, description="Enable word wrap")
    minimap_enabled: bool = Field(True, description="Show minimap")
    line_numbers: bool = Field(True, description="Show line numbers")
    auto_save: bool = Field(True, description="Auto-save on changes")
    auto_save_delay: int = Field(1000, description="Auto-save delay in milliseconds")
    
    @field_validator('font_size', 'tab_size')
    def validate_positive_int(cls, v):
        if v <= 0:
            raise ValueError('Value must be positive')
        return v
    
    @field_validator('auto_save_delay')
    def validate_auto_save_delay(cls, v):
        if v < 100:
            raise ValueError('Auto-save delay must be at least 100ms')
        return v


class EditorPreferences(BaseModel):
    """User editor preferences"""
    user_id: UUID
    settings: EditorSettings
    language_preferences: Dict[str, str] = Field(default_factory=dict)
    snippet_collections: List[str] = Field(default_factory=list)
    keybindings: Dict[str, str] = Field(default_factory=dict)
    extensions: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class EditorStats(BaseModel):
    """Editor usage statistics"""
    total_sessions: int = Field(0, description="Total editor sessions")
    total_files_edited: int = Field(0, description="Total files edited")
    total_lines_edited: int = Field(0, description="Total lines edited")
    collaboration_sessions: int = Field(0, description="Collaboration sessions")
    languages_used: Dict[str, int] = Field(default_factory=dict)
    average_session_duration: float = Field(0.0, description="Average session duration in minutes")
    
    class Config:
        from_attributes = True


class EditorError(BaseModel):
    """Editor error response"""
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EditorSuccess(BaseModel):
    """Editor success response"""
    success: bool = Field(True, description="Success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# WebSocket message schemas
class WebSocketMessage(BaseModel):
    """Base WebSocket message"""
    type: str = Field(..., description="Message type")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TextChangeMessage(WebSocketMessage):
    """Text change WebSocket message"""
    type: str = Field("text_change", description="Message type")
    change: TextChangeRequest = Field(..., description="Text change details")


class CursorPositionMessage(WebSocketMessage):
    """Cursor position WebSocket message"""
    type: str = Field("cursor_position", description="Message type")
    line: int = Field(..., description="Line number")
    column: int = Field(..., description="Column number")


class TextSelectionMessage(WebSocketMessage):
    """Text selection WebSocket message"""
    type: str = Field("text_selection", description="Message type")
    start_line: int = Field(..., description="Start line number")
    start_column: int = Field(..., description="Start column number")
    end_line: int = Field(..., description="End line number")
    end_column: int = Field(..., description="End column number")


class PingMessage(WebSocketMessage):
    """Ping WebSocket message"""
    type: str = Field("ping", description="Message type")


class PongMessage(WebSocketMessage):
    """Pong WebSocket message"""
    type: str = Field("pong", description="Message type")


class SessionStateMessage(WebSocketMessage):
    """Session state WebSocket message"""
    type: str = Field("session_state", description="Message type")
    content: str = Field(..., description="File content")
    participants: List[UUID] = Field(..., description="Session participants")
    cursor_positions: List[Dict[str, Any]] = Field(..., description="Cursor positions")
    selections: List[Dict[str, Any]] = Field(..., description="Text selections")


class ParticipantJoinedMessage(WebSocketMessage):
    """Participant joined WebSocket message"""
    type: str = Field("participant_joined", description="Message type")
    user_id: UUID = Field(..., description="User ID who joined")


class ParticipantLeftMessage(WebSocketMessage):
    """Participant left WebSocket message"""
    type: str = Field("participant_left", description="Message type")
    user_id: UUID = Field(..., description="User ID who left")


# Enums
class ChangeType(str, Enum):
    """Text change types"""
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


class DiagnosticSeverity(str, Enum):
    """Diagnostic severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class SuggestionType(str, Enum):
    """Autocomplete suggestion types"""
    KEYWORD = "keyword"
    FUNCTION = "function"
    CLASS = "class"
    VARIABLE = "variable"
    PROPERTY = "property"
    METHOD = "method"
    MODULE = "module"
    SNIPPET = "snippet"
