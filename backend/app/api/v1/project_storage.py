"""
Expert-Level Project Storage API Endpoints
Enterprise-grade file storage, Git integration, and template management
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from typing import List, Dict, Optional, Any
from uuid import UUID
import io
import json

from app.core.auth import get_current_user
from app.models.user import User
from app.services.storage.file_storage_service import FileStorageService
from app.services.git.git_service import GitService
from app.services.templates.template_service import TemplateService
from app.schemas.project_storage import (
    FileUploadResponse, FileListResponse, FileDownloadResponse,
    GitCloneRequest, GitCommitRequest, GitPushRequest, GitPullRequest,
    TemplateCreateRequest, TemplateApplyRequest, TemplateListResponse,
    TemplateDetailsResponse, TemplateUpdateRequest, TemplateShareRequest
)

router = APIRouter(prefix="/project-storage", tags=["Project Storage"])

# Initialize services
file_storage = FileStorageService()
git_service = GitService()
template_service = TemplateService()


# File Storage Endpoints

@router.post("/projects/{project_id}/files/upload", response_model=FileUploadResponse)
async def upload_file(
    project_id: UUID,
    file: UploadFile = File(...),
    file_path: str = Form(...),
    commit_message: str = Form(None),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file to project storage with version control
    """
    try:
        # Read file content
        content = await file.read()
        
        # Upload file
        project_file = await file_storage.upload_file(
            project_id=project_id,
            file_path=file_path,
            content=content,
            user_id=current_user.id,
            commit_message=commit_message
        )
        
        return FileUploadResponse(
            success=True,
            file_id=str(project_file.id),
            file_path=project_file.file_path,
            file_size=project_file.file_size,
            version=project_file.version,
            message="File uploaded successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/files/download")
