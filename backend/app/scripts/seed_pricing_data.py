"""
Seed data for tokenized pricing system
"""

import asyncio
import logging
from decimal import Decimal
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.models.pricing import ServiceToken, UnitType, ServiceCategory, PricingRule

logger = logging.getLogger(__name__)


async def seed_service_tokens(db: AsyncSession):
    """Seed initial service tokens"""
    
    service_tokens = [
        # Scanning Services
        {
            "name": "EC2 Instance Analysis",
            "description": "Deep analysis of EC2 instances for rightsizing opportunities, including CPU, memory, and network utilization patterns",
            "base_price": Decimal("2.50"),
            "unit_type": UnitType.PER_RESOURCE,
            "category": ServiceCategory.SCANNING,
            "minimum_quantity": 1,
            "volume_discount_threshold": 50,
            "volume_discount_rate": Decimal("0.15"),  # 15% discount
            "estimated_duration_hours": Decimal("0.1")
        },
        {
            "name": "RDS Database Analysis",
            "description": "Comprehensive analysis of RDS instances including performance metrics, storage optimization, and Multi-AZ recommendations",
            "base_price": Decimal("5.00"),
            "unit_type": UnitType.PER_RESOURCE,
            "category": ServiceCategory.SCANNING,
            "minimum_quantity": 1,
            "volume_discount_threshold": 20,
            "volume_discount_rate": Decimal("0.10"),
            "estimated_duration_hours": Decimal("0.25")
        },
        {
            "name": "S3 Storage Analysis",
            "description": "Analysis of S3 buckets for storage class optimization, lifecycle policies, and cost reduction opportunities",
            "base_price": Decimal("2.50"),
            "unit_type": UnitType.PER_RESOURCE,
            "category": ServiceCategory.SCANNING,
            "minimum_quantity": 1,
            "volume_discount_threshold": 100,
            "volume_discount_rate": Decimal("0.20"),
            "estimated_duration_hours": Decimal("0.05")
        },
        {
            "name": "Network Architecture Scan",
            "description": "Comprehensive network analysis including VPC configuration, NAT gateways, load balancers, and data transfer costs",
            "base_price": Decimal("200.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.SCANNING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("4.0")
        },
        {
            "name": "Lambda Function Analysis",
            "description": "Analysis of Lambda functions for memory optimization, execution time, and cold start reduction",
            "base_price": Decimal("1.00"),
            "unit_type": UnitType.PER_RESOURCE,
            "category": ServiceCategory.SCANNING,
            "minimum_quantity": 1,
            "volume_discount_threshold": 200,
            "volume_discount_rate": Decimal("0.25"),
            "estimated_duration_hours": Decimal("0.02")
        },
        
        # Optimization Services
        {
            "name": "Cost Optimization Implementation",
            "description": "Hands-on implementation of cost optimization recommendations with monitoring and validation",
            "base_price": Decimal("15.00"),  # 15% of monthly savings
            "unit_type": UnitType.PERCENTAGE_SAVINGS,
            "category": ServiceCategory.IMPLEMENTATION,
            "minimum_quantity": 1,
            "requires_approval": True,
            "estimated_duration_hours": Decimal("8.0")
        },
        {
            "name": "Reserved Instance Planning",
            "description": "Strategic planning and procurement of Reserved Instances and Savings Plans for maximum cost reduction",
            "base_price": Decimal("500.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.OPTIMIZATION,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("6.0")
        },
        {
            "name": "Auto-Scaling Configuration",
            "description": "Implementation of intelligent auto-scaling policies to optimize performance and costs",
            "base_price": Decimal("150.00"),
            "unit_type": UnitType.PER_HOUR,
            "category": ServiceCategory.IMPLEMENTATION,
            "minimum_quantity": 2,
            "estimated_duration_hours": Decimal("4.0")
        },
        
        # Documentation Services
        {
            "name": "Executive Summary Report",
            "description": "High-level executive summary with key findings, recommendations, and ROI projections",
            "base_price": Decimal("150.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.DOCUMENTATION,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("2.0")
        },
        {
            "name": "Technical Implementation Guide",
            "description": "Detailed technical documentation with step-by-step implementation instructions and best practices",
            "base_price": Decimal("300.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.DOCUMENTATION,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("4.0")
        },
        {
            "name": "Architecture Diagrams",
            "description": "Professional architecture diagrams showing current state, optimized state, and migration paths",
            "base_price": Decimal("200.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.DOCUMENTATION,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("3.0")
        },
        {
            "name": "GitHub Repository Setup",
            "description": "Private GitHub repository with all deliverables, documentation, and Infrastructure-as-Code templates",
            "base_price": Decimal("100.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.DOCUMENTATION,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("1.0")
        },
        
        # Monitoring Services
        {
            "name": "Cost Monitoring Setup",
            "description": "Implementation of comprehensive cost monitoring with alerts and automated reporting",
            "base_price": Decimal("400.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.MONITORING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("6.0")
        },
        {
            "name": "Ongoing Monitoring (Monthly)",
            "description": "Monthly monitoring and optimization recommendations with detailed reports",
            "base_price": Decimal("200.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.MONITORING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("2.0")
        },
        
        # Consulting Services
        {
            "name": "Strategic Consulting Session",
            "description": "One-on-one strategic consulting session with cloud architecture and cost optimization expert",
            "base_price": Decimal("200.00"),
            "unit_type": UnitType.PER_HOUR,
            "category": ServiceCategory.CONSULTING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("1.0")
        },
        {
            "name": "Team Training Workshop",
            "description": "Comprehensive training workshop for your team on cloud cost optimization best practices",
            "base_price": Decimal("1200.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.TRAINING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("8.0")
        },
        {
            "name": "24/7 Support Package",
            "description": "Premium support package with 24/7 access to cloud optimization experts",
            "base_price": Decimal("500.00"),
            "unit_type": UnitType.FLAT_RATE,
            "category": ServiceCategory.CONSULTING,
            "minimum_quantity": 1,
            "estimated_duration_hours": Decimal("0.0")  # Ongoing support
        }
    ]
    
    for token_data in service_tokens:
        token = ServiceToken(
            id=uuid4(),
            **token_data
        )
        db.add(token)
    
    await db.commit()
    logger.info(f"✅ Seeded {len(service_tokens)} service tokens")


async def seed_pricing_rules(db: AsyncSession):
    """Seed initial pricing rules"""
    
    pricing_rules = [
        {
            "name": "Enterprise Volume Discount",
            "description": "15% discount for engagements with more than 500 total resources",
            "condition_expression": "total_cost > 5000",
            "modifier_type": "discount",
            "modifier_value": Decimal("0.85"),  # 15% discount
            "priority": 10,
            "minimum_engagement_value": Decimal("5000.00")
        },
        {
            "name": "Multi-Cloud Complexity Premium",
            "description": "25% premium for multi-cloud environments (AWS + GCP + Azure)",
            "condition_expression": "total_cost > 2000",
            "modifier_type": "premium",
            "modifier_value": Decimal("1.25"),  # 25% premium
            "priority": 5,
            "minimum_engagement_value": Decimal("2000.00")
        },
        {
            "name": "Repeat Client Discount",
            "description": "10% discount for clients with previous engagements",
            "condition_expression": "engagement_count > 0",
            "modifier_type": "discount",
            "modifier_value": Decimal("0.90"),  # 10% discount
            "priority": 8
        },
        {
            "name": "Startup Discount",
            "description": "20% discount for small engagements under $1000",
            "condition_expression": "total_cost < 1000",
            "modifier_type": "discount",
            "modifier_value": Decimal("0.80"),  # 20% discount
            "priority": 15,
            "maximum_engagement_value": Decimal("1000.00")
        },
        {
            "name": "Rush Job Premium",
            "description": "50% premium for expedited delivery (less than 1 week)",
            "condition_expression": "total_cost > 500",
            "modifier_type": "premium",
            "modifier_value": Decimal("1.50"),  # 50% premium
            "priority": 20,
            "minimum_engagement_value": Decimal("500.00")
        }
    ]
    
    for rule_data in pricing_rules:
        rule = PricingRule(
            id=uuid4(),
            **rule_data
        )
        db.add(rule)
    
    await db.commit()
    logger.info(f"✅ Seeded {len(pricing_rules)} pricing rules")


async def main():
    """Main seeding function"""
    logging.basicConfig(level=logging.INFO)
    
    async for db in get_async_session():
        try:
            logger.info("🌱 Starting pricing data seeding...")
            
            await seed_service_tokens(db)
            await seed_pricing_rules(db)
            
            logger.info("✅ Pricing data seeding completed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Seeding failed: {e}")
            await db.rollback()
            raise
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(main())
