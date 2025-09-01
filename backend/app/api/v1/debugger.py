"""
Advanced Debugging API Endpoints
Provides REST API for debugging functionality
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
from app.services.debugger.debugger_service import debugger_service
from app.services.debugger.performance_profiler import performance_profiler
from app.schemas.debugger import (
    StartDebugSessionRequest, StartDebugSessionResponse, SetBreakpointRequest,
    StepRequest, EvaluateExpressionRequest, AddWatchExpressionRequest,
    StartProfilingRequest, DebugInfo, WebSocketDebugMessage
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/debugger", tags=["Advanced Debugging"])


@router.post("/start", response_model=StartDebugSessionResponse)
async def start_debug_session(
    request: StartDebugSessionRequest,
    current_user: User = Depends(get_current_user)
):
    """Start a new debug session"""
    try:
        session = await debugger_service.start_debug_session(
            project_id=request.project_id,
            user_id=current_user.id,
            target_file=request.target_file,
            language=request.language,
            debugger_type=request.debugger_type,
            working_directory=request.working_directory,
            environment_variables=request.environment_variables,
            command_line_args=request.command_line_args
        )
        
        # Create WebSocket URL
        websocket_url = f"/debugger/ws/{session.id}"
        
        return StartDebugSessionResponse(
            session=session,
            websocket_url=websocket_url
        )
        
    except Exception as e:
        logger.error(f"Failed to start debug session: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/breakpoint/set")
async def set_breakpoint(
    request: SetBreakpointRequest,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Set a breakpoint"""
    try:
        breakpoint = await debugger_service.set_breakpoint(
            session_id=session_id,
            file_path=request.file_path,
            line_number=request.line_number,
            breakpoint_type=request.type,
            condition=request.condition,
            ignore_count=request.ignore_count
        )
        
        return breakpoint
        
    except Exception as e:
        logger.error(f"Failed to set breakpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/breakpoint/{breakpoint_id}")
