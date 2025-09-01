"""
Tokenized Pricing Service for CloudMind Consulting Platform
"""

import json
import logging
from decimal import Decimal
from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.pricing import (
    ServiceToken, ClientEngagement, EngagementItem, ProgressEvent,
    Invoice, PricingRule, UnitType, ServiceCategory, EngagementStatus
)
from app.schemas.pricing import (
    PricingCalculationRequest, PricingCalculationResponse,
    ClientEngagementCreate, EngagementItemCreate
)

logger = logging.getLogger(__name__)


class TokenizedPricingService:
    """Service for managing tokenized pricing and calculations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_service_tokens(
        self, 
        category: Optional[ServiceCategory] = None,
        is_active: bool = True
    ) -> List[ServiceToken]:
        """Get available service tokens"""
        query = select(ServiceToken).where(ServiceToken.is_active == is_active)
        
        if category:
            query = query.where(ServiceToken.category == category)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def create_service_token(self, token_data: Dict[str, Any]) -> ServiceToken:
        """Create a new service token"""
        token = ServiceToken(**token_data)
        self.db.add(token)
        await self.db.commit()
        await self.db.refresh(token)
        return token
    
    async def calculate_pricing(
        self, 
        request: PricingCalculationRequest,
        projected_savings: Optional[Decimal] = None
    ) -> PricingCalculationResponse:
        """Calculate pricing for a set of service tokens"""
        
        # Get service tokens
        token_ids = [UUID(item['service_token_id']) for item in request.service_tokens]
        query = select(ServiceToken).where(ServiceToken.id.in_(token_ids))
        result = await self.db.execute(query)
        tokens = {str(token.id): token for token in result.scalars().all()}
        
        total_cost = Decimal('0')
        subtotal = Decimal('0')
        total_discount = Decimal('0')
        items = []
        breakdown_by_category = {}
        applied_rules = []
        estimated_duration = Decimal('0')
        
        # Calculate base pricing for each item
        for item_request in request.service_tokens:
            token_id = item_request['service_token_id']
            quantity = item_request['quantity']
            
            if token_id not in tokens:
                continue
                
            token = tokens[token_id]
            
            # Calculate base price
            if token.unit_type == UnitType.PERCENTAGE_SAVINGS and projected_savings:
                # For percentage-based pricing, use projected savings
                unit_price = projected_savings * token.base_price / 100
                total_price = unit_price * quantity
            else:
                unit_price = token.base_price
                total_price = unit_price * quantity
            
            # Apply volume discounts if applicable
            discount = Decimal('0')
            if (request.apply_volume_discounts and 
                token.volume_discount_threshold and 
                quantity >= token.volume_discount_threshold and
                token.volume_discount_rate):
                
                discount = total_price * token.volume_discount_rate
                applied_rules.append(f"Volume discount ({token.volume_discount_rate * 100}%) on {token.name}")
            
            discounted_price = total_price - discount
            
            # Add to category breakdown
            category_name = token.category.value
            if category_name not in breakdown_by_category:
                breakdown_by_category[category_name] = Decimal('0')
            breakdown_by_category[category_name] += discounted_price
            
            # Add estimated duration
            if token.estimated_duration_hours:
                estimated_duration += token.estimated_duration_hours * quantity
            
            items.append({
                'service_token_id': token_id,
                'service_name': token.name,
                'quantity': quantity,
                'unit_price': float(unit_price),
                'total_price': float(total_price),
                'discount': float(discount),
                'final_price': float(discounted_price),
                'category': token.category.value,
                'unit_type': token.unit_type.value
            })
            
            subtotal += total_price
            total_discount += discount
            total_cost += discounted_price
        
        # Apply pricing rules if requested
        if request.apply_pricing_rules and request.client_id:
            rule_discount, rule_names = await self._apply_pricing_rules(
                request.client_id, total_cost, breakdown_by_category
            )
            total_discount += rule_discount
            total_cost -= rule_discount
            applied_rules.extend(rule_names)
        
        # Calculate discount percentage
        discount_percentage = (total_discount / subtotal * 100) if subtotal > 0 else Decimal('0')
        
        # Calculate ROI if projected savings provided
        roi_percentage = None
        payback_months = None
        if projected_savings and projected_savings > 0:
            annual_savings = projected_savings * 12
            roi_percentage = (annual_savings - total_cost) / total_cost * 100
            payback_months = total_cost / projected_savings if projected_savings > 0 else None
        
        return PricingCalculationResponse(
            total_cost=total_cost,
            subtotal=subtotal,
            total_discount=total_discount,
            discount_percentage=discount_percentage,
            estimated_duration_hours=estimated_duration if estimated_duration > 0 else None,
            breakdown_by_category=breakdown_by_category,
            items=items,
            applied_rules=applied_rules,
            projected_monthly_savings=projected_savings,
            roi_percentage=roi_percentage,
            payback_months=payback_months
        )
    
    async def _apply_pricing_rules(
        self, 
        client_id: UUID, 
        total_cost: Decimal,
        breakdown_by_category: Dict[str, Decimal]
    ) -> Tuple[Decimal, List[str]]:
        """Apply dynamic pricing rules"""
        
        # Get active pricing rules
        query = select(PricingRule).where(
            PricingRule.is_active == True
        ).order_by(PricingRule.priority.desc())
        
        result = await self.db.execute(query)
        rules = result.scalars().all()
        
        total_discount = Decimal('0')
        applied_rule_names = []
        
        for rule in rules:
            # Check if rule applies
            if await self._evaluate_pricing_rule_condition(
                rule, client_id, total_cost, breakdown_by_category
            ):
                # Apply the rule
                if rule.modifier_type == 'discount':
                    discount = total_cost * (1 - rule.modifier_value)
                    total_discount += discount
                    applied_rule_names.append(f"{rule.name} ({(1-rule.modifier_value)*100}% discount)")
                elif rule.modifier_type == 'premium':
                    # Premium increases cost, so negative discount
                    premium = total_cost * (rule.modifier_value - 1)
                    total_discount -= premium
                    applied_rule_names.append(f"{rule.name} ({(rule.modifier_value-1)*100}% premium)")
                elif rule.modifier_type == 'flat_fee':
                    total_discount -= rule.modifier_value
                    applied_rule_names.append(f"{rule.name} (${rule.modifier_value} fee)")
        
        return total_discount, applied_rule_names
    
    async def _evaluate_pricing_rule_condition(
        self,
        rule: PricingRule,
        client_id: UUID,
        total_cost: Decimal,
        breakdown_by_category: Dict[str, Decimal]
    ) -> bool:
        """Evaluate if a pricing rule condition is met"""
        
        try:
            # Simple condition evaluation
            # In a production system, you'd want a more sophisticated rule engine
            condition = rule.condition_expression
            
            # Replace variables in condition
            condition = condition.replace('total_cost', str(float(total_cost)))
            
            # Get client engagement history for more complex rules
            engagement_count_query = select(func.count(ClientEngagement.id)).where(
                ClientEngagement.client_id == client_id
            )
            result = await self.db.execute(engagement_count_query)
            engagement_count = result.scalar() or 0
            
            condition = condition.replace('engagement_count', str(engagement_count))
            
            # Evaluate the condition (be careful with eval in production!)
            # This is a simplified implementation
            return eval(condition)
            
        except Exception as e:
            logger.warning(f"Failed to evaluate pricing rule condition: {e}")
            return False
    
    async def create_engagement(
        self, 
        engagement_data: ClientEngagementCreate
    ) -> ClientEngagement:
        """Create a new client engagement with pricing calculation"""
        
        # Calculate pricing for the engagement
        pricing_request = PricingCalculationRequest(
            service_tokens=[
                {
                    'service_token_id': str(item.service_token_id),
                    'quantity': item.quantity
                }
                for item in engagement_data.items
            ],
            client_id=engagement_data.client_id
        )
        
        pricing = await self.calculate_pricing(pricing_request)
        
        # Create engagement
        engagement = ClientEngagement(
            client_id=engagement_data.client_id,
            title=engagement_data.title,
            description=engagement_data.description,
            estimated_cost=engagement_data.estimated_cost or pricing.total_cost,
            total_cost=pricing.total_cost,
            approved_budget=engagement_data.approved_budget,
            start_date=engagement_data.start_date,
            estimated_completion_date=engagement_data.estimated_completion_date,
            status=EngagementStatus.DRAFT
        )
        
        self.db.add(engagement)
        await self.db.flush()  # Get the engagement ID
        
        # Create engagement items
        for item_data in engagement_data.items:
            # Find the corresponding pricing item
            pricing_item = next(
                (item for item in pricing.items 
                 if item['service_token_id'] == str(item_data.service_token_id)),
                None
            )
            
            if pricing_item:
                engagement_item = EngagementItem(
                    engagement_id=engagement.id,
                    service_token_id=item_data.service_token_id,
                    quantity=item_data.quantity,
                    unit_price=Decimal(str(pricing_item['unit_price'])),
                    total_price=Decimal(str(pricing_item['final_price'])),
                    discount_applied=Decimal(str(pricing_item['discount'])) / Decimal(str(pricing_item['total_price'])) if pricing_item['total_price'] > 0 else Decimal('0'),
                    notes=item_data.notes,
                    estimated_hours=item_data.estimated_hours
                )
                self.db.add(engagement_item)
        
        await self.db.commit()
        await self.db.refresh(engagement)
        
        return engagement
    
    async def get_engagement_with_items(self, engagement_id: UUID) -> Optional[ClientEngagement]:
        """Get engagement with all related items"""
        query = select(ClientEngagement).options(
            selectinload(ClientEngagement.items).selectinload(EngagementItem.service_token),
            selectinload(ClientEngagement.progress_events)
        ).where(ClientEngagement.id == engagement_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_engagement_progress(
        self,
        engagement_id: UUID,
        progress_percentage: int,
        event_type: str,
        event_description: str,
        cost_incurred: Decimal = Decimal('0'),
        savings_identified: Decimal = Decimal('0'),
        resources_processed: Optional[int] = None,
        event_data: Optional[Dict[str, Any]] = None
    ) -> ProgressEvent:
        """Update engagement progress and create progress event"""
        
        # Update engagement progress
        engagement_query = select(ClientEngagement).where(
            ClientEngagement.id == engagement_id
        )
        result = await self.db.execute(engagement_query)
        engagement = result.scalar_one_or_none()
        
        if not engagement:
            raise ValueError(f"Engagement {engagement_id} not found")
        
        # Update engagement fields
        engagement.progress_percentage = progress_percentage
        engagement.total_cost += cost_incurred
        engagement.projected_monthly_savings += savings_identified
        
        if resources_processed is not None:
            engagement.resources_analyzed = resources_processed
        
        # Calculate ROI
        if engagement.projected_monthly_savings > 0 and engagement.total_cost > 0:
            annual_savings = engagement.projected_monthly_savings * 12
            engagement.roi_percentage = (annual_savings - engagement.total_cost) / engagement.total_cost * 100
            engagement.payback_months = engagement.total_cost / engagement.projected_monthly_savings
        
        # Create progress event
        progress_event = ProgressEvent(
            engagement_id=engagement_id,
            event_type=event_type,
            event_description=event_description,
            progress_percentage=Decimal(str(progress_percentage)),
            resources_processed=resources_processed,
            cost_incurred=cost_incurred,
            savings_identified=savings_identified,
            event_data=json.dumps(event_data) if event_data else None,
            visible_to_client=True
        )
        
        self.db.add(progress_event)
        await self.db.commit()
        await self.db.refresh(progress_event)
        
        return progress_event
    
    async def get_client_engagements(
        self, 
        client_id: UUID,
        status: Optional[EngagementStatus] = None
    ) -> List[ClientEngagement]:
        """Get all engagements for a client"""
        query = select(ClientEngagement).where(
            ClientEngagement.client_id == client_id
        ).options(
            selectinload(ClientEngagement.items).selectinload(EngagementItem.service_token)
        )
        
        if status:
            query = query.where(ClientEngagement.status == status)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_admin_dashboard_data(self) -> Dict[str, Any]:
        """Get admin dashboard data for pricing management"""
        
        # Active engagements
        active_engagements_query = select(ClientEngagement).where(
            ClientEngagement.status.in_([
                EngagementStatus.IN_PROGRESS,
                EngagementStatus.APPROVED
            ])
        ).options(selectinload(ClientEngagement.items))
        
        result = await self.db.execute(active_engagements_query)
        active_engagements = result.scalars().all()
        
        # Monthly revenue (current month)
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue_query = select(func.sum(ClientEngagement.total_cost)).where(
            and_(
                ClientEngagement.created_at >= current_month_start,
                ClientEngagement.status != EngagementStatus.CANCELLED
            )
        )
        result = await self.db.execute(monthly_revenue_query)
        monthly_revenue = result.scalar() or Decimal('0')
        
        # YTD revenue
        year_start = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        ytd_revenue_query = select(func.sum(ClientEngagement.total_cost)).where(
            and_(
                ClientEngagement.created_at >= year_start,
                ClientEngagement.status != EngagementStatus.CANCELLED
            )
        )
        result = await self.db.execute(ytd_revenue_query)
        ytd_revenue = result.scalar() or Decimal('0')
        
        # Total savings delivered
        total_savings_query = select(func.sum(ClientEngagement.actual_monthly_savings)).where(
            ClientEngagement.actual_monthly_savings.isnot(None)
        )
        result = await self.db.execute(total_savings_query)
        total_savings = result.scalar() or Decimal('0')
        
        return {
            'active_engagements': active_engagements,
            'monthly_revenue': monthly_revenue,
            'ytd_revenue': ytd_revenue,
            'total_savings_delivered': total_savings * 12,  # Annualized
            'average_engagement_value': ytd_revenue / len(active_engagements) if active_engagements else Decimal('0')
        }
