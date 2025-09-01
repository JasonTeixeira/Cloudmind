"""
Integrated Terminal API Endpoints
Provides REST API for terminal functionality
"""

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
import json
from datetime import datetime

from app.core.auth import get_current_user
from app.models.user import User
from app.services.terminal.terminal_service import terminal_service
from app.services.terminal.command_history import command_history_service
from app.schemas.terminal import (
    CreateTerminalRequest, CreateTerminalResponse, ExecuteCommandRequest, ExecuteCommandResponse,
    GetSuggestionsRequest, GetSuggestionsResponse, ResizeTerminalRequest, SendInputRequest,
    TerminalInfo, TerminalStatistics, WebSocketMessage
)
from app.schemas.terminal_ai import (
    PlanRequest, PlanResponse, ExecutePlanRequest, ExecutePlanResponse
)
from app.services.terminal.ai_terminal_service import ai_terminal_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/terminal", tags=["Integrated Terminal"])
@router.post("/ai/plan", response_model=PlanResponse)
async def ai_plan_commands(
    request: PlanRequest,
    current_user: User = Depends(get_current_user)
):
    """AI plans a safe set of commands for a given goal (feature-flagged)."""
    if not getattr(settings, "ENABLE_AI_TERMINAL", False):
        raise HTTPException(status_code=403, detail="AI terminal is disabled")
    # Restrict to admin/master roles
    if not (current_user.is_master_user or current_user.role in ("admin", "master")):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    commands = await ai_terminal_service.plan_commands(goal=request.goal, context=request.context)
    return PlanResponse(commands=commands)


