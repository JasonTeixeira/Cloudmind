"""
WebSocket API Router - Real-time Communication Endpoints
"""

import logging
from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from datetime import datetime

from app.core.websocket import websocket_handler
from app.core.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint for real-time communication"""
    await websocket_handler.handle_websocket(websocket)


@router.websocket("/ws/authenticated")
async def authenticated_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """Authenticated WebSocket endpoint"""
    # Extract token from query parameters or headers
    if not token:
        # Try to get token from query parameters
        token = websocket.query_params.get("token")
    
    if not token:
        # Try to get token from headers
        auth_header = websocket.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/notifications")
async def notifications_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time notifications"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/metrics")
async def metrics_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time metrics streaming"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/cost-analysis")
async def cost_analysis_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time cost analysis updates"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/security-alerts")
async def security_alerts_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time security alerts"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/infrastructure")
async def infrastructure_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time infrastructure updates"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/ai-insights")
async def ai_insights_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time AI insights"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.websocket("/ws/chat")
async def chat_websocket_endpoint(websocket: WebSocket, token: Optional[str] = None):
    """WebSocket endpoint for real-time chat functionality"""
    # Extract token from query parameters
    if not token:
        token = websocket.query_params.get("token")
    
    await websocket_handler.handle_websocket(websocket, token)


@router.get("/ws/status")
async def websocket_status():
    """Get WebSocket connection status and statistics"""
    stats = websocket_handler.manager.get_connection_stats()
    return {
        "status": "operational",
        "connections": stats["total_connections"],
        "active_users": stats["total_users"],
        "connections_per_user": stats["connections_per_user"],
        "timestamp": datetime.utcnow().isoformat()
    } 