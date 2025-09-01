"""
Advanced File Search Service
Professional file search with multiple search methods and intelligent ranking
"""

import asyncio
import logging
import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID
from pathlib import Path
import mimetypes
import fnmatch
from difflib import SequenceMatcher

from app.core.config import settings
from app.schemas.explorer import FileResult, FileFilters, FileType, GitStatus

logger = logging.getLogger(__name__)


class SearchCriteria:
    """Search criteria for advanced file search"""
    def __init__(self, **kwargs):
        self.query = kwargs.get('query', '')
        self.file_types = kwargs.get('file_types', [])
        self.min_size = kwargs.get('min_size', 0)
        self.max_size = kwargs.get('max_size', None)
        self.modified_after = kwargs.get('modified_after', None)
        self.modified_before = kwargs.get('modified_before', None)
        self.git_status = kwargs.get('git_status', [])
        self.is_hidden = kwargs.get('is_hidden', None)
        self.owner = kwargs.get('owner', '')
        self.group = kwargs.get('group', '')
        self.include_content = kwargs.get('include_content', False)
        self.case_sensitive = kwargs.get('case_sensitive', False)
        self.use_regex = kwargs.get('use_regex', False)
        self.max_results = kwargs.get('max_results', 100)


class FileSearchService:
    """Advanced file search service"""
    
    def __init__(self):
        self.search_index = {}
        self.content_index = {}
        self.search_history = []
        
    async def search_by_name(
        self, 
        project_id: UUID, 
        query: str,
        filters: Optional[FileFilters] = None,
        limit: int = 100
    ) -> List[FileResult]:
        """Search files by name with fuzzy matching"""
        try:
            project_path = Path(settings.LOCAL_STORAGE_PATH) / str(project_id)
            if not project_path.exists():
                return []
            
            results = []
            query_lower = query.lower()
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_path):
                # Apply filters to directories
                if filters and filters.is_hidden is False:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                # Search in files
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(file_path, filters):
                        continue
                    
                    # Calculate relevance score
                    score = self._calculate_name_relevance(file, query_lower)
                    
                    if score > 0:
                        file_result = await self._create_file_result(
                            file_path, relative_path, score, project_id
                        )
                        results.append(file_result)
                
                # Search in directory names
                for dir_name in dirs:
                    dir_path = Path(root) / dir_name
                    relative_path = dir_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(dir_path, filters):
                        continue
                    
                    # Calculate relevance score
                    score = self._calculate_name_relevance(dir_name, query_lower)
                    
                    if score > 0:
                        dir_result = await self._create_file_result(
                            dir_path, relative_path, score, project_id, is_directory=True
                        )
                        results.append(dir_result)
            
            # Sort by relevance score and limit results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Name search failed: {e}")
            return []
    
    async def search_by_content(
        self, 
        project_id: UUID, 
        query: str,
        filters: Optional[FileFilters] = None,
        limit: int = 100
    ) -> List[FileResult]:
        """Search files by content with full-text search"""
        try:
            project_path = Path(settings.LOCAL_STORAGE_PATH) / str(project_id)
            if not project_path.exists():
                return []
            
            results = []
            query_lower = query.lower()
            
            # Text file extensions
            text_extensions = {
                '.txt', '.md', '.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', 
                '.scss', '.sass', '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
                '.conf', '.cfg', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
                '.sql', '.r', '.rb', '.php', '.java', '.cpp', '.c', '.h', '.hpp',
                '.cs', '.go', '.rs', '.swift', '.kt', '.scala', '.clj', '.hs',
                '.dockerfile', '.dockerignore', '.gitignore', '.gitattributes',
                '.env', '.env.example', '.env.local', '.env.production'
            }
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_path):
                # Apply filters to directories
                if filters and filters.is_hidden is False:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(file_path, filters):
                        continue
                    
                    # Check if it's a text file
                    if file_path.suffix.lower() not in text_extensions:
                        continue
                    
                    # Search in file content
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Calculate content relevance
                        score, matches = self._calculate_content_relevance(content, query_lower)
                        
                        if score > 0:
                            file_result = await self._create_file_result(
                                file_path, relative_path, score, project_id,
                                highlight_matches=matches
                            )
                            results.append(file_result)
                            
                    except Exception as e:
                        logger.debug(f"Could not read file {file_path}: {e}")
                        continue
            
            # Sort by relevance score and limit results
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Content search failed: {e}")
            return []
    
    async def search_by_type(
        self, 
        project_id: UUID, 
        file_types: List[str],
        filters: Optional[FileFilters] = None,
        limit: int = 100
    ) -> List[FileResult]:
        """Search files by type and extension"""
        try:
            project_path = Path(settings.LOCAL_STORAGE_PATH) / str(project_id)
            if not project_path.exists():
                return []
            
            results = []
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_path):
                # Apply filters to directories
                if filters and filters.is_hidden is False:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(file_path, filters):
                        continue
                    
                    # Check file type
                    file_extension = file_path.suffix.lower()
                    mime_type, _ = mimetypes.guess_type(str(file_path))
                    
                    # Match against requested types
                    for file_type in file_types:
                        if (file_extension == file_type.lower() or 
                            (mime_type and file_type.lower() in mime_type.lower())):
                            
                            file_result = await self._create_file_result(
                                file_path, relative_path, 1.0, project_id
                            )
                            results.append(file_result)
                            break
            
            # Sort by modification time and limit results
            results.sort(key=lambda x: x.modified_at or datetime.utcnow(), reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Type search failed: {e}")
            return []
    
    async def search_by_size(
        self, 
        project_id: UUID, 
        min_size: int, 
        max_size: Optional[int] = None,
        filters: Optional[FileFilters] = None,
        limit: int = 100
    ) -> List[FileResult]:
        """Search files by size range"""
        try:
            project_path = Path(settings.LOCAL_STORAGE_PATH) / str(project_id)
            if not project_path.exists():
                return []
            
            results = []
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_path):
                # Apply filters to directories
                if filters and filters.is_hidden is False:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(file_path, filters):
                        continue
                    
                    # Check file size
                    try:
                        file_size = file_path.stat().st_size
                        
                        if file_size >= min_size and (max_size is None or file_size <= max_size):
                            file_result = await self._create_file_result(
                                file_path, relative_path, 1.0, project_id
                            )
                            results.append(file_result)
                            
                    except Exception as e:
                        logger.debug(f"Could not get size for {file_path}: {e}")
                        continue
            
            # Sort by size and limit results
            results.sort(key=lambda x: x.size or 0, reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Size search failed: {e}")
            return []
    
    async def search_by_date(
        self, 
        project_id: UUID, 
        start_date: datetime, 
        end_date: datetime,
        filters: Optional[FileFilters] = None,
        limit: int = 100
    ) -> List[FileResult]:
        """Search files by modification date"""
        try:
            project_path = Path(settings.LOCAL_STORAGE_PATH) / str(project_id)
            if not project_path.exists():
                return []
            
            results = []
            
            # Walk through project directory
            for root, dirs, files in os.walk(project_path):
                # Apply filters to directories
                if filters and filters.is_hidden is False:
                    dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)
                    
                    # Apply filters
                    if not await self._apply_filters(file_path, filters):
                        continue
                    
                    # Check modification date
                    try:
                        stat = file_path.stat()
                        modified_time = datetime.fromtimestamp(stat.st_mtime)
                        
                        if start_date <= modified_time <= end_date:
                            file_result = await self._create_file_result(
                                file_path, relative_path, 1.0, project_id
                            )
                            results.append(file_result)
                            
                    except Exception as e:
                        logger.debug(f"Could not get date for {file_path}: {e}")
                        continue
            
            # Sort by modification date and limit results
            results.sort(key=lambda x: x.modified_at or datetime.utcnow(), reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Date search failed: {e}")
            return []
    
    async def advanced_search(
        self, 
        project_id: UUID, 
        criteria: SearchCriteria
    ) -> List[FileResult]:
        """Advanced search with multiple criteria"""
        try:
            # Start with name search
            results = await self.search_by_name(
                project_id, criteria.query, 
                self._criteria_to_filters(criteria), criteria.max_results
            )
            
            # If content search is requested, also search content
            if criteria.include_content:
                content_results = await self.search_by_content(
                    project_id, criteria.query,
                    self._criteria_to_filters(criteria), criteria.max_results
                )
                
                # Merge results, avoiding duplicates
                seen_paths = set()
                merged_results = []
                
                for result in results + content_results:
                    if result.path not in seen_paths:
                        seen_paths.add(result.path)
                        merged_results.append(result)
                
                results = merged_results
            
            # Apply additional filters
            filtered_results = []
            for result in results:
                if await self._apply_advanced_filters(result, criteria):
                    filtered_results.append(result)
            
            # Sort by relevance and limit
            filtered_results.sort(key=lambda x: x.relevance_score, reverse=True)
            return filtered_results[:criteria.max_results]
            
        except Exception as e:
            logger.error(f"Advanced search failed: {e}")
            return []
    
    def _calculate_name_relevance(self, filename: str, query: str) -> float:
        """Calculate relevance score for filename matching"""
        filename_lower = filename.lower()
        
        # Exact match gets highest score
        if query == filename_lower:
            return 1.0
        
        # Starts with query
        if filename_lower.startswith(query):
            return 0.9
        
        # Contains query
        if query in filename_lower:
            return 0.7
        
        # Fuzzy matching
        similarity = SequenceMatcher(None, filename_lower, query).ratio()
        if similarity > 0.6:
            return similarity * 0.5
        
        # Extension matching
        if filename_lower.endswith(query):
            return 0.3
        
        return 0.0
    
    def _calculate_content_relevance(self, content: str, query: str) -> Tuple[float, List[str]]:
        """Calculate relevance score for content matching"""
        content_lower = content.lower()
        matches = []
        
        # Count occurrences
        occurrences = content_lower.count(query)
        if occurrences == 0:
            return 0.0, matches
        
        # Calculate base score
        base_score = min(occurrences / 10.0, 1.0)  # Cap at 1.0
        
        # Find match positions for highlighting
        start = 0
        while True:
            pos = content_lower.find(query, start)
            if pos == -1:
                break
            
            # Extract context around match
            context_start = max(0, pos - 20)
            context_end = min(len(content), pos + len(query) + 20)
            context = content[context_start:context_end]
            matches.append(context)
            
            start = pos + 1
        
        return base_score, matches[:5]  # Limit to 5 matches
    
    async def _apply_filters(self, file_path: Path, filters: Optional[FileFilters]) -> bool:
        """Apply filters to a file path"""
        if not filters:
            return True
        
        try:
            stat = file_path.stat()
            
            # Size filter
            if stat.st_size < filters.min_size:
                return False
            
            if filters.max_size and stat.st_size > filters.max_size:
                return False
            
            # Date filter
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            if filters.modified_after and modified_time < filters.modified_after:
                return False
            
            if filters.modified_before and modified_time > filters.modified_before:
                return False
            
            # Hidden file filter
            if filters.is_hidden is False and file_path.name.startswith('.'):
                return False
            
            return True
            
        except Exception as e:
            logger.debug(f"Error applying filters to {file_path}: {e}")
            return False
    
    async def _apply_advanced_filters(self, result: FileResult, criteria: SearchCriteria) -> bool:
        """Apply advanced filters to search result"""
        # This would include additional filtering logic
        # For now, return True (no additional filtering)
        return True
    
    def _criteria_to_filters(self, criteria: SearchCriteria) -> FileFilters:
        """Convert search criteria to file filters"""
        return FileFilters(
            file_types=criteria.file_types,
            min_size=criteria.min_size,
            max_size=criteria.max_size,
            modified_after=criteria.modified_after,
            modified_before=criteria.modified_before,
            git_status=criteria.git_status,
            is_hidden=criteria.is_hidden,
            owner=criteria.owner,
            group=criteria.group
        )
    
    async def _create_file_result(
        self, 
        file_path: Path, 
        relative_path: Path, 
        score: float, 
        project_id: UUID,
        is_directory: bool = False,
        highlight_matches: List[str] = None
    ) -> FileResult:
        """Create a file result object"""
        try:
            stat = file_path.stat()
            
            # Determine file type
            if is_directory:
                file_type = FileType.DIRECTORY
            else:
                file_type = FileType.FILE
            
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            # Get Git status (placeholder - would integrate with Git service)
            git_status = None
            
            return FileResult(
                id=str(file_path),
                name=file_path.name,
                path=str(relative_path),
                type=file_type,
                size=stat.st_size if not is_directory else None,
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                git_status=git_status,
                relevance_score=score,
                highlight_matches=highlight_matches or []
            )
            
        except Exception as e:
            logger.error(f"Error creating file result for {file_path}: {e}")
            # Return a basic result
            return FileResult(
                id=str(file_path),
                name=file_path.name,
                path=str(relative_path),
                type=FileType.FILE,
                relevance_score=score,
                highlight_matches=highlight_matches or []
            )


# Global instance
file_search_service = FileSearchService()
