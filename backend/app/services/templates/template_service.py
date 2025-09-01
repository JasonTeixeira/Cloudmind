"""
Expert-Level Template Service
Enterprise-grade project template management with validation and sharing
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path
from uuid import UUID, uuid4
import asyncio
import shutil
import zipfile
import tempfile

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
import yaml
import jinja2

from app.models.project_storage import ProjectTemplate, ProjectFile, ProjectDirectory
from app.core.database import get_db
from app.core.config import settings
from app.services.storage.file_storage_service import FileStorageService
# from app.services.ai.template_analysis import TemplateAnalysisService

logger = logging.getLogger(__name__)


class TemplateService:
    """
    Expert-level template service with enterprise features
    """
    
    def __init__(self):
        self.file_storage = FileStorageService()
        # self.analysis_service = TemplateAnalysisService()
        self.template_root = Path(settings.TEMPLATE_STORAGE_PATH)
        self.template_root.mkdir(parents=True, exist_ok=True)
        
        # Initialize Jinja2 environment for template rendering
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_root)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    async def create_template(
        self, 
        project_id: UUID, 
        template_name: str,
        description: str = None,
        category: str = "custom",
        subcategory: str = None,
        tags: List[str] = None,
        is_public: bool = False,
        user_id: UUID = None
    ) -> ProjectTemplate:
        """
        Create a template from an existing project
        """
        try:
            db = next(get_db())
            
            # Get all files from the project
            files = await self.file_storage.list_files(project_id, limit=1000)
            
            if not files:
                raise ValueError("No files found in project to create template")
            
            # Analyze project structure
            project_analysis = await self._analyze_project_structure(files)
            
            # Create template file structure
            file_structure = await self._create_file_structure(files)
            
            # Extract template files
            template_files = await self._extract_template_files(files)
            
            # Generate template variables
            variables = await self._generate_template_variables(files, project_analysis)
            
            # Create template record
            template = ProjectTemplate(
                name=template_name,
                description=description or f"Template created from project {project_id}",
                category=category,
                subcategory=subcategory,
                tags=tags or [],
                file_structure=file_structure,
                template_files=template_files,
                variables=variables,
                dependencies=project_analysis.get('dependencies', {}),
                complexity_level=project_analysis.get('complexity_level', 'intermediate'),
                estimated_duration=project_analysis.get('estimated_duration', 8),
                technology_stack=project_analysis.get('technology_stack', []),
                architecture_pattern=project_analysis.get('architecture_pattern', 'custom'),
                created_by=user_id,
                is_public=is_public
            )
            
            db.add(template)
            db.commit()
            db.refresh(template)
            
            # Save template files to storage
            await self._save_template_files(template.id, template_files)
            
            logger.info(f"Template created successfully: {template_name} (ID: {template.id})")
            return template
            
        except Exception as e:
            logger.error(f"Failed to create template: {e}")
            raise
    
    async def apply_template(
        self, 
        template_id: UUID, 
        new_project_id: UUID,
        variables: Dict[str, Any] = None,
        user_id: UUID = None
    ) -> Dict:
        """
        Apply a template to create a new project
        """
        try:
            db = next(get_db())
            
            # Get template
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Validate variables
            validated_variables = await self._validate_template_variables(template.variables, variables or {})
            
            # Get template files
            template_files = await self._load_template_files(template_id)
            
            # Apply template to files
            applied_files = await self._apply_template_to_files(template_files, validated_variables)
            
            # Create project structure
            created_files = []
            for file_info in applied_files:
                file_path = file_info['path']
                content = file_info['content']
                
                # Create file in new project
                project_file = await self.file_storage.upload_file(
                    project_id=new_project_id,
                    file_path=file_path,
                    content=content.encode('utf-8'),
                    user_id=user_id,
                    commit_message=f"Apply template: {template.name}"
                )
                created_files.append(project_file)
            
            # Update template usage count
            template.usage_count += 1
            db.commit()
            
            logger.info(f"Template applied successfully: {template.name} -> Project {new_project_id}")
            return {
                'success': True,
                'template_name': template.name,
                'project_id': str(new_project_id),
                'files_created': len(created_files),
                'applied_variables': validated_variables
            }
            
        except Exception as e:
            logger.error(f"Failed to apply template: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def list_templates(
        self, 
        category: str = None,
        subcategory: str = None,
        tags: List[str] = None,
        complexity_level: str = None,
        is_public: bool = True,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """
        List templates with advanced filtering
        """
        try:
            db = next(get_db())
            
            # Build query
            query = db.query(ProjectTemplate)
            
            # Apply filters
            if category:
                query = query.filter(ProjectTemplate.category == category)
            
            if subcategory:
                query = query.filter(ProjectTemplate.subcategory == subcategory)
            
            if complexity_level:
                query = query.filter(ProjectTemplate.complexity_level == complexity_level)
            
            if is_public is not None:
                query = query.filter(ProjectTemplate.is_public == is_public)
            
            if tags:
                # Filter by tags (JSONB contains)
                for tag in tags:
                    query = query.filter(ProjectTemplate.tags.contains([tag]))
            
            # Apply pagination and ordering
            query = query.order_by(desc(ProjectTemplate.usage_count), desc(ProjectTemplate.created_at))
            query = query.offset(offset).limit(limit)
            
            templates = query.all()
            
            # Format response
            template_list = []
            for template in templates:
                template_info = {
                    'id': str(template.id),
                    'name': template.name,
                    'description': template.description,
                    'category': template.category,
                    'subcategory': template.subcategory,
                    'tags': template.tags,
                    'complexity_level': template.complexity_level,
                    'estimated_duration': template.estimated_duration,
                    'technology_stack': template.technology_stack,
                    'architecture_pattern': template.architecture_pattern,
                    'usage_count': template.usage_count,
                    'rating': template.rating,
                    'is_public': template.is_public,
                    'is_featured': template.is_featured,
                    'created_at': template.created_at.isoformat(),
                    'updated_at': template.updated_at.isoformat(),
                    'created_by': str(template.created_by)
                }
                template_list.append(template_info)
            
            return template_list
            
        except Exception as e:
            logger.error(f"Failed to list templates: {e}")
            raise
    
    async def get_template_details(self, template_id: UUID) -> Dict:
        """
        Get detailed template information
        """
        try:
            db = next(get_db())
            
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Get template files
            template_files = await self._load_template_files(template_id)
            
            # Get usage statistics
            usage_stats = await self._get_template_usage_stats(template_id)
            
            template_details = {
                'id': str(template.id),
                'name': template.name,
                'description': template.description,
                'category': template.category,
                'subcategory': template.subcategory,
                'tags': template.tags,
                'file_structure': template.file_structure,
                'variables': template.variables,
                'dependencies': template.dependencies,
                'complexity_level': template.complexity_level,
                'estimated_duration': template.estimated_duration,
                'technology_stack': template.technology_stack,
                'architecture_pattern': template.architecture_pattern,
                'template_version': template.template_version,
                'is_validated': template.is_validated,
                'validation_results': template.validation_results,
                'test_coverage': template.test_coverage,
                'usage_count': template.usage_count,
                'rating': template.rating,
                'reviews': template.reviews,
                'is_public': template.is_public,
                'is_featured': template.is_featured,
                'shared_with': template.shared_with,
                'created_at': template.created_at.isoformat(),
                'updated_at': template.updated_at.isoformat(),
                'created_by': str(template.created_by),
                'template_files': template_files,
                'usage_stats': usage_stats
            }
            
            return template_details
            
        except Exception as e:
            logger.error(f"Failed to get template details: {e}")
            raise
    
    async def update_template(
        self, 
        template_id: UUID, 
        updates: Dict[str, Any],
        user_id: UUID = None
    ) -> ProjectTemplate:
        """
        Update template with validation
        """
        try:
            db = next(get_db())
            
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Update allowed fields
            allowed_fields = [
                'name', 'description', 'category', 'subcategory', 'tags',
                'complexity_level', 'estimated_duration', 'technology_stack',
                'architecture_pattern', 'is_public', 'is_featured', 'shared_with'
            ]
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(template, field):
                    setattr(template, field, value)
            
            # Update version
            template.template_version = self._increment_version(template.template_version)
            template.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(template)
            
            logger.info(f"Template updated successfully: {template.name}")
            return template
            
        except Exception as e:
            logger.error(f"Failed to update template: {e}")
            raise
    
    async def share_template(self, template_id: UUID, user_ids: List[UUID]) -> bool:
        """
        Share template with specific users
        """
        try:
            db = next(get_db())
            
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Update shared_with list
            current_shared = template.shared_with or []
            new_shared = list(set(current_shared + [str(uid) for uid in user_ids]))
            template.shared_with = new_shared
            
            db.commit()
            
            logger.info(f"Template shared with {len(user_ids)} users")
            return True
            
        except Exception as e:
            logger.error(f"Failed to share template: {e}")
            raise
    
    async def validate_template(self, template_id: UUID) -> Dict:
        """
        Validate template structure and content
        """
        try:
            db = next(get_db())
            
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Get template files
            template_files = await self._load_template_files(template_id)
            
            # Perform validation
            validation_results = await self._perform_template_validation(template, template_files)
            
            # Update template validation status
            template.is_validated = validation_results['is_valid']
            template.validation_results = validation_results
            db.commit()
            
            logger.info(f"Template validation completed: {template.name}")
            return validation_results
            
        except Exception as e:
            logger.error(f"Failed to validate template: {e}")
            raise
    
    async def export_template(self, template_id: UUID, format: str = "zip") -> bytes:
        """
        Export template as downloadable package
        """
        try:
            db = next(get_db())
            
            template = db.query(ProjectTemplate).filter(ProjectTemplate.id == template_id).first()
            if not template:
                raise ValueError(f"Template not found: {template_id}")
            
            # Get template files
            template_files = await self._load_template_files(template_id)
            
            if format == "zip":
                return await self._create_template_zip(template, template_files)
            else:
                raise ValueError(f"Unsupported export format: {format}")
                
        except Exception as e:
            logger.error(f"Failed to export template: {e}")
            raise
    
    # Helper methods
    
    async def _analyze_project_structure(self, files: List[Dict]) -> Dict:
        """Analyze project structure for template creation"""
        try:
            # Analyze file types and structure
            file_types = {}
            directories = set()
            total_size = 0
            
            for file_info in files:
                file_type = file_info['file_type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
                directories.add(file_info['directory_path'])
                total_size += file_info['file_size']
            
            # Detect technology stack
            technology_stack = await self.analysis_service.detect_technology_stack(files)
            
            # Determine architecture pattern
            architecture_pattern = await self.analysis_service.detect_architecture_pattern(files)
            
            # Calculate complexity
            complexity_level = await self.analysis_service.calculate_complexity_level(files)
            
            # Estimate duration
            estimated_duration = await self.analysis_service.estimate_implementation_duration(files)
            
            # Detect dependencies
            dependencies = await self.analysis_service.extract_dependencies(files)
            
            return {
                'file_types': file_types,
                'directories': list(directories),
                'total_files': len(files),
                'total_size': total_size,
                'technology_stack': technology_stack,
                'architecture_pattern': architecture_pattern,
                'complexity_level': complexity_level,
                'estimated_duration': estimated_duration,
                'dependencies': dependencies
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze project structure: {e}")
            return {}
    
    async def _create_file_structure(self, files: List[Dict]) -> Dict:
        """Create hierarchical file structure"""
        try:
            structure = {
                'root': {},
                'directories': {},
                'files': []
            }
            
            for file_info in files:
                file_path = file_info['file_path']
                directory = file_info['directory_path']
                
                # Add to files list
                structure['files'].append({
                    'path': file_path,
                    'name': file_info['file_name'],
                    'type': file_info['file_type'],
                    'size': file_info['file_size'],
                    'directory': directory
                })
                
                # Build directory structure
                if directory not in structure['directories']:
                    structure['directories'][directory] = []
                structure['directories'][directory].append(file_info['file_name'])
            
            return structure
            
        except Exception as e:
            logger.error(f"Failed to create file structure: {e}")
            return {}
    
    async def _extract_template_files(self, files: List[Dict]) -> Dict:
        """Extract template files with variable placeholders"""
        try:
            template_files = {}
            
            for file_info in files:
                file_path = file_info['file_path']
                
                # Get file content
                content, _ = await self.file_storage.download_file(
                    project_id=file_info['project_id'],
                    file_path=file_path
                )
                
                # Convert content to template
                template_content = await self._convert_to_template(content.decode('utf-8'), file_path)
                
                template_files[file_path] = {
                    'content': template_content,
                    'type': file_info['file_type'],
                    'size': len(template_content),
                    'variables': await self._extract_variables_from_content(template_content)
                }
            
            return template_files
            
        except Exception as e:
            logger.error(f"Failed to extract template files: {e}")
            return {}
    
    async def _convert_to_template(self, content: str, file_path: str) -> str:
        """Convert file content to template with variables"""
        try:
            # Replace common patterns with template variables
            template_content = content
            
            # Replace project names
            template_content = template_content.replace('cloudmind', '{{ project_name }}')
            template_content = template_content.replace('CloudMind', '{{ project_title }}')
            
            # Replace URLs and endpoints
            template_content = template_content.replace('localhost:8000', '{{ api_host }}')
            template_content = template_content.replace('localhost:3000', '{{ frontend_host }}')
            
            # Replace database configurations
            template_content = template_content.replace('postgresql://', '{{ database_url }}')
            
            # Replace API keys (with placeholders)
            template_content = template_content.replace('your-api-key', '{{ api_key }}')
            
            return template_content
            
        except Exception as e:
            logger.error(f"Failed to convert to template: {e}")
            return content
    
    async def _extract_variables_from_content(self, content: str) -> List[str]:
        """Extract template variables from content"""
        try:
            import re
            variables = []
            
            # Find Jinja2 variables
            pattern = r'\{\{\s*(\w+)\s*\}\}'
            matches = re.findall(pattern, content)
            variables.extend(matches)
            
            return list(set(variables))
            
        except Exception as e:
            logger.error(f"Failed to extract variables: {e}")
            return []
    
    async def _generate_template_variables(self, files: List[Dict], analysis: Dict) -> Dict:
        """Generate template variables with defaults and validation"""
        try:
            variables = {
                'project_name': {
                    'type': 'string',
                    'default': 'my-project',
                    'description': 'Name of the project',
                    'required': True,
                    'validation': {
                        'pattern': r'^[a-z0-9-]+$',
                        'min_length': 3,
                        'max_length': 50
                    }
                },
                'project_title': {
                    'type': 'string',
                    'default': 'My Project',
                    'description': 'Display title of the project',
                    'required': True
                },
                'api_host': {
                    'type': 'string',
                    'default': 'localhost:8000',
                    'description': 'API server host and port',
                    'required': True
                },
                'frontend_host': {
                    'type': 'string',
                    'default': 'localhost:3000',
                    'description': 'Frontend server host and port',
                    'required': True
                },
                'database_url': {
                    'type': 'string',
                    'default': 'postgresql://user:password@localhost:5432/dbname',
                    'description': 'Database connection URL',
                    'required': True
                },
                'api_key': {
                    'type': 'string',
                    'default': '',
                    'description': 'API key for external services',
                    'required': False,
                    'sensitive': True
                }
            }
            
            # Add technology-specific variables
            if analysis.get('technology_stack'):
                for tech in analysis['technology_stack']:
                    if tech == 'react':
                        variables['react_version'] = {
                            'type': 'string',
                            'default': '18.2.0',
                            'description': 'React version',
                            'required': False
                        }
                    elif tech == 'python':
                        variables['python_version'] = {
                            'type': 'string',
                            'default': '3.11',
                            'description': 'Python version',
                            'required': False
                        }
            
            return variables
            
        except Exception as e:
            logger.error(f"Failed to generate template variables: {e}")
            return {}
    
    async def _save_template_files(self, template_id: UUID, template_files: Dict):
        """Save template files to storage"""
        try:
            template_path = self.template_root / str(template_id)
            template_path.mkdir(exist_ok=True)
            
            for file_path, file_info in template_files.items():
                # Create directory structure
                file_full_path = template_path / file_path
                file_full_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save file content
                with open(file_full_path, 'w', encoding='utf-8') as f:
                    f.write(file_info['content'])
            
            logger.info(f"Template files saved: {template_id}")
            
        except Exception as e:
            logger.error(f"Failed to save template files: {e}")
    
    async def _load_template_files(self, template_id: UUID) -> Dict:
        """Load template files from storage"""
        try:
            template_path = self.template_root / str(template_id)
            
            if not template_path.exists():
                return {}
            
            template_files = {}
            for file_path in template_path.rglob('*'):
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(template_path))
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    template_files[relative_path] = {
                        'content': content,
                        'size': len(content)
                    }
            
            return template_files
            
        except Exception as e:
            logger.error(f"Failed to load template files: {e}")
            return {}
    
    async def _validate_template_variables(self, template_variables: Dict, provided_variables: Dict) -> Dict:
        """Validate and merge template variables"""
        try:
            validated_variables = {}
            
            for var_name, var_config in template_variables.items():
                if var_name in provided_variables:
                    value = provided_variables[var_name]
                    
                    # Validate value
                    if not await self._validate_variable_value(value, var_config):
                        raise ValueError(f"Invalid value for variable {var_name}")
                    
                    validated_variables[var_name] = value
                else:
                    # Use default value
                    if var_config.get('required', False):
                        raise ValueError(f"Required variable {var_name} not provided")
                    validated_variables[var_name] = var_config.get('default', '')
            
            return validated_variables
            
        except Exception as e:
            logger.error(f"Failed to validate template variables: {e}")
            raise
    
    async def _validate_variable_value(self, value: Any, config: Dict) -> bool:
        """Validate a single variable value"""
        try:
            # Type validation
            expected_type = config.get('type', 'string')
            if expected_type == 'string' and not isinstance(value, str):
                return False
            
            # Pattern validation
            if 'validation' in config and 'pattern' in config['validation']:
                import re
                if not re.match(config['validation']['pattern'], str(value)):
                    return False
            
            # Length validation
            if 'validation' in config:
                validation = config['validation']
                if 'min_length' in validation and len(str(value)) < validation['min_length']:
                    return False
                if 'max_length' in validation and len(str(value)) > validation['max_length']:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate variable value: {e}")
            return False
    
    async def _apply_template_to_files(self, template_files: Dict, variables: Dict) -> List[Dict]:
        """Apply template variables to files"""
        try:
            applied_files = []
            
            for file_path, file_info in template_files.items():
                content = file_info['content']
                
                # Render template with variables
                try:
                    template = self.jinja_env.from_string(content)
                    rendered_content = template.render(**variables)
                except Exception as e:
                    logger.warning(f"Failed to render template for {file_path}: {e}")
                    rendered_content = content
                
                applied_files.append({
                    'path': file_path,
                    'content': rendered_content,
                    'size': len(rendered_content)
                })
            
            return applied_files
            
        except Exception as e:
            logger.error(f"Failed to apply template to files: {e}")
            raise
    
    async def _perform_template_validation(self, template: ProjectTemplate, template_files: Dict) -> Dict:
        """Perform comprehensive template validation"""
        try:
            validation_results = {
                'is_valid': True,
                'errors': [],
                'warnings': [],
                'checks': {}
            }
            
            # Check file structure
            if not template.file_structure:
                validation_results['errors'].append("No file structure defined")
                validation_results['is_valid'] = False
            
            # Check template files
            if not template_files:
                validation_results['errors'].append("No template files found")
                validation_results['is_valid'] = False
            
            # Validate variables
            if template.variables:
                for var_name, var_config in template.variables.items():
                    if not await self._validate_variable_config(var_config):
                        validation_results['errors'].append(f"Invalid variable configuration: {var_name}")
                        validation_results['is_valid'] = False
            
            # Check for required files
            required_files = ['README.md', 'package.json', 'requirements.txt']
            for required_file in required_files:
                if not any(required_file in file_path for file_path in template_files.keys()):
                    validation_results['warnings'].append(f"Missing recommended file: {required_file}")
            
            # Check template syntax
            for file_path, file_info in template_files.items():
                try:
                    self.jinja_env.from_string(file_info['content'])
                except Exception as e:
                    validation_results['errors'].append(f"Invalid template syntax in {file_path}: {str(e)}")
                    validation_results['is_valid'] = False
            
            validation_results['checks'] = {
                'total_files': len(template_files),
                'total_variables': len(template.variables or {}),
                'has_readme': any('README' in path for path in template_files.keys()),
                'has_config': any('config' in path.lower() for path in template_files.keys())
            }
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Failed to perform template validation: {e}")
            return {
                'is_valid': False,
                'errors': [f"Validation failed: {str(e)}"],
                'warnings': [],
                'checks': {}
            }
    
    async def _validate_variable_config(self, config: Dict) -> bool:
        """Validate variable configuration"""
        try:
            required_fields = ['type', 'description']
            for field in required_fields:
                if field not in config:
                    return False
            
            # Validate type
            valid_types = ['string', 'number', 'boolean', 'select']
            if config['type'] not in valid_types:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate variable config: {e}")
            return False
    
    async def _get_template_usage_stats(self, template_id: UUID) -> Dict:
        """Get template usage statistics"""
        try:
            db = next(get_db())
            
            # Get usage count
            usage_count = db.query(ProjectTemplate).filter(
                ProjectTemplate.id == template_id
            ).first().usage_count
            
            # Get recent usage (last 30 days)
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            recent_usage = db.query(ProjectTemplate).filter(
                and_(
                    ProjectTemplate.id == template_id,
                    ProjectTemplate.updated_at >= thirty_days_ago
                )
            ).count()
            
            return {
                'total_usage': usage_count,
                'recent_usage': recent_usage,
                'popularity_score': usage_count * 0.7 + recent_usage * 0.3
            }
            
        except Exception as e:
            logger.error(f"Failed to get template usage stats: {e}")
            return {}
    
    async def _create_template_zip(self, template: ProjectTemplate, template_files: Dict) -> bytes:
        """Create ZIP archive of template files"""
        try:
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_file:
                with zipfile.ZipFile(temp_file.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Add template metadata
                    metadata = {
                        'name': template.name,
                        'description': template.description,
                        'category': template.category,
                        'variables': template.variables,
                        'dependencies': template.dependencies,
                        'version': template.template_version
                    }
                    zip_file.writestr('template.json', json.dumps(metadata, indent=2))
                    
                    # Add template files
                    for file_path, file_info in template_files.items():
                        zip_file.writestr(file_path, file_info['content'])
                
                # Read the ZIP file
                with open(temp_file.name, 'rb') as f:
                    zip_content = f.read()
                
                # Clean up
                os.unlink(temp_file.name)
                
                return zip_content
                
        except Exception as e:
            logger.error(f"Failed to create template ZIP: {e}")
            raise
    
    def _increment_version(self, current_version: str) -> str:
        """Increment template version"""
        try:
            if not current_version:
                return "1.0.0"
            
            parts = current_version.split('.')
            if len(parts) == 3:
                major, minor, patch = parts
                patch = str(int(patch) + 1)
                return f"{major}.{minor}.{patch}"
            else:
                return "1.0.0"
                
        except Exception as e:
            logger.error(f"Failed to increment version: {e}")
            return "1.0.0"
