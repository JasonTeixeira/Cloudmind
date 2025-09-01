"""
File Explorer API Endpoints
Provides REST API for file explorer functionality
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging

from app.core.auth import get_current_user
from app.models.user import User
from app.services.explorer.file_explorer_service import file_explorer_service
from app.services.explorer.file_operations import file_operations_service
from app.services.explorer.file_search import file_search_service
from app.schemas.explorer import (
    FileTreeResponse, FileSearchRequest, FileSearchResponse, FilePreviewRequest,
    FilePreviewResponse, FileOperationRequest, FileOperationResponse,
    FileMetadataResponse, GitStatusResponse, FileFiltersRequest
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/explorer", tags=["File Explorer"])


@router.get("/tree/{project_id}", response_model=FileTreeResponse)
async def get_file_tree(
    project_id: UUID,
    path: str = Query("/", description="Path to explore"),
    current_user: User = Depends(get_current_user)
):
    """Get hierarchical file tree for a project"""
    try:
        file_tree = await file_explorer_service.get_file_tree(project_id, path)
        
        return FileTreeResponse(
            project_id=str(project_id),
            path=path,
            root_node=file_tree.root,
            total_files=file_tree.total_files,
            total_directories=file_tree.total_directories,
            total_size=file_tree.total_size,
            last_updated=file_tree.last_updated
        )
        
    except Exception as e:
        logger.error(f"Failed to get file tree: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/search/{project_id}", response_model=FileSearchResponse)
async def search_files(
    project_id: UUID,
    request: FileSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search files in a project"""
    try:
        # Convert request to FileFilters
        filters = FileFilters(
            file_types=request.filters.file_types if request.filters else [],
            min_size=request.filters.min_size if request.filters else 0,
            max_size=request.filters.max_size if request.filters else None,
            modified_after=request.filters.modified_after if request.filters else None,
            modified_before=request.filters.modified_before if request.filters else None,
            git_status=request.filters.git_status if request.filters else [],
            is_hidden=request.filters.is_hidden if request.filters else None,
            owner=request.filters.owner if request.filters else '',
            group=request.filters.group if request.filters else ''
        )
        
        results = await file_explorer_service.search_files(project_id, request.query, filters)
        
        return FileSearchResponse(
            project_id=str(project_id),
            query=request.query,
            results=results,
            total_count=len(results)
        )
        
    except Exception as e:
        logger.error(f"Failed to search files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/{project_id}")
async def search_files_simple(
    project_id: UUID,
    query: str = Query(..., description="Search query"),
    file_types: Optional[str] = Query(None, description="Comma-separated file types"),
    current_user: User = Depends(get_current_user)
):
    """Simple file search endpoint"""
    try:
        # Parse file types
        file_type_list = []
        if file_types:
            file_type_list = [ft.strip() for ft in file_types.split(',')]
        
        filters = FileFilters(file_types=file_type_list)
        results = await file_explorer_service.search_files(project_id, query, filters)
        
        return {
            "project_id": str(project_id),
            "query": query,
            "results": [
                {
                    "file_path": result.file_path,
                    "name": result.name,
                    "score": result.score,
                    "is_directory": result.is_directory,
                    "size": result.size,
                    "modified": result.modified.isoformat(),
                    "file_type": result.file_type,
                    "mime_type": result.mime_type,
                    "git_status": result.git_status,
                    "highlighted_name": result.highlighted_name,
                    "matched_content": result.matched_content
                }
                for result in results
            ],
            "total_count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Failed to search files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/preview", response_model=FilePreviewResponse)
async def get_file_preview(
    request: FilePreviewRequest,
    current_user: User = Depends(get_current_user)
):
    """Get file preview with syntax highlighting"""
    try:
        preview = await file_explorer_service.get_file_preview(request.file_path)
        
        return FilePreviewResponse(
            file_path=request.file_path,
            content=preview.content,
            language=preview.language,
            tokens=preview.tokens,
            line_count=preview.line_count,
            file_size=preview.file_size,
            encoding=preview.encoding,
            is_binary=preview.is_binary,
            preview_only=preview.preview_only
        )
        
    except Exception as e:
        logger.error(f"Failed to get file preview: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/preview/{file_path:path}")
