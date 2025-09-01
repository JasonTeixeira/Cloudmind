"""
Production-ready monitoring for CloudMind
"""

import asyncio
import logging
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, Summary

logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('cloudmind_http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('cloudmind_http_request_duration_seconds', 'HTTP request latency')
ACTIVE_CONNECTIONS = Gauge('cloudmind_active_connections', 'Number of active connections')
DATABASE_QUERIES = Counter('cloudmind_database_queries_total', 'Total database queries', ['operation'])
AI_REQUESTS = Counter('cloudmind_ai_requests_total', 'Total AI requests', ['provider', 'model'])
CLOUD_SCANS = Counter('cloudmind_cloud_scans_total', 'Total cloud scans', ['provider'])
SECURITY_EVENTS = Counter('cloudmind_security_events_total', 'Total security events', ['severity'])

async def init_monitoring():
    """Initialize monitoring"""
    try:
        logger.info("Initializing monitoring...")
        
        # Initialize metrics
        ACTIVE_CONNECTIONS.set(0)
        
        logger.info("✅ Monitoring initialized")
        
    except Exception as e:
        logger.error(f"❌ Monitoring initialization failed: {e}")
        raise

def record_request(method: str, endpoint: str, status: int, duration: float):
    """Record HTTP request metrics"""
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.observe(duration)

def record_database_query(operation: str):
    """Record database query metrics"""
    DATABASE_QUERIES.labels(operation=operation).inc()

def record_ai_request(provider: str, model: str):
    """Record AI request metrics"""
    AI_REQUESTS.labels(provider=provider, model=model).inc()

def record_cloud_scan(provider: str):
    """Record cloud scan metrics"""
    CLOUD_SCANS.labels(provider=provider).inc()

def record_security_event(severity: str):
    """Record security event metrics"""
    SECURITY_EVENTS.labels(severity=severity).inc()

def increment_active_connections():
    """Increment active connections"""
    ACTIVE_CONNECTIONS.inc()

def decrement_active_connections():
    """Decrement active connections"""
    ACTIVE_CONNECTIONS.dec()
