"""
Advanced File Operations Service
Professional file operations with error handling and progress tracking
"""

import asyncio
import logging
import os
import shutil
import tempfile
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple
from uuid import UUID, uuid4
from pathlib import Path
import json
import hashlib

from app.core.config import settings
from app.services.storage.file_storage_service import FileStorageService

logger = logging.getLogger(__name__)


class FileOperationError(Exception):
    """Custom exception for file operation errors"""
    def __init__(self, message: str, operation: str, affected_files: List[str] = None):
        super().__init__(message)
        self.operation = operation
        self.affected_files = affected_files or []


class OperationProgress:
    """Progress tracking for file operations"""
    def __init__(self, operation_id: str, total_files: int):
        self.operation_id = operation_id
        self.total_files = total_files
        self.processed_files = 0
        self.current_file = ""
        self.status = "pending"
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.error_message = None
        self.success_count = 0
        self.error_count = 0


class FileOperationsService:
    """Advanced file operations service"""
    
    def __init__(self):
        self.file_storage = FileStorageService()
        self.active_operations: Dict[str, OperationProgress] = {}
        
    async def copy_files(
        self, 
        source_paths: List[str], 
        destination: str, 
        user_id: UUID,
        overwrite: bool = False,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """Copy multiple files with progress tracking"""
        operation_id = str(uuid4())
        progress = OperationProgress(operation_id, len(source_paths))
        self.active_operations[operation_id] = progress
        
        try:
            progress.status = "running"
            results = []
            
            # Ensure destination exists
            dest_path = Path(destination)
            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)
            
            for source_path in source_paths:
                progress.current_file = source_path
                source = Path(source_path)
                
                if not source.exists():
                    raise FileOperationError(f"Source file not found: {source_path}", "copy", [source_path])
                
                # Determine destination path
                if dest_path.is_dir():
                    dest_file = dest_path / source.name
                else:
                    dest_file = dest_path
                
                # Check if destination exists
                if dest_file.exists() and not overwrite:
                    if create_backup:
                        backup_path = await self._create_backup(dest_file)
                        results.append({
                            "file": str(source),
                            "backup": str(backup_path),
                            "status": "backup_created"
                        })
                    else:
                        raise FileOperationError(f"Destination exists: {dest_file}", "copy", [str(source)])
                
                # Perform copy operation
                if source.is_file():
                    shutil.copy2(source, dest_file)
                elif source.is_dir():
                    shutil.copytree(source, dest_file, dirs_exist_ok=overwrite)
                
                progress.processed_files += 1
                progress.success_count += 1
                
                results.append({
                    "file": str(source),
                    "destination": str(dest_file),
                    "status": "success"
                })
                
                # Small delay to prevent overwhelming the system
                await asyncio.sleep(0.01)
            
            progress.status = "completed"
            progress.end_time = datetime.utcnow()
            
            return {
                "operation_id": operation_id,
                "success": True,
                "results": results,
                "total_files": len(source_paths),
                "success_count": progress.success_count,
                "error_count": progress.error_count,
                "duration": (progress.end_time - progress.start_time).total_seconds()
            }
            
        except Exception as e:
            progress.status = "failed"
            progress.error_message = str(e)
            progress.end_time = datetime.utcnow()
            
            logger.error(f"Copy operation failed: {e}")
            raise FileOperationError(str(e), "copy", source_paths)
        
        finally:
            # Clean up progress tracking after some time
            asyncio.create_task(self._cleanup_progress(operation_id))
    
    async def move_files(
        self, 
        source_paths: List[str], 
        destination: str, 
        user_id: UUID,
        overwrite: bool = False,
        create_backup: bool = True
    ) -> Dict[str, Any]:
        """Move multiple files with conflict resolution"""
        operation_id = str(uuid4())
        progress = OperationProgress(operation_id, len(source_paths))
        self.active_operations[operation_id] = progress
        
        try:
            progress.status = "running"
            results = []
            
            # Ensure destination exists
            dest_path = Path(destination)
            if not dest_path.exists():
                dest_path.mkdir(parents=True, exist_ok=True)
            
            for source_path in source_paths:
                progress.current_file = source_path
                source = Path(source_path)
                
                if not source.exists():
                    raise FileOperationError(f"Source file not found: {source_path}", "move", [source_path])
                
                # Determine destination path
                if dest_path.is_dir():
                    dest_file = dest_path / source.name
                else:
                    dest_file = dest_path
                
                # Check if destination exists
                if dest_file.exists() and not overwrite:
                    if create_backup:
                        backup_path = await self._create_backup(dest_file)
                        results.append({
                            "file": str(source),
                            "backup": str(backup_path),
                            "status": "backup_created"
                        })
                    else:
                        raise FileOperationError(f"Destination exists: {dest_file}", "move", [str(source)])
                
                # Perform move operation
                shutil.move(str(source), str(dest_file))
                
                progress.processed_files += 1
                progress.success_count += 1
                
                results.append({
                    "file": str(source),
                    "destination": str(dest_file),
                    "status": "success"
                })
                
                await asyncio.sleep(0.01)
            
            progress.status = "completed"
            progress.end_time = datetime.utcnow()
            
            return {
                "operation_id": operation_id,
                "success": True,
                "results": results,
                "total_files": len(source_paths),
                "success_count": progress.success_count,
                "error_count": progress.error_count,
                "duration": (progress.end_time - progress.start_time).total_seconds()
            }
            
        except Exception as e:
            progress.status = "failed"
            progress.error_message = str(e)
            progress.end_time = datetime.utcnow()
            
            logger.error(f"Move operation failed: {e}")
            raise FileOperationError(str(e), "move", source_paths)
        
        finally:
            asyncio.create_task(self._cleanup_progress(operation_id))
    
    async def delete_files(
        self, 
        file_paths: List[str], 
        user_id: UUID,
        create_backup: bool = True,
        permanent: bool = False
    ) -> Dict[str, Any]:
        """Delete files with confirmation and recovery"""
        operation_id = str(uuid4())
        progress = OperationProgress(operation_id, len(file_paths))
        self.active_operations[operation_id] = progress
        
        try:
            progress.status = "running"
            results = []
            
            for file_path in file_paths:
                progress.current_file = file_path
                path = Path(file_path)
                
                if not path.exists():
                    results.append({
                        "file": file_path,
                        "status": "not_found"
                    })
                    progress.processed_files += 1
                    continue
                
                # Create backup if requested
                backup_path = None
                if create_backup and not permanent:
                    backup_path = await self._create_backup(path)
                
                # Perform delete operation
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    shutil.rmtree(path)
                
                progress.processed_files += 1
                progress.success_count += 1
                
                results.append({
                    "file": file_path,
                    "backup": str(backup_path) if backup_path else None,
                    "status": "success"
                })
                
                await asyncio.sleep(0.01)
            
            progress.status = "completed"
            progress.end_time = datetime.utcnow()
            
            return {
                "operation_id": operation_id,
                "success": True,
                "results": results,
                "total_files": len(file_paths),
                "success_count": progress.success_count,
                "error_count": progress.error_count,
                "duration": (progress.end_time - progress.start_time).total_seconds()
            }
            
        except Exception as e:
            progress.status = "failed"
            progress.error_message = str(e)
            progress.end_time = datetime.utcnow()
            
            logger.error(f"Delete operation failed: {e}")
            raise FileOperationError(str(e), "delete", file_paths)
        
        finally:
            asyncio.create_task(self._cleanup_progress(operation_id))
    
    async def create_directory(
        self, 
        path: str, 
        user_id: UUID,
        create_parents: bool = True
    ) -> Dict[str, Any]:
        """Create new directory with permissions"""
        try:
            dir_path = Path(path)
            
            if dir_path.exists():
                if dir_path.is_dir():
                    return {
                        "success": True,
                        "message": "Directory already exists",
                        "path": str(dir_path)
                    }
                else:
                    raise FileOperationError(f"Path exists but is not a directory: {path}", "create_directory", [path])
            
            # Create directory
            dir_path.mkdir(parents=create_parents, exist_ok=True)
            
            return {
                "success": True,
                "message": "Directory created successfully",
                "path": str(dir_path)
            }
            
        except Exception as e:
            logger.error(f"Create directory failed: {e}")
            raise FileOperationError(str(e), "create_directory", [path])
    
    async def rename_file(
        self, 
        old_path: str, 
        new_path: str, 
        user_id: UUID,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """Rename file or directory with validation"""
        try:
            old_file = Path(old_path)
            new_file = Path(new_path)
            
            if not old_file.exists():
                raise FileOperationError(f"Source file not found: {old_path}", "rename", [old_path])
            
            if new_file.exists() and not overwrite:
                raise FileOperationError(f"Destination already exists: {new_path}", "rename", [old_path])
            
            # Perform rename
            old_file.rename(new_file)
            
            return {
                "success": True,
                "message": "File renamed successfully",
                "old_path": old_path,
                "new_path": str(new_file)
            }
            
        except Exception as e:
            logger.error(f"Rename operation failed: {e}")
            raise FileOperationError(str(e), "rename", [old_path])
    
    async def duplicate_file(
        self, 
        file_path: str, 
        user_id: UUID
    ) -> Dict[str, Any]:
        """Duplicate file with auto-naming"""
        try:
            source = Path(file_path)
            
            if not source.exists():
                raise FileOperationError(f"Source file not found: {file_path}", "duplicate", [file_path])
            
            # Generate duplicate name
            counter = 1
            while True:
                if source.is_file():
                    name_parts = source.stem, f"copy_{counter}", source.suffix
                    duplicate_name = "".join(name_parts)
                else:
                    duplicate_name = f"{source.name}_copy_{counter}"
                
                duplicate_path = source.parent / duplicate_name
                
                if not duplicate_path.exists():
                    break
                counter += 1
            
            # Perform duplication
            if source.is_file():
                shutil.copy2(source, duplicate_path)
            else:
                shutil.copytree(source, duplicate_path)
            
            return {
                "success": True,
                "message": "File duplicated successfully",
                "original_path": file_path,
                "duplicate_path": str(duplicate_path)
            }
            
        except Exception as e:
            logger.error(f"Duplicate operation failed: {e}")
            raise FileOperationError(str(e), "duplicate", [file_path])
    
    async def get_operation_progress(self, operation_id: str) -> Optional[OperationProgress]:
        """Get progress for a specific operation"""
        return self.active_operations.get(operation_id)
    
    async def cancel_operation(self, operation_id: str) -> bool:
        """Cancel a running operation"""
        if operation_id in self.active_operations:
            progress = self.active_operations[operation_id]
            if progress.status == "running":
                progress.status = "cancelled"
                progress.end_time = datetime.utcnow()
                return True
        return False
    
    async def _create_backup(self, file_path: Path) -> Path:
        """Create backup of a file"""
        backup_dir = Path(settings.LOCAL_STORAGE_PATH) / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.backup_{timestamp}"
        backup_path = backup_dir / backup_name
        
        if file_path.is_file():
            shutil.copy2(file_path, backup_path)
        else:
            shutil.copytree(file_path, backup_path)
        
        return backup_path
    
    async def _cleanup_progress(self, operation_id: str, delay: int = 3600):
        """Clean up progress tracking after delay"""
        await asyncio.sleep(delay)
        if operation_id in self.active_operations:
            del self.active_operations[operation_id]


# Global instance
file_operations_service = FileOperationsService()
