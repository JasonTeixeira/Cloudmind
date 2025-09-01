"""
World-Class File Explorer Service
Provides professional IDE-like file management capabilities
"""

import asyncio
import logging
import os
import shutil
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID, uuid4
from pathlib import Path
import json
import mimetypes
import hashlib

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import git

from app.models.project_storage import ProjectFile, ProjectDirectory
from app.core.database import get_db
from app.core.config import settings
from app.services.storage.file_storage_service import FileStorageService
from app.services.git.git_service import GitService

logger = logging.getLogger(__name__)


class FileNode:
    """File or directory node in the file tree"""
    def __init__(self, name: str, path: str, is_directory: bool = False, **kwargs):
        self.name = name
        self.path = path
        self.is_directory = is_directory
        self.children = []
        self.size = kwargs.get('size', 0)
        self.modified = kwargs.get('modified', datetime.utcnow())
        self.created = kwargs.get('created', datetime.utcnow())
        self.file_type = kwargs.get('file_type', '')
        self.mime_type = kwargs.get('mime_type', '')
        self.git_status = kwargs.get('git_status', '')
        self.is_hidden = kwargs.get('is_hidden', False)
        self.permissions = kwargs.get('permissions', '')
        self.owner = kwargs.get('owner', '')
        self.group = kwargs.get('group', '')


class FileTree:
    """Hierarchical file tree structure"""
    def __init__(self, root: FileNode):
        self.root = root
        self.total_files = 0
        self.total_directories = 0
        self.total_size = 0
        self.last_updated = datetime.utcnow()


class FileResult:
    """File search result"""
    def __init__(self, file_path: str, name: str, score: float, **kwargs):
        self.file_path = file_path
        self.name = name
        self.score = score
        self.is_directory = kwargs.get('is_directory', False)
        self.size = kwargs.get('size', 0)
        self.modified = kwargs.get('modified', datetime.utcnow())
        self.file_type = kwargs.get('file_type', '')
        self.mime_type = kwargs.get('mime_type', '')
        self.git_status = kwargs.get('git_status', '')
        self.highlighted_name = kwargs.get('highlighted_name', name)
        self.matched_content = kwargs.get('matched_content', '')


class FilePreview:
    """File preview with syntax highlighting"""
    def __init__(self, content: str, language: str, **kwargs):
        self.content = content
        self.language = language
        self.tokens = kwargs.get('tokens', [])
        self.line_count = kwargs.get('line_count', 0)
        self.file_size = kwargs.get('file_size', 0)
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.is_binary = kwargs.get('is_binary', False)
        self.preview_only = kwargs.get('preview_only', True)


class FileMetadata:
    """Detailed file metadata"""
    def __init__(self, file_path: str, **kwargs):
        self.file_path = file_path
        self.name = kwargs.get('name', '')
        self.size = kwargs.get('size', 0)
        self.modified = kwargs.get('modified', datetime.utcnow())
        self.created = kwargs.get('created', datetime.utcnow())
        self.accessed = kwargs.get('accessed', datetime.utcnow())
        self.file_type = kwargs.get('file_type', '')
        self.mime_type = kwargs.get('mime_type', '')
        self.encoding = kwargs.get('encoding', 'utf-8')
        self.is_binary = kwargs.get('is_binary', False)
        self.is_hidden = kwargs.get('is_hidden', False)
        self.permissions = kwargs.get('permissions', '')
        self.owner = kwargs.get('owner', '')
        self.group = kwargs.get('group', '')
        self.git_status = kwargs.get('git_status', '')
        self.content_hash = kwargs.get('content_hash', '')
        self.line_count = kwargs.get('line_count', 0)
        self.word_count = kwargs.get('word_count', 0)
        self.complexity_score = kwargs.get('complexity_score', 0)


class GitStatus:
    """Git status information"""
    def __init__(self, status: str, **kwargs):
        self.status = status  # modified, added, deleted, untracked, etc.
        self.staged = kwargs.get('staged', False)
        self.conflicted = kwargs.get('conflicted', False)
        self.renamed = kwargs.get('renamed', False)
        self.old_path = kwargs.get('old_path', '')
        self.new_path = kwargs.get('new_path', '')


class FileOperation:
    """File operation request"""
    def __init__(self, operation_type: str, **kwargs):
        self.operation_type = operation_type  # copy, move, delete, rename, create
        self.source_paths = kwargs.get('source_paths', [])
        self.destination = kwargs.get('destination', '')
        self.user_id = kwargs.get('user_id')
        self.project_id = kwargs.get('project_id')
        self.overwrite = kwargs.get('overwrite', False)
        self.recursive = kwargs.get('recursive', False)


