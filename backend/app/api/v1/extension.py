"""
Advanced Extension API Endpoints
Provides REST API for extension management and marketplace functionality
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
import json
from datetime import datetime

from app.core.auth import get_current_user
from app.models.user import User
from app.services.extension.extension_service import extension_manager
from app.services.extension.marketplace_service import marketplace_service
from app.schemas.extension import (
    InstallExtensionRequest, InstallExtensionResponse, UpdateExtensionRequest,
    UpdateExtensionResponse, UninstallExtensionRequest, UninstallExtensionResponse,
    EnableExtensionRequest, EnableExtensionResponse, DisableExtensionRequest,
    DisableExtensionResponse, SearchExtensionsRequest, SearchExtensionsResponse,
    ExtensionDetails, ExtensionMarketplaceInfo
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/extensions", tags=["Advanced Extensions"])


# Extension Management Endpoints
@router.post("/install", response_model=InstallExtensionResponse)
async def install_extension(
    request: InstallExtensionRequest,
    current_user: User = Depends(get_current_user)
):
    """Install an extension"""
    try:
        # First, add extension to marketplace if not exists
        if request.extension_id not in marketplace_service.extensions:
            # This would typically come from marketplace search
            # For now, we'll create a basic extension
            from app.schemas.extension import Extension, ExtensionType, ExtensionCategory, ExtensionCompatibility, ExtensionRating
            
            extension = Extension(
                id=request.extension_id,
                name=request.extension_id,
                display_name=request.extension_id.replace("-", " ").title(),
                description=f"Extension {request.extension_id}",
                version=request.version or "1.0.0",
                author="Unknown",
                publisher="unknown",
                type=ExtensionType.UTILITY,
                category=ExtensionCategory.OTHER,
                status="available",
                compatibility=ExtensionCompatibility.COMPATIBLE,
                rating=ExtensionRating.UNRATED
            )
            marketplace_service.extensions[request.extension_id] = extension
            extension_manager.extensions[request.extension_id] = extension
        
        installation = await extension_manager.install_extension(
            extension_id=request.extension_id,
            user_id=current_user.id,
            version=request.version,
            auto_enable=request.auto_enable,
            grant_permissions=request.grant_permissions
        )
        
        return InstallExtensionResponse(
            installation=installation,
            success=True,
            message=f"Extension {request.extension_id} installed successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to install extension {request.extension_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/uninstall", response_model=UninstallExtensionResponse)
async def uninstall_extension(
    request: UninstallExtensionRequest,
    current_user: User = Depends(get_current_user)
):
    """Uninstall an extension"""
    try:
        success = await extension_manager.uninstall_extension(
            extension_id=request.extension_id,
            user_id=current_user.id,
            remove_settings=request.remove_settings,
            remove_data=request.remove_data
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to uninstall extension")
        
        return UninstallExtensionResponse(
            success=True,
            message=f"Extension {request.extension_id} uninstalled successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to uninstall extension {request.extension_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/enable", response_model=EnableExtensionResponse)
async def enable_extension(
    request: EnableExtensionRequest,
    current_user: User = Depends(get_current_user)
):
    """Enable an extension"""
    try:
        installation = await extension_manager.enable_extension(
            extension_id=request.extension_id,
            user_id=current_user.id,
            enable_dependencies=request.enable_dependencies
        )
        
        return EnableExtensionResponse(
            installation=installation,
            success=True,
            message=f"Extension {request.extension_id} enabled successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to enable extension {request.extension_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/disable", response_model=DisableExtensionResponse)
async def disable_extension(
    request: DisableExtensionRequest,
    current_user: User = Depends(get_current_user)
):
    """Disable an extension"""
    try:
        installation = await extension_manager.disable_extension(
            extension_id=request.extension_id,
            user_id=current_user.id,
            disable_dependents=request.disable_dependents
        )
        
        return DisableExtensionResponse(
            installation=installation,
            success=True,
            message=f"Extension {request.extension_id} disabled successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to disable extension {request.extension_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/update", response_model=UpdateExtensionResponse)
async def update_extension(
    request: UpdateExtensionRequest,
    current_user: User = Depends(get_current_user)
):
    """Update an extension"""
    try:
        installation = await extension_manager.update_extension(
            extension_id=request.extension_id,
            user_id=current_user.id,
            version=request.version,
            backup_settings=request.backup_settings
        )
        
        return UpdateExtensionResponse(
            installation=installation,
            success=True,
            message=f"Extension {request.extension_id} updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to update extension {request.extension_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/installed")
async def get_installed_extensions(
    current_user: User = Depends(get_current_user)
):
    """Get installed extensions for current user"""
    try:
        installations = await extension_manager.get_installed_extensions(current_user.id)
        return {
            "installations": installations,
            "total_count": len(installations),
            "enabled_count": len([i for i in installations if i.is_enabled])
        }
        
    except Exception as e:
        logger.error(f"Failed to get installed extensions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/details/{extension_id}")
async def get_extension_details(
    extension_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get extension details"""
    try:
        details = await extension_manager.get_extension_details(extension_id, current_user.id)
        
        if not details:
            raise HTTPException(status_code=404, detail="Extension not found")
        
        return details
        
    except Exception as e:
        logger.error(f"Failed to get extension details: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Marketplace Endpoints
@router.post("/search", response_model=SearchExtensionsResponse)
async def search_extensions(
    request: SearchExtensionsRequest,
    current_user: User = Depends(get_current_user)
):
    """Search extensions in marketplace"""
    try:
        response = await marketplace_service.search_extensions(request)
        return response
        
    except Exception as e:
        logger.error(f"Failed to search extensions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/marketplace/{extension_id}")
async def get_marketplace_extension(
    extension_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get extension from marketplace"""
    try:
        extension = await marketplace_service.get_extension_details(extension_id)
        
        if not extension:
            raise HTTPException(status_code=404, detail="Extension not found")
        
        # Get installation status
        installation = None
        installation_id = f"{current_user.id}_{extension_id}"
        if installation_id in extension_manager.installations:
            installation = extension_manager.installations[installation_id]
        
        # Get reviews
        reviews = await marketplace_service.get_extension_reviews(extension_id)
        
        # Get updates if installed
        updates = []
        if installation:
            updates = await marketplace_service.get_extension_updates(
                extension_id, 
                installation.version
            )
        
        return ExtensionDetails(
            extension=extension,
            installation=installation,
            reviews=reviews,
            updates=updates,
            statistics={
                "download_count": extension.download_count,
                "review_count": extension.review_count,
                "average_rating": extension.average_rating
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get marketplace extension: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/featured")
async def get_featured_extensions(
    limit: int = Query(10, description="Number of featured extensions to return"),
    current_user: User = Depends(get_current_user)
):
    """Get featured extensions"""
    try:
        extensions = await marketplace_service.get_featured_extensions(limit)
        return {
            "extensions": extensions,
            "total_count": len(extensions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get featured extensions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/popular")
async def get_popular_extensions(
    limit: int = Query(10, description="Number of popular extensions to return"),
    current_user: User = Depends(get_current_user)
):
    """Get popular extensions"""
    try:
        extensions = await marketplace_service.get_popular_extensions(limit)
        return {
            "extensions": extensions,
            "total_count": len(extensions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get popular extensions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/category/{category}")
async def get_extensions_by_category(
    category: str,
    limit: int = Query(20, description="Number of extensions to return"),
    current_user: User = Depends(get_current_user)
):
    """Get extensions by category"""
    try:
        from app.schemas.extension import ExtensionCategory
        
        try:
            category_enum = ExtensionCategory(category)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
        
        extensions = await marketplace_service.get_extensions_by_category(category_enum, limit)
        return {
            "category": category,
            "extensions": extensions,
            "total_count": len(extensions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extensions by category: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/type/{extension_type}")
async def get_extensions_by_type(
    extension_type: str,
    limit: int = Query(20, description="Number of extensions to return"),
    current_user: User = Depends(get_current_user)
):
    """Get extensions by type"""
    try:
        from app.schemas.extension import ExtensionType
        
        try:
            type_enum = ExtensionType(extension_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid extension type: {extension_type}")
        
        extensions = await marketplace_service.get_extensions_by_type(type_enum, limit)
        return {
            "type": extension_type,
            "extensions": extensions,
            "total_count": len(extensions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extensions by type: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Review Endpoints
@router.get("/reviews/{extension_id}")
async def get_extension_reviews(
    extension_id: str,
    limit: int = Query(20, description="Number of reviews to return"),
    current_user: User = Depends(get_current_user)
):
    """Get extension reviews"""
    try:
        reviews = await marketplace_service.get_extension_reviews(extension_id, limit)
        return {
            "extension_id": extension_id,
            "reviews": reviews,
            "total_count": len(reviews)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extension reviews: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{extension_id}")
async def add_extension_review(
    extension_id: str,
    rating: int = Query(..., ge=1, le=5, description="Rating (1-5)"),
    title: str = Query(..., description="Review title"),
    content: str = Query(..., description="Review content"),
    current_user: User = Depends(get_current_user)
):
    """Add extension review"""
    try:
        review = await marketplace_service.add_extension_review(
            extension_id=extension_id,
            user_id=current_user.id,
            rating=rating,
            title=title,
            content=content
        )
        
        return {
            "review": review,
            "success": True,
            "message": "Review added successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to add extension review: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Update Endpoints
@router.get("/updates/{extension_id}")
async def get_extension_updates(
    extension_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get available updates for extension"""
    try:
        # Get current version
        installation_id = f"{current_user.id}_{extension_id}"
        current_version = "1.0.0"  # Default version
        
        if installation_id in extension_manager.installations:
            installation = extension_manager.installations[installation_id]
            current_version = installation.version
        
        updates = await marketplace_service.get_extension_updates(extension_id, current_version)
        return {
            "extension_id": extension_id,
            "current_version": current_version,
            "updates": updates,
            "total_count": len(updates)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extension updates: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Marketplace Management Endpoints
@router.get("/marketplace/info")
async def get_marketplace_info(
    current_user: User = Depends(get_current_user)
):
    """Get marketplace information"""
    try:
        # Get default marketplace
        marketplace = marketplace_service.marketplaces.get("cloudmind-official")
        if not marketplace:
            raise HTTPException(status_code=404, detail="Marketplace not found")
        
        # Get featured extensions
        featured_extensions = await marketplace_service.get_featured_extensions(5)
        
        # Get categories
        from app.schemas.extension import ExtensionCategory
        categories = list(ExtensionCategory)
        
        # Get statistics
        statistics = await marketplace_service.get_marketplace_statistics()
        
        return ExtensionMarketplaceInfo(
            marketplace=marketplace,
            extensions=featured_extensions,
            categories=categories,
            statistics=statistics
        )
        
    except Exception as e:
        logger.error(f"Failed to get marketplace info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/marketplace/sync/{marketplace_id}")
async def sync_marketplace(
    marketplace_id: str,
    current_user: User = Depends(get_current_user)
):
    """Sync marketplace with external source"""
    try:
        success = await marketplace_service.sync_marketplace(marketplace_id)
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to sync marketplace")
        
        return {
            "success": True,
            "message": f"Marketplace {marketplace_id} synced successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to sync marketplace: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/marketplace/statistics")
async def get_marketplace_statistics(
    current_user: User = Depends(get_current_user)
):
    """Get marketplace statistics"""
    try:
        statistics = await marketplace_service.get_marketplace_statistics()
        return statistics
        
    except Exception as e:
        logger.error(f"Failed to get marketplace statistics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Extension Development Endpoints
@router.post("/develop/upload")
async def upload_extension_for_development(
    file: UploadFile = File(..., description="Extension package file"),
    current_user: User = Depends(get_current_user)
):
    """Upload extension for development"""
    try:
        # This would handle extension package upload for development
        # For now, we'll just return a success message
        
        return {
            "success": True,
            "message": f"Extension package {file.filename} uploaded successfully",
            "file_size": file.size,
            "content_type": file.content_type
        }
        
    except Exception as e:
        logger.error(f"Failed to upload extension: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/develop/{extension_id}")
async def get_development_info(
    extension_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get extension development information"""
    try:
        from app.schemas.extension import ExtensionDevelopmentInfo
        
        # This would return development configuration
        development_info = ExtensionDevelopmentInfo(
            extension_id=extension_id,
            development_mode=True,
            hot_reload=True,
            debug_mode=False,
            log_level="info",
            development_path=f"/extensions/dev/{extension_id}",
            build_output=f"/extensions/build/{extension_id}",
            watch_patterns=["**/*.py", "**/*.js", "**/*.json"],
            build_scripts={
                "build": "npm run build",
                "test": "npm run test",
                "lint": "npm run lint"
            },
            test_scripts={
                "unit": "npm run test:unit",
                "integration": "npm run test:integration"
            }
        )
        
        return development_info
        
    except Exception as e:
        logger.error(f"Failed to get development info: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Health and Status Endpoints
@router.get("/health")
async def extension_health():
    """Health check for extension system"""
    return {
        "status": "healthy",
        "service": "advanced_extensions",
        "features": [
            "extension_management",
            "marketplace",
            "installation",
            "updates",
            "reviews",
            "development_tools"
        ],
        "installed_extensions": len(extension_manager.installations),
        "available_extensions": len(marketplace_service.extensions),
        "marketplaces": len(marketplace_service.marketplaces)
    }


@router.get("/categories")
async def get_extension_categories(
    current_user: User = Depends(get_current_user)
):
    """Get all extension categories"""
    try:
        from app.schemas.extension import ExtensionCategory
        
        categories = []
        for category in ExtensionCategory:
            # Get count for each category
            category_extensions = await marketplace_service.get_extensions_by_category(category)
            
            categories.append({
                "category": category.value,
                "name": category.value.replace("_", " ").title(),
                "extension_count": len(category_extensions)
            })
        
        return {
            "categories": categories,
            "total_count": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extension categories: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/types")
async def get_extension_types(
    current_user: User = Depends(get_current_user)
):
    """Get all extension types"""
    try:
        from app.schemas.extension import ExtensionType
        
        types = []
        for ext_type in ExtensionType:
            # Get count for each type
            type_extensions = await marketplace_service.get_extensions_by_type(ext_type)
            
            types.append({
                "type": ext_type.value,
                "name": ext_type.value.replace("_", " ").title(),
                "extension_count": len(type_extensions)
            })
        
        return {
            "types": types,
            "total_count": len(types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get extension types: {e}")
        raise HTTPException(status_code=400, detail=str(e))
