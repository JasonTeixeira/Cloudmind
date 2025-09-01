"""
Advanced UI API Endpoints
Provides REST API for UI theme, layout, and settings management
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
import json
from datetime import datetime, timedelta

from app.core.auth import get_current_user
from app.models.user import User
from app.services.ui.ui_service import ui_service
from app.schemas.ui import (
    ApplyThemeRequest, ApplyThemeResponse, CreateThemeRequest, CreateThemeResponse,
    ApplyLayoutRequest, ApplyLayoutResponse, CreateLayoutRequest, CreateLayoutResponse,
    UpdateUISettingsRequest, UpdateUISettingsResponse, AddShortcutRequest, AddShortcutResponse,
    UIPreview, UIStatistics
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ui", tags=["Advanced UI"])


# Theme Management Endpoints
@router.get("/themes")
async def get_themes(
    current_user: User = Depends(get_current_user)
):
    """Get all available themes"""
    try:
        themes = await ui_service.get_themes()
        return {
            "themes": themes,
            "total_count": len(themes),
            "default_theme": next((t.id for t in themes if t.is_default), None)
        }
        
    except Exception as e:
        logger.error(f"Failed to get themes: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/themes/{theme_id}")
async def get_theme(
    theme_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific theme details"""
    try:
        themes = await ui_service.get_themes()
        theme = next((t for t in themes if t.id == theme_id), None)
        
        if not theme:
            raise HTTPException(status_code=404, detail="Theme not found")
        
        return theme
        
    except Exception as e:
        logger.error(f"Failed to get theme {theme_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/themes/apply", response_model=ApplyThemeResponse)
async def apply_theme(
    request: ApplyThemeRequest,
    current_user: User = Depends(get_current_user)
):
    """Apply theme to user"""
    try:
        theme = await ui_service.apply_theme(
            user_id=current_user.id,
            theme_id=request.theme_id,
            preview=request.preview
        )
        
        return ApplyThemeResponse(
            theme=theme,
            success=True,
            message=f"Theme {theme.display_name} applied successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to apply theme: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/themes/create", response_model=CreateThemeResponse)