async def remove_breakpoint(
    breakpoint_id: str,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Remove a breakpoint"""
    try:
        success = await debugger_service.remove_breakpoint(session_id, breakpoint_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to remove breakpoint")
        
        return {"success": True, "message": "Breakpoint removed successfully"}
        
    except Exception as e:
        logger.error(f"Failed to remove breakpoint: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/breakpoints/{session_id}")
async def get_breakpoints(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all breakpoints for a session"""
    try:
        breakpoint_manager = debugger_service.breakpoint_managers.get(session_id)
        if not breakpoint_manager:
            return {"breakpoints": []}
        
        breakpoints = list(breakpoint_manager.breakpoints.values())
        return {"breakpoints": breakpoints}
        
    except Exception as e:
        logger.error(f"Failed to get breakpoints: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/step")
async def step_through_code(
    request: StepRequest,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Step through code"""
    try:
        debug_state = await debugger_service.step(
            session_id=session_id,
            step_type=request.step_type,
            count=request.count
        )
        
        return debug_state
        
    except Exception as e:
        logger.error(f"Failed to step through code: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/variables/{session_id}")
async def get_variables(
    session_id: str,
    scope: str = Query("local", description="Variable scope"),
    current_user: User = Depends(get_current_user)
):
    """Get variables in current scope"""
    try:
        from app.schemas.debugger import VariableScope
        
        scope_enum = VariableScope.LOCAL
        if scope == "global":
            scope_enum = VariableScope.GLOBAL
        elif scope == "builtin":
            scope_enum = VariableScope.BUILTIN
        
        variables = await debugger_service.get_variables(session_id, scope_enum)
        return {"variables": variables}
        
    except Exception as e:
        logger.error(f"Failed to get variables: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/call-stack/{session_id}")
async def get_call_stack(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get call stack"""
    try:
        call_stack = await debugger_service.get_call_stack(session_id)
        return {"call_stack": call_stack}
        
    except Exception as e:
        logger.error(f"Failed to get call stack: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/evaluate")
async def evaluate_expression(
    request: EvaluateExpressionRequest,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Evaluate expression in debug context"""
    try:
        result = await debugger_service.evaluate_expression(
            session_id=session_id,
            expression=request.expression,
            frame_level=request.frame_level,
            timeout=request.timeout
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to evaluate expression: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/watch/add")
async def add_watch_expression(
    request: AddWatchExpressionRequest,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Add watch expression"""
    try:
        watch_expression = await debugger_service.add_watch_expression(
            session_id=session_id,
            expression=request.expression,
            name=request.name
        )
        
        return watch_expression
        
    except Exception as e:
        logger.error(f"Failed to add watch expression: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/watch/{session_id}")
async def get_watch_expressions(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get watch expressions"""
    try:
        debugger_process = debugger_service.debugger_processes.get(session_id)
        if not debugger_process:
            return {"watch_expressions": []}
        
        watch_expressions = list(debugger_process.watch_expressions.values())
        return {"watch_expressions": watch_expressions}
        
    except Exception as e:
        logger.error(f"Failed to get watch expressions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/watch/{watch_id}")
async def remove_watch_expression(
    watch_id: str,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Remove watch expression"""
    try:
        debugger_process = debugger_service.debugger_processes.get(session_id)
        if debugger_process and watch_id in debugger_process.watch_expressions:
            del debugger_process.watch_expressions[watch_id]
            return {"success": True, "message": "Watch expression removed successfully"}
        
        raise HTTPException(status_code=404, detail="Watch expression not found")
        
    except Exception as e:
        logger.error(f"Failed to remove watch expression: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/state/{session_id}")
async def get_debug_state(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get current debug state"""
    try:
        debug_state = await debugger_service.get_debug_state(session_id)
        return debug_state
        
    except Exception as e:
        logger.error(f"Failed to get debug state: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/info/{session_id}", response_model=DebugInfo)
async def get_debug_info(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get debug session information"""
    try:
        session = debugger_service.sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Debug session not found")
        
        # Get current state
        current_state = await debugger_service.get_debug_state(session_id)
        
        # Get breakpoints
        breakpoint_manager = debugger_service.breakpoint_managers.get(session_id)
        breakpoints = list(breakpoint_manager.breakpoints.values()) if breakpoint_manager else []
        
        # Get watch expressions
        debugger_process = debugger_service.debugger_processes.get(session_id)
        watch_expressions = list(debugger_process.watch_expressions.values()) if debugger_process else []
        
        # Get profiling sessions
        profile_sessions = [
            ps for ps in performance_profiler.profiling_sessions.values()
            if ps.debug_session_id == session_id
        ]
        
        # Calculate statistics
        statistics = {
            "total_breakpoints": len(breakpoints),
            "active_breakpoints": len([bp for bp in breakpoints if bp.enabled]),
            "watch_expressions": len(watch_expressions),
            "profile_sessions": len(profile_sessions),
            "session_duration": (datetime.utcnow() - session.created_at).total_seconds()
        }
        
        return DebugInfo(
            session=session,
            current_state=current_state,
            breakpoints=breakpoints,
            watch_expressions=watch_expressions,
            profile_sessions=profile_sessions,
            statistics=statistics
        )
        
    except Exception as e:
        logger.error(f"Failed to get debug info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/stop/{session_id}")
async def stop_debug_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Stop debug session"""
    try:
        success = await debugger_service.stop_debug_session(session_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to stop debug session")
        
        return {"success": True, "message": "Debug session stopped successfully"}
        
    except Exception as e:
        logger.error(f"Failed to stop debug session: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/sessions")
async def list_debug_sessions(
    project_id: Optional[UUID] = Query(None, description="Project ID"),
    current_user: User = Depends(get_current_user)
):
    """List debug sessions for user"""
    try:
        sessions = list(debugger_service.sessions.values())
        
        if project_id:
            sessions = [s for s in sessions if s.project_id == project_id]
        
        return {
            "sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        logger.error(f"Failed to list debug sessions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Performance Profiling Endpoints
@router.post("/profiling/start")
async def start_profiling(
    request: StartProfilingRequest,
    session_id: str = Query(..., description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """Start performance profiling"""
    try:
        profile_session = await performance_profiler.start_profiling(
            debug_session_id=session_id,
            profiler_type=request.profiler_type,
            configuration=request.configuration
        )
        
        return profile_session
        
    except Exception as e:
        logger.error(f"Failed to start profiling: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/profiling/stop/{profile_session_id}")
async def stop_profiling(
    profile_session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Stop performance profiling"""
    try:
        profile_data = await performance_profiler.stop_profiling(profile_session_id)
        return profile_data
        
    except Exception as e:
        logger.error(f"Failed to stop profiling: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profiling/results/{profile_session_id}")
async def get_profiling_results(
    profile_session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get profiling results"""
    try:
        profile_data = await performance_profiler.get_profiling_results(profile_session_id)
        
        if not profile_data:
            raise HTTPException(status_code=404, detail="Profiling results not found")
        
        return profile_data
        
    except Exception as e:
        logger.error(f"Failed to get profiling results: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/profiling/analyze/{profile_session_id}")
async def analyze_performance(
    profile_session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Analyze performance and generate recommendations"""
    try:
        analysis = await performance_profiler.analyze_performance(profile_session_id)
        return analysis
        
    except Exception as e:
        logger.error(f"Failed to analyze performance: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/profiling/sessions")
async def list_profiling_sessions(
    debug_session_id: Optional[str] = Query(None, description="Debug session ID"),
    current_user: User = Depends(get_current_user)
):
    """List profiling sessions"""
    try:
        sessions = list(performance_profiler.profiling_sessions.values())
        
        if debug_session_id:
            sessions = [s for s in sessions if s.debug_session_id == debug_session_id]
        
        return {
            "sessions": sessions,
            "total_count": len(sessions)
        }
        
    except Exception as e:
        logger.error(f"Failed to list profiling sessions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health")
async def debugger_health():
    """Health check for debugger service"""
    return {
        "status": "healthy",
        "service": "advanced_debugger",
        "features": [
            "debug_sessions",
            "breakpoint_management",
            "step_through_debugging",
            "variable_inspection",
            "call_stack_viewing",
            "expression_evaluation",
            "watch_expressions",
            "performance_profiling",
            "memory_analysis",
            "call_graph_profiling"
        ],
        "active_debug_sessions": len(debugger_service.sessions),
        "active_profiling_sessions": len(performance_profiler.profiling_sessions)
    }


# WebSocket endpoint for real-time debug communication
@router.websocket("/ws/{session_id}")
async def debugger_websocket(
    websocket: WebSocket,
    session_id: str
):
    """WebSocket endpoint for real-time debug communication"""
    await websocket.accept()
    
    try:
        # Verify session exists
        if session_id not in debugger_service.sessions:
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": "Debug session not found"
            }))
            return
        
        session = debugger_service.sessions[session_id]
        
        # Send session info
        await websocket.send_text(json.dumps({
            "type": "session_info",
            "data": {
                "session_id": session_id,
                "name": session.name,
                "status": session.status,
                "target_file": session.target_file,
                "language": session.language
            }
        }))
        
        # Main WebSocket loop
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                message_type = message.get("type")
                
                if message_type == "step":
                    # Step through code
                    step_type = message.get("data", {}).get("step_type", "over")
                    count = message.get("data", {}).get("count", 1)
                    
                    from app.schemas.debugger import StepType
                    step_enum = StepType.OVER
                    if step_type == "into":
                        step_enum = StepType.INTO
                    elif step_type == "out":
                        step_enum = StepType.OUT
                    elif step_type == "continue":
                        step_enum = StepType.CONTINUE
                    
                    debug_state = await debugger_service.step(session_id, step_enum, count)
                    
                    await websocket.send_text(json.dumps({
                        "type": "step_result",
                        "data": debug_state.dict()
                    }))
                
                elif message_type == "evaluate":
                    # Evaluate expression
                    expression = message.get("data", {}).get("expression", "")
                    result = await debugger_service.evaluate_expression(session_id, expression)
                    
                    await websocket.send_text(json.dumps({
                        "type": "evaluate_result",
                        "data": result.dict()
                    }))
                
                elif message_type == "get_variables":
                    # Get variables
                    scope = message.get("data", {}).get("scope", "local")
                    from app.schemas.debugger import VariableScope
                    scope_enum = VariableScope.LOCAL
                    if scope == "global":
                        scope_enum = VariableScope.GLOBAL
                    
                    variables = await debugger_service.get_variables(session_id, scope_enum)
                    
                    await websocket.send_text(json.dumps({
                        "type": "variables",
                        "data": {"variables": [v.dict() for v in variables]}
                    }))
                
                elif message_type == "get_call_stack":
                    # Get call stack
                    call_stack = await debugger_service.get_call_stack(session_id)
                    
                    await websocket.send_text(json.dumps({
                        "type": "call_stack",
                        "data": {"call_stack": [frame.dict() for frame in call_stack]}
                    }))
                
                elif message_type == "get_debug_state":
                    # Get debug state
                    debug_state = await debugger_service.get_debug_state(session_id)
                    
                    await websocket.send_text(json.dumps({
                        "type": "debug_state",
                        "data": debug_state.dict()
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
                logger.info(f"WebSocket disconnected for debug session {session_id}")
                break
                
            except Exception as e:
                logger.error(f"WebSocket error for debug session {session_id}: {e}")
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
