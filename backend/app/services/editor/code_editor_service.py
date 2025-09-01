"""
World-Class Code Editor Service
Provides professional IDE-like code editing capabilities
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID, uuid4
import json
import re
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import pygments
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name

from app.models.project_storage import ProjectFile
from app.core.database import get_db
from app.core.config import settings
from app.services.storage.file_storage_service import FileStorageService

logger = logging.getLogger(__name__)


class Token:
    """Syntax highlighting token"""
    def __init__(self, type: str, value: str, start: int, end: int, line: int):
        self.type = type
        self.value = value
        self.start = start
        self.end = end
        self.line = line


class Suggestion:
    """Autocomplete suggestion"""
    def __init__(self, text: str, type: str, description: str = "", detail: str = ""):
        self.text = text
        self.type = type
        self.description = description
        self.detail = detail


class Diagnostic:
    """Code diagnostic/error"""
    def __init__(self, message: str, severity: str, line: int, column: int, end_line: int = None, end_column: int = None):
        self.message = message
        self.severity = severity  # error, warning, info, hint
        self.line = line
        self.column = column
        self.end_line = end_line or line
        self.end_column = end_column or column


class EditorSession:
    """Editor session for a file"""
    def __init__(self, session_id: str, file_path: str, user_id: UUID, content: str = ""):
        self.session_id = session_id
        self.file_path = file_path
        self.user_id = user_id
        self.content = content
        self.language = self._detect_language(file_path)
        self.created_at = datetime.utcnow()
        self.last_modified = datetime.utcnow()
        self.collaborators = set()
        self.cursor_positions = {}
        self.selections = {}
        self.breakpoints = set()
        self.folded_lines = set()
        self.bookmarks = set()


class CodeEditorService:
    """World-class code editor service"""
    
    def __init__(self):
        self.file_storage = FileStorageService()
        self.active_sessions: Dict[str, EditorSession] = {}
        self.language_servers: Dict[str, Any] = {}
        self._init_language_support()
    
    def _init_language_support(self):
        """Initialize language support"""
        self.supported_languages = {
            # Programming Languages
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.jsx': 'javascript', '.tsx': 'typescript', '.java': 'java',
            '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.go': 'go', '.rs': 'rust',
            '.php': 'php', '.rb': 'ruby', '.swift': 'swift', '.kt': 'kotlin',
            '.scala': 'scala', '.clj': 'clojure', '.hs': 'haskell',
            
            # Web Technologies
            '.html': 'html', '.css': 'css', '.scss': 'scss', '.sass': 'sass',
            '.less': 'less', '.xml': 'xml', '.json': 'json', '.yaml': 'yaml',
            '.yml': 'yaml', '.toml': 'toml', '.ini': 'ini', '.conf': 'ini',
            
            # Configuration & Data
            '.sql': 'sql', '.sh': 'bash', '.bat': 'batch', '.ps1': 'powershell',
            '.dockerfile': 'dockerfile', '.tf': 'hcl', '.env': 'properties',
            '.md': 'markdown', '.rst': 'rst', '.tex': 'latex',
            
            # Other
            '.txt': 'text', '.log': 'text', '.csv': 'csv'
        }
        
        # Initialize Pygments lexers for syntax highlighting
        self.lexers = {}
        for ext, lang in self.supported_languages.items():
            try:
                self.lexers[ext] = get_lexer_by_name(lang)
            except:
                self.lexers[ext] = TextLexer()
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file path"""
        ext = Path(file_path).suffix.lower()
        return self.supported_languages.get(ext, 'text')
    
    async def open_file(self, file_path: str, user_id: UUID) -> EditorSession:
        """Open file in editor with full context"""
        try:
            # Check if session already exists
            session_id = f"{user_id}_{file_path}"
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.collaborators.add(user_id)
                return session
            
            # Load file content
            content = ""
            try:
                # Try to get from project storage first
                project_id = self._extract_project_id(file_path)
                if project_id:
                    file_content, _ = await self.file_storage.download_file(project_id, file_path)
                    content = file_content.decode('utf-8')
            except:
                # Fallback to local file system
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    content = ""
            
            # Create new session
            session = EditorSession(session_id, file_path, user_id, content)
            session.collaborators.add(user_id)
            self.active_sessions[session_id] = session
            
            logger.info(f"Opened file {file_path} for user {user_id}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to open file {file_path}: {e}")
            raise
    
    async def save_file(self, session_id: str, content: str, user_id: UUID) -> bool:
        """Save file with version control"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("Session not found")
            
            session = self.active_sessions[session_id]
            if user_id not in session.collaborators:
                raise ValueError("User not authorized for this session")
            
            # Update session content
            session.content = content
            session.last_modified = datetime.utcnow()
            
            # Save to storage
            project_id = self._extract_project_id(session.file_path)
            if project_id:
                # Save to project storage
                content_bytes = content.encode('utf-8')
                await self.file_storage.upload_file(
                    project_id=project_id,
                    file_path=session.file_path,
                    content=content_bytes,
                    user_id=user_id,
                    commit_message=f"Updated by {user_id}"
                )
            else:
                # Save to local file system
                with open(session.file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            logger.info(f"Saved file {session.file_path} for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            return False
    
    async def get_syntax_highlighting(self, content: str, language: str) -> List[Token]:
        """Get syntax highlighting tokens"""
        try:
            tokens = []
            lexer = get_lexer_by_name(language)
            
            # Tokenize content
            for token_type, value in lexer.get_tokens(content):
                # Calculate position
                start = len(''.join(t[1] for t in tokens))
                end = start + len(value)
                
                # Calculate line number
                line = content[:start].count('\n') + 1
                
                tokens.append(Token(
                    type=str(token_type),
                    value=value,
                    start=start,
                    end=end,
                    line=line
                ))
            
            return tokens
            
        except Exception as e:
            logger.error(f"Failed to get syntax highlighting: {e}")
            return []
    
    async def get_autocomplete(self, content: str, cursor_pos: int, language: str) -> List[Suggestion]:
        """Get intelligent autocomplete suggestions"""
        try:
            suggestions = []
            
            # Get context around cursor
            context = self._get_context_around_cursor(content, cursor_pos)
            
            # Language-specific autocomplete
            if language == 'python':
                suggestions.extend(await self._get_python_suggestions(context, cursor_pos))
            elif language == 'javascript':
                suggestions.extend(await self._get_javascript_suggestions(context, cursor_pos))
            elif language == 'typescript':
                suggestions.extend(await self._get_typescript_suggestions(context, cursor_pos))
            else:
                # Generic suggestions
                suggestions.extend(await self._get_generic_suggestions(context, cursor_pos))
            
            return suggestions[:50]  # Limit to 50 suggestions
            
        except Exception as e:
            logger.error(f"Failed to get autocomplete: {e}")
            return []
    
    async def validate_syntax(self, content: str, language: str) -> List[Diagnostic]:
        """Validate code syntax and return diagnostics"""
        try:
            diagnostics = []
            
            if language == 'python':
                diagnostics.extend(await self._validate_python(content))
            elif language == 'javascript':
                diagnostics.extend(await self._validate_javascript(content))
            elif language == 'typescript':
                diagnostics.extend(await self._validate_typescript(content))
            else:
                # Basic validation for other languages
                diagnostics.extend(await self._validate_generic(content, language))
            
            return diagnostics
            
        except Exception as e:
            logger.error(f"Failed to validate syntax: {e}")
            return []
    
    def _get_context_around_cursor(self, content: str, cursor_pos: int, context_size: int = 100) -> str:
        """Get context around cursor position"""
        start = max(0, cursor_pos - context_size)
        end = min(len(content), cursor_pos + context_size)
        return content[start:end]
    
    async def _get_python_suggestions(self, context: str, cursor_pos: int) -> List[Suggestion]:
        """Get Python-specific autocomplete suggestions"""
        suggestions = []
        
        # Common Python keywords
        keywords = [
            'def', 'class', 'import', 'from', 'as', 'if', 'else', 'elif',
            'for', 'while', 'try', 'except', 'finally', 'with', 'return',
            'yield', 'raise', 'assert', 'pass', 'break', 'continue',
            'True', 'False', 'None', 'self', 'super'
        ]
        
        # Common Python built-ins
        builtins = [
            'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set',
            'tuple', 'range', 'enumerate', 'zip', 'map', 'filter', 'sorted',
            'min', 'max', 'sum', 'abs', 'round', 'type', 'isinstance'
        ]
        
        # Add suggestions based on context
        for keyword in keywords:
            suggestions.append(Suggestion(keyword, 'keyword', f'Python keyword: {keyword}'))
        
        for builtin in builtins:
            suggestions.append(Suggestion(builtin, 'function', f'Built-in function: {builtin}'))
        
        return suggestions
    
    async def _get_javascript_suggestions(self, context: str, cursor_pos: int) -> List[Suggestion]:
        """Get JavaScript-specific autocomplete suggestions"""
        suggestions = []
        
        # Common JavaScript keywords
        keywords = [
            'function', 'var', 'let', 'const', 'if', 'else', 'for', 'while',
            'try', 'catch', 'finally', 'throw', 'return', 'break', 'continue',
            'switch', 'case', 'default', 'class', 'extends', 'super', 'new',
            'this', 'null', 'undefined', 'true', 'false'
        ]
        
        # Common JavaScript built-ins
        builtins = [
            'console', 'Math', 'Date', 'Array', 'Object', 'String', 'Number',
            'Boolean', 'RegExp', 'JSON', 'Promise', 'Set', 'Map', 'Symbol'
        ]
        
        for keyword in keywords:
            suggestions.append(Suggestion(keyword, 'keyword', f'JavaScript keyword: {keyword}'))
        
        for builtin in builtins:
            suggestions.append(Suggestion(builtin, 'class', f'Built-in object: {builtin}'))
        
        return suggestions
    
    async def _get_typescript_suggestions(self, context: str, cursor_pos: int) -> List[Suggestion]:
        """Get TypeScript-specific autocomplete suggestions"""
        suggestions = []
        
        # TypeScript-specific keywords
        typescript_keywords = [
            'interface', 'type', 'enum', 'namespace', 'module', 'declare',
            'export', 'import', 'public', 'private', 'protected', 'static',
            'readonly', 'abstract', 'implements', 'extends', 'keyof', 'typeof',
            'infer', 'never', 'unknown', 'any', 'void', 'undefined', 'null'
        ]
        
        # Add TypeScript suggestions
        for keyword in typescript_keywords:
            suggestions.append(Suggestion(keyword, 'keyword', f'TypeScript keyword: {keyword}'))
        
        # Add JavaScript suggestions as well
        js_suggestions = await self._get_javascript_suggestions(context, cursor_pos)
        suggestions.extend(js_suggestions)
        
        return suggestions
    
    async def _get_generic_suggestions(self, context: str, cursor_pos: int) -> List[Suggestion]:
        """Get generic autocomplete suggestions"""
        suggestions = []
        
        # Common programming patterns
        patterns = [
            'function', 'class', 'if', 'else', 'for', 'while', 'try', 'catch',
            'return', 'import', 'export', 'const', 'let', 'var', 'public', 'private'
        ]
        
        for pattern in patterns:
            suggestions.append(Suggestion(pattern, 'keyword', f'Common pattern: {pattern}'))
        
        return suggestions
    
    async def _validate_python(self, content: str) -> List[Diagnostic]:
        """Validate Python syntax"""
        diagnostics = []
        
        try:
            # Basic Python syntax validation
            compile(content, '<string>', 'exec')
        except SyntaxError as e:
            diagnostics.append(Diagnostic(
                message=str(e),
                severity='error',
                line=e.lineno or 1,
                column=e.offset or 1
            ))
        except Exception as e:
            diagnostics.append(Diagnostic(
                message=f"Validation error: {str(e)}",
                severity='error',
                line=1,
                column=1
            ))
        
        return diagnostics
    
    async def _validate_javascript(self, content: str) -> List[Diagnostic]:
        """Validate JavaScript syntax"""
        diagnostics = []
        
        # Basic JavaScript validation patterns
        # Check for common syntax errors
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for unmatched brackets
            if line.count('{') != line.count('}'):
                diagnostics.append(Diagnostic(
                    message="Unmatched curly braces",
                    severity='warning',
                    line=i,
                    column=1
                ))
            
            # Check for unmatched parentheses
            if line.count('(') != line.count(')'):
                diagnostics.append(Diagnostic(
                    message="Unmatched parentheses",
                    severity='warning',
                    line=i,
                    column=1
                ))
        
        return diagnostics
    
    async def _validate_typescript(self, content: str) -> List[Diagnostic]:
        """Validate TypeScript syntax"""
        diagnostics = []
        
        # TypeScript-specific validation
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for TypeScript-specific syntax
            if 'interface' in line and not line.strip().endswith('{'):
                diagnostics.append(Diagnostic(
                    message="Interface declaration should end with '{'",
                    severity='error',
                    line=i,
                    column=1
                ))
            
            # Check for type annotations
            if ':' in line and 'function' in line:
                # Basic function type validation
                pass
        
        return diagnostics
    
    async def _validate_generic(self, content: str, language: str) -> List[Diagnostic]:
        """Generic syntax validation"""
        diagnostics = []
        
        # Basic validation for any language
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            # Check for very long lines
            if len(line) > 120:
                diagnostics.append(Diagnostic(
                    message="Line too long (consider breaking it)",
                    severity='warning',
                    line=i,
                    column=120
                ))
            
            # Check for trailing whitespace
            if line.rstrip() != line:
                diagnostics.append(Diagnostic(
                    message="Trailing whitespace",
                    severity='warning',
                    line=i,
                    column=len(line.rstrip()) + 1
                ))
        
        return diagnostics
    
    def _extract_project_id(self, file_path: str) -> Optional[UUID]:
        """Extract project ID from file path"""
        try:
            # This is a simplified implementation
            # In a real system, you'd have a mapping of file paths to project IDs
            parts = file_path.split('/')
            if len(parts) > 2 and parts[0] == 'projects':
                return UUID(parts[1])
            return None
        except:
            return None
    
    async def close_session(self, session_id: str, user_id: UUID) -> bool:
        """Close editor session"""
        try:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session.collaborators.discard(user_id)
                
                if not session.collaborators:
                    del self.active_sessions[session_id]
                    logger.info(f"Closed session {session_id}")
                
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to close session: {e}")
            return False
    
    async def get_session_info(self, session_id: str) -> Optional[EditorSession]:
        """Get session information"""
        return self.active_sessions.get(session_id)
    
    async def get_active_sessions(self, user_id: UUID) -> List[EditorSession]:
        """Get all active sessions for a user"""
        return [
            session for session in self.active_sessions.values()
            if user_id in session.collaborators
        ]


# Global instance
code_editor_service = CodeEditorService()
