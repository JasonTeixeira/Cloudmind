"""
AI Connection Test API Endpoints
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.services.ai_engine.ai_providers import AIProvidersService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/test/openai")
async def test_openai_connection(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test OpenAI API connection"""
    try:
        ai_service = AIProvidersService()
        result = await ai_service.test_openai_connection()
        
        return {
            "success": result["status"] == "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error testing OpenAI connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OpenAI connection test failed: {str(e)}"
        )


@router.get("/test/anthropic")
async def test_anthropic_connection(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test Anthropic API connection"""
    try:
        ai_service = AIProvidersService()
        result = await ai_service.test_anthropic_connection()
        
        return {
            "success": result["status"] == "success",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Error testing Anthropic connection: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Anthropic connection test failed: {str(e)}"
        )


@router.get("/test/all")
async def test_all_ai_connections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Test all AI provider connections"""
    try:
        ai_service = AIProvidersService()
        
        # Test both providers
        openai_result = await ai_service.test_openai_connection()
        anthropic_result = await ai_service.test_anthropic_connection()
        
        # Get provider status
        status = await ai_service.get_provider_status()
        
        return {
            "success": all([
                openai_result["status"] == "success" if openai_result["status"] != "error" else False,
                anthropic_result["status"] == "success" if anthropic_result["status"] != "error" else False
            ]),
            "data": {
                "openai": openai_result,
                "anthropic": anthropic_result,
                "status": status
            }
        }
        
    except Exception as e:
        logger.error(f"Error testing AI connections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI connection test failed: {str(e)}"
        )


@router.get("/status")
async def get_ai_provider_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get status of all AI providers"""
    try:
        ai_service = AIProvidersService()
        status = await ai_service.get_provider_status()
        
        return {
            "success": True,
            "data": status
        }
        
    except Exception as e:
        logger.error(f"Error getting AI provider status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get AI provider status: {str(e)}"
        ) 