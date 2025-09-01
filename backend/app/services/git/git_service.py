"""
Expert-Level Git Integration Service
Enterprise-grade Git integration with full version control and collaboration
"""

import os
import subprocess
import tempfile
import shutil
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path
from uuid import UUID
import asyncio
import json

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import git
from git import Repo, GitCommandError
import requests

from app.models.project_storage import ProjectFile, FileChange
from app.core.database import get_db
from app.core.config import settings
from app.services.storage.file_storage_service import FileStorageService

logger = logging.getLogger(__name__)


class GitService:
    """
    Expert-level Git integration service with enterprise features
    """
    
    def __init__(self):
        self.file_storage = FileStorageService()
        self.git_root = Path(settings.GIT_REPOSITORIES_PATH)
        self.git_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize Git configuration
        self._init_git_config()
    
    def _init_git_config(self):
        """Initialize Git configuration"""
        try:
            # Set global Git configuration
            subprocess.run(['git', 'config', '--global', 'user.name', 'CloudMind System'], check=True)
            subprocess.run(['git', 'config', '--global', 'user.email', 'system@cloudmind.ai'], check=True)
            
            # Configure Git for better performance
            subprocess.run(['git', 'config', '--global', 'core.compression', '9'], check=True)
            subprocess.run(['git', 'config', '--global', 'core.packedGitLimit', '512m'], check=True)
            subprocess.run(['git', 'config', '--global', 'core.packedGitWindowSize', '512m'], check=True)
            
            logger.info("Git configuration initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Git configuration: {e}")
    
    async def clone_repository(
        self, 
        project_id: UUID, 
        repo_url: str, 
        branch: str = "main",
        credentials: Dict = None
    ) -> Dict:
        """
        Clone a repository with authentication and error handling
        """
        try:
            project_path = self.git_root / str(project_id)
            
            # Remove existing repository if it exists
            if project_path.exists():
                shutil.rmtree(project_path)
            
            # Prepare clone URL with credentials if provided
            clone_url = self._prepare_clone_url(repo_url, credentials)
            
            # Clone repository
            logger.info(f"Cloning repository: {repo_url} to {project_path}")
            repo = Repo.clone_from(clone_url, project_path, branch=branch)
            
            # Configure repository
            self._configure_repository(repo, project_id)
            
            # Import all files to storage
            await self._import_repository_files(project_id, project_path)
            
            # Get repository information
            repo_info = self._get_repository_info(repo)
            
            logger.info(f"Repository cloned successfully: {repo_url}")
            return {
                'success': True,
                'repository_path': str(project_path),
                'repository_info': repo_info,
                'files_imported': repo_info['total_files']
            }
            
        except GitCommandError as e:
            logger.error(f"Git command failed: {e}")
            return {
                'success': False,
                'error': f"Git command failed: {str(e)}",
                'error_code': 'GIT_COMMAND_ERROR'
            }
        except Exception as e:
            logger.error(f"Failed to clone repository: {e}")
            return {
                'success': False,
                'error': f"Failed to clone repository: {str(e)}",
                'error_code': 'CLONE_ERROR'
            }
    
    async def commit_changes(
        self, 
        project_id: UUID, 
        message: str, 
        user_id: UUID,
        files: List[str] = None,
        author_name: str = None,
        author_email: str = None
    ) -> Dict:
        """
        Commit changes with detailed tracking
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Configure author if provided
            if author_name and author_email:
                repo.config_writer().set_value('user', 'name', author_name).release()
                repo.config_writer().set_value('user', 'email', author_email).release()
            
            # Stage files
            if files:
                for file_path in files:
                    full_path = project_path / file_path
                    if full_path.exists():
                        repo.index.add([str(full_path)])
            else:
                # Stage all changes
                repo.index.add('*')
            
            # Check if there are changes to commit
            if not repo.index.diff('HEAD') and not repo.untracked_files:
                return {
                    'success': True,
                    'message': 'No changes to commit',
                    'commit_hash': None
                }
            
            # Create commit
            commit = repo.index.commit(message)
            
            # Update file records in database
            await self._update_file_records_after_commit(project_id, commit, user_id)
            
            logger.info(f"Changes committed successfully: {commit.hexsha}")
            return {
                'success': True,
                'commit_hash': commit.hexsha,
                'commit_message': message,
                'author': commit.author.name,
                'author_email': commit.author.email,
                'timestamp': commit.committed_datetime.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to commit changes: {e}")
            return {
                'success': False,
                'error': f"Failed to commit changes: {str(e)}",
                'error_code': 'COMMIT_ERROR'
            }
    
    async def push_changes(self, project_id: UUID, remote: str = "origin", branch: str = None) -> Dict:
        """
        Push changes to remote repository
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Get current branch if not specified
            if not branch:
                branch = repo.active_branch.name
            
            # Push changes
            origin = repo.remotes[remote]
            push_info = origin.push(branch)
            
            # Check for errors
            for info in push_info:
                if info.flags & git.PushInfo.ERROR:
                    raise GitCommandError(f"Push failed: {info.summary}")
            
            logger.info(f"Changes pushed successfully to {remote}/{branch}")
            return {
                'success': True,
                'remote': remote,
                'branch': branch,
                'push_info': [str(info) for info in push_info]
            }
            
        except Exception as e:
            logger.error(f"Failed to push changes: {e}")
            return {
                'success': False,
                'error': f"Failed to push changes: {str(e)}",
                'error_code': 'PUSH_ERROR'
            }
    
    async def pull_changes(self, project_id: UUID, remote: str = "origin", branch: str = None) -> Dict:
        """
        Pull changes from remote repository
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Get current branch if not specified
            if not branch:
                branch = repo.active_branch.name
            
            # Pull changes
            origin = repo.remotes[remote]
            pull_info = origin.pull(branch)
            
            # Import new/changed files
            await self._import_repository_files(project_id, project_path)
            
            logger.info(f"Changes pulled successfully from {remote}/{branch}")
            return {
                'success': True,
                'remote': remote,
                'branch': branch,
                'pull_info': [str(info) for info in pull_info],
                'files_updated': len(pull_info)
            }
            
        except Exception as e:
            logger.error(f"Failed to pull changes: {e}")
            return {
                'success': False,
                'error': f"Failed to pull changes: {str(e)}",
                'error_code': 'PULL_ERROR'
            }
    
    async def get_branch_history(self, project_id: UUID, branch: str = None, limit: int = 50) -> List[Dict]:
        """
        Get detailed branch history with file changes
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Get branch
            if not branch:
                branch = repo.active_branch.name
            
            # Get commits
            commits = list(repo.iter_commits(branch, max_count=limit))
            
            # Format commit history
            history = []
            for commit in commits:
                commit_info = {
                    'hash': commit.hexsha,
                    'short_hash': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': {
                        'name': commit.author.name,
                        'email': commit.author.email
                    },
                    'timestamp': commit.committed_datetime.isoformat(),
                    'files_changed': [],
                    'stats': {
                        'insertions': commit.stats.total['insertions'],
                        'deletions': commit.stats.total['deletions'],
                        'lines': commit.stats.total['lines']
                    }
                }
                
                # Get files changed in this commit
                if commit.parents:
                    parent = commit.parents[0]
                    diff = parent.diff(commit)
                    for change in diff:
                        file_info = {
                            'path': change.a_path or change.b_path,
                            'change_type': change.change_type,
                            'additions': change.stats.get('insertions', 0),
                            'deletions': change.stats.get('deletions', 0)
                        }
                        commit_info['files_changed'].append(file_info)
                
                history.append(commit_info)
            
            return history
            
        except Exception as e:
            logger.error(f"Failed to get branch history: {e}")
            raise
    
    async def create_branch(self, project_id: UUID, branch_name: str, source_branch: str = "main") -> Dict:
        """
        Create a new branch
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Check if branch already exists
            if branch_name in [branch.name for branch in repo.branches]:
                return {
                    'success': False,
                    'error': f"Branch '{branch_name}' already exists",
                    'error_code': 'BRANCH_EXISTS'
                }
            
            # Create new branch
            new_branch = repo.create_head(branch_name, source_branch)
            new_branch.checkout()
            
            logger.info(f"Branch created successfully: {branch_name}")
            return {
                'success': True,
                'branch_name': branch_name,
                'source_branch': source_branch,
                'current_branch': repo.active_branch.name
            }
            
        except Exception as e:
            logger.error(f"Failed to create branch: {e}")
            return {
                'success': False,
                'error': f"Failed to create branch: {str(e)}",
                'error_code': 'BRANCH_CREATE_ERROR'
            }
    
    async def switch_branch(self, project_id: UUID, branch_name: str) -> Dict:
        """
        Switch to a different branch
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                raise ValueError(f"Repository not found for project: {project_id}")
            
            repo = Repo(project_path)
            
            # Check if branch exists
            if branch_name not in [branch.name for branch in repo.branches]:
                return {
                    'success': False,
                    'error': f"Branch '{branch_name}' does not exist",
                    'error_code': 'BRANCH_NOT_FOUND'
                }
            
            # Switch to branch
            repo.heads[branch_name].checkout()
            
            # Import files from new branch
            await self._import_repository_files(project_id, project_path)
            
            logger.info(f"Switched to branch: {branch_name}")
            return {
                'success': True,
                'current_branch': branch_name,
                'files_imported': True
            }
            
        except Exception as e:
            logger.error(f"Failed to switch branch: {e}")
            return {
                'success': False,
                'error': f"Failed to switch branch: {str(e)}",
                'error_code': 'BRANCH_SWITCH_ERROR'
            }
    
    async def get_repository_status(self, project_id: UUID) -> Dict:
        """
        Get comprehensive repository status
        """
        try:
            project_path = self.git_root / str(project_id)
            
            if not project_path.exists():
                return {
                    'success': False,
                    'error': f"Repository not found for project: {project_id}",
                    'error_code': 'REPO_NOT_FOUND'
                }
            
            repo = Repo(project_path)
            
            # Get repository information
            repo_info = self._get_repository_info(repo)
            
            # Get status
            status = {
                'current_branch': repo.active_branch.name,
                'branches': [branch.name for branch in repo.branches],
                'remotes': [remote.name for remote in repo.remotes],
                'is_dirty': repo.is_dirty(),
                'untracked_files': repo.untracked_files,
                'staged_files': [item.a_path for item in repo.index.diff('HEAD')],
                'modified_files': [item.a_path for item in repo.index.diff(None)],
                'last_commit': {
                    'hash': repo.head.commit.hexsha,
                    'message': repo.head.commit.message.strip(),
                    'author': repo.head.commit.author.name,
                    'timestamp': repo.head.commit.committed_datetime.isoformat()
                } if repo.head.commit else None
            }
            
            return {
                'success': True,
                'repository_info': repo_info,
                'status': status
            }
            
        except Exception as e:
            logger.error(f"Failed to get repository status: {e}")
            return {
                'success': False,
                'error': f"Failed to get repository status: {str(e)}",
                'error_code': 'STATUS_ERROR'
            }
    
    # Helper methods
    
    def _prepare_clone_url(self, repo_url: str, credentials: Dict = None) -> str:
        """Prepare clone URL with credentials if provided"""
        if not credentials:
            return repo_url
        
        # Handle different authentication methods
        if 'username' in credentials and 'password' in credentials:
            # HTTPS with username/password
            url_parts = repo_url.split('://')
            if len(url_parts) == 2:
                return f"{url_parts[0]}://{credentials['username']}:{credentials['password']}@{url_parts[1]}"
        
        elif 'token' in credentials:
            # HTTPS with token
            url_parts = repo_url.split('://')
            if len(url_parts) == 2:
                return f"{url_parts[0]}://{credentials['token']}@{url_parts[1]}"
        
        return repo_url
    
    def _configure_repository(self, repo: Repo, project_id: UUID):
        """Configure repository settings"""
        try:
            # Set repository-specific configuration
            repo.config_writer().set_value('core', 'autocrlf', 'input').release()
            repo.config_writer().set_value('core', 'safecrlf', 'warn').release()
            
            # Configure merge strategy
            repo.config_writer().set_value('merge', 'ff', 'false').release()
            
            logger.info(f"Repository configured for project: {project_id}")
        except Exception as e:
            logger.warning(f"Failed to configure repository: {e}")
    
    async def _import_repository_files(self, project_id: UUID, repo_path: Path):
        """Import all files from repository to storage"""
        try:
            # Walk through all files in repository
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not self._is_git_file(file_path):
                    # Calculate relative path
                    relative_path = str(file_path.relative_to(repo_path))
                    
                    # Read file content
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    
                    # Upload to storage (this will handle versioning)
                    await self.file_storage.upload_file(
                        project_id=project_id,
                        file_path=relative_path,
                        content=content,
                        user_id=UUID('00000000-0000-0000-0000-000000000000'),  # System user
                        commit_message=f"Import from Git: {relative_path}"
                    )
            
            logger.info(f"Repository files imported for project: {project_id}")
            
        except Exception as e:
            logger.error(f"Failed to import repository files: {e}")
    
    def _is_git_file(self, file_path: Path) -> bool:
        """Check if file is a Git metadata file"""
        git_patterns = ['.git', '.gitignore', '.gitattributes']
        return any(pattern in str(file_path) for pattern in git_patterns)
    
    def _get_repository_info(self, repo: Repo) -> Dict:
        """Get comprehensive repository information"""
        try:
            # Get repository statistics
            total_files = len(list(repo.working_tree_dir.rglob('*')))
            total_commits = len(list(repo.iter_commits()))
            
            # Get file types
            file_types = {}
            for file_path in repo.working_tree_dir.rglob('*'):
                if file_path.is_file() and not self._is_git_file(file_path):
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                'total_files': total_files,
                'total_commits': total_commits,
                'file_types': file_types,
                'repository_size': self._calculate_repo_size(repo.working_tree_dir),
                'last_activity': repo.head.commit.committed_datetime.isoformat() if repo.head.commit else None
            }
        except Exception as e:
            logger.error(f"Failed to get repository info: {e}")
            return {}
    
    def _calculate_repo_size(self, repo_path: Path) -> int:
        """Calculate repository size in bytes"""
        total_size = 0
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
    async def _update_file_records_after_commit(self, project_id: UUID, commit, user_id: UUID):
        """Update file records in database after commit"""
        try:
            db = next(get_db())
            
            # Get files changed in this commit
            if commit.parents:
                parent = commit.parents[0]
                diff = parent.diff(commit)
                
                for change in diff:
                    file_path = change.a_path or change.b_path
                    
                    # Update file record
                    project_file = db.query(ProjectFile).filter(
                        and_(
                            ProjectFile.project_id == project_id,
                            ProjectFile.file_path == file_path,
                            ProjectFile.is_latest == True
                        )
                    ).first()
                    
                    if project_file:
                        # Update commit information
                        project_file.commit_message = commit.message.strip()
                        project_file.commit_author_id = user_id
                        project_file.updated_at = datetime.utcnow()
                        
                        # Create change record
                        change_record = FileChange(
                            file_id=project_file.id,
                            change_type=change.change_type,
                            change_hash=commit.hexsha,
                            author_id=user_id,
                            commit_message=commit.message.strip(),
                            branch_name=commit.repo.active_branch.name
                        )
                        db.add(change_record)
            
            db.commit()
            
        except Exception as e:
            logger.error(f"Failed to update file records after commit: {e}")
