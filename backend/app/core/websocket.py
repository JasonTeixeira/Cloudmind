"""
Advanced WebSocket Manager for Real-time Communication
"""

import asyncio
import json
import logging
from typing import Dict, Set, Optional, Any, Callable
from datetime import datetime, timedelta
from uuid import uuid4
import jwt
from fastapi import WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.project import Project
from app.models.cost_analysis import CostAnalysis
from app.models.security_scan import SecurityScan
from app.models.infrastructure import Infrastructure
from app.models.ai_insight import AIInsight
from app.services.ai_engine import AIEngineService
from app.services.cost_optimization import CostOptimizationService
from app.services.security_audit import SecurityAuditService

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Advanced WebSocket connection manager with authentication and message queuing"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, Set[str]] = {}  # user_id -> set of connection_ids
        self.connection_users: Dict[str, str] = {}  # connection_id -> user_id
        self.message_queue: Dict[str, asyncio.Queue] = {}
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
        
    async def connect(self, websocket: WebSocket, token: Optional[str] = None) -> str:
        """Connect a new WebSocket with authentication"""
        await websocket.accept()
        
        connection_id = str(uuid4())
        user_id = None
        
        # Authenticate user if token provided
        if token:
            try:
                user_id = await self._authenticate_user(token)
                if user_id:
                    # Track user connections
                    if user_id not in self.user_connections:
                        self.user_connections[user_id] = set()
                    self.user_connections[user_id].add(connection_id)
                    self.connection_users[connection_id] = user_id
                    
                    logger.info(f"✅ WebSocket connected for user {user_id}")
                else:
                    logger.warning("⚠️ WebSocket connection without valid authentication")
            except Exception as e:
                logger.error(f"❌ WebSocket authentication failed: {str(e)}")
        
        # Store connection
        self.active_connections[connection_id] = websocket
        self.message_queue[connection_id] = asyncio.Queue()
        self.connection_metadata[connection_id] = {
            "connected_at": datetime.utcnow(),
            "user_id": user_id,
            "last_activity": datetime.utcnow()
        }
        
        # Send welcome message
        await self.send_personal_message(connection_id, {
            "type": "connection_established",
            "connection_id": connection_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return connection_id
    
    async def disconnect(self, connection_id: str):
        """Disconnect a WebSocket connection"""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            await websocket.close()
            
            # Clean up user tracking
            user_id = self.connection_users.get(connection_id)
            if user_id and user_id in self.user_connections:
                self.user_connections[user_id].discard(connection_id)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
            
            # Clean up connection data
            del self.active_connections[connection_id]
            del self.connection_users[connection_id]
            del self.connection_metadata[connection_id]
            
            if connection_id in self.message_queue:
                del self.message_queue[connection_id]
            
            logger.info(f"🔌 WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(self, connection_id: str, message: Dict[str, Any]):
        """Send message to specific connection"""
        if connection_id in self.active_connections:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.send_text(json.dumps(message))
                self.connection_metadata[connection_id]["last_activity"] = datetime.utcnow()
            except Exception as e:
                logger.error(f"❌ Failed to send message to {connection_id}: {str(e)}")
                await self.disconnect(connection_id)
    
    async def broadcast(self, message: Dict[str, Any], exclude_connection: Optional[str] = None):
        """Broadcast message to all connections"""
        disconnected = []
        
        for connection_id, websocket in self.active_connections.items():
            if connection_id != exclude_connection:
                try:
                    await websocket.send_text(json.dumps(message))
                    self.connection_metadata[connection_id]["last_activity"] = datetime.utcnow()
                except Exception as e:
                    logger.error(f"❌ Failed to broadcast to {connection_id}: {str(e)}")
                    disconnected.append(connection_id)
        
        # Clean up disconnected connections
        for connection_id in disconnected:
            await self.disconnect(connection_id)
    
    async def send_to_user(self, user_id: str, message: Dict[str, Any]):
        """Send message to all connections of a specific user"""
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id]:
                await self.send_personal_message(connection_id, message)
    
    async def send_to_project(self, project_id: str, message: Dict[str, Any]):
        """Send message to all users in a specific project"""
        # This would require project membership tracking
        # For now, broadcast to all authenticated users
        for user_id in self.user_connections:
            await self.send_to_user(user_id, message)
    
    async def _authenticate_user(self, token: str) -> Optional[str]:
        """Authenticate user from JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            if user_id:
                return user_id
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
        except jwt.JWTError as e:
            logger.error(f"JWT validation error: {str(e)}")
        
        return None
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "total_users": len(self.user_connections),
            "connections_per_user": {
                user_id: len(connections) 
                for user_id, connections in self.user_connections.items()
            },
            "connection_metadata": self.connection_metadata
        }
    
    async def cleanup_inactive_connections(self, max_idle_minutes: int = 30):
        """Clean up inactive connections"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=max_idle_minutes)
        inactive_connections = []
        
        for connection_id, metadata in self.connection_metadata.items():
            if metadata["last_activity"] < cutoff_time:
                inactive_connections.append(connection_id)
        
        for connection_id in inactive_connections:
            await self.disconnect(connection_id)
        
        if inactive_connections:
            logger.info(f"🧹 Cleaned up {len(inactive_connections)} inactive connections")


# Global connection manager instance
manager = ConnectionManager()


class WebSocketHandler:
    """WebSocket handler with advanced features"""
    
    def __init__(self):
        self.manager = manager
    
    async def handle_websocket(self, websocket: WebSocket, token: Optional[str] = None):
        """Handle WebSocket connection with full lifecycle management"""
        connection_id = await self.manager.connect(websocket, token)
        
        try:
            # Start message processing task
            process_task = asyncio.create_task(
                self._process_messages(connection_id, websocket)
            )
            
            # Start heartbeat task
            heartbeat_task = asyncio.create_task(
                self._heartbeat(connection_id)
            )
            
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [process_task, heartbeat_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel remaining tasks
            for task in pending:
                task.cancel()
            
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {connection_id}")
        except Exception as e:
            logger.error(f"❌ WebSocket error for {connection_id}: {str(e)}")
        finally:
            await self.manager.disconnect(connection_id)
    
    async def _process_messages(self, connection_id: str, websocket: WebSocket):
        """Process incoming WebSocket messages"""
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Update last activity
                self.manager.connection_metadata[connection_id]["last_activity"] = datetime.utcnow()
                
                # Handle different message types
                await self._handle_message(connection_id, message)
                
        except WebSocketDisconnect:
            raise
        except Exception as e:
            logger.error(f"❌ Message processing error: {str(e)}")
            await self.manager.send_personal_message(connection_id, {
                "type": "error",
                "message": "Message processing failed",
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def _handle_message(self, connection_id: str, message: Dict[str, Any]):
        """Handle different types of WebSocket messages"""
        message_type = message.get("type")
        
        if message_type == "ping":
            await self.manager.send_personal_message(connection_id, {
                "type": "pong",
                "timestamp": datetime.utcnow().isoformat()
            })
        
        elif message_type == "subscribe":
            # Handle subscription to specific channels
            channel = message.get("channel")
            if channel:
                await self._subscribe_to_channel(connection_id, channel)
        
        elif message_type == "unsubscribe":
            # Handle unsubscription from channels
            channel = message.get("channel")
            if channel:
                await self._unsubscribe_from_channel(connection_id, channel)
        
        elif message_type == "chat":
            # Handle chat messages
            await self._handle_chat_message(connection_id, message)
        
        else:
            # Unknown message type
            await self.manager.send_personal_message(connection_id, {
                "type": "error",
                "message": f"Unknown message type: {message_type}",
                "timestamp": datetime.utcnow().isoformat()
            })
    
    async def _subscribe_to_channel(self, connection_id: str, channel: str):
        """Subscribe to a specific channel"""
        # Implementation for channel subscription
        await self.manager.send_personal_message(connection_id, {
            "type": "subscribed",
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def _unsubscribe_from_channel(self, connection_id: str, channel: str):
        """Unsubscribe from a specific channel"""
        # Implementation for channel unsubscription
        await self.manager.send_personal_message(connection_id, {
            "type": "unsubscribed",
            "channel": channel,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def _handle_chat_message(self, connection_id: str, message: Dict[str, Any]):
        """Handle chat messages"""
        # Broadcast chat message to all connections
        await self.manager.broadcast({
            "type": "chat",
            "message": message.get("message"),
            "user_id": self.manager.connection_users.get(connection_id),
            "timestamp": datetime.utcnow().isoformat()
        }, exclude_connection=connection_id)
    
    async def _heartbeat(self, connection_id: str):
        """Send periodic heartbeat to keep connection alive"""
        while connection_id in self.manager.active_connections:
            try:
                await asyncio.sleep(30)  # Send heartbeat every 30 seconds
                await self.manager.send_personal_message(connection_id, {
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })
            except Exception as e:
                logger.error(f"❌ Heartbeat failed for {connection_id}: {str(e)}")
                break


# Global WebSocket handler instance
websocket_handler = WebSocketHandler() 