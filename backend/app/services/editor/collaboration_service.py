"""
Real-time Collaboration Service
Enables multiple users to edit files simultaneously
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import List, Dict, Optional, Any, Set
from uuid import UUID, uuid4
from dataclasses import dataclass, asdict

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.services.editor.code_editor_service import code_editor_service

logger = logging.getLogger(__name__)


@dataclass
class CursorPosition:
    """Cursor position for a user"""
    user_id: UUID
    line: int
    column: int
    timestamp: datetime


@dataclass
class TextSelection:
    """Text selection for a user"""
    user_id: UUID
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    timestamp: datetime


@dataclass
class TextChange:
    """Text change operation"""
    user_id: UUID
    session_id: str
    change_type: str  # 'insert', 'delete', 'replace'
    position: int
    text: str
    deleted_text: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class Conflict:
    """Editing conflict"""
    user_id: UUID
    change: TextChange
    conflicting_changes: List[TextChange]
    resolution: str = ""


@dataclass
class Resolution:
    """Conflict resolution"""
    resolved: bool
    final_content: str
    applied_changes: List[TextChange]
    rejected_changes: List[TextChange]


class CollaborationSession:
    """Collaborative editing session"""
    
    def __init__(self, session_id: str, file_path: str, content: str = ""):
        self.session_id = session_id
        self.file_path = file_path
        self.content = content
        self.participants: Set[UUID] = set()
        self.cursor_positions: Dict[UUID, CursorPosition] = {}
        self.selections: Dict[UUID, TextSelection] = {}
        self.change_history: List[TextChange] = []
        self.websocket_connections: Dict[UUID, WebSocket] = {}
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.is_active = True
    
    def add_participant(self, user_id: UUID, websocket: WebSocket):
        """Add participant to session"""
        self.participants.add(user_id)
        self.websocket_connections[user_id] = websocket
        self.last_activity = datetime.utcnow()
        logger.info(f"User {user_id} joined session {self.session_id}")
    
    def remove_participant(self, user_id: UUID):
        """Remove participant from session"""
        self.participants.discard(user_id)
        self.cursor_positions.pop(user_id, None)
        self.selections.pop(user_id, None)
        self.websocket_connections.pop(user_id, None)
        self.last_activity = datetime.utcnow()
        logger.info(f"User {user_id} left session {self.session_id}")
    
    def update_cursor(self, user_id: UUID, line: int, column: int):
        """Update cursor position for user"""
        self.cursor_positions[user_id] = CursorPosition(
            user_id=user_id,
            line=line,
            column=column,
            timestamp=datetime.utcnow()
        )
        self.last_activity = datetime.utcnow()
    
    def update_selection(self, user_id: UUID, start_line: int, start_column: int, 
                        end_line: int, end_column: int):
        """Update text selection for user"""
        self.selections[user_id] = TextSelection(
            user_id=user_id,
            start_line=start_line,
            start_column=start_column,
            end_line=end_line,
            end_column=end_column,
            timestamp=datetime.utcnow()
        )
        self.last_activity = datetime.utcnow()
    
    def apply_change(self, change: TextChange) -> bool:
        """Apply text change to content"""
        try:
            if change.change_type == 'insert':
                self.content = (
                    self.content[:change.position] + 
                    change.text + 
                    self.content[change.position:]
                )
            elif change.change_type == 'delete':
                self.content = (
                    self.content[:change.position] + 
                    self.content[change.position + len(change.deleted_text):]
                )
            elif change.change_type == 'replace':
                self.content = (
                    self.content[:change.position] + 
                    change.text + 
                    self.content[change.position + len(change.deleted_text):]
                )
            
            self.change_history.append(change)
            self.last_activity = datetime.utcnow()
            return True
            
        except Exception as e:
            logger.error(f"Failed to apply change: {e}")
            return False
    
    def get_cursor_positions(self) -> List[CursorPosition]:
        """Get all cursor positions"""
        return list(self.cursor_positions.values())
    
    def get_selections(self) -> List[TextSelection]:
        """Get all text selections"""
        return list(self.selections.values())
    
    def is_empty(self) -> bool:
        """Check if session has no participants"""
        return len(self.participants) == 0


class CollaborationService:
    """Real-time collaborative editing service"""
    
    def __init__(self):
        self.active_sessions: Dict[str, CollaborationSession] = {}
        self.user_sessions: Dict[UUID, Set[str]] = {}  # user_id -> set of session_ids
    
    async def join_session(self, session_id: str, user_id: UUID, 
                          websocket: WebSocket) -> CollaborationSession:
        """Join collaborative editing session"""
        try:
            # Get or create session
            if session_id not in self.active_sessions:
                # Get session info from code editor service
                editor_session = await code_editor_service.get_session_info(session_id)
                if not editor_session:
                    raise ValueError("Editor session not found")
                
                collaboration_session = CollaborationSession(
                    session_id=session_id,
                    file_path=editor_session.file_path,
                    content=editor_session.content
                )
                self.active_sessions[session_id] = collaboration_session
            else:
                collaboration_session = self.active_sessions[session_id]
            
            # Add participant
            collaboration_session.add_participant(user_id, websocket)
            
            # Track user sessions
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = set()
            self.user_sessions[user_id].add(session_id)
            
            # Send current state to new participant
            await self._send_session_state(collaboration_session, user_id)
            
            # Notify other participants
            await self._broadcast_participant_joined(collaboration_session, user_id)
            
            logger.info(f"User {user_id} joined collaboration session {session_id}")
            return collaboration_session
            
        except Exception as e:
            logger.error(f"Failed to join session {session_id}: {e}")
            raise
    
    async def leave_session(self, session_id: str, user_id: UUID):
        """Leave collaborative editing session"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.remove_participant(user_id)
                
                # Remove from user sessions tracking
                if user_id in self.user_sessions:
                    self.user_sessions[user_id].discard(session_id)
                
                # Notify other participants
                await self._broadcast_participant_left(session, user_id)
                
                # Clean up empty sessions
                if session.is_empty():
                    del self.active_sessions[session_id]
                    logger.info(f"Cleaned up empty session {session_id}")
                
                logger.info(f"User {user_id} left session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to leave session {session_id}: {e}")
    
    async def broadcast_change(self, session_id: str, change: TextChange):
        """Broadcast text change to all participants"""
        try:
            if session_id not in self.active_sessions:
                return
            
            session = self.active_sessions[session_id]
            
            # Apply change to session content
            if session.apply_change(change):
                # Broadcast to all participants except the sender
                await self._broadcast_change_to_participants(session, change)
                
                # Update code editor session
                await self._update_editor_session(session_id, session.content)
                
                logger.debug(f"Broadcasted change in session {session_id}")
            
        except Exception as e:
            logger.error(f"Failed to broadcast change: {e}")
    
    async def update_cursor_position(self, session_id: str, user_id: UUID, 
                                   line: int, column: int):
        """Update and broadcast cursor position"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.update_cursor(user_id, line, column)
                
                # Broadcast cursor position to other participants
                await self._broadcast_cursor_position(session, user_id, line, column)
        
        except Exception as e:
            logger.error(f"Failed to update cursor position: {e}")
    
    async def update_text_selection(self, session_id: str, user_id: UUID,
                                  start_line: int, start_column: int,
                                  end_line: int, end_column: int):
        """Update and broadcast text selection"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.update_selection(user_id, start_line, start_column, 
                                       end_line, end_column)
                
                # Broadcast selection to other participants
                await self._broadcast_text_selection(session, user_id, 
                                                   start_line, start_column,
                                                   end_line, end_column)
        
        except Exception as e:
            logger.error(f"Failed to update text selection: {e}")
    
    async def get_cursor_positions(self, session_id: str) -> List[CursorPosition]:
        """Get all cursor positions for a session"""
        if session_id in self.active_sessions:
            return self.active_sessions[session_id].get_cursor_positions()
        return []
    
    async def resolve_conflicts(self, session_id: str, 
                              conflicts: List[Conflict]) -> Resolution:
        """Resolve editing conflicts"""
        try:
            if session_id not in self.active_sessions:
                return Resolution(resolved=False, final_content="", 
                                applied_changes=[], rejected_changes=[])
            
            session = self.active_sessions[session_id]
            applied_changes = []
            rejected_changes = []
            
            # Simple conflict resolution: apply changes in timestamp order
            sorted_conflicts = sorted(conflicts, 
                                    key=lambda c: c.change.timestamp)
            
            for conflict in sorted_conflicts:
                # Check if change can be applied without conflicts
                if self._can_apply_change(session.content, conflict.change):
                    session.apply_change(conflict.change)
                    applied_changes.append(conflict.change)
                else:
                    rejected_changes.append(conflict.change)
            
            return Resolution(
                resolved=len(rejected_changes) == 0,
                final_content=session.content,
                applied_changes=applied_changes,
                rejected_changes=rejected_changes
            )
            
        except Exception as e:
            logger.error(f"Failed to resolve conflicts: {e}")
            return Resolution(resolved=False, final_content="", 
                            applied_changes=[], rejected_changes=[])
    
    def _can_apply_change(self, content: str, change: TextChange) -> bool:
        """Check if change can be applied without conflicts"""
        try:
            if change.position > len(content):
                return False
            
            if change.change_type == 'delete':
                if change.position + len(change.deleted_text) > len(content):
                    return False
                return content[change.position:change.position + len(change.deleted_text)] == change.deleted_text
            
            return True
            
        except Exception:
            return False
    
    async def _send_session_state(self, session: CollaborationSession, user_id: UUID):
        """Send current session state to user"""
        try:
            websocket = session.websocket_connections.get(user_id)
            if websocket:
                state_message = {
                    "type": "session_state",
                    "content": session.content,
                    "participants": list(session.participants),
                    "cursor_positions": [asdict(pos) for pos in session.get_cursor_positions()],
                    "selections": [asdict(sel) for sel in session.get_selections()]
                }
                await websocket.send_text(json.dumps(state_message))
        
        except Exception as e:
            logger.error(f"Failed to send session state: {e}")
    
    async def _broadcast_participant_joined(self, session: CollaborationSession, user_id: UUID):
        """Broadcast participant joined message"""
        try:
            message = {
                "type": "participant_joined",
                "user_id": str(user_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_participants(session, message, exclude_user=user_id)
        
        except Exception as e:
            logger.error(f"Failed to broadcast participant joined: {e}")
    
    async def _broadcast_participant_left(self, session: CollaborationSession, user_id: UUID):
        """Broadcast participant left message"""
        try:
            message = {
                "type": "participant_left",
                "user_id": str(user_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_participants(session, message)
        
        except Exception as e:
            logger.error(f"Failed to broadcast participant left: {e}")
    
    async def _broadcast_change_to_participants(self, session: CollaborationSession, change: TextChange):
        """Broadcast text change to participants"""
        try:
            message = {
                "type": "text_change",
                "change": asdict(change)
            }
            await self._broadcast_to_participants(session, message, exclude_user=change.user_id)
        
        except Exception as e:
            logger.error(f"Failed to broadcast change: {e}")
    
    async def _broadcast_cursor_position(self, session: CollaborationSession, 
                                       user_id: UUID, line: int, column: int):
        """Broadcast cursor position to participants"""
        try:
            message = {
                "type": "cursor_position",
                "user_id": str(user_id),
                "line": line,
                "column": column,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_participants(session, message, exclude_user=user_id)
        
        except Exception as e:
            logger.error(f"Failed to broadcast cursor position: {e}")
    
    async def _broadcast_text_selection(self, session: CollaborationSession,
                                      user_id: UUID, start_line: int, start_column: int,
                                      end_line: int, end_column: int):
        """Broadcast text selection to participants"""
        try:
            message = {
                "type": "text_selection",
                "user_id": str(user_id),
                "start_line": start_line,
                "start_column": start_column,
                "end_line": end_line,
                "end_column": end_column,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self._broadcast_to_participants(session, message, exclude_user=user_id)
        
        except Exception as e:
            logger.error(f"Failed to broadcast text selection: {e}")
    
    async def _broadcast_to_participants(self, session: CollaborationSession, 
                                       message: dict, exclude_user: UUID = None):
        """Broadcast message to all participants"""
        try:
            message_json = json.dumps(message)
            for user_id, websocket in session.websocket_connections.items():
                if user_id != exclude_user:
                    try:
                        await websocket.send_text(message_json)
                    except Exception as e:
                        logger.warning(f"Failed to send message to user {user_id}: {e}")
                        # Remove disconnected user
                        session.remove_participant(user_id)
        
        except Exception as e:
            logger.error(f"Failed to broadcast message: {e}")
    
    async def _update_editor_session(self, session_id: str, content: str):
        """Update code editor session with new content"""
        try:
            editor_session = await code_editor_service.get_session_info(session_id)
            if editor_session:
                editor_session.content = content
                editor_session.last_modified = datetime.utcnow()
        
        except Exception as e:
            logger.error(f"Failed to update editor session: {e}")
    
    async def get_user_sessions(self, user_id: UUID) -> List[str]:
        """Get all sessions for a user"""
        return list(self.user_sessions.get(user_id, set()))
    
    async def cleanup_inactive_sessions(self):
        """Clean up inactive sessions"""
        try:
            current_time = datetime.utcnow()
            inactive_sessions = []
            
            for session_id, session in self.active_sessions.items():
                # Check if session has been inactive for more than 1 hour
                if (current_time - session.last_activity).total_seconds() > 3600:
                    inactive_sessions.append(session_id)
            
            for session_id in inactive_sessions:
                del self.active_sessions[session_id]
                logger.info(f"Cleaned up inactive session {session_id}")
        
        except Exception as e:
            logger.error(f"Failed to cleanup inactive sessions: {e}")


# Global instance
collaboration_service = CollaborationService()
