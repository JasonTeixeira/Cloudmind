"""
Advanced Extension Service
Professional extension system with installation, management, and lifecycle handling
"""

import asyncio
import logging
import os
import shutil
import zipfile
import json
import tempfile
import subprocess
import importlib
import importlib.util
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple, Union
from uuid import UUID, uuid4
from pathlib import Path
import hashlib
import requests
import yaml

from app.core.config import settings
from app.schemas.extension import (
    Extension, ExtensionManifest, ExtensionInstallation, ExtensionStatus,
    ExtensionType, ExtensionCategory, ExtensionPermission, ExtensionCompatibility,
    ExtensionRating
)

logger = logging.getLogger(__name__)


class ExtensionManager:
    """Manages extension lifecycle and operations"""
    
    def __init__(self):
        self.extensions: Dict[str, Extension] = {}
        self.installations: Dict[str, ExtensionInstallation] = {}
        self.manifests: Dict[str, ExtensionManifest] = {}
        self.extension_path = Path(settings.LOCAL_STORAGE_PATH) / "extensions"
        self.extension_path.mkdir(parents=True, exist_ok=True)
        
    async def install_extension(
        self, 
        extension_id: str, 
        user_id: UUID,
        version: Optional[str] = None,
        auto_enable: bool = True,
        grant_permissions: List[ExtensionPermission] = None
    ) -> ExtensionInstallation:
        """Install an extension"""
        try:
            # Check if extension exists
            if extension_id not in self.extensions:
                raise ValueError(f"Extension {extension_id} not found")
            
            extension = self.extensions[extension_id]
            
            # Check if already installed
            installation_id = f"{user_id}_{extension_id}"
            if installation_id in self.installations:
                raise ValueError(f"Extension {extension_id} already installed")
            
            # Create installation directory
            installation_path = self.extension_path / user_id / extension_id
            installation_path.mkdir(parents=True, exist_ok=True)
            
            # Download extension if needed
            if not (installation_path / "extension.json").exists():
                await self._download_extension(extension, installation_path, version)
            
            # Load manifest
            manifest = await self._load_manifest(installation_path)
            
            # Validate dependencies
            await self._validate_dependencies(manifest, user_id)
            
            # Create installation record
            installation = ExtensionInstallation(
                id=installation_id,
                extension_id=extension_id,
                user_id=user_id,
                status=ExtensionStatus.INSTALLING,
                installed_at=datetime.utcnow(),
                installation_path=str(installation_path),
                version=manifest.version,
                permissions_granted=grant_permissions or []
            )
            
            # Store installation
            self.installations[installation_id] = installation
            
            # Install dependencies
            await self._install_dependencies(manifest, user_id)
            
            # Initialize extension
            await self._initialize_extension(manifest, installation_path)
            
            # Update status
            installation.status = ExtensionStatus.INSTALLED
            if auto_enable:
                installation.status = ExtensionStatus.ENABLED
                installation.enabled_at = datetime.utcnow()
                installation.is_enabled = True
            
            # Store manifest
            self.manifests[extension_id] = manifest
            
            logger.info(f"Extension {extension_id} installed successfully for user {user_id}")
            return installation
            
        except Exception as e:
            logger.error(f"Failed to install extension {extension_id}: {e}")
            raise
    
    async def uninstall_extension(
        self, 
        extension_id: str, 
        user_id: UUID,
        remove_settings: bool = False,
        remove_data: bool = False
    ) -> bool:
        """Uninstall an extension"""
        try:
            installation_id = f"{user_id}_{extension_id}"
            
            if installation_id not in self.installations:
                raise ValueError(f"Extension {extension_id} not installed")
            
            installation = self.installations[installation_id]
            
            # Update status
            installation.status = ExtensionStatus.UNINSTALLING
            
            # Disable extension first
            await self.disable_extension(extension_id, user_id)
            
            # Remove extension files
            installation_path = Path(installation.installation_path)
            if installation_path.exists():
                shutil.rmtree(installation_path)
            
            # Remove settings if requested
            if remove_settings:
                await self._remove_extension_settings(extension_id, user_id)
            
            # Remove data if requested
            if remove_data:
                await self._remove_extension_data(extension_id, user_id)
            
            # Remove installation record
            del self.installations[installation_id]
            
            # Remove manifest
            if extension_id in self.manifests:
                del self.manifests[extension_id]
            
            logger.info(f"Extension {extension_id} uninstalled successfully for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to uninstall extension {extension_id}: {e}")
            return False
    
    async def enable_extension(
        self, 
        extension_id: str, 
        user_id: UUID,
        enable_dependencies: bool = True
    ) -> ExtensionInstallation:
        """Enable an extension"""
        try:
            installation_id = f"{user_id}_{extension_id}"
            
            if installation_id not in self.installations:
                raise ValueError(f"Extension {extension_id} not installed")
            
            installation = self.installations[installation_id]
            
            # Enable dependencies if requested
            if enable_dependencies and installation_id in self.manifests:
                manifest = self.manifests[installation_id]
                for dep_id in manifest.dependencies:
                    await self.enable_extension(dep_id, user_id, enable_dependencies=False)
            
            # Update installation
            installation.is_enabled = True
            installation.status = ExtensionStatus.ENABLED
            installation.enabled_at = datetime.utcnow()
            
            # Activate extension
            await self._activate_extension(extension_id, user_id)
            
            logger.info(f"Extension {extension_id} enabled for user {user_id}")
            return installation
            
        except Exception as e:
            logger.error(f"Failed to enable extension {extension_id}: {e}")
            raise
    
    async def disable_extension(
        self, 
        extension_id: str, 
        user_id: UUID,
        disable_dependents: bool = False
    ) -> ExtensionInstallation:
        """Disable an extension"""
        try:
            installation_id = f"{user_id}_{extension_id}"
            
            if installation_id not in self.installations:
                raise ValueError(f"Extension {extension_id} not installed")
            
            installation = self.installations[installation_id]
            
            # Disable dependents if requested
            if disable_dependents:
                dependents = await self._get_dependent_extensions(extension_id, user_id)
                for dep_id in dependents:
                    await self.disable_extension(dep_id, user_id, disable_dependents=False)
            
            # Deactivate extension
            await self._deactivate_extension(extension_id, user_id)
            
            # Update installation
            installation.is_enabled = False
            installation.status = ExtensionStatus.DISABLED
            installation.disabled_at = datetime.utcnow()
            
            logger.info(f"Extension {extension_id} disabled for user {user_id}")
            return installation
            
        except Exception as e:
            logger.error(f"Failed to disable extension {extension_id}: {e}")
            raise
    
    async def update_extension(
        self, 
        extension_id: str, 
        user_id: UUID,
        version: Optional[str] = None,
        backup_settings: bool = True
    ) -> ExtensionInstallation:
        """Update an extension"""
        try:
            installation_id = f"{user_id}_{extension_id}"
            
            if installation_id not in self.installations:
                raise ValueError(f"Extension {extension_id} not installed")
            
            installation = self.installations[installation_id]
            
            # Backup settings if requested
            if backup_settings:
                await self._backup_extension_settings(extension_id, user_id)
            
            # Update status
            installation.status = ExtensionStatus.UPDATING
            
            # Download new version
            installation_path = Path(installation.installation_path)
            await self._download_extension(
                self.extensions[extension_id], 
                installation_path, 
                version
            )
            
            # Load new manifest
            manifest = await self._load_manifest(installation_path)
            
            # Update installation
            installation.version = manifest.version
            installation.updated_at = datetime.utcnow()
            installation.status = ExtensionStatus.INSTALLED
            
            # Re-enable if it was enabled before
            if installation.is_enabled:
                installation.status = ExtensionStatus.ENABLED
            
            # Store new manifest
            self.manifests[extension_id] = manifest
            
            logger.info(f"Extension {extension_id} updated successfully for user {user_id}")
            return installation
            
        except Exception as e:
            logger.error(f"Failed to update extension {extension_id}: {e}")
            raise
    
    async def get_installed_extensions(self, user_id: UUID) -> List[ExtensionInstallation]:
        """Get installed extensions for a user"""
        try:
            user_installations = [
                installation for installation_id, installation in self.installations.items()
                if installation.user_id == user_id
            ]
            return user_installations
            
        except Exception as e:
            logger.error(f"Failed to get installed extensions for user {user_id}: {e}")
            return []
    
    async def get_extension_details(
        self, 
        extension_id: str, 
        user_id: UUID
    ) -> Optional[Dict[str, Any]]:
        """Get detailed extension information"""
        try:
            installation_id = f"{user_id}_{extension_id}"
            
            if installation_id not in self.installations:
                return None
            
            installation = self.installations[installation_id]
            extension = self.extensions.get(extension_id)
            manifest = self.manifests.get(extension_id)
            
            return {
                "extension": extension,
                "installation": installation,
                "manifest": manifest,
                "is_enabled": installation.is_enabled,
                "version": installation.version,
                "installed_at": installation.installed_at,
                "permissions": installation.permissions_granted
            }
            
        except Exception as e:
            logger.error(f"Failed to get extension details for {extension_id}: {e}")
            return None
    
    async def _download_extension(
        self, 
        extension: Extension, 
        installation_path: Path, 
        version: Optional[str] = None
    ):
        """Download extension files"""
        try:
            # This is a simplified implementation
            # In a real implementation, you would download from a marketplace or repository
            
            # Create extension.json file
            extension_data = {
                "id": extension.id,
                "name": extension.name,
                "display_name": extension.display_name,
                "description": extension.description,
                "version": version or extension.version,
                "author": extension.author,
                "publisher": extension.publisher,
                "type": extension.type,
                "category": extension.category,
                "main": "main.py",
                "activation_events": ["onStartupFinished"],
                "contributes": {},
                "permissions": extension.permissions,
                "dependencies": extension.dependencies,
                "conflicts": extension.conflicts
            }
            
            with open(installation_path / "extension.json", "w") as f:
                json.dump(extension_data, f, indent=2)
            
            # Create main.py file
            main_content = f'''
"""
{extension.display_name}
{extension.description}
"""

def activate(context):
    """Activate the extension"""
    print(f"Extension {extension.name} activated")

def deactivate():
    """Deactivate the extension"""
    print(f"Extension {extension.name} deactivated")
'''
            
            with open(installation_path / "main.py", "w") as f:
                f.write(main_content)
            
            # Create README.md
            readme_content = f'''
# {extension.display_name}

{extension.description}

## Installation

This extension is installed automatically by CloudMind.

## Usage

This extension provides {extension.type} functionality.

## Configuration

No configuration required.

## License

{extension.license or "MIT"}
'''
            
            with open(installation_path / "README.md", "w") as f:
                f.write(readme_content)
            
        except Exception as e:
            logger.error(f"Failed to download extension {extension.id}: {e}")
            raise
    
    async def _load_manifest(self, installation_path: Path) -> ExtensionManifest:
        """Load extension manifest"""
        try:
            manifest_path = installation_path / "extension.json"
            
            if not manifest_path.exists():
                raise ValueError("Extension manifest not found")
            
            with open(manifest_path, "r") as f:
                manifest_data = json.load(f)
            
            return ExtensionManifest(**manifest_data)
            
        except Exception as e:
            logger.error(f"Failed to load manifest from {installation_path}: {e}")
            raise
    
    async def _validate_dependencies(
        self, 
        manifest: ExtensionManifest, 
        user_id: UUID
    ):
        """Validate extension dependencies"""
        try:
            for dep_id in manifest.dependencies:
                dep_installation_id = f"{user_id}_{dep_id}"
                if dep_installation_id not in self.installations:
                    raise ValueError(f"Dependency {dep_id} not installed")
                
                dep_installation = self.installations[dep_installation_id]
                if not dep_installation.is_enabled:
                    raise ValueError(f"Dependency {dep_id} not enabled")
            
        except Exception as e:
            logger.error(f"Failed to validate dependencies: {e}")
            raise
    
    async def _install_dependencies(
        self, 
        manifest: ExtensionManifest, 
        user_id: UUID
    ):
        """Install extension dependencies"""
        try:
            for dep_id in manifest.dependencies:
                dep_installation_id = f"{user_id}_{dep_id}"
                if dep_installation_id not in self.installations:
                    # Install dependency
                    await self.install_extension(dep_id, user_id, auto_enable=True)
            
        except Exception as e:
            logger.error(f"Failed to install dependencies: {e}")
            raise
    
    async def _initialize_extension(
        self, 
        manifest: ExtensionManifest, 
        installation_path: Path
    ):
        """Initialize extension"""
        try:
            # Load extension module
            main_path = installation_path / manifest.main
            
            if main_path.exists():
                spec = importlib.util.spec_from_file_location(
                    f"extension_{manifest.id}", 
                    main_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Store module reference
                manifest.metadata["module"] = module
            
        except Exception as e:
            logger.error(f"Failed to initialize extension {manifest.id}: {e}")
            raise
    
    async def _activate_extension(self, extension_id: str, user_id: UUID):
        """Activate extension"""
        try:
            manifest = self.manifests.get(extension_id)
            if not manifest:
                return
            
            module = manifest.metadata.get("module")
            if module and hasattr(module, "activate"):
                # Create context for activation
                context = {
                    "extension_id": extension_id,
                    "user_id": user_id,
                    "subscriptions": []
                }
                
                module.activate(context)
                
                # Store context
                manifest.metadata["context"] = context
            
        except Exception as e:
            logger.error(f"Failed to activate extension {extension_id}: {e}")
            raise
    
    async def _deactivate_extension(self, extension_id: str, user_id: UUID):
        """Deactivate extension"""
        try:
            manifest = self.manifests.get(extension_id)
            if not manifest:
                return
            
            module = manifest.metadata.get("module")
            if module and hasattr(module, "deactivate"):
                module.deactivate()
            
            # Clear context
            if "context" in manifest.metadata:
                del manifest.metadata["context"]
            
        except Exception as e:
            logger.error(f"Failed to deactivate extension {extension_id}: {e}")
            raise
    
    async def _get_dependent_extensions(
        self, 
        extension_id: str, 
        user_id: UUID
    ) -> List[str]:
        """Get extensions that depend on this extension"""
        try:
            dependents = []
            
            for installation_id, installation in self.installations.items():
                if installation.user_id != user_id:
                    continue
                
                manifest = self.manifests.get(installation.extension_id)
                if manifest and extension_id in manifest.dependencies:
                    dependents.append(installation.extension_id)
            
            return dependents
            
        except Exception as e:
            logger.error(f"Failed to get dependent extensions: {e}")
            return []
    
    async def _backup_extension_settings(self, extension_id: str, user_id: UUID):
        """Backup extension settings"""
        try:
            # This would backup extension settings to a safe location
            backup_path = Path(settings.LOCAL_STORAGE_PATH) / "backups" / "extensions" / user_id / extension_id
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Copy settings file if it exists
            settings_path = Path(settings.LOCAL_STORAGE_PATH) / "extensions" / user_id / extension_id / "settings.json"
            if settings_path.exists():
                shutil.copy2(settings_path, backup_path / f"settings_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json")
            
        except Exception as e:
            logger.error(f"Failed to backup extension settings: {e}")
    
    async def _remove_extension_settings(self, extension_id: str, user_id: UUID):
        """Remove extension settings"""
        try:
            settings_path = Path(settings.LOCAL_STORAGE_PATH) / "extensions" / user_id / extension_id / "settings.json"
            if settings_path.exists():
                settings_path.unlink()
            
        except Exception as e:
            logger.error(f"Failed to remove extension settings: {e}")
    
    async def _remove_extension_data(self, extension_id: str, user_id: UUID):
        """Remove extension data"""
        try:
            data_path = Path(settings.LOCAL_STORAGE_PATH) / "extensions" / user_id / extension_id / "data"
            if data_path.exists():
                shutil.rmtree(data_path)
            
        except Exception as e:
            logger.error(f"Failed to remove extension data: {e}")


# Global instance
extension_manager = ExtensionManager()
