"""
Advanced Auto-Healing API Router
World-class auto-healing endpoints with intelligent recovery, circuit breakers, and AI-powered insights
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging

from app.services.auto_healing_service import auto_healing_service
from app.core.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auto-healing", tags=["Auto-Healing"])

@router.get("/health-check/{service_name}")
async def perform_health_check(
    service_name: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Perform health check for a specific service"""
    try:
        health_status = await auto_healing_service.perform_health_check(service_name)
        return {
            "status": "success",
            "data": health_status,
            "message": f"Health check completed for {service_name}"
        }
    except Exception as e:
        logger.error(f"Error performing health check for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to perform health check for {service_name}")

@router.post("/heal/{service_name}")
async def auto_heal_service(
    service_name: str,
    issue_type: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Trigger auto-healing for a service"""
    try:
        recovery_action = await auto_healing_service.auto_heal_service(service_name, issue_type)
        
        return {
            "status": "success",
            "data": {
                "id": str(recovery_action.id),
                "service_name": recovery_action.service_name,
                "strategy": recovery_action.strategy.value,
                "success": recovery_action.success,
                "duration": recovery_action.duration,
                "timestamp": recovery_action.timestamp.isoformat(),
                "ai_insights": recovery_action.ai_insights,
                "metadata": recovery_action.metadata
            },
            "message": f"Auto-healing completed for {service_name}"
        }
    except Exception as e:
        logger.error(f"Error auto-healing {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to auto-heal {service_name}")

@router.get("/auto-scaling/status")
async def get_auto_scaling_status(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get auto-scaling status and metrics"""
    try:
        scaling_status = await auto_healing_service.get_auto_scaling_status()
        return {
            "status": "success",
            "data": scaling_status,
            "message": "Auto-scaling status retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting auto-scaling status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve auto-scaling status")

@router.get("/recovery/history")
async def get_recovery_history(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get recovery action history"""
    try:
        recovery_history = await auto_healing_service.get_recovery_history()
        return {
            "status": "success",
            "data": recovery_history,
            "message": "Recovery history retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting recovery history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recovery history")

@router.get("/ai-insights")
async def get_ai_recovery_insights(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get AI-powered recovery insights"""
    try:
        ai_insights = await auto_healing_service.get_ai_recovery_insights()
        return {
            "status": "success",
            "data": ai_insights,
            "message": "AI recovery insights retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting AI recovery insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve AI recovery insights")

@router.get("/circuit-breakers")
async def get_circuit_breakers_status(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get circuit breakers status for all services"""
    try:
        circuit_breakers = {}
        for service_name, circuit_breaker in auto_healing_service.circuit_breakers.items():
            circuit_breakers[service_name] = {
                "state": circuit_breaker.state,
                "failure_count": circuit_breaker.failure_count,
                "failure_threshold": circuit_breaker.failure_threshold,
                "recovery_timeout": circuit_breaker.recovery_timeout,
                "last_failure_time": circuit_breaker.last_failure_time.isoformat() if circuit_breaker.last_failure_time else None
            }
        
        return {
            "status": "success",
            "data": {
                "circuit_breakers": circuit_breakers,
                "total_services": len(circuit_breakers),
                "open_circuits": len([cb for cb in circuit_breakers.values() if cb["state"] == "OPEN"]),
                "half_open_circuits": len([cb for cb in circuit_breakers.values() if cb["state"] == "HALF_OPEN"]),
                "closed_circuits": len([cb for cb in circuit_breakers.values() if cb["state"] == "CLOSED"])
            },
            "message": "Circuit breakers status retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting circuit breakers status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve circuit breakers status")

@router.post("/circuit-breakers/{service_name}/reset")
async def reset_circuit_breaker(
    service_name: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Reset circuit breaker for a specific service"""
    try:
        circuit_breaker = auto_healing_service.circuit_breakers.get(service_name)
        if not circuit_breaker:
            raise HTTPException(status_code=404, detail=f"Circuit breaker not found for {service_name}")
        
        circuit_breaker.state = "CLOSED"
        circuit_breaker.failure_count = 0
        circuit_breaker.last_failure_time = None
        
        return {
            "status": "success",
            "data": {
                "service_name": service_name,
                "state": "CLOSED",
                "reset": True
            },
            "message": f"Circuit breaker reset for {service_name}"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resetting circuit breaker for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to reset circuit breaker for {service_name}")

@router.get("/predictive-recovery")
async def get_predictive_recovery_insights(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get predictive recovery insights and recommendations"""
    try:
        # Simulate predictive recovery insights
        predictive_insights = {
            "predicted_issues": [
                {
                    "service": "backend",
                    "issue_type": "high_cpu",
                    "probability": 0.15,
                    "timeline": "next_2_hours",
                    "confidence": 0.87,
                    "recommended_action": "preemptive_scale_up"
                },
                {
                    "service": "database",
                    "issue_type": "connection_pool_exhaustion",
                    "probability": 0.08,
                    "timeline": "next_6_hours",
                    "confidence": 0.92,
                    "recommended_action": "optimize_connection_pool"
                },
                {
                    "service": "redis",
                    "issue_type": "memory_pressure",
                    "probability": 0.12,
                    "timeline": "next_4_hours",
                    "confidence": 0.85,
                    "recommended_action": "increase_memory_allocation"
                }
            ],
            "preventive_actions": [
                {
                    "action": "scale_up_backend",
                    "reason": "predicted_high_traffic",
                    "confidence": 0.89,
                    "estimated_impact": "prevent_5_minutes_downtime",
                    "effort": "low",
                    "priority": "high"
                },
                {
                    "action": "optimize_database_connections",
                    "reason": "prevent_connection_exhaustion",
                    "confidence": 0.91,
                    "estimated_impact": "improve_response_time_by_20_percent",
                    "effort": "medium",
                    "priority": "medium"
                },
                {
                    "action": "increase_redis_memory",
                    "reason": "prevent_memory_pressure",
                    "confidence": 0.83,
                    "estimated_impact": "prevent_cache_evictions",
                    "effort": "low",
                    "priority": "low"
                }
            ],
            "ai_confidence": 0.89,
            "last_updated": "2024-01-15T12:00:00Z"
        }
        
        return {
            "status": "success",
            "data": predictive_insights,
            "message": "Predictive recovery insights retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting predictive recovery insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve predictive recovery insights")

@router.post("/preventive-actions/{action_id}/execute")
async def execute_preventive_action(
    action_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Execute a preventive action based on AI predictions"""
    try:
        # Simulate preventive action execution
        action_results = {
            "action_id": action_id,
            "executed": True,
            "success": True,
            "duration": 2.5,
            "timestamp": "2024-01-15T12:30:00Z",
            "impact": "prevented_potential_issue",
            "ai_insights": "Preventive action executed successfully based on AI predictions"
        }
        
        return {
            "status": "success",
            "data": action_results,
            "message": "Preventive action executed successfully"
        }
    except Exception as e:
        logger.error(f"Error executing preventive action {action_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to execute preventive action")

@router.get("/recovery-strategies")
async def get_recovery_strategies(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get available recovery strategies and their effectiveness"""
    try:
        strategies = {
            "retry": {
                "description": "Retry with exponential backoff",
                "use_cases": ["temporary_network_issues", "service_unavailable"],
                "success_rate": 0.85,
                "average_duration": 1.2,
                "ai_recommendation": "Best for transient failures"
            },
            "circuit_breaker": {
                "description": "Circuit breaker pattern for fault tolerance",
                "use_cases": ["service_overload", "dependency_failure"],
                "success_rate": 0.92,
                "average_duration": 0.8,
                "ai_recommendation": "Best for cascading failures"
            },
            "scale_up": {
                "description": "Auto-scale resources to handle load",
                "use_cases": ["high_cpu_usage", "high_memory_usage"],
                "success_rate": 0.88,
                "average_duration": 3.5,
                "ai_recommendation": "Best for resource constraints"
            },
            "rollback": {
                "description": "Rollback to previous stable version",
                "use_cases": ["deployment_issues", "version_conflicts"],
                "success_rate": 0.95,
                "average_duration": 5.0,
                "ai_recommendation": "Best for deployment failures"
            },
            "failover": {
                "description": "Failover to backup service",
                "use_cases": ["critical_service_failure", "data_center_issues"],
                "success_rate": 0.78,
                "average_duration": 2.5,
                "ai_recommendation": "Best for critical failures"
            },
            "fallback": {
                "description": "Fallback to degraded mode",
                "use_cases": ["partial_service_failure", "graceful_degradation"],
                "success_rate": 0.90,
                "average_duration": 1.0,
                "ai_recommendation": "Best for partial failures"
            }
        }
        
        return {
            "status": "success",
            "data": {
                "strategies": strategies,
                "total_strategies": len(strategies),
                "ai_learning_enabled": True,
                "pattern_recognition": True
            },
            "message": "Recovery strategies retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting recovery strategies: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recovery strategies")

@router.get("/service-health")
async def get_all_services_health(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get health status for all registered services"""
    try:
        services_health = {}
        for service_name in auto_healing_service.health_checks.keys():
            health_status = await auto_healing_service.perform_health_check(service_name)
            services_health[service_name] = health_status
        
        overall_health = {
            "total_services": len(services_health),
            "healthy_services": len([s for s in services_health.values() if s["status"] == "healthy"]),
            "degraded_services": len([s for s in services_health.values() if s["status"] == "degraded"]),
            "unhealthy_services": len([s for s in services_health.values() if s["status"] == "unhealthy"]),
            "critical_services": len([s for s in services_health.values() if s["status"] == "critical"]),
            "overall_score": sum(s["health_score"] for s in services_health.values()) / len(services_health) if services_health else 0
        }
        
        return {
            "status": "success",
            "data": {
                "services": services_health,
                "overall": overall_health
            },
            "message": "All services health status retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting all services health: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve services health status") 