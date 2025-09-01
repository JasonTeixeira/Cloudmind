"""
Tokenized Pricing API endpoints for CloudMind consulting platform
"""

import logging
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User, UserRole
from app.models.pricing import ServiceCategory, EngagementStatus
from app.schemas.pricing import (
    ServiceToken, ServiceTokenCreate, ServiceTokenUpdate,
    ClientEngagement, ClientEngagementCreate, ClientEngagementUpdate,
    EngagementItem, ProgressEvent, ProgressEventCreate,
    PricingCalculationRequest, PricingCalculationResponse,
    EngagementDashboard, AdminPricingDashboard
)
from app.services.pricing import TokenizedPricingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pricing", tags=["pricing"])


def require_admin_or_master(current_user: User = Depends(get_current_user)) -> User:
    """Require admin or master user access"""
    if not (current_user.is_master or current_user.role in [UserRole.ADMIN, UserRole.MASTER]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin or master access required"
        )
    return current_user


def require_master(current_user: User = Depends(get_current_user)) -> User:
    """Require master user access"""
    if not current_user.is_master:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Master user access required"
        )
    return current_user


# Service Token Management (Admin/Master only)

@router.get("/service-tokens", response_model=List[ServiceToken])
async def get_service_tokens(
    category: Optional[ServiceCategory] = Query(None),
    is_active: bool = Query(True),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Get available service tokens"""
    pricing_service = TokenizedPricingService(db)
    tokens = await pricing_service.get_service_tokens(category=category, is_active=is_active)
    return tokens


@router.post("/service-tokens", response_model=ServiceToken, status_code=status.HTTP_201_CREATED)
async def create_service_token(
    token_data: ServiceTokenCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_master)
):
    """Create a new service token (Master only)"""
    pricing_service = TokenizedPricingService(db)
    token = await pricing_service.create_service_token(token_data.model_dump())
    return token


@router.put("/service-tokens/{token_id}", response_model=ServiceToken)
async def update_service_token(
    token_id: UUID,
    token_data: ServiceTokenUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_master)
):
    """Update a service token (Master only)"""
    # Implementation would go here
    raise HTTPException(status_code=501, detail="Not implemented yet")


# Pricing Calculations

@router.post("/calculate", response_model=PricingCalculationResponse)
async def calculate_pricing(
    request: PricingCalculationRequest,
    projected_savings: Optional[Decimal] = Query(None, description="Projected monthly savings for ROI calculation"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Calculate pricing for a set of service tokens"""
    pricing_service = TokenizedPricingService(db)
    
    try:
        pricing = await pricing_service.calculate_pricing(
            request=request,
            projected_savings=projected_savings
        )
        return pricing
    except Exception as e:
        logger.error(f"Pricing calculation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Pricing calculation failed: {str(e)}"
        )


# Client Engagement Management

@router.post("/engagements", response_model=ClientEngagement, status_code=status.HTTP_201_CREATED)
async def create_engagement(
    engagement_data: ClientEngagementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Create a new client engagement"""
    pricing_service = TokenizedPricingService(db)
    
    try:
        engagement = await pricing_service.create_engagement(engagement_data)
        return engagement
    except Exception as e:
        logger.error(f"Engagement creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Engagement creation failed: {str(e)}"
        )


@router.get("/engagements", response_model=List[ClientEngagement])
async def get_engagements(
    client_id: Optional[UUID] = Query(None),
    status: Optional[EngagementStatus] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get client engagements"""
    pricing_service = TokenizedPricingService(db)
    
    # If not admin/master, can only see own engagements
    if not (current_user.is_master or current_user.role in [UserRole.ADMIN, UserRole.MASTER]):
        client_id = current_user.id
    
    if client_id:
        engagements = await pricing_service.get_client_engagements(
            client_id=client_id,
            status=status
        )
    else:
        # Admin view - get all engagements (implementation needed)
        raise HTTPException(status_code=501, detail="Admin view not implemented yet")
    
    return engagements


@router.get("/engagements/{engagement_id}", response_model=ClientEngagement)
async def get_engagement(
    engagement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific engagement with details"""
    pricing_service = TokenizedPricingService(db)
    
    engagement = await pricing_service.get_engagement_with_items(engagement_id)
    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found"
        )
    
    # Check access permissions
    if not (current_user.is_master or 
            current_user.role in [UserRole.ADMIN, UserRole.MASTER] or
            engagement.client_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return engagement


@router.put("/engagements/{engagement_id}", response_model=ClientEngagement)
async def update_engagement(
    engagement_id: UUID,
    engagement_data: ClientEngagementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Update an engagement"""
    # Implementation would go here
    raise HTTPException(status_code=501, detail="Not implemented yet")


# Progress Tracking

@router.post("/engagements/{engagement_id}/progress", response_model=ProgressEvent, status_code=status.HTTP_201_CREATED)
async def create_progress_event(
    engagement_id: UUID,
    progress_data: ProgressEventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Create a progress event for an engagement"""
    pricing_service = TokenizedPricingService(db)
    
    try:
        progress_event = await pricing_service.update_engagement_progress(
            engagement_id=engagement_id,
            progress_percentage=int(progress_data.progress_percentage or 0),
            event_type=progress_data.event_type,
            event_description=progress_data.event_description,
            cost_incurred=progress_data.cost_incurred,
            savings_identified=progress_data.savings_identified,
            resources_processed=progress_data.resources_processed,
            event_data={"raw_data": progress_data.event_data} if progress_data.event_data else None
        )
        return progress_event
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Progress event creation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Progress event creation failed: {str(e)}"
        )


@router.get("/engagements/{engagement_id}/progress", response_model=List[ProgressEvent])
async def get_engagement_progress(
    engagement_id: UUID,
    limit: int = Query(50, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress events for an engagement"""
    # Implementation would go here
    raise HTTPException(status_code=501, detail="Not implemented yet")


# Dashboard Views

@router.get("/engagements/{engagement_id}/dashboard", response_model=EngagementDashboard)
async def get_engagement_dashboard(
    engagement_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard view for a client engagement"""
    pricing_service = TokenizedPricingService(db)
    
    engagement = await pricing_service.get_engagement_with_items(engagement_id)
    if not engagement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Engagement not found"
        )
    
    # Check access permissions
    if not (current_user.is_master or 
            current_user.role in [UserRole.ADMIN, UserRole.MASTER] or
            engagement.client_id == current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Build dashboard data
    dashboard = EngagementDashboard(
        engagement=engagement,
        recent_progress=engagement.progress_events[-10:] if engagement.progress_events else [],
        cost_breakdown={
            item.service_token.category.value: float(item.total_price)
            for item in engagement.items
            if item.service_token
        },
        savings_timeline=[],  # Would be populated with historical data
        next_milestones=[],   # Would be populated based on engagement status
        current_roi=engagement.roi_percentage,
        time_to_break_even=f"{engagement.payback_months:.1f} months" if engagement.payback_months else None,
        completion_eta=engagement.estimated_completion_date
    )
    
    return dashboard


@router.get("/admin/dashboard", response_model=AdminPricingDashboard)
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Get admin dashboard for pricing management"""
    pricing_service = TokenizedPricingService(db)
    
    try:
        dashboard_data = await pricing_service.get_admin_dashboard_data()
        
        dashboard = AdminPricingDashboard(
            active_engagements=dashboard_data['active_engagements'],
            monthly_revenue=dashboard_data['monthly_revenue'],
            ytd_revenue=dashboard_data['ytd_revenue'],
            average_engagement_value=dashboard_data['average_engagement_value'],
            total_savings_delivered=dashboard_data['total_savings_delivered'],
            popular_services=[],  # Would be populated with service usage stats
            revenue_by_category={},  # Would be populated with category breakdown
            monthly_trends=[]  # Would be populated with historical trends
        )
        
        return dashboard
    except Exception as e:
        logger.error(f"Admin dashboard failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load admin dashboard"
        )


# Real-time Progress Updates (WebSocket endpoint would be separate)

@router.post("/engagements/{engagement_id}/simulate-progress")
async def simulate_progress_update(
    engagement_id: UUID,
    progress_percentage: int = Query(..., ge=0, le=100),
    resources_processed: int = Query(0, ge=0),
    cost_incurred: Decimal = Query(Decimal('0'), ge=0),
    savings_identified: Decimal = Query(Decimal('0'), ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin_or_master)
):
    """Simulate a progress update (for testing/demo purposes)"""
    pricing_service = TokenizedPricingService(db)
    
    try:
        progress_event = await pricing_service.update_engagement_progress(
            engagement_id=engagement_id,
            progress_percentage=progress_percentage,
            event_type="simulation",
            event_description=f"Simulated progress update: {progress_percentage}% complete",
            cost_incurred=cost_incurred,
            savings_identified=savings_identified,
            resources_processed=resources_processed,
            event_data={"simulation": True}
        )
        
        return {
            "message": "Progress updated successfully",
            "progress_event_id": str(progress_event.id),
            "new_progress": progress_percentage,
            "total_cost": float(progress_event.engagement.total_cost),
            "total_savings": float(progress_event.engagement.projected_monthly_savings)
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Progress simulation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Progress simulation failed: {str(e)}"
        )