async def download_file(
    project_id: UUID,
    file_path: str = Query(...),
    version: int = Query(None),
    current_user: User = Depends(get_current_user)
):
    """
    Download a file from project storage
    """
    try:
        # Download file
        content, metadata = await file_storage.download_file(
            project_id=project_id,
            file_path=file_path,
            version=version
        )
        
        # Create streaming response
        return StreamingResponse(
            io.BytesIO(content),
            media_type=metadata.get('mime_type', 'application/octet-stream'),
            headers={
                'Content-Disposition': f'attachment; filename="{metadata["file_name"]}"',
                'X-File-Metadata': json.dumps(metadata)
            }
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/files", response_model=FileListResponse)
async def list_files(
    project_id: UUID,
    directory_path: str = Query(None),
    file_type: str = Query(None),
    search_query: str = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    """
    List files in project with advanced filtering
    """
    try:
        files = await file_storage.list_files(
            project_id=project_id,
            directory_path=directory_path,
            file_type=file_type,
            search_query=search_query,
            limit=limit,
            offset=offset
        )
        
        return FileListResponse(
            success=True,
            files=files,
            total_count=len(files),
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/projects/{project_id}/files")
async def delete_file(
    project_id: UUID,
    file_path: str = Query(...),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a file from project storage
    """
    try:
        success = await file_storage.delete_file(
            project_id=project_id,
            file_path=file_path,
            user_id=current_user.id
        )
        
        return {"success": success, "message": "File deleted successfully"}
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/directories")
async def create_directory(
    project_id: UUID,
    directory_path: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """
    Create a directory in project storage
    """
    try:
        directory = await file_storage.create_directory(
            project_id=project_id,
            directory_path=directory_path,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "directory_id": str(directory.id),
            "directory_path": directory.directory_path,
            "message": "Directory created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/file-tree")
async def get_file_tree(
    project_id: UUID,
    root_path: str = Query(""),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete file tree structure
    """
    try:
        tree = await file_storage.get_file_tree(
            project_id=project_id,
            root_path=root_path
        )
        
        return {"success": True, "file_tree": tree}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/files/search")
async def search_files(
    project_id: UUID,
    query: str = Query(...),
    file_types: List[str] = Query(None),
    search_content: bool = Query(True),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Search files with advanced filtering
    """
    try:
        results = await file_storage.search_files(
            project_id=project_id,
            query=query,
            file_types=file_types,
            search_content=search_content,
            limit=limit
        )
        
        return {
            "success": True,
            "results": results,
            "total_count": len(results),
            "query": query
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Git Integration Endpoints

@router.post("/projects/{project_id}/git/clone")
async def clone_repository(
    project_id: UUID,
    request: GitCloneRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Clone a Git repository into project storage
    """
    try:
        result = await git_service.clone_repository(
            project_id=project_id,
            repo_url=request.repo_url,
            branch=request.branch,
            credentials=request.credentials
        )
        
        if result['success']:
            return {
                "success": True,
                "repository_path": result['repository_path'],
                "repository_info": result['repository_info'],
                "files_imported": result['files_imported'],
                "message": "Repository cloned successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/git/commit")
async def commit_changes(
    project_id: UUID,
    request: GitCommitRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Commit changes to Git repository
    """
    try:
        result = await git_service.commit_changes(
            project_id=project_id,
            message=request.message,
            user_id=current_user.id,
            files=request.files,
            author_name=request.author_name,
            author_email=request.author_email
        )
        
        if result['success']:
            return {
                "success": True,
                "commit_hash": result['commit_hash'],
                "commit_message": result['commit_message'],
                "author": result['author'],
                "timestamp": result['timestamp'],
                "message": "Changes committed successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/git/push")
async def push_changes(
    project_id: UUID,
    request: GitPushRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Push changes to remote repository
    """
    try:
        result = await git_service.push_changes(
            project_id=project_id,
            remote=request.remote,
            branch=request.branch
        )
        
        if result['success']:
            return {
                "success": True,
                "remote": result['remote'],
                "branch": result['branch'],
                "push_info": result['push_info'],
                "message": "Changes pushed successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/git/pull")
async def pull_changes(
    project_id: UUID,
    request: GitPullRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Pull changes from remote repository
    """
    try:
        result = await git_service.pull_changes(
            project_id=project_id,
            remote=request.remote,
            branch=request.branch
        )
        
        if result['success']:
            return {
                "success": True,
                "remote": result['remote'],
                "branch": result['branch'],
                "pull_info": result['pull_info'],
                "files_updated": result['files_updated'],
                "message": "Changes pulled successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/git/history")
async def get_git_history(
    project_id: UUID,
    branch: str = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user)
):
    """
    Get Git commit history
    """
    try:
        history = await git_service.get_branch_history(
            project_id=project_id,
            branch=branch,
            limit=limit
        )
        
        return {
            "success": True,
            "history": history,
            "total_commits": len(history)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/git/branches")
async def create_branch(
    project_id: UUID,
    branch_name: str = Form(...),
    source_branch: str = Form("main"),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new Git branch
    """
    try:
        result = await git_service.create_branch(
            project_id=project_id,
            branch_name=branch_name,
            source_branch=source_branch
        )
        
        if result['success']:
            return {
                "success": True,
                "branch_name": result['branch_name'],
                "source_branch": result['source_branch'],
                "current_branch": result['current_branch'],
                "message": "Branch created successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/git/switch-branch")
async def switch_branch(
    project_id: UUID,
    branch_name: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """
    Switch to a different Git branch
    """
    try:
        result = await git_service.switch_branch(
            project_id=project_id,
            branch_name=branch_name
        )
        
        if result['success']:
            return {
                "success": True,
                "current_branch": result['current_branch'],
                "files_imported": result['files_imported'],
                "message": "Switched to branch successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/git/status")
async def get_git_status(
    project_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Get Git repository status
    """
    try:
        status = await git_service.get_repository_status(project_id)
        
        if status['success']:
            return status
        else:
            raise HTTPException(status_code=400, detail=status['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Template Management Endpoints

@router.post("/templates", response_model=Dict)
async def create_template(
    request: TemplateCreateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Create a template from an existing project
    """
    try:
        template = await template_service.create_template(
            project_id=request.project_id,
            template_name=request.template_name,
            description=request.description,
            category=request.category,
            subcategory=request.subcategory,
            tags=request.tags,
            is_public=request.is_public,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "template_id": str(template.id),
            "template_name": template.name,
            "category": template.category,
            "message": "Template created successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/templates/{template_id}/apply")
async def apply_template(
    template_id: UUID,
    request: TemplateApplyRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Apply a template to create a new project
    """
    try:
        result = await template_service.apply_template(
            template_id=template_id,
            new_project_id=request.new_project_id,
            variables=request.variables,
            user_id=current_user.id
        )
        
        if result['success']:
            return {
                "success": True,
                "template_name": result['template_name'],
                "project_id": result['project_id'],
                "files_created": result['files_created'],
                "applied_variables": result['applied_variables'],
                "message": "Template applied successfully"
            }
        else:
            raise HTTPException(status_code=400, detail=result['error'])
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates", response_model=TemplateListResponse)
async def list_templates(
    category: str = Query(None),
    subcategory: str = Query(None),
    tags: List[str] = Query(None),
    complexity_level: str = Query(None),
    is_public: bool = Query(True),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user)
):
    """
    List templates with advanced filtering
    """
    try:
        templates = await template_service.list_templates(
            category=category,
            subcategory=subcategory,
            tags=tags,
            complexity_level=complexity_level,
            is_public=is_public,
            limit=limit,
            offset=offset
        )
        
        return TemplateListResponse(
            success=True,
            templates=templates,
            total_count=len(templates),
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates/{template_id}", response_model=TemplateDetailsResponse)
async def get_template_details(
    template_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Get detailed template information
    """
    try:
        template_details = await template_service.get_template_details(template_id)
        
        return TemplateDetailsResponse(
            success=True,
            template=template_details
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/templates/{template_id}")
async def update_template(
    template_id: UUID,
    request: TemplateUpdateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Update template with validation
    """
    try:
        template = await template_service.update_template(
            template_id=template_id,
            updates=request.updates,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "template_id": str(template.id),
            "template_name": template.name,
            "message": "Template updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/templates/{template_id}/share")
async def share_template(
    template_id: UUID,
    request: TemplateShareRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Share template with specific users
    """
    try:
        success = await template_service.share_template(
            template_id=template_id,
            user_ids=request.user_ids
        )
        
        return {
            "success": success,
            "template_id": str(template_id),
            "shared_with": request.user_ids,
            "message": "Template shared successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/templates/{template_id}/validate")
async def validate_template(
    template_id: UUID,
    current_user: User = Depends(get_current_user)
):
    """
    Validate template structure and content
    """
    try:
        validation_results = await template_service.validate_template(template_id)
        
        return {
            "success": True,
            "template_id": str(template_id),
            "validation_results": validation_results,
            "message": "Template validation completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates/{template_id}/export")
async def export_template(
    template_id: UUID,
    format: str = Query("zip"),
    current_user: User = Depends(get_current_user)
):
    """
    Export template as downloadable package
    """
    try:
        template_data = await template_service.export_template(template_id, format)
        
        return StreamingResponse(
            io.BytesIO(template_data),
            media_type="application/zip",
            headers={
                'Content-Disposition': f'attachment; filename="template_{template_id}.zip"'
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
