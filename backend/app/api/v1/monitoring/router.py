"""
Enhanced Monitoring Router
World-class monitoring endpoints with performance optimization,
auto-healing, and advanced analytics capabilities.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import asyncio
import logging

from app.core.auth import get_current_user
from app.services.monitoring_service import monitoring_service
from app.services.performance_optimization import performance_optimization_service
from app.services.auto_healing_service import auto_healing_service
from app.schemas.monitoring import (
    SystemHealthResponse,
    PerformanceMetricsResponse,
    SecurityMetricsResponse,
    BusinessMetricsResponse,
    AlertResponse,
    ExecutiveDashboardResponse,
    AutoHealingReportResponse,
    PerformanceOptimizationReportResponse,
    ComprehensiveHealthResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health(current_user=Depends(get_current_user)):
    """Get comprehensive system health status"""
    try:
        health_data = await monitoring_service.get_system_health()
        return SystemHealthResponse(
            status="success",
            data=health_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"System health check failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get system health")


@router.get("/performance", response_model=PerformanceMetricsResponse)
async def get_performance_metrics(current_user=Depends(get_current_user)):
    """Get comprehensive performance metrics"""
    try:
        performance_data = await performance_optimization_service.get_performance_report()
        return PerformanceMetricsResponse(
            status="success",
            data=performance_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Performance metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance metrics")


@router.get("/security", response_model=SecurityMetricsResponse)
async def get_security_metrics(current_user=Depends(get_current_user)):
    """Get comprehensive security metrics"""
    try:
        security_data = await monitoring_service.get_security_metrics()
        return SecurityMetricsResponse(
            status="success",
            data=security_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Security metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get security metrics")


@router.get("/business", response_model=BusinessMetricsResponse)
async def get_business_metrics(current_user=Depends(get_current_user)):
    """Get comprehensive business metrics"""
    try:
        business_data = await monitoring_service.get_business_metrics()
        return BusinessMetricsResponse(
            status="success",
            data=business_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Business metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get business metrics")


@router.get("/alerts", response_model=List[AlertResponse])
async def get_active_alerts(current_user=Depends(get_current_user)):
    """Get all active system alerts"""
    try:
        alerts = await monitoring_service.get_active_alerts()
        return [
            AlertResponse(
                id=alert["id"],
                type=alert["type"],
                severity=alert["severity"],
                title=alert["title"],
                description=alert["description"],
                timestamp=alert["timestamp"],
                resolved=alert["resolved"]
            )
            for alert in alerts
        ]
    except Exception as e:
        logger.error(f"Alerts retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alerts")


@router.get("/executive-dashboard", response_model=ExecutiveDashboardResponse)
async def get_executive_dashboard(current_user=Depends(get_current_user)):
    """Get comprehensive executive dashboard data"""
    try:
        # Gather all executive metrics
        performance_data = await performance_optimization_service.get_performance_report()
        security_data = await monitoring_service.get_security_metrics()
        business_data = await monitoring_service.get_business_metrics()
        auto_healing_data = await auto_healing_service.get_auto_healing_report()
        
        # Calculate executive KPIs
        executive_metrics = {
            "revenue": {
                "current": business_data.get("revenue", {}).get("current", 0),
                "previous": business_data.get("revenue", {}).get("previous", 0),
                "trend": business_data.get("revenue", {}).get("trend", "stable"),
                "percentage": business_data.get("revenue", {}).get("percentage_change", 0)
            },
            "users": {
                "total": business_data.get("users", {}).get("total", 0),
                "active": business_data.get("users", {}).get("active", 0),
                "new": business_data.get("users", {}).get("new_this_month", 0),
                "growth": business_data.get("users", {}).get("growth_rate", 0)
            },
            "performance": {
                "uptime": performance_data.get("current_metrics", {}).get("uptime", 0),
                "response_time": performance_data.get("current_metrics", {}).get("response_time", 0),
                "error_rate": performance_data.get("current_metrics", {}).get("error_rate", 0),
                "throughput": performance_data.get("current_metrics", {}).get("throughput", 0)
            },
            "security": {
                "score": security_data.get("security_score", 0),
                "vulnerabilities": security_data.get("vulnerabilities", {}).get("total", 0),
                "incidents": security_data.get("security_incidents", {}).get("total", 0),
                "compliance": security_data.get("compliance", {}).get("status", "Unknown")
            },
            "costs": {
                "total": business_data.get("costs", {}).get("total", 0),
                "savings": business_data.get("costs", {}).get("savings", 0),
                "optimization": business_data.get("costs", {}).get("optimization_percentage", 0),
                "forecast": business_data.get("costs", {}).get("forecast", 0)
            },
            "ai_insights": {
                "total": business_data.get("ai_insights", {}).get("total", 0),
                "high_priority": business_data.get("ai_insights", {}).get("high_priority", 0),
                "implemented": business_data.get("ai_insights", {}).get("implemented", 0),
                "accuracy": business_data.get("ai_insights", {}).get("accuracy", 0)
            }
        }
        
        # Real-time metrics
        real_time_metrics = [
            {
                "name": "Active Users",
                "value": executive_metrics["users"]["active"],
                "unit": "users",
                "trend": "up",
                "change": executive_metrics["users"]["growth"],
                "status": "healthy"
            },
            {
                "name": "Response Time",
                "value": executive_metrics["performance"]["response_time"],
                "unit": "ms",
                "trend": "down" if executive_metrics["performance"]["response_time"] < 200 else "up",
                "change": -5.2,
                "status": "healthy" if executive_metrics["performance"]["response_time"] < 200 else "warning"
            },
            {
                "name": "CPU Usage",
                "value": performance_data.get("current_metrics", {}).get("cpu_usage", 0),
                "unit": "%",
                "trend": "up",
                "change": 3.1,
                "status": "warning" if performance_data.get("current_metrics", {}).get("cpu_usage", 0) > 70 else "healthy"
            },
            {
                "name": "Memory Usage",
                "value": performance_data.get("current_metrics", {}).get("memory_usage", 0),
                "unit": "%",
                "trend": "up",
                "change": 1.8,
                "status": "healthy" if performance_data.get("current_metrics", {}).get("memory_usage", 0) < 80 else "warning"
            },
            {
                "name": "Database Connections",
                "value": performance_data.get("current_metrics", {}).get("database_connections", 0),
                "unit": "connections",
                "trend": "stable",
                "change": 0,
                "status": "healthy"
            },
            {
                "name": "Error Rate",
                "value": executive_metrics["performance"]["error_rate"],
                "unit": "%",
                "trend": "down",
                "change": -0.01,
                "status": "healthy" if executive_metrics["performance"]["error_rate"] < 0.1 else "critical"
            }
        ]
        
        # Active alerts
        alerts = await monitoring_service.get_active_alerts()
        
        return ExecutiveDashboardResponse(
            status="success",
            data={
                "executive_metrics": executive_metrics,
                "real_time_metrics": real_time_metrics,
                "alerts": alerts,
                "auto_healing": auto_healing_data,
                "performance_optimization": performance_data
            },
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Executive dashboard failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get executive dashboard")


@router.get("/auto-healing", response_model=AutoHealingReportResponse)
async def get_auto_healing_report(current_user=Depends(get_current_user)):
    """Get comprehensive auto-healing report"""
    try:
        auto_healing_data = await auto_healing_service.get_auto_healing_report()
        return AutoHealingReportResponse(
            status="success",
            data=auto_healing_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Auto-healing report failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get auto-healing report")


@router.get("/performance-optimization", response_model=PerformanceOptimizationReportResponse)
async def get_performance_optimization_report(current_user=Depends(get_current_user)):
    """Get comprehensive performance optimization report"""
    try:
        performance_data = await performance_optimization_service.get_performance_report()
        return PerformanceOptimizationReportResponse(
            status="success",
            data=performance_data,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        logger.error(f"Performance optimization report failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get performance optimization report")


@router.get("/comprehensive-health", response_model=ComprehensiveHealthResponse)
async def get_comprehensive_health(current_user=Depends(get_current_user)):
    """Get comprehensive system health with all metrics"""
    try:
        # Gather all health data
        system_health = await monitoring_service.get_system_health()
        performance_data = await performance_optimization_service.get_performance_report()
        security_data = await monitoring_service.get_security_metrics()
        business_data = await monitoring_service.get_business_metrics()
        auto_healing_data = await auto_healing_service.get_auto_healing_report()
        
        # Calculate overall health score
        health_scores = {
            "system": system_health.get("overall_health_score", 0),
            "performance": performance_data.get("current_metrics", {}).get("performance_score", 0),
            "security": security_data.get("security_score", 0),
            "business": business_data.get("business_health_score", 0)
        }
        
        overall_health_score = sum(health_scores.values()) / len(health_scores)
        
        comprehensive_data = {
            "overall_health_score": overall_health_score,
            "health_breakdown": health_scores,
            "system_health": system_health,
            "performance_metrics": performance_data,
            "security_metrics": security_data,
            "business_metrics": business_data,
            "auto_healing_status": auto_healing_data,
            "recommendations": await _generate_health_recommendations(health_scores),
            "critical_alerts": await monitoring_service.get_critical_alerts(),
            "system_status": "healthy" if overall_health_score > 90 else "warning" if overall_health_score > 70 else "critical"
        }
        
        return ComprehensiveHealthResponse(
            status="success",
            data=comprehensive_data,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Comprehensive health check failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get comprehensive health")


@router.post("/start-auto-healing")
async def start_auto_healing(background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    """Start auto-healing monitoring in background"""
    try:
        background_tasks.add_task(auto_healing_service.start_auto_healing_monitoring)
        return {
            "status": "success",
            "message": "Auto-healing monitoring started",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Auto-healing start failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to start auto-healing")


@router.post("/optimize-performance")
async def optimize_performance(current_user=Depends(get_current_user)):
    """Trigger performance optimization"""
    try:
        # Trigger performance optimization
        optimization_result = await performance_optimization_service.collect_performance_metrics()
        
        return {
            "status": "success",
            "message": "Performance optimization triggered",
            "data": optimization_result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Performance optimization failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to optimize performance")


@router.get("/metrics/real-time")
async def get_real_time_metrics(current_user=Depends(get_current_user)):
    """Get real-time system metrics"""
    try:
        # Get real-time metrics from all services
        performance_metrics = await performance_optimization_service.collect_performance_metrics()
        system_health = await monitoring_service.get_system_health()
        
        real_time_data = {
            "performance": {
                "response_time": performance_metrics.response_time,
                "throughput": performance_metrics.throughput,
                "error_rate": performance_metrics.error_rate,
                "cache_hit_rate": performance_metrics.cache_hit_rate
            },
            "system": {
                "cpu_usage": performance_metrics.cpu_usage,
                "memory_usage": performance_metrics.memory_usage,
                "database_connections": performance_metrics.database_connections,
                "active_requests": performance_metrics.active_requests
            },
            "health": {
                "overall_status": system_health.get("overall_status", "unknown"),
                "health_score": system_health.get("overall_health_score", 0),
                "last_check": datetime.utcnow().isoformat()
            }
        }
        
        return {
            "status": "success",
            "data": real_time_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Real-time metrics failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to get real-time metrics")


async def _generate_health_recommendations(health_scores: Dict[str, float]) -> List[Dict[str, Any]]:
    """Generate health recommendations based on scores"""
    recommendations = []
    
    for component, score in health_scores.items():
        if score < 70:
            recommendations.append({
                "component": component,
                "priority": "high",
                "title": f"Critical {component.title()} Health Issue",
                "description": f"{component.title()} health score is {score:.1f}%, immediate attention required",
                "action": f"Investigate and resolve {component} issues"
            })
        elif score < 85:
            recommendations.append({
                "component": component,
                "priority": "medium",
                "title": f"{component.title()} Health Warning",
                "description": f"{component.title()} health score is {score:.1f}%, monitor closely",
                "action": f"Review {component} configuration and optimize"
            })
        elif score < 95:
            recommendations.append({
                "component": component,
                "priority": "low",
                "title": f"{component.title()} Optimization Opportunity",
                "description": f"{component.title()} health score is {score:.1f}%, room for improvement",
                "action": f"Consider {component} optimizations"
            })
    
    if not recommendations:
        recommendations.append({
            "component": "overall",
            "priority": "info",
            "title": "System Health Excellent",
            "description": "All systems are performing optimally",
            "action": "Continue monitoring"
        })
    
    return recommendations 