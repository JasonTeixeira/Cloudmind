"""
Code Editor API Endpoints
Provides REST API for code editor functionality
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
import json
import logging

from app.core.auth import get_current_user
from app.models.user import User
from app.services.editor.code_editor_service import (
    code_editor_service, EditorSession, Token, Suggestion, Diagnostic
)
from app.services.editor.collaboration_service import (
    collaboration_service, TextChange, CursorPosition
)
from app.schemas.editor import (
    EditorOpenRequest, EditorSaveRequest, EditorSessionResponse,
    AutocompleteRequest, AutocompleteResponse, ValidationRequest,
    ValidationResponse, SyntaxHighlightingRequest, SyntaxHighlightingResponse,
    CollaborationJoinRequest, CollaborationLeaveRequest, TextChangeRequest,
    CursorPositionRequest, TextSelectionRequest
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/editor", tags=["Code Editor"])


@router.post("/open", response_model=EditorSessionResponse)
async def open_file(
    request: EditorOpenRequest,
    current_user: User = Depends(get_current_user)
):
    """Open file in code editor"""
    try:
        session = await code_editor_service.open_file(
            file_path=request.file_path,
            user_id=current_user.id
        )
        
        return EditorSessionResponse(
            session_id=session.session_id,
            file_path=session.file_path,
            content=session.content,
            language=session.language,
            created_at=session.created_at,
            last_modified=session.last_modified,
            collaborators=list(session.collaborators)
        )
        
    except Exception as e:
        logger.error(f"Failed to open file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/save")
async def save_file(
    request: EditorSaveRequest,
    current_user: User = Depends(get_current_user)
):
    """Save file from editor"""
    try:
        success = await code_editor_service.save_file(
            session_id=request.session_id,
            content=request.content,
            user_id=current_user.id
        )
        
        if success:
            return {"success": True, "message": "File saved successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to save file")
            
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/autocomplete", response_model=AutocompleteResponse)
async def get_autocomplete(
    content: str = Query(..., description="File content"),
    cursor_pos: int = Query(..., description="Cursor position"),
    language: str = Query(..., description="Programming language"),
    current_user: User = Depends(get_current_user)
):
    """Get autocomplete suggestions"""
    try:
        suggestions = await code_editor_service.get_autocomplete(
            content=content,
            cursor_pos=cursor_pos,
            language=language
        )
        
        return AutocompleteResponse(
            suggestions=[
                {
                    "text": s.text,
                    "type": s.type,
                    "description": s.description,
                    "detail": s.detail
                }
                for s in suggestions
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to get autocomplete: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/validate", response_model=ValidationResponse)
async def validate_syntax(
    request: ValidationRequest,
    current_user: User = Depends(get_current_user)
):
    """Validate code syntax"""
    try:
        diagnostics = await code_editor_service.validate_syntax(
            content=request.content,
            language=request.language
        )
        
        return ValidationResponse(
            diagnostics=[
                {
                    "message": d.message,
                    "severity": d.severity,
                    "line": d.line,
                    "column": d.column,
                    "end_line": d.end_line,
                    "end_column": d.end_column
                }
                for d in diagnostics
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to validate syntax: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/syntax-highlighting", response_model=SyntaxHighlightingResponse)
async def get_syntax_highlighting(
    request: SyntaxHighlightingRequest,
    current_user: User = Depends(get_current_user)
):
    """Get syntax highlighting tokens"""
    try:
        tokens = await code_editor_service.get_syntax_highlighting(
            content=request.content,
            language=request.language
        )
        
        return SyntaxHighlightingResponse(
            tokens=[
                {
                    "type": t.type,
                    "value": t.value,
                    "start": t.start,
                    "end": t.end,
                    "line": t.line
                }
                for t in tokens
            ]
        )
        
    except Exception as e:
        logger.error(f"Failed to get syntax highlighting: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions", response_model=List[EditorSessionResponse])
async def get_active_sessions(
    current_user: User = Depends(get_current_user)
):
    """Get all active editor sessions for user"""
    try:
        sessions = await code_editor_service.get_active_sessions(current_user.id)
        
        return [
            EditorSessionResponse(
                session_id=session.session_id,
                file_path=session.file_path,
                content=session.content,
                language=session.language,
                created_at=session.created_at,
                last_modified=session.last_modified,
                collaborators=list(session.collaborators)
            )
            for session in sessions
        ]
        
    except Exception as e:
        logger.error(f"Failed to get active sessions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/sessions/{session_id}")
async def close_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Close editor session"""
    try:
        success = await code_editor_service.close_session(
            session_id=session_id,
            user_id=current_user.id
        )
        
        if success:
            return {"success": True, "message": "Session closed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to close session")
            
    except Exception as e:
        logger.error(f"Failed to close session: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Collaboration endpoints
@router.post("/collaboration/join")
async def join_collaboration(
    request: CollaborationJoinRequest,
    current_user: User = Depends(get_current_user)
):
    """Join collaborative editing session"""
    try:
        # This endpoint is for preparing to join collaboration
        # The actual WebSocket connection is handled separately
        return {
            "success": True,
            "session_id": request.session_id,
            "message": "Ready to join collaboration session"
        }
        
    except Exception as e:
        logger.error(f"Failed to join collaboration: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/collaboration/leave")
async def leave_collaboration(
    request: CollaborationLeaveRequest,
    current_user: User = Depends(get_current_user)
):
    """Leave collaborative editing session"""
    try:
        await collaboration_service.leave_session(
            session_id=request.session_id,
            user_id=current_user.id
        )
        
        return {"success": True, "message": "Left collaboration session"}
        
    except Exception as e:
        logger.error(f"Failed to leave collaboration: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/collaboration/cursors/{session_id}")
async def get_cursor_positions(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all cursor positions for a session"""
    try:
        positions = await collaboration_service.get_cursor_positions(session_id)
        
        return {
            "session_id": session_id,
            "cursor_positions": [
                {
                    "user_id": str(pos.user_id),
                    "line": pos.line,
                    "column": pos.column,
                    "timestamp": pos.timestamp.isoformat()
                }
                for pos in positions
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get cursor positions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# WebSocket endpoint for real-time collaboration
@router.websocket("/collaborate/{session_id}")
async def collaborate_websocket(
    websocket: WebSocket,
    session_id: str,
    token: str = Query(..., description="Authentication token")
):
    """WebSocket endpoint for real-time collaboration"""
    try:
        # Accept the WebSocket connection
        await websocket.accept()
        
        # Extract and validate token from query parameters
        token = websocket.query_params.get("token")
        if not token:
            await websocket.close(code=4001, reason="Missing authentication token")
            return
        
        # Validate token and get user_id
        from app.core.auth import verify_token
        payload = verify_token(token)
        if not payload:
            await websocket.close(code=4001, reason="Invalid authentication token")
            return
        
        user_id = UUID(payload.get("sub"))
        
        # Join collaboration session
        collaboration_session = await collaboration_service.join_session(
            session_id=session_id,
            user_id=user_id,
            websocket=websocket
        )
        
        logger.info(f"User {user_id} connected to collaboration session {session_id}")
        
        try:
            # Handle WebSocket messages
            while True:
                # Receive message
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await handle_collaboration_message(
                    websocket=websocket,
                    session_id=session_id,
                    user_id=user_id,
                    message=message
                )
                
        except WebSocketDisconnect:
            logger.info(f"User {user_id} disconnected from session {session_id}")
        except Exception as e:
            logger.error(f"Error in collaboration WebSocket: {e}")
        finally:
            # Clean up when connection is closed
            await collaboration_service.leave_session(session_id, user_id)
            
    except Exception as e:
        logger.error(f"Failed to establish collaboration WebSocket: {e}")
        if websocket.client_state.value != 3:  # Not closed
            await websocket.close(code=1000)


async def handle_collaboration_message(
    websocket: WebSocket,
    session_id: str,
    user_id: UUID,
    message: Dict[str, Any]
):
    """Handle collaboration WebSocket messages"""
    try:
        message_type = message.get("type")
        
        if message_type == "text_change":
            # Handle text change
            change_data = message.get("change", {})
            change = TextChange(
                user_id=user_id,
                session_id=session_id,
                change_type=change_data.get("change_type"),
                position=change_data.get("position"),
                text=change_data.get("text", ""),
                deleted_text=change_data.get("deleted_text", "")
            )
            await collaboration_service.broadcast_change(session_id, change)
            
        elif message_type == "cursor_position":
            # Handle cursor position update
            line = message.get("line", 0)
            column = message.get("column", 0)
            await collaboration_service.update_cursor_position(
                session_id, user_id, line, column
            )
            
        elif message_type == "text_selection":
            # Handle text selection update
            start_line = message.get("start_line", 0)
            start_column = message.get("start_column", 0)
            end_line = message.get("end_line", 0)
            end_column = message.get("end_column", 0)
            await collaboration_service.update_text_selection(
                session_id, user_id, start_line, start_column, end_line, end_column
            )
            
        elif message_type == "ping":
            # Handle ping message
            await websocket.send_text(json.dumps({"type": "pong"}))
            
        else:
            logger.warning(f"Unknown message type: {message_type}")
            
    except Exception as e:
        logger.error(f"Failed to handle collaboration message: {e}")


# Health check endpoint
@router.get("/health")
async def editor_health():
    """Health check for editor service"""
    return {
        "status": "healthy",
        "service": "code_editor",
        "active_sessions": len(code_editor_service.active_sessions),
        "collaboration_sessions": len(collaboration_service.active_sessions)
    }