async def create_theme(
    request: CreateThemeRequest,
    current_user: User = Depends(get_current_user)
):
    """Create custom theme"""
    try:
        theme_data = {
            "name": request.name,
            "display_name": request.display_name,
            "description": request.description,
            "type": request.type,
            "color_scheme": request.color_scheme,
            "colors": request.colors,
            "token_colors": request.token_colors,
            "semantic_token_colors": request.semantic_token_colors,
            "ui_colors": request.ui_colors
        }
        
        theme = await ui_service.create_theme(
            user_id=current_user.id,
            theme_data=theme_data
        )
        
        return CreateThemeResponse(
            theme=theme,
            success=True,
            message=f"Theme {theme.display_name} created successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to create theme: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Layout Management Endpoints
@router.get("/layouts")
async def get_layouts(
    current_user: User = Depends(get_current_user)
):
    """Get all available layouts"""
    try:
        layouts = await ui_service.get_layouts()
        return {
            "layouts": layouts,
            "total_count": len(layouts),
            "default_layout": next((l.id for l in layouts if l.is_default), None)
        }
        
    except Exception as e:
        logger.error(f"Failed to get layouts: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/layouts/{layout_id}")
async def get_layout(
    layout_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific layout details"""
    try:
        layouts = await ui_service.get_layouts()
        layout = next((l for l in layouts if l.id == layout_id), None)
        
        if not layout:
            raise HTTPException(status_code=404, detail="Layout not found")
        
        return layout
        
    except Exception as e:
        logger.error(f"Failed to get layout {layout_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/layouts/apply", response_model=ApplyLayoutResponse)
async def apply_layout(
    request: ApplyLayoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Apply layout to user"""
    try:
        layout = await ui_service.apply_layout(
            user_id=current_user.id,
            layout_id=request.layout_id,
            preview=request.preview
        )
        
        return ApplyLayoutResponse(
            layout=layout,
            success=True,
            message=f"Layout {layout.display_name} applied successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to apply layout: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/layouts/create", response_model=CreateLayoutResponse)
async def create_layout(
    request: CreateLayoutRequest,
    current_user: User = Depends(get_current_user)
):
    """Create custom layout"""
    try:
        layout_data = {
            "name": request.name,
            "display_name": request.display_name,
            "description": request.description,
            "type": request.type,
            "panels": request.panels,
            "views": request.views,
            "splits": request.splits
        }
        
        layout = await ui_service.create_layout(
            user_id=current_user.id,
            layout_data=layout_data
        )
        
        return CreateLayoutResponse(
            layout=layout,
            success=True,
            message=f"Layout {layout.display_name} created successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to create layout: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Settings Management Endpoints
@router.get("/settings")
async def get_ui_settings(
    current_user: User = Depends(get_current_user)
):
    """Get user UI settings"""
    try:
        settings = await ui_service.get_user_settings(current_user.id)
        return settings
        
    except Exception as e:
        logger.error(f"Failed to get UI settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/settings/update", response_model=UpdateUISettingsResponse)
async def update_ui_settings(
    request: UpdateUISettingsRequest,
    current_user: User = Depends(get_current_user)
):
    """Update user UI settings"""
    try:
        updates = {}
        
        if request.theme_id:
            updates["theme_id"] = request.theme_id
        
        if request.layout_id:
            updates["layout_id"] = request.layout_id
        
        if request.font_settings:
            updates["font_settings"] = request.font_settings.dict()
        
        if request.editor_settings:
            updates["editor_settings"] = request.editor_settings.dict()
        
        if request.animation_settings:
            updates["animation_settings"] = request.animation_settings.dict()
        
        if request.custom_css:
            updates["custom_css"] = request.custom_css
        
        if request.custom_js:
            updates["custom_js"] = request.custom_js
        
        settings = await ui_service.update_user_settings(
            user_id=current_user.id,
            updates=updates
        )
        
        return UpdateUISettingsResponse(
            settings=settings,
            success=True,
            message="UI settings updated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to update UI settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Shortcut Management Endpoints
@router.get("/shortcuts")
async def get_shortcuts(
    current_user: User = Depends(get_current_user)
):
    """Get user shortcuts"""
    try:
        shortcuts = await ui_service.get_shortcuts(current_user.id)
        return {
            "shortcuts": shortcuts,
            "total_count": len(shortcuts),
            "custom_count": len([s for s in shortcuts if s.is_custom])
        }
        
    except Exception as e:
        logger.error(f"Failed to get shortcuts: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/shortcuts/add", response_model=AddShortcutResponse)
async def add_shortcut(
    request: AddShortcutRequest,
    current_user: User = Depends(get_current_user)
):
    """Add custom shortcut"""
    try:
        shortcut_data = {
            "name": request.name,
            "description": request.description,
            "category": request.category,
            "key": request.key,
            "command": request.command,
            "context": request.context,
            "is_global": request.is_global
        }
        
        shortcut = await ui_service.add_shortcut(
            user_id=current_user.id,
            shortcut_data=shortcut_data
        )
        
        return AddShortcutResponse(
            shortcut=shortcut,
            success=True,
            message=f"Shortcut {shortcut.name} added successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to add shortcut: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/shortcuts/categories")
async def get_shortcut_categories(
    current_user: User = Depends(get_current_user)
):
    """Get shortcut categories"""
    try:
        from app.schemas.ui import ShortcutCategory
        
        categories = []
        for category in ShortcutCategory:
            shortcuts = await ui_service.get_shortcuts(current_user.id)
            category_shortcuts = [s for s in shortcuts if s.category == category]
            
            categories.append({
                "category": category.value,
                "name": category.value.replace("_", " ").title(),
                "shortcut_count": len(category_shortcuts)
            })
        
        return {
            "categories": categories,
            "total_count": len(categories)
        }
        
    except Exception as e:
        logger.error(f"Failed to get shortcut categories: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Preview Endpoints
@router.post("/preview/create")
async def create_ui_preview(
    preview_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Create UI preview"""
    try:
        preview_id = await ui_service.create_preview(
            user_id=current_user.id,
            preview_data=preview_data
        )
        
        return {
            "preview_id": preview_id,
            "preview_url": f"/ui/preview/{preview_id}",
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
            "success": True,
            "message": "UI preview created successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to create UI preview: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/preview/{preview_id}")
async def get_ui_preview(
    preview_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get UI preview"""
    try:
        preview_data = await ui_service.get_preview(preview_id)
        
        if not preview_data:
            raise HTTPException(status_code=404, detail="Preview not found or expired")
        
        return {
            "preview_id": preview_id,
            "data": preview_data,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Failed to get UI preview {preview_id}: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Statistics Endpoints
@router.get("/statistics")
async def get_ui_statistics(
    current_user: User = Depends(get_current_user)
):
    """Get UI statistics"""
    try:
        statistics = await ui_service.get_ui_statistics(current_user.id)
        return statistics
        
    except Exception as e:
        logger.error(f"Failed to get UI statistics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Theme Types and Categories
@router.get("/themes/types")
async def get_theme_types(
    current_user: User = Depends(get_current_user)
):
    """Get theme types"""
    try:
        from app.schemas.ui import ThemeType
        
        types = []
        for theme_type in ThemeType:
            themes = await ui_service.get_themes()
            type_themes = [t for t in themes if t.type == theme_type]
            
            types.append({
                "type": theme_type.value,
                "name": theme_type.value.replace("_", " ").title(),
                "theme_count": len(type_themes)
            })
        
        return {
            "types": types,
            "total_count": len(types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get theme types: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/themes/color-schemes")
async def get_color_schemes(
    current_user: User = Depends(get_current_user)
):
    """Get color schemes"""
    try:
        from app.schemas.ui import ColorScheme
        
        schemes = []
        for scheme in ColorScheme:
            themes = await ui_service.get_themes()
            scheme_themes = [t for t in themes if t.color_scheme == scheme]
            
            schemes.append({
                "scheme": scheme.value,
                "name": scheme.value.replace("_", " ").title(),
                "theme_count": len(scheme_themes)
            })
        
        return {
            "schemes": schemes,
            "total_count": len(schemes)
        }
        
    except Exception as e:
        logger.error(f"Failed to get color schemes: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Layout Types
@router.get("/layouts/types")
async def get_layout_types(
    current_user: User = Depends(get_current_user)
):
    """Get layout types"""
    try:
        from app.schemas.ui import LayoutType
        
        types = []
        for layout_type in LayoutType:
            layouts = await ui_service.get_layouts()
            type_layouts = [l for l in layouts if l.type == layout_type]
            
            types.append({
                "type": layout_type.value,
                "name": layout_type.value.replace("_", " ").title(),
                "layout_count": len(type_layouts)
            })
        
        return {
            "types": types,
            "total_count": len(types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get layout types: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Font Settings
@router.get("/fonts")
async def get_font_families(
    current_user: User = Depends(get_current_user)
):
    """Get available font families"""
    try:
        from app.schemas.ui import FontFamily
        
        families = []
        for font_family in FontFamily:
            families.append({
                "family": font_family.value,
                "name": font_family.value.replace("_", " "),
                "is_custom": font_family == FontFamily.CUSTOM
            })
        
        return {
            "families": families,
            "total_count": len(families)
        }
        
    except Exception as e:
        logger.error(f"Failed to get font families: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fonts/weights")
async def get_font_weights(
    current_user: User = Depends(get_current_user)
):
    """Get available font weights"""
    try:
        from app.schemas.ui import FontWeight
        
        weights = []
        for weight in FontWeight:
            weights.append({
                "weight": weight.value,
                "name": weight.value.replace("_", " ").title()
            })
        
        return {
            "weights": weights,
            "total_count": len(weights)
        }
        
    except Exception as e:
        logger.error(f"Failed to get font weights: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/fonts/styles")
async def get_font_styles(
    current_user: User = Depends(get_current_user)
):
    """Get available font styles"""
    try:
        from app.schemas.ui import FontStyle
        
        styles = []
        for style in FontStyle:
            styles.append({
                "style": style.value,
                "name": style.value.replace("_", " ").title()
            })
        
        return {
            "styles": styles,
            "total_count": len(styles)
        }
        
    except Exception as e:
        logger.error(f"Failed to get font styles: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Cursor Styles
@router.get("/cursor/styles")
async def get_cursor_styles(
    current_user: User = Depends(get_current_user)
):
    """Get available cursor styles"""
    try:
        from app.schemas.ui import CursorStyle
        
        styles = []
        for style in CursorStyle:
            styles.append({
                "style": style.value,
                "name": style.value.replace("_", " ").title()
            })
        
        return {
            "styles": styles,
            "total_count": len(styles)
        }
        
    except Exception as e:
        logger.error(f"Failed to get cursor styles: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Animation Types
@router.get("/animations/types")
async def get_animation_types(
    current_user: User = Depends(get_current_user)
):
    """Get available animation types"""
    try:
        from app.schemas.ui import AnimationType
        
        types = []
        for anim_type in AnimationType:
            types.append({
                "type": anim_type.value,
                "name": anim_type.value.replace("_", " ").title()
            })
        
        return {
            "types": types,
            "total_count": len(types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get animation types: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Panel Positions
@router.get("/panels/positions")
async def get_panel_positions(
    current_user: User = Depends(get_current_user)
):
    """Get available panel positions"""
    try:
        from app.schemas.ui import PanelPosition
        
        positions = []
        for position in PanelPosition:
            positions.append({
                "position": position.value,
                "name": position.value.replace("_", " ").title()
            })
        
        return {
            "positions": positions,
            "total_count": len(positions)
        }
        
    except Exception as e:
        logger.error(f"Failed to get panel positions: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# View Types
@router.get("/views/types")
async def get_view_types(
    current_user: User = Depends(get_current_user)
):
    """Get available view types"""
    try:
        from app.schemas.ui import ViewType
        
        types = []
        for view_type in ViewType:
            types.append({
                "type": view_type.value,
                "name": view_type.value.replace("_", " ").title()
            })
        
        return {
            "types": types,
            "total_count": len(types)
        }
        
    except Exception as e:
        logger.error(f"Failed to get view types: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Health and Status Endpoints
@router.get("/health")
async def ui_health():
    """Health check for UI system"""
    return {
        "status": "healthy",
        "service": "advanced_ui",
        "features": [
            "theme_management",
            "layout_management",
            "settings_management",
            "shortcut_management",
            "preview_system",
            "customization"
        ],
        "themes": len(ui_service.themes),
        "layouts": len(ui_service.layouts),
        "user_settings": len(ui_service.user_settings)
    }


# Export/Import Endpoints
@router.get("/export")
async def export_ui_settings(
    current_user: User = Depends(get_current_user)
):
    """Export user UI settings"""
    try:
        settings = await ui_service.get_user_settings(current_user.id)
        
        export_data = {
            "version": "1.0.0",
            "exported_at": datetime.utcnow().isoformat(),
            "user_id": str(current_user.id),
            "settings": settings.dict()
        }
        
        return {
            "export_data": export_data,
            "success": True,
            "message": "UI settings exported successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to export UI settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/import")
async def import_ui_settings(
    import_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Import user UI settings"""
    try:
        # Validate import data
        if "settings" not in import_data:
            raise HTTPException(status_code=400, detail="Invalid import data")
        
        settings_data = import_data["settings"]
        
        # Update settings with imported data
        updates = {}
        
        if "theme_id" in settings_data:
            updates["theme_id"] = settings_data["theme_id"]
        
        if "layout_id" in settings_data:
            updates["layout_id"] = settings_data["layout_id"]
        
        if "font_settings" in settings_data:
            updates["font_settings"] = settings_data["font_settings"]
        
        if "editor_settings" in settings_data:
            updates["editor_settings"] = settings_data["editor_settings"]
        
        if "animation_settings" in settings_data:
            updates["animation_settings"] = settings_data["animation_settings"]
        
        if "custom_css" in settings_data:
            updates["custom_css"] = settings_data["custom_css"]
        
        if "custom_js" in settings_data:
            updates["custom_js"] = settings_data["custom_js"]
        
        settings = await ui_service.update_user_settings(
            user_id=current_user.id,
            updates=updates
        )
        
        return {
            "settings": settings,
            "success": True,
            "message": "UI settings imported successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to import UI settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# Reset Endpoints
@router.post("/reset")
async def reset_ui_settings(
    current_user: User = Depends(get_current_user)
):
    """Reset user UI settings to defaults"""
    try:
        # Remove user settings to force recreation of defaults
        if str(current_user.id) in ui_service.user_settings:
            del ui_service.user_settings[str(current_user.id)]
        
        # Get fresh default settings
        settings = await ui_service.get_user_settings(current_user.id)
        
        return {
            "settings": settings,
            "success": True,
            "message": "UI settings reset to defaults successfully"
        }
        
    except Exception as e:
        logger.error(f"Failed to reset UI settings: {e}")
        raise HTTPException(status_code=400, detail=str(e))
