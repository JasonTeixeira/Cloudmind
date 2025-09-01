"""
Command History and Auto-completion Service
Intelligent command suggestions and history management
"""

import asyncio
import logging
import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID
from pathlib import Path
import sqlite3
from collections import defaultdict, Counter
import difflib

from app.core.config import settings
from app.schemas.terminal import Suggestion, CommandContext

logger = logging.getLogger(__name__)


class CommandHistoryService:
    """Command history and auto-completion service"""
    
    def __init__(self):
        self.history_db_path = Path(settings.LOCAL_STORAGE_PATH) / "terminal_history.db"
        self.history_db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        
        # In-memory caches for performance
        self.user_history_cache: Dict[UUID, List[Dict[str, Any]]] = {}
        self.command_frequency_cache: Dict[str, int] = {}
        self.suggestion_cache: Dict[str, List[Suggestion]] = {}
        
        # Common commands and their descriptions
        self.common_commands = {
            # File operations
            "ls": "List directory contents",
            "cd": "Change directory",
            "pwd": "Print working directory",
            "mkdir": "Create directory",
            "rm": "Remove files or directories",
            "cp": "Copy files or directories",
            "mv": "Move or rename files",
            "touch": "Create empty file",
            "cat": "Concatenate and display file contents",
            "head": "Display first lines of file",
            "tail": "Display last lines of file",
            "less": "View file contents page by page",
            "more": "View file contents page by page",
            "find": "Find files by name or pattern",
            "grep": "Search for patterns in files",
            
            # System information
            "ps": "Show process status",
            "top": "Show system processes",
            "htop": "Interactive process viewer",
            "df": "Show disk space usage",
            "du": "Show directory space usage",
            "free": "Show memory usage",
            "uname": "Show system information",
            "whoami": "Show current user",
            "id": "Show user and group information",
            "date": "Show current date and time",
            "uptime": "Show system uptime",
            
            # Network
            "ping": "Test network connectivity",
            "curl": "Transfer data from or to a server",
            "wget": "Retrieve files from the web",
            "ssh": "Secure shell client",
            "scp": "Secure copy",
            "rsync": "Remote file synchronization",
            
            # Package management
            "apt": "Debian package manager",
            "apt-get": "Debian package manager",
            "yum": "RPM package manager",
            "dnf": "Modern RPM package manager",
            "brew": "macOS package manager",
            "pip": "Python package installer",
            "npm": "Node.js package manager",
            
            # Development
            "git": "Version control system",
            "python": "Python interpreter",
            "node": "Node.js runtime",
            "npm": "Node.js package manager",
            "docker": "Container platform",
            "docker-compose": "Multi-container Docker applications",
            "kubectl": "Kubernetes command line tool",
            
            # Text processing
            "sed": "Stream editor",
            "awk": "Text processing language",
            "sort": "Sort lines of text",
            "uniq": "Remove duplicate lines",
            "wc": "Word count",
            "cut": "Remove sections from lines",
            "paste": "Merge lines of files",
            
            # Compression
            "tar": "Tape archive",
            "gzip": "Compress files",
            "gunzip": "Decompress files",
            "zip": "Compress files",
            "unzip": "Decompress files",
            
            # Permissions
            "chmod": "Change file permissions",
            "chown": "Change file owner",
            "sudo": "Execute command as superuser",
            "su": "Switch user",
            
            # Process management
            "kill": "Terminate processes",
            "killall": "Kill processes by name",
            "nohup": "Run command immune to hangups",
            "bg": "Move job to background",
            "fg": "Move job to foreground",
            "jobs": "Show background jobs",
            
            # Environment
            "export": "Set environment variable",
            "env": "Show environment variables",
            "source": "Execute commands from file",
            "alias": "Create command alias",
            "unalias": "Remove command alias",
            "history": "Show command history",
            "clear": "Clear terminal screen",
            "reset": "Reset terminal",
        }
        
        # Command categories for better organization
        self.command_categories = {
            "file_operations": ["ls", "cd", "pwd", "mkdir", "rm", "cp", "mv", "touch", "cat", "head", "tail"],
            "system_info": ["ps", "top", "htop", "df", "du", "free", "uname", "whoami", "id", "date", "uptime"],
            "network": ["ping", "curl", "wget", "ssh", "scp", "rsync"],
            "package_management": ["apt", "apt-get", "yum", "dnf", "brew", "pip", "npm"],
            "development": ["git", "python", "node", "npm", "docker", "docker-compose", "kubectl"],
            "text_processing": ["sed", "awk", "sort", "uniq", "wc", "cut", "paste"],
            "compression": ["tar", "gzip", "gunzip", "zip", "unzip"],
            "permissions": ["chmod", "chown", "sudo", "su"],
            "process_management": ["kill", "killall", "nohup", "bg", "fg", "jobs"],
            "environment": ["export", "env", "source", "alias", "unalias", "history", "clear", "reset"]
        }
    
    def _init_database(self):
        """Initialize the command history database"""
        try:
            with sqlite3.connect(self.history_db_path) as conn:
                cursor = conn.cursor()
                
                # Create command history table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS command_history (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        project_id TEXT,
                        command TEXT NOT NULL,
                        working_directory TEXT,
                        exit_code INTEGER,
                        execution_time REAL,
                        success BOOLEAN,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        usage_count INTEGER DEFAULT 1,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create command suggestions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS command_suggestions (
                        id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        command TEXT NOT NULL,
                        description TEXT,
                        category TEXT,
                        relevance_score REAL DEFAULT 1.0,
                        usage_count INTEGER DEFAULT 0,
                        last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_commands ON command_history(user_id, created_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_command_frequency ON command_history(command, usage_count)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_suggestions ON command_suggestions(user_id, relevance_score)")
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Failed to initialize command history database: {e}")
    
    async def save_command(
        self, 
        user_id: UUID, 
        command: str, 
        project_id: Optional[UUID] = None,
        working_directory: str = "",
        exit_code: int = 0,
        execution_time: float = 0.0,
        success: bool = True
    ):
        """Save command to history"""
        try:
            command_id = f"{user_id}_{datetime.utcnow().timestamp()}"
            
            with sqlite3.connect(self.history_db_path) as conn:
                cursor = conn.cursor()
                
                # Check if command already exists for this user
                cursor.execute("""
                    SELECT id, usage_count FROM command_history 
                    WHERE user_id = ? AND command = ? AND working_directory = ?
                """, (str(user_id), command, working_directory))
                
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing command
                    command_id, usage_count = existing
                    cursor.execute("""
                        UPDATE command_history 
                        SET usage_count = ?, last_used = CURRENT_TIMESTAMP, 
                            exit_code = ?, execution_time = ?, success = ?
                        WHERE id = ?
                    """, (usage_count + 1, exit_code, execution_time, success, command_id))
                else:
                    # Insert new command
                    cursor.execute("""
                        INSERT INTO command_history 
                        (id, user_id, project_id, command, working_directory, exit_code, execution_time, success)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (command_id, str(user_id), str(project_id) if project_id else None, 
                         command, working_directory, exit_code, execution_time, success))
                
                conn.commit()
            
            # Update cache
            await self._update_cache(user_id)
            
        except Exception as e:
            logger.error(f"Failed to save command: {e}")
    
    async def get_history(
        self, 
        user_id: UUID, 
        project_id: Optional[UUID] = None,
        limit: int = 100,
        offset: int = 0,
        search_query: str = ""
    ) -> List[Dict[str, Any]]:
        """Get command history for a user"""
        try:
            # Check cache first
            cache_key = f"{user_id}_{project_id}_{limit}_{offset}_{search_query}"
            if cache_key in self.user_history_cache:
                return self.user_history_cache[cache_key]
            
            with sqlite3.connect(self.history_db_path) as conn:
                cursor = conn.cursor()
                
                # Build query
                query = """
                    SELECT id, command, working_directory, exit_code, execution_time, 
                           success, created_at, usage_count, last_used
                    FROM command_history 
                    WHERE user_id = ?
                """
                params = [str(user_id)]
                
                if project_id:
                    query += " AND project_id = ?"
                    params.append(str(project_id))
                
                if search_query:
                    query += " AND command LIKE ?"
                    params.append(f"%{search_query}%")
                
                query += " ORDER BY last_used DESC LIMIT ? OFFSET ?"
                params.extend([limit, offset])
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                # Convert to list of dictionaries
                history = []
                for row in rows:
                    history.append({
                        "id": row[0],
                        "command": row[1],
                        "working_directory": row[2],
                        "exit_code": row[3],
                        "execution_time": row[4],
                        "success": bool(row[5]),
                        "created_at": row[6],
                        "usage_count": row[7],
                        "last_used": row[8]
                    })
                
                # Cache the result
                self.user_history_cache[cache_key] = history
                
                return history
                
        except Exception as e:
            logger.error(f"Failed to get command history: {e}")
            return []
    
    async def get_suggestions(
        self, 
        partial_command: str, 
        context: Optional[CommandContext] = None,
        user_id: Optional[UUID] = None,
        limit: int = 10
    ) -> List[Suggestion]:
        """Get command suggestions based on partial command"""
        try:
            suggestions = []
            
            # 1. Get suggestions from user history
            if user_id:
                user_suggestions = await self._get_user_suggestions(user_id, partial_command, context, limit // 2)
                suggestions.extend(user_suggestions)
            
            # 2. Get suggestions from common commands
            common_suggestions = await self._get_common_suggestions(partial_command, limit // 2)
            suggestions.extend(common_suggestions)
            
            # 3. Get suggestions from file context
            if context and context.file_context:
                file_suggestions = await self._get_file_context_suggestions(partial_command, context, limit // 4)
                suggestions.extend(file_suggestions)
            
            # 4. Get suggestions from recent commands
            if context and context.recent_commands:
                recent_suggestions = await self._get_recent_suggestions(partial_command, context.recent_commands, limit // 4)
                suggestions.extend(recent_suggestions)
            
            # Sort by relevance score and remove duplicates
            unique_suggestions = {}
            for suggestion in suggestions:
                if suggestion.suggestion not in unique_suggestions:
                    unique_suggestions[suggestion.suggestion] = suggestion
                else:
                    # Merge relevance scores
                    unique_suggestions[suggestion.suggestion].relevance_score = max(
                        unique_suggestions[suggestion.suggestion].relevance_score,
                        suggestion.relevance_score
                    )
            
            # Sort by relevance score and limit
            sorted_suggestions = sorted(
                unique_suggestions.values(),
                key=lambda x: x.relevance_score,
                reverse=True
            )
            
            return sorted_suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get suggestions: {e}")
            return []
    
    async def learn_from_usage(
        self, 
        command: str, 
        success: bool, 
        context: Optional[CommandContext] = None,
        user_id: Optional[UUID] = None
    ):
        """Learn from command usage patterns"""
        try:
            if not user_id:
                return
            
            # Update command frequency
            self.command_frequency_cache[command] = self.command_frequency_cache.get(command, 0) + 1
            
            # Update suggestion relevance based on success
            with sqlite3.connect(self.history_db_path) as conn:
                cursor = conn.cursor()
                
                # Update existing suggestion or create new one
                cursor.execute("""
                    INSERT OR REPLACE INTO command_suggestions 
                    (id, user_id, command, usage_count, last_used, relevance_score)
                    VALUES (?, ?, ?, 
                           COALESCE((SELECT usage_count FROM command_suggestions WHERE user_id = ? AND command = ?), 0) + 1,
                           CURRENT_TIMESTAMP,
                           CASE WHEN ? THEN 1.0 ELSE 0.5 END)
                """, (f"{user_id}_{command}", str(user_id), command, str(user_id), command, success))
                
                conn.commit()
            
            # Clear suggestion cache
            self.suggestion_cache.clear()
            
        except Exception as e:
            logger.error(f"Failed to learn from usage: {e}")
    
    async def get_aliases(self, user_id: UUID) -> Dict[str, str]:
        """Get user-defined command aliases"""
        try:
            # This would typically be stored in a separate table
            # For now, return common aliases
            return {
                "ll": "ls -la",
                "la": "ls -A",
                "l": "ls -CF",
                "..": "cd ..",
                "...": "cd ../..",
                "....": "cd ../../..",
                "g": "git",
                "d": "docker",
                "dc": "docker-compose",
                "k": "kubectl"
            }
            
        except Exception as e:
            logger.error(f"Failed to get aliases: {e}")
            return {}
    
    async def _get_user_suggestions(
        self, 
        user_id: UUID, 
        partial_command: str, 
        context: Optional[CommandContext],
        limit: int
    ) -> List[Suggestion]:
        """Get suggestions from user's command history"""
        try:
            with sqlite3.connect(self.history_db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT command, usage_count, last_used, success
                    FROM command_history 
                    WHERE user_id = ? AND command LIKE ? AND success = 1
                    ORDER BY usage_count DESC, last_used DESC
                    LIMIT ?
                """, (str(user_id), f"{partial_command}%", limit))
                
                rows = cursor.fetchall()
                suggestions = []
                
                for row in rows:
                    command, usage_count, last_used, success = row
                    
                    # Calculate relevance score based on usage and recency
                    recency_score = self._calculate_recency_score(last_used)
                    usage_score = min(usage_count / 10.0, 1.0)  # Cap at 1.0
                    relevance_score = (recency_score + usage_score) / 2.0
                    
                    suggestions.append(Suggestion(
                        suggestion=command,
                        description=f"Used {usage_count} times",
                        category="history",
                        relevance_score=relevance_score,
                        usage_count=usage_count,
                        last_used=datetime.fromisoformat(last_used) if last_used else None
                    ))
                
                return suggestions
                
        except Exception as e:
            logger.error(f"Failed to get user suggestions: {e}")
            return []
    
    async def _get_common_suggestions(self, partial_command: str, limit: int) -> List[Suggestion]:
        """Get suggestions from common commands"""
        try:
            suggestions = []
            
            for command, description in self.common_commands.items():
                if command.startswith(partial_command):
                    # Calculate relevance based on command frequency
                    frequency = self.command_frequency_cache.get(command, 1)
                    relevance_score = min(frequency / 100.0, 1.0)
                    
                    # Determine category
                    category = "general"
                    for cat, commands in self.command_categories.items():
                        if command in commands:
                            category = cat
                            break
                    
                    suggestions.append(Suggestion(
                        suggestion=command,
                        description=description,
                        category=category,
                        relevance_score=relevance_score,
                        usage_count=frequency
                    ))
            
            # Sort by relevance and limit
            suggestions.sort(key=lambda x: x.relevance_score, reverse=True)
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get common suggestions: {e}")
            return []
    
    async def _get_file_context_suggestions(
        self, 
        partial_command: str, 
        context: CommandContext, 
        limit: int
    ) -> List[Suggestion]:
        """Get suggestions based on file context"""
        try:
            suggestions = []
            
            # Suggest file operations based on current directory contents
            if any(cmd in partial_command for cmd in ["ls", "cat", "head", "tail", "less", "more"]):
                for file_name in context.file_context:
                    if file_name.startswith(partial_command.split()[-1] if partial_command.split() else ""):
                        full_command = f"{partial_command} {file_name}"
                        suggestions.append(Suggestion(
                            suggestion=full_command,
                            description=f"File: {file_name}",
                            category="file_context",
                            relevance_score=0.8
                        ))
            
            # Suggest directory navigation
            elif "cd" in partial_command:
                for file_name in context.file_context:
                    if os.path.isdir(os.path.join(context.working_directory, file_name)):
                        full_command = f"{partial_command} {file_name}"
                        suggestions.append(Suggestion(
                            suggestion=full_command,
                            description=f"Directory: {file_name}",
                            category="file_context",
                            relevance_score=0.9
                        ))
            
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get file context suggestions: {e}")
            return []
    
    async def _get_recent_suggestions(
        self, 
        partial_command: str, 
        recent_commands: List[str], 
        limit: int
    ) -> List[Suggestion]:
        """Get suggestions from recent commands"""
        try:
            suggestions = []
            
            for command in recent_commands:
                if command.startswith(partial_command):
                    suggestions.append(Suggestion(
                        suggestion=command,
                        description="Recently used",
                        category="recent",
                        relevance_score=0.7
                    ))
            
            return suggestions[:limit]
            
        except Exception as e:
            logger.error(f"Failed to get recent suggestions: {e}")
            return []
    
    def _calculate_recency_score(self, last_used: str) -> float:
        """Calculate recency score based on last usage time"""
        try:
            if not last_used:
                return 0.5
            
            last_used_dt = datetime.fromisoformat(last_used)
            days_ago = (datetime.utcnow() - last_used_dt).days
            
            # Exponential decay: newer commands get higher scores
            if days_ago == 0:
                return 1.0
            elif days_ago <= 7:
                return 0.9
            elif days_ago <= 30:
                return 0.7
            elif days_ago <= 90:
                return 0.5
            else:
                return 0.3
                
        except Exception:
            return 0.5
    
    async def _update_cache(self, user_id: UUID):
        """Update user history cache"""
        try:
            # Clear user-specific cache entries
            keys_to_remove = [key for key in self.user_history_cache.keys() if str(user_id) in key]
            for key in keys_to_remove:
                del self.user_history_cache[key]
                
        except Exception as e:
            logger.error(f"Failed to update cache: {e}")


# Global instance
command_history_service = CommandHistoryService()