async def get_file_preview_simple(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """Simple file preview endpoint"""
    try:
        preview = await file_explorer_service.get_file_preview(file_path)
        
        return {
            "file_path": file_path,
            "content": preview.content,
            "language": preview.language,
            "line_count": preview.line_count,
            "file_size": preview.file_size,
            "encoding": preview.encoding,
            "is_binary": preview.is_binary,
            "preview_only": preview.preview_only
        }
        
    except Exception as e:
        logger.error(f"Failed to get file preview: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/operation", response_model=FileOperationResponse)
async def perform_file_operation(
    request: FileOperationRequest,
    current_user: User = Depends(get_current_user)
):
    """Perform file operations (copy, move, delete, etc.)"""
    try:
        # Convert request to FileOperation
        operation = FileOperation(
            operation_type=request.operation_type,
            source_paths=request.source_paths,
            destination=request.destination,
            user_id=current_user.id,
            project_id=request.project_id,
            overwrite=request.overwrite,
            recursive=request.recursive
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return FileOperationResponse(
            success=result.success,
            message=result.message,
            affected_files=result.affected_files,
            errors=result.errors,
            warnings=result.warnings,
            operation_id=result.operation_id
        )
        
    except Exception as e:
        logger.error(f"Failed to perform file operation: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/git-status/{project_id}", response_model=GitStatusResponse)
async def get_git_status(
    project_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """Get Git status for all files in a project"""
    try:
        git_status = await file_explorer_service.get_git_status(project_id)
        
        return GitStatusResponse(
            project_id=str(project_id),
            git_status={
                file_path: {
                    "status": status.status,
                    "staged": status.staged,
                    "conflicted": status.conflicted,
                    "renamed": status.renamed,
                    "old_path": status.old_path,
                    "new_path": status.new_path
                }
                for file_path, status in git_status.items()
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get Git status: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metadata/{file_path:path}", response_model=FileMetadataResponse)
async def get_file_metadata(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed file metadata"""
    try:
        metadata = await file_explorer_service.get_file_metadata(file_path)
        
        return FileMetadataResponse(
            file_path=metadata.file_path,
            name=metadata.name,
            size=metadata.size,
            modified=metadata.modified,
            created=metadata.created,
            accessed=metadata.accessed,
            file_type=metadata.file_type,
            mime_type=metadata.mime_type,
            encoding=metadata.encoding,
            is_binary=metadata.is_binary,
            is_hidden=metadata.is_hidden,
            permissions=metadata.permissions,
            owner=metadata.owner,
            group=metadata.group,
            git_status=metadata.git_status,
            content_hash=metadata.content_hash,
            line_count=metadata.line_count,
            word_count=metadata.word_count,
            complexity_score=metadata.complexity_score
        )
        
    except Exception as e:
        logger.error(f"Failed to get file metadata: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Convenience endpoints for common operations
@router.post("/copy")
async def copy_files(
    source_paths: List[str],
    destination: str,
    project_id: Optional[UUID] = None,
    overwrite: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Copy multiple files"""
    try:
        operation = FileOperation(
            operation_type="copy",
            source_paths=source_paths,
            destination=destination,
            user_id=current_user.id,
            project_id=project_id,
            overwrite=overwrite
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return {
            "success": result.success,
            "message": result.message,
            "affected_files": result.affected_files,
            "errors": result.errors
        }
        
    except Exception as e:
        logger.error(f"Failed to copy files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/move")
async def move_files(
    source_paths: List[str],
    destination: str,
    project_id: Optional[UUID] = None,
    overwrite: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Move multiple files"""
    try:
        operation = FileOperation(
            operation_type="move",
            source_paths=source_paths,
            destination=destination,
            user_id=current_user.id,
            project_id=project_id,
            overwrite=overwrite
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return {
            "success": result.success,
            "message": result.message,
            "affected_files": result.affected_files,
            "errors": result.errors
        }
        
    except Exception as e:
        logger.error(f"Failed to move files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_files(
    file_paths: List[str],
    current_user: User = Depends(get_current_user)
):
    """Delete multiple files"""
    try:
        operation = FileOperation(
            operation_type="delete",
            source_paths=file_paths,
            destination="",
            user_id=current_user.id
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return {
            "success": result.success,
            "message": result.message,
            "affected_files": result.affected_files,
            "errors": result.errors
        }
        
    except Exception as e:
        logger.error(f"Failed to delete files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-directory")
async def create_directory(
    path: str,
    project_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user)
):
    """Create a new directory"""
    try:
        operation = FileOperation(
            operation_type="create_directory",
            source_paths=[],
            destination=path,
            user_id=current_user.id,
            project_id=project_id
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return {
            "success": result.success,
            "message": result.message,
            "affected_files": result.affected_files,
            "errors": result.errors
        }
        
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rename")
async def rename_file(
    old_path: str,
    new_path: str,
    current_user: User = Depends(get_current_user)
):
    """Rename a file or directory"""
    try:
        operation = FileOperation(
            operation_type="rename",
            source_paths=[old_path],
            destination=new_path,
            user_id=current_user.id
        )
        
        result = await file_explorer_service.perform_file_operation(operation, current_user.id)
        
        return {
            "success": result.success,
            "message": result.message,
            "affected_files": result.affected_files,
            "errors": result.errors
        }
        
    except Exception as e:
        logger.error(f"Failed to rename file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# File Operations Endpoints
@router.post("/copy")
async def copy_files(
    request: FileOperationRequest,
    current_user: User = Depends(get_current_user)
):
    """Copy multiple files"""
    try:
        result = await file_operations_service.copy_files(
            source_paths=request.source_paths,
            destination=request.destination,
            user_id=current_user.id,
            overwrite=request.overwrite,
            create_backup=request.create_backup
        )
        
        return FileOperationResponse(
            result=result,
            affected_files=result.get("results", []),
            backup_paths=None
        )
        
    except Exception as e:
        logger.error(f"Failed to copy files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/move")
async def move_files(
    request: FileOperationRequest,
    current_user: User = Depends(get_current_user)
):
    """Move multiple files"""
    try:
        result = await file_operations_service.move_files(
            source_paths=request.source_paths,
            destination=request.destination,
            user_id=current_user.id,
            overwrite=request.overwrite,
            create_backup=request.create_backup
        )
        
        return FileOperationResponse(
            result=result,
            affected_files=result.get("results", []),
            backup_paths=None
        )
        
    except Exception as e:
        logger.error(f"Failed to move files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete")
async def delete_files(
    file_paths: List[str],
    create_backup: bool = True,
    permanent: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Delete multiple files"""
    try:
        result = await file_operations_service.delete_files(
            file_paths=file_paths,
            user_id=current_user.id,
            create_backup=create_backup,
            permanent=permanent
        )
        
        return FileOperationResponse(
            result=result,
            affected_files=result.get("results", []),
            backup_paths=None
        )
        
    except Exception as e:
        logger.error(f"Failed to delete files: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-directory")
async def create_directory(
    path: str,
    create_parents: bool = True,
    current_user: User = Depends(get_current_user)
):
    """Create a new directory"""
    try:
        result = await file_operations_service.create_directory(
            path=path,
            user_id=current_user.id,
            create_parents=create_parents
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to create directory: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rename")
async def rename_file(
    old_path: str,
    new_path: str,
    overwrite: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Rename a file or directory"""
    try:
        result = await file_operations_service.rename_file(
            old_path=old_path,
            new_path=new_path,
            user_id=current_user.id,
            overwrite=overwrite
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to rename file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/duplicate")
async def duplicate_file(
    file_path: str,
    current_user: User = Depends(get_current_user)
):
    """Duplicate a file"""
    try:
        result = await file_operations_service.duplicate_file(
            file_path=file_path,
            user_id=current_user.id
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to duplicate file: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/operation/{operation_id}/progress")
async def get_operation_progress(
    operation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get progress for a file operation"""
    try:
        progress = await file_operations_service.get_operation_progress(operation_id)
        
        if not progress:
            raise HTTPException(status_code=404, detail="Operation not found")
        
        return {
            "operation_id": progress.operation_id,
            "status": progress.status,
            "processed_files": progress.processed_files,
            "total_files": progress.total_files,
            "current_file": progress.current_file,
            "success_count": progress.success_count,
            "error_count": progress.error_count,
            "start_time": progress.start_time,
            "end_time": progress.end_time,
            "error_message": progress.error_message
        }
        
    except Exception as e:
        logger.error(f"Failed to get operation progress: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/operation/{operation_id}/cancel")
async def cancel_operation(
    operation_id: str,
    current_user: User = Depends(get_current_user)
):
    """Cancel a running file operation"""
    try:
        success = await file_operations_service.cancel_operation(operation_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Could not cancel operation")
        
        return {"success": True, "message": "Operation cancelled successfully"}
        
    except Exception as e:
        logger.error(f"Failed to cancel operation: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Advanced Search Endpoints
@router.get("/search/{project_id}/name")
async def search_by_name(
    project_id: UUID,
    query: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Search files by name"""
    try:
        results = await file_search_service.search_by_name(
            project_id=project_id,
            query=query,
            limit=limit
        )
        
        return FileSearchResponse(
            project_id=str(project_id),
            query=query,
            results=results,
            total_count=len(results),
            has_more=len(results) == limit,
            search_time_ms=0
        )
        
    except Exception as e:
        logger.error(f"Failed to search by name: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/{project_id}/content")
async def search_by_content(
    project_id: UUID,
    query: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Search files by content"""
    try:
        results = await file_search_service.search_by_content(
            project_id=project_id,
            query=query,
            limit=limit
        )
        
        return FileSearchResponse(
            project_id=str(project_id),
            query=query,
            results=results,
            total_count=len(results),
            has_more=len(results) == limit,
            search_time_ms=0
        )
        
    except Exception as e:
        logger.error(f"Failed to search by content: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/search/{project_id}/type")
async def search_by_type(
    project_id: UUID,
    file_types: str,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Search files by type"""
    try:
        file_type_list = [t.strip() for t in file_types.split(",")]
        results = await file_search_service.search_by_type(
            project_id=project_id,
            file_types=file_type_list,
            limit=limit
        )
        
        return FileSearchResponse(
            project_id=str(project_id),
            query=f"type:{file_types}",
            results=results,
            total_count=len(results),
            has_more=len(results) == limit,
            search_time_ms=0
        )
        
    except Exception as e:
        logger.error(f"Failed to search by type: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Health check endpoint
@router.get("/health")
async def explorer_health():
    """Health check for file explorer service"""
    return {
        "status": "healthy",
        "service": "file_explorer",
        "features": [
            "file_tree",
            "file_search",
            "file_preview",
            "file_operations",
            "git_integration",
            "metadata_analysis",
            "advanced_search",
            "progress_tracking"
        ]
    }