@router.post("/ai/execute", response_model=ExecutePlanResponse)
async def ai_execute_plan(
    request: ExecutePlanRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute an AI-planned set of commands with guardrails (feature-flagged)."""
    if not getattr(settings, "ENABLE_AI_TERMINAL", False):
        raise HTTPException(status_code=403, detail="AI terminal is disabled")
    # Restrict to admin/master roles
    if not (current_user.is_master_user or current_user.role in ("admin", "master")):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    results = await ai_terminal_service.execute_planned(session_id=request.session_id, commands=request.commands)
    return ExecutePlanResponse(results=results)


@router.post("/create", response_model=CreateTerminalResponse)
async def create_terminal(
    request: CreateTerminalRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a new terminal session"""
    try:
        session = await terminal_service.create_terminal(
            project_id=request.project_id,
            user_id=current_user.id,
            name=request.name,
            terminal_type=request.type,
            working_directory=request.working_directory,
            environment_variables=request.environment_variables,
            custom_shell=request.custom_shell,
            theme=request.theme,
            columns=request.columns,
            rows=request.rows
        )
        
        # Create WebSocket URL
        websocket_url = f"/terminal/ws/{session.id}"
        
        return CreateTerminalResponse(
            session=session,
            websocket_url=websocket_url
        )
        
    except Exception as e:
        logger.error(f"Failed to create terminal: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/execute", response_model=ExecuteCommandResponse)
async def execute_command(
    request: ExecuteCommandRequest,
    session_id: str = Query(..., description="Terminal session ID"),
    current_user: User = Depends(get_current_user)
):
    """Execute a command in a terminal session"""
    try:
        # Execute command
        result = await terminal_service.execute_command(
            session_id=session_id,
            command=request.command,
            working_directory=request.working_directory,
            environment_variables=request.environment_variables,
            timeout=request.timeout
        )
        
        # Save command to history
        await command_history_service.save_command(
            user_id=current_user.id,
            command=request.command,
            working_directory=result.working_directory,
            exit_code=result.exit_code,
            execution_time=result.execution_time,
            success=result.success
        )
        
        # Learn from usage
        await command_history_service.learn_from_usage(
            command=request.command,
            success=result.success,
            user_id=current_user.id
        )
        
        return ExecuteCommandResponse(
            command_id=result.command_id,
            status=result.status,
            result=result
        )
        
    except Exception as e:
        logger.error(f"Failed to execute command: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/output/{session_id}")
async def get_output(
    session_id: str,
    limit: int = Query(100, description="Maximum number of output lines"),
    current_user: User = Depends(get_current_user)
):
    """Get terminal output"""
    try:
        outputs = await terminal_service.get_output(session_id, limit)
        return {
            "session_id": session_id,
            "outputs": outputs,
            "count": len(outputs)
        }
        
    except Exception as e:
        logger.error(f"Failed to get output: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/input/{session_id}")
async def send_input(
    session_id: str,
    request: SendInputRequest,
    current_user: User = Depends(get_current_user)
):
    """Send input to terminal"""
    try:
        success = await terminal_service.send_input(session_id, request.input_data)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to send input")
        
        return {"success": True, "message": "Input sent successfully"}
        
    except Exception as e:
        logger.error(f"Failed to send input: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/resize/{session_id}")
async def resize_terminal(
    session_id: str,
    request: ResizeTerminalRequest,
    current_user: User = Depends(get_current_user)
):
    """Resize terminal window"""
    try:
        success = await terminal_service.resize_terminal(
            session_id, 
            request.columns, 
            request.rows
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to resize terminal")
        
        return {"success": True, "message": "Terminal resized successfully"}
        
    except Exception as e:
        logger.error(f"Failed to resize terminal: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/kill/{session_id}")
async def kill_process(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Kill terminal process"""
    try:
        success = await terminal_service.kill_process(session_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to kill process")
        
        return {"success": True, "message": "Process killed successfully"}
        
    except Exception as e:
        logger.error(f"Failed to kill process: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info/{session_id}", response_model=TerminalInfo)
async def get_terminal_info(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get terminal session information"""
    try:
        info = await terminal_service.get_terminal_info(session_id)
        
        if not info:
            raise HTTPException(status_code=404, detail="Terminal session not found")
        
        return TerminalInfo(**info)
        
    except Exception as e:
        logger.error(f"Failed to get terminal info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tab/create")
async def create_tab(
    session_id: str = Query(..., description="Terminal session ID"),
    name: Optional[str] = Query(None, description="Tab name"),
    current_user: User = Depends(get_current_user)
):
    """Create a new terminal tab"""
    try:
        tab = await terminal_service.create_tab(session_id, name)
        
        if not tab:
            raise HTTPException(status_code=400, detail="Failed to create tab")
        
        return tab
        
    except Exception as e:
        logger.error(f"Failed to create tab: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/tab/switch")
async def switch_tab(
    session_id: str = Query(..., description="Terminal session ID"),
    tab_id: str = Query(..., description="Tab ID to switch to"),
    current_user: User = Depends(get_current_user)
):
    """Switch to a different terminal tab"""
    try:
        success = await terminal_service.switch_tab(session_id, tab_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to switch tab")
        
        return {"success": True, "message": "Tab switched successfully"}
        
    except Exception as e:
        logger.error(f"Failed to switch tab: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history")
async def get_command_history(
    project_id: Optional[UUID] = Query(None, description="Project ID"),
    limit: int = Query(100, description="Maximum number of commands"),
    offset: int = Query(0, description="Offset for pagination"),
    search_query: str = Query("", description="Search query"),
    current_user: User = Depends(get_current_user)
):
    """Get command history"""
    try:
        history = await command_history_service.get_history(
            user_id=current_user.id,
            project_id=project_id,
            limit=limit,
            offset=offset,
            search_query=search_query
        )
        
        return {
            "history": history,
            "total_count": len(history),
            "has_more": len(history) == limit
        }
        
    except Exception as e:
        logger.error(f"Failed to get command history: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/suggestions", response_model=GetSuggestionsResponse)
async def get_suggestions(
    request: GetSuggestionsRequest,
    current_user: User = Depends(get_current_user)
):
    """Get command suggestions"""
    try:
        suggestions = await command_history_service.get_suggestions(
            partial_command=request.partial_command,
            context=request.context,
            user_id=current_user.id,
            limit=request.limit
        )
        
        return GetSuggestionsResponse(
            suggestions=suggestions,
            total_count=len(suggestions)
        )
        
    except Exception as e:
        logger.error(f"Failed to get suggestions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/suggestions/simple")
async def get_simple_suggestions(
    partial_command: str = Query(..., description="Partial command"),
    limit: int = Query(10, description="Maximum suggestions"),
    current_user: User = Depends(get_current_user)
):
    """Get simple command suggestions"""
    try:
        suggestions = await command_history_service.get_suggestions(
            partial_command=partial_command,
            user_id=current_user.id,
            limit=limit
        )
        
        return {
            "suggestions": suggestions,
            "total_count": len(suggestions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get simple suggestions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/aliases")
async def get_aliases(
    current_user: User = Depends(get_current_user)
):
    """Get user command aliases"""
    try:
        aliases = await command_history_service.get_aliases(current_user.id)
        return {"aliases": aliases}
        
    except Exception as e:
        logger.error(f"Failed to get aliases: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/statistics/{session_id}")
async def get_terminal_statistics(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get terminal usage statistics"""
    try:
        info = await terminal_service.get_terminal_info(session_id)
        
        if not info:
            raise HTTPException(status_code=404, detail="Terminal session not found")
        
        statistics = info.get("statistics", {})
        
        return TerminalStatistics(
            session_id=session_id,
            total_commands=statistics.get("total_commands", 0),
            successful_commands=statistics.get("successful_commands", 0),
            failed_commands=statistics.get("failed_commands", 0),
            total_execution_time=statistics.get("total_execution_time", 0.0),
            average_execution_time=statistics.get("average_execution_time", 0.0),
            most_used_commands=statistics.get("most_used_commands", []),
            session_duration=statistics.get("session_duration", 0.0),
            created_at=info["session"].created_at,
            updated_at=info["session"].last_activity
        )
        
    except Exception as e:
        logger.error(f"Failed to get terminal statistics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions")
async def list_sessions(
    project_id: Optional[UUID] = Query(None, description="Project ID"),
    current_user: User = Depends(get_current_user)
):
    """List terminal sessions for user"""
    try:
        # This would typically filter sessions by user and project
        # For now, return all sessions (in production, filter by user)
        sessions = list(terminal_service.sessions.values())
        
        if project_id:
            sessions = [s for s in sessions if s.project_id == project_id]
        
        return {
            "sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/sessions/{session_id}")
async def close_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Close a terminal session"""
    try:
        # Kill the process first
        await terminal_service.kill_process(session_id)
        
        # Remove from sessions (in production, mark as inactive instead of deleting)
        if session_id in terminal_service.sessions:
            del terminal_service.sessions[session_id]
        
        return {"success": True, "message": "Session closed successfully"}
        
    except Exception as e:
        logger.error(f"Failed to close session: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def terminal_health():
    """Health check for terminal service"""
    return {
        "status": "healthy",
        "service": "integrated_terminal",
        "features": [
            "terminal_sessions",
            "command_execution",
            "real_time_output",
            "command_history",
            "auto_completion",
            "terminal_tabs",
            "process_management",
            "statistics_tracking"
        ],
        "active_sessions": len(terminal_service.sessions),
        "active_processes": len(terminal_service.process_manager.processes)
    }


# WebSocket endpoint for real-time terminal communication
@router.websocket("/ws/{session_id}")
async def terminal_websocket(
    websocket: WebSocket,
    session_id: str
):
    """WebSocket endpoint for real-time terminal communication"""
    await websocket.accept()
    
    try:
        # Verify session exists
        if session_id not in terminal_service.sessions:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Terminal session not found"
            }))
            return
        
        session = terminal_service.sessions[session_id]
        
        # Send session info
        await websocket.send_text(json.dumps({
            "type": "session_info",
            "data": {
                "session_id": session_id,
                "name": session.name,
                "type": session.type,
                "status": session.status,
                "working_directory": session.working_directory
            }
        }))
        
        # Main WebSocket loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                message_type = message.get("type")
                
                if message_type == "input":
                    # Send input to terminal
                    input_data = message.get("data", "")
                    success = await terminal_service.send_input(session_id, input_data)
                    
                    await websocket.send_text(json.dumps({
                        "type": "input_result",
                        "success": success
                    }))
                
                elif message_type == "resize":
                    # Resize terminal
                    columns = message.get("data", {}).get("columns", 80)
                    rows = message.get("data", {}).get("rows", 24)
                    success = await terminal_service.resize_terminal(session_id, columns, rows)
                    
                    await websocket.send_text(json.dumps({
                        "type": "resize_result",
                        "success": success
                    }))
                
                elif message_type == "get_output":
                    # Get terminal output
                    limit = message.get("data", {}).get("limit", 100)
                    outputs = await terminal_service.get_output(session_id, limit)
                    
                    await websocket.send_text(json.dumps({
                        "type": "output",
                        "data": {
                            "outputs": [output.dict() for output in outputs],
                            "count": len(outputs)
                        }
                    }))
                
                elif message_type == "ping":
                    # Respond to ping
                    await websocket.send_text(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    }))
                
                else:
                    # Unknown message type
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    }))
                    
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for session {session_id}")
                break
                
            except Exception as e:
                logger.error(f"WebSocket error for session {session_id}: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
                
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        try:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": str(e)
            }))
        except:
            pass