class OperationResult:
    """File operation result"""
    def __init__(self, success: bool, **kwargs):
        self.success = success
        self.message = kwargs.get('message', '')
        self.affected_files = kwargs.get('affected_files', [])
        self.errors = kwargs.get('errors', [])
        self.warnings = kwargs.get('warnings', [])
        self.operation_id = kwargs.get('operation_id', str(uuid4()))


class FileFilters:
    """File search filters"""
    def __init__(self, **kwargs):
        self.file_types = kwargs.get('file_types', [])
        self.min_size = kwargs.get('min_size', 0)
        self.max_size = kwargs.get('max_size', None)
        self.modified_after = kwargs.get('modified_after', None)
        self.modified_before = kwargs.get('modified_before', None)
        self.git_status = kwargs.get('git_status', [])
        self.is_hidden = kwargs.get('is_hidden', None)
        self.owner = kwargs.get('owner', '')
        self.group = kwargs.get('group', '')


class FileExplorerService:
    """Professional file explorer service"""
    
    def __init__(self):
        self.file_storage = FileStorageService()
        self.git_service = GitService()
        self._init_mime_types()
    
    def _init_mime_types(self):
        """Initialize MIME type detection"""
        # Add custom MIME types for common development files
        mimetypes.add_type('application/json', '.json')
        mimetypes.add_type('text/yaml', '.yaml')
        mimetypes.add_type('text/yaml', '.yml')
        mimetypes.add_type('text/toml', '.toml')
        mimetypes.add_type('text/ini', '.ini')
        mimetypes.add_type('text/ini', '.conf')
        mimetypes.add_type('text/markdown', '.md')
        mimetypes.add_type('text/restructuredtext', '.rst')
        mimetypes.add_type('text/xml', '.xml')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('text/scss', '.scss')
        mimetypes.add_type('text/sass', '.sass')
        mimetypes.add_type('text/less', '.less')
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('application/typescript', '.ts')
        mimetypes.add_type('application/x-python', '.py')
        mimetypes.add_type('application/x-java', '.java')
        mimetypes.add_type('application/x-c++', '.cpp')
        mimetypes.add_type('application/x-c++', '.cc')
        mimetypes.add_type('application/x-c', '.c')
        mimetypes.add_type('application/x-go', '.go')
        mimetypes.add_type('application/x-rust', '.rs')
        mimetypes.add_type('application/x-php', '.php')
        mimetypes.add_type('application/x-ruby', '.rb')
        mimetypes.add_type('application/x-swift', '.swift')
        mimetypes.add_type('application/x-kotlin', '.kt')
        mimetypes.add_type('application/x-scala', '.scala')
        mimetypes.add_type('application/x-clojure', '.clj')
        mimetypes.add_type('application/x-haskell', '.hs')
    
    async def get_file_tree(self, project_id: UUID, path: str = "/") -> FileTree:
        """Get hierarchical file tree with metadata"""
        try:
            # Get project files from storage
            files = await self.file_storage.list_files(project_id, path)
            
            # Build tree structure
            root = FileNode(name="root", path="/", is_directory=True)
            file_map = {"/": root}
            
            total_files = 0
            total_directories = 0
            total_size = 0
            
            # Process files and build tree
            for file_info in files:
                file_path = file_info['file_path']
                file_name = Path(file_path).name
                parent_path = str(Path(file_path).parent)
                
                # Create parent directories if they don't exist
                if parent_path not in file_map:
                    await self._create_directory_nodes(parent_path, file_map)
                
                # Create file node
                file_node = FileNode(
                    name=file_name,
                    path=file_path,
                    is_directory=False,
                    size=file_info.get('file_size', 0),
                    modified=file_info.get('updated_at', datetime.utcnow()),
                    created=file_info.get('created_at', datetime.utcnow()),
                    file_type=file_info.get('file_type', ''),
                    mime_type=self._get_mime_type(file_path),
                    is_hidden=file_name.startswith('.')
                )
                
                # Add to parent
                if parent_path in file_map:
                    file_map[parent_path].children.append(file_node)
                
                file_map[file_path] = file_node
                total_files += 1
                total_size += file_node.size
            
            # Get Git status for all files
            git_status = await self.get_git_status(project_id)
            await self._add_git_status_to_tree(root, git_status)
            
            # Sort children
            await self._sort_tree_children(root)
            
            return FileTree(
                root=root,
                total_files=total_files,
                total_directories=total_directories,
                total_size=total_size
            )
            
        except Exception as e:
            logger.error(f"Failed to get file tree: {e}")
            raise
    
    async def search_files(self, project_id: UUID, query: str, filters: FileFilters) -> List[FileResult]:
        """Advanced file search with filters and ranking"""
        try:
            results = []
            
            # Get all files for the project
            all_files = await self.file_storage.list_files(project_id, "/")
            
            # Apply filters
            filtered_files = await self._apply_filters(all_files, filters)
            
            # Search by name
            name_results = await self._search_by_name(filtered_files, query)
            results.extend(name_results)
            
            # Search by content (for text files)
            content_results = await self._search_by_content(filtered_files, query)
            results.extend(content_results)
            
            # Remove duplicates and sort by score
            unique_results = self._deduplicate_results(results)
            unique_results.sort(key=lambda x: x.score, reverse=True)
            
            return unique_results[:100]  # Limit to top 100 results
            
        except Exception as e:
            logger.error(f"Failed to search files: {e}")
            return []
    
    async def get_file_preview(self, file_path: str) -> FilePreview:
        """Get file preview with syntax highlighting"""
        try:
            # Get file content
            project_id = self._extract_project_id(file_path)
            if not project_id:
                raise ValueError("Invalid file path")
            
            content_bytes, _ = await self.file_storage.download_file(project_id, file_path)
            
            # Check if binary
            is_binary = self._is_binary_content(content_bytes)
            if is_binary:
                return FilePreview(
                    content="[Binary file - preview not available]",
                    language="binary",
                    is_binary=True,
                    file_size=len(content_bytes)
                )
            
            # Decode content
            try:
                content = content_bytes.decode('utf-8')
                encoding = 'utf-8'
            except UnicodeDecodeError:
                try:
                    content = content_bytes.decode('latin-1')
                    encoding = 'latin-1'
                except:
                    content = content_bytes.decode('utf-8', errors='replace')
                    encoding = 'utf-8'
            
            # Get language for syntax highlighting
            language = self._detect_language(file_path)
            
            # Get line count
            line_count = content.count('\n') + 1
            
            # Limit preview content
            preview_content = content[:5000] if len(content) > 5000 else content
            preview_only = len(content) > 5000
            
            return FilePreview(
                content=preview_content,
                language=language,
                line_count=line_count,
                file_size=len(content_bytes),
                encoding=encoding,
                is_binary=False,
                preview_only=preview_only
            )
            
        except Exception as e:
            logger.error(f"Failed to get file preview: {e}")
            raise
    
    async def perform_file_operation(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Perform file operations (copy, move, delete, etc.)"""
        try:
            if operation.operation_type == "copy":
                return await self._copy_files(operation, user_id)
            elif operation.operation_type == "move":
                return await self._move_files(operation, user_id)
            elif operation.operation_type == "delete":
                return await self._delete_files(operation, user_id)
            elif operation.operation_type == "rename":
                return await self._rename_file(operation, user_id)
            elif operation.operation_type == "create_directory":
                return await self._create_directory(operation, user_id)
            else:
                raise ValueError(f"Unsupported operation type: {operation.operation_type}")
                
        except Exception as e:
            logger.error(f"Failed to perform file operation: {e}")
            return OperationResult(success=False, message=str(e))
    
    async def get_git_status(self, project_id: UUID) -> Dict[str, GitStatus]:
        """Get Git status for all files"""
        try:
            # Get Git status from GitService
            git_status = await self.git_service.get_repository_status(project_id)
            
            # Convert to our format
            status_map = {}
            for file_path, status_info in git_status.items():
                status_map[file_path] = GitStatus(
                    status=status_info.get('status', ''),
                    staged=status_info.get('staged', False),
                    conflicted=status_info.get('conflicted', False),
                    renamed=status_info.get('renamed', False),
                    old_path=status_info.get('old_path', ''),
                    new_path=status_info.get('new_path', '')
                )
            
            return status_map
            
        except Exception as e:
            logger.error(f"Failed to get Git status: {e}")
            return {}
    
    async def get_file_metadata(self, file_path: str) -> FileMetadata:
        """Get detailed file metadata"""
        try:
            project_id = self._extract_project_id(file_path)
            if not project_id:
                raise ValueError("Invalid file path")
            
            # Get file info from storage
            file_info = await self.file_storage.get_file_info(project_id, file_path)
            
            # Get content for analysis
            content_bytes, _ = await self.file_storage.download_file(project_id, file_path)
            
            # Calculate content hash
            content_hash = hashlib.sha256(content_bytes).hexdigest()
            
            # Analyze content
            is_binary = self._is_binary_content(content_bytes)
            line_count = 0
            word_count = 0
            
            if not is_binary:
                try:
                    content = content_bytes.decode('utf-8')
                    line_count = content.count('\n') + 1
                    word_count = len(content.split())
                except:
                    pass
            
            return FileMetadata(
                file_path=file_path,
                name=Path(file_path).name,
                size=file_info.get('file_size', 0),
                modified=file_info.get('updated_at', datetime.utcnow()),
                created=file_info.get('created_at', datetime.utcnow()),
                accessed=datetime.utcnow(),
                file_type=file_info.get('file_type', ''),
                mime_type=self._get_mime_type(file_path),
                encoding='utf-8' if not is_binary else 'binary',
                is_binary=is_binary,
                is_hidden=Path(file_path).name.startswith('.'),
                permissions='rw-r--r--',
                owner='user',
                group='group',
                git_status='',
                content_hash=content_hash,
                line_count=line_count,
                word_count=word_count,
                complexity_score=0
            )
            
        except Exception as e:
            logger.error(f"Failed to get file metadata: {e}")
            raise
    
    async def _create_directory_nodes(self, path: str, file_map: Dict[str, FileNode]):
        """Create directory nodes for a path"""
        parts = Path(path).parts
        current_path = ""
        
        for part in parts:
            if current_path:
                current_path = f"{current_path}/{part}"
            else:
                current_path = part
            
            if current_path not in file_map:
                file_map[current_path] = FileNode(
                    name=part,
                    path=current_path,
                    is_directory=True,
                    is_hidden=part.startswith('.')
                )
                
                # Add to parent
                parent_path = str(Path(current_path).parent)
                if parent_path in file_map:
                    file_map[parent_path].children.append(file_map[current_path])
    
    async def _add_git_status_to_tree(self, node: FileNode, git_status: Dict[str, GitStatus]):
        """Add Git status to file tree nodes"""
        if node.path in git_status:
            node.git_status = git_status[node.path].status
        
        for child in node.children:
            await self._add_git_status_to_tree(child, git_status)
    
    async def _sort_tree_children(self, node: FileNode):
        """Sort children of a tree node"""
        # Sort directories first, then files, both alphabetically
        node.children.sort(key=lambda x: (not x.is_directory, x.name.lower()))
        
        for child in node.children:
            if child.is_directory:
                await self._sort_tree_children(child)
    
    async def _apply_filters(self, files: List[Dict], filters: FileFilters) -> List[Dict]:
        """Apply filters to file list"""
        filtered = []
        
        for file_info in files:
            # File type filter
            if filters.file_types and file_info.get('file_type') not in filters.file_types:
                continue
            
            # Size filter
            file_size = file_info.get('file_size', 0)
            if file_size < filters.min_size:
                continue
            if filters.max_size and file_size > filters.max_size:
                continue
            
            # Date filter
            modified = file_info.get('updated_at', datetime.utcnow())
            if filters.modified_after and modified < filters.modified_after:
                continue
            if filters.modified_before and modified > filters.modified_before:
                continue
            
            # Hidden filter
            file_name = Path(file_info['file_path']).name
            if filters.is_hidden is not None:
                is_hidden = file_name.startswith('.')
                if is_hidden != filters.is_hidden:
                    continue
            
            filtered.append(file_info)
        
        return filtered
    
    async def _search_by_name(self, files: List[Dict], query: str) -> List[FileResult]:
        """Search files by name"""
        results = []
        query_lower = query.lower()
        
        for file_info in files:
            file_path = file_info['file_path']
            file_name = Path(file_path).name
            
            # Calculate name match score
            score = 0
            highlighted_name = file_name
            
            # Exact match
            if query_lower == file_name.lower():
                score = 100
                highlighted_name = f"**{file_name}**"
            # Starts with
            elif file_name.lower().startswith(query_lower):
                score = 80
                highlighted_name = f"**{file_name[:len(query)]}**{file_name[len(query):]}"
            # Contains
            elif query_lower in file_name.lower():
                score = 60
                idx = file_name.lower().find(query_lower)
                highlighted_name = f"{file_name[:idx]}**{file_name[idx:idx+len(query)]}**{file_name[idx+len(query):]}"
            # Fuzzy match
            else:
                # Simple fuzzy matching
                query_chars = set(query_lower)
                name_chars = set(file_name.lower())
                intersection = query_chars.intersection(name_chars)
                if len(intersection) >= len(query_chars) * 0.7:
                    score = 30
            
            if score > 0:
                results.append(FileResult(
                    file_path=file_path,
                    name=file_name,
                    score=score,
                    is_directory=False,
                    size=file_info.get('file_size', 0),
                    modified=file_info.get('updated_at', datetime.utcnow()),
                    file_type=file_info.get('file_type', ''),
                    mime_type=self._get_mime_type(file_path),
                    highlighted_name=highlighted_name
                ))
        
        return results
    
    async def _search_by_content(self, files: List[Dict], query: str) -> List[FileResult]:
        """Search files by content"""
        results = []
        query_lower = query.lower()
        
        for file_info in files:
            file_path = file_info['file_path']
            file_type = file_info.get('file_type', '')
            
            # Only search text files
            if file_type in ['binary', 'image', 'video', 'audio']:
                continue
            
            try:
                # Get file content
                project_id = self._extract_project_id(file_path)
                content_bytes, _ = await self.file_storage.download_file(project_id, file_path)
                
                # Check if binary
                if self._is_binary_content(content_bytes):
                    continue
                
                # Decode content
                try:
                    content = content_bytes.decode('utf-8')
                except:
                    continue
                
                # Search in content
                if query_lower in content.lower():
                    # Find matching line
                    lines = content.split('\n')
                    matched_line = ""
                    for line in lines:
                        if query_lower in line.lower():
                            matched_line = line.strip()
                            break
                    
                    results.append(FileResult(
                        file_path=file_path,
                        name=Path(file_path).name,
                        score=40,  # Lower score than name matches
                        is_directory=False,
                        size=file_info.get('file_size', 0),
                        modified=file_info.get('updated_at', datetime.utcnow()),
                        file_type=file_type,
                        mime_type=self._get_mime_type(file_path),
                        matched_content=matched_line[:100] + "..." if len(matched_line) > 100 else matched_line
                    ))
                    
            except Exception as e:
                logger.debug(f"Failed to search content in {file_path}: {e}")
                continue
        
        return results
    
    def _deduplicate_results(self, results: List[FileResult]) -> List[FileResult]:
        """Remove duplicate search results"""
        seen = set()
        unique_results = []
        
        for result in results:
            if result.file_path not in seen:
                seen.add(result.file_path)
                unique_results.append(result)
        
        return unique_results
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type for file"""
        return mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    
    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file path"""
        ext = Path(file_path).suffix.lower()
        
        language_map = {
            '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
            '.jsx': 'javascript', '.tsx': 'typescript', '.java': 'java',
            '.cpp': 'cpp', '.c': 'c', '.h': 'c', '.go': 'go', '.rs': 'rust',
            '.php': 'php', '.rb': 'ruby', '.swift': 'swift', '.kt': 'kotlin',
            '.scala': 'scala', '.clj': 'clojure', '.hs': 'haskell',
            '.html': 'html', '.css': 'css', '.scss': 'scss', '.sass': 'sass',
            '.less': 'less', '.xml': 'xml', '.json': 'json', '.yaml': 'yaml',
            '.yml': 'yaml', '.toml': 'toml', '.ini': 'ini', '.conf': 'ini',
            '.sql': 'sql', '.sh': 'bash', '.bat': 'batch', '.ps1': 'powershell',
            '.dockerfile': 'dockerfile', '.tf': 'hcl', '.env': 'properties',
            '.md': 'markdown', '.rst': 'rst', '.tex': 'latex',
            '.txt': 'text', '.log': 'text', '.csv': 'csv'
        }
        
        return language_map.get(ext, 'text')
    
    def _is_binary_content(self, content: bytes) -> bool:
        """Check if content is binary"""
        # Check for null bytes
        if b'\x00' in content[:1024]:
            return True
        
        # Check for common binary file signatures
        binary_signatures = [
            b'\xff\xd8\xff',  # JPEG
            b'\x89PNG\r\n\x1a\n',  # PNG
            b'GIF87a',  # GIF
            b'GIF89a',  # GIF
            b'PK\x03\x04',  # ZIP
            b'PK\x05\x06',  # ZIP
            b'PK\x07\x08',  # ZIP
            b'\x1f\x8b\x08',  # GZIP
            b'\x7fELF',  # ELF
            b'MZ',  # PE/EXE
        ]
        
        for sig in binary_signatures:
            if content.startswith(sig):
                return True
        
        return False
    
    def _extract_project_id(self, file_path: str) -> Optional[UUID]:
        """Extract project ID from file path"""
        try:
            parts = file_path.split('/')
            if len(parts) > 2 and parts[0] == 'projects':
                return UUID(parts[1])
            return None
        except:
            return None
    
    async def _copy_files(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Copy files operation"""
        try:
            affected_files = []
            errors = []
            
            for source_path in operation.source_paths:
                try:
                    # Extract project ID
                    project_id = self._extract_project_id(source_path)
                    if not project_id:
                        errors.append(f"Invalid source path: {source_path}")
                        continue
                    
                    # Copy file
                    await self.file_storage.copy_file(
                        project_id=project_id,
                        source_path=source_path,
                        destination_path=operation.destination,
                        user_id=user_id
                    )
                    
                    affected_files.append(source_path)
                    
                except Exception as e:
                    errors.append(f"Failed to copy {source_path}: {str(e)}")
            
            return OperationResult(
                success=len(errors) == 0,
                message=f"Copied {len(affected_files)} files",
                affected_files=affected_files,
                errors=errors
            )
            
        except Exception as e:
            return OperationResult(success=False, message=str(e))
    
    async def _move_files(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Move files operation"""
        try:
            affected_files = []
            errors = []
            
            for source_path in operation.source_paths:
                try:
                    # Extract project ID
                    project_id = self._extract_project_id(source_path)
                    if not project_id:
                        errors.append(f"Invalid source path: {source_path}")
                        continue
                    
                    # Move file
                    await self.file_storage.move_file(
                        project_id=project_id,
                        source_path=source_path,
                        destination_path=operation.destination,
                        user_id=user_id
                    )
                    
                    affected_files.append(source_path)
                    
                except Exception as e:
                    errors.append(f"Failed to move {source_path}: {str(e)}")
            
            return OperationResult(
                success=len(errors) == 0,
                message=f"Moved {len(affected_files)} files",
                affected_files=affected_files,
                errors=errors
            )
            
        except Exception as e:
            return OperationResult(success=False, message=str(e))
    
    async def _delete_files(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Delete files operation"""
        try:
            affected_files = []
            errors = []
            
            for file_path in operation.source_paths:
                try:
                    # Extract project ID
                    project_id = self._extract_project_id(file_path)
                    if not project_id:
                        errors.append(f"Invalid file path: {file_path}")
                        continue
                    
                    # Delete file
                    await self.file_storage.delete_file(
                        project_id=project_id,
                        file_path=file_path,
                        user_id=user_id
                    )
                    
                    affected_files.append(file_path)
                    
                except Exception as e:
                    errors.append(f"Failed to delete {file_path}: {str(e)}")
            
            return OperationResult(
                success=len(errors) == 0,
                message=f"Deleted {len(affected_files)} files",
                affected_files=affected_files,
                errors=errors
            )
            
        except Exception as e:
            return OperationResult(success=False, message=str(e))
    
    async def _rename_file(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Rename file operation"""
        try:
            if len(operation.source_paths) != 1:
                return OperationResult(success=False, message="Rename operation requires exactly one source file")
            
            source_path = operation.source_paths[0]
            new_path = operation.destination
            
            # Extract project ID
            project_id = self._extract_project_id(source_path)
            if not project_id:
                return OperationResult(success=False, message="Invalid source path")
            
            # Rename file
            await self.file_storage.move_file(
                project_id=project_id,
                source_path=source_path,
                destination_path=new_path,
                user_id=user_id
            )
            
            return OperationResult(
                success=True,
                message=f"Renamed {source_path} to {new_path}",
                affected_files=[source_path, new_path]
            )
            
        except Exception as e:
            return OperationResult(success=False, message=str(e))
    
    async def _create_directory(self, operation: FileOperation, user_id: UUID) -> OperationResult:
        """Create directory operation"""
        try:
            # Extract project ID
            project_id = self._extract_project_id(operation.destination)
            if not project_id:
                return OperationResult(success=False, message="Invalid destination path")
            
            # Create directory
            await self.file_storage.create_directory(
                project_id=project_id,
                directory_path=operation.destination,
                user_id=user_id
            )
            
            return OperationResult(
                success=True,
                message=f"Created directory {operation.destination}",
                affected_files=[operation.destination]
            )
            
        except Exception as e:
            return OperationResult(success=False, message=str(e))


# Global instance
file_explorer_service = FileExplorerService()
