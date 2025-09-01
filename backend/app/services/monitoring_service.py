"""
World-Class Monitoring Service for CloudMind
Enterprise-grade monitoring with enhanced security
"""

import asyncio
import logging
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# Enhanced logging
logger = logging.getLogger(__name__)

# Optional OpenTelemetry imports with fallback
try:
    from opentelemetry import trace, metrics
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
    from opentelemetry.exporter.jaeger.thrift import JaegerExporter
    from opentelemetry.exporter.prometheus import PrometheusExporter
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    logger.warning("OpenTelemetry not available, using fallback monitoring")
    OPENTELEMETRY_AVAILABLE = False

from app.core.config import settings

class MonitoringLevel(Enum):
    """Monitoring levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class SystemMetrics:
    """System metrics data"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, float]
    load_average: Optional[float]
    timestamp: datetime

@dataclass
class SecurityEvent:
    """Security event data"""
    event_type: str
    severity: MonitoringLevel
    description: str
    source_ip: Optional[str]
    user_id: Optional[str]
    metadata: Dict[str, Any]
    timestamp: datetime

class WorldClassMonitoringService:
    """World-class monitoring service with enhanced security"""
    
    def __init__(self):
        self.metrics_history: List[SystemMetrics] = []
        self.security_events: List[SecurityEvent] = []
        self.performance_metrics: Dict[str, Any] = {}
        self.health_status: Dict[str, Any] = {}
        
        # Initialize OpenTelemetry if available
        if OPENTELEMETRY_AVAILABLE:
            self._initialize_opentelemetry()
        else:
            self._initialize_fallback_monitoring()
    
    def _initialize_opentelemetry(self):
        """Initialize OpenTelemetry monitoring"""
        try:
            # Initialize trace provider
            trace_provider = TracerProvider()
            trace.set_tracer_provider(trace_provider)
            
            # Add Jaeger exporter
            jaeger_exporter = JaegerExporter(
                agent_host_name="localhost",
                agent_port=6831,
            )
            trace_provider.add_span_processor(
                BatchSpanProcessor(jaeger_exporter)
            )
            
            # Initialize metrics
            metric_reader = PeriodicExportingMetricReader(
                PrometheusExporter()
            )
            meter_provider = MeterProvider(metric_reader=metric_reader)
            metrics.set_meter_provider(meter_provider)
            
            self.tracer = trace.get_tracer(__name__)
            self.meter = metrics.get_meter(__name__)
            
            logger.info("✅ OpenTelemetry monitoring initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenTelemetry: {e}")
            self._initialize_fallback_monitoring()
    
    def _initialize_fallback_monitoring(self):
        """Initialize fallback monitoring without OpenTelemetry"""
        self.tracer = None
        self.meter = None
        logger.info("✅ Fallback monitoring initialized")
    
    async def collect_system_metrics(self) -> SystemMetrics:
        """Collect comprehensive system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network metrics
            network_io = psutil.net_io_counters()
            network_metrics = {
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv,
                'packets_sent': network_io.packets_sent,
                'packets_recv': network_io.packets_recv
            }
            
            # Load average (Unix systems)
            try:
                load_average = os.getloadavg()[0]
            except AttributeError:
                load_average = None
            
            metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                disk_percent=disk_percent,
                network_io=network_metrics,
                load_average=load_average,
                timestamp=datetime.utcnow()
            )
            
            # Store metrics history (keep last 1000 entries)
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > 1000:
                self.metrics_history.pop(0)
            
            # Update performance metrics
            self.performance_metrics = {
                'current_cpu': cpu_percent,
                'current_memory': memory_percent,
                'current_disk': disk_percent,
                'avg_cpu_1h': self._calculate_average_cpu(60),
                'avg_memory_1h': self._calculate_average_memory(60),
                'peak_cpu_24h': self._calculate_peak_cpu(1440),
                'peak_memory_24h': self._calculate_peak_memory(1440)
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return SystemMetrics(
                cpu_percent=0.0,
                memory_percent=0.0,
                disk_percent=0.0,
                network_io={},
                load_average=None,
                timestamp=datetime.utcnow()
            )
    
    def _calculate_average_cpu(self, minutes: int) -> float:
        """Calculate average CPU usage over specified minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_time
        ]
        
        if not recent_metrics:
            return 0.0
        
        return sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics)
    
    def _calculate_average_memory(self, minutes: int) -> float:
        """Calculate average memory usage over specified minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_time
        ]
        
        if not recent_metrics:
            return 0.0
        
        return sum(m.memory_percent for m in recent_metrics) / len(recent_metrics)
    
    def _calculate_peak_cpu(self, minutes: int) -> float:
        """Calculate peak CPU usage over specified minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_time
        ]
        
        if not recent_metrics:
            return 0.0
        
        return max(m.cpu_percent for m in recent_metrics)
    
    def _calculate_peak_memory(self, minutes: int) -> float:
        """Calculate peak memory usage over specified minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp > cutoff_time
        ]
        
        if not recent_metrics:
            return 0.0
        
        return max(m.memory_percent for m in recent_metrics)
    
    async def record_security_event(
        self,
        event_type: str,
        severity: MonitoringLevel,
        description: str,
        source_ip: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Record security event with enhanced logging"""
        try:
            event = SecurityEvent(
                event_type=event_type,
                severity=severity,
                description=description,
                source_ip=source_ip,
                user_id=user_id,
                metadata=metadata or {},
                timestamp=datetime.utcnow()
            )
            
            # Store security event
            self.security_events.append(event)
            
            # Keep only last 1000 security events
            if len(self.security_events) > 1000:
                self.security_events.pop(0)
            
            # Log security event
            log_message = f"SECURITY_EVENT: {event_type} - {description}"
            if source_ip:
                log_message += f" (IP: {source_ip})"
            if user_id:
                log_message += f" (User: {user_id})"
            
            if severity == MonitoringLevel.CRITICAL:
                logger.critical(log_message)
            elif severity == MonitoringLevel.ERROR:
                logger.error(log_message)
            elif severity == MonitoringLevel.WARNING:
                logger.warning(log_message)
            else:
                logger.info(log_message)
            
            # Update health status
            self._update_health_status(event)
            
        except Exception as e:
            logger.error(f"Failed to record security event: {e}")
    
    def _update_health_status(self, event: SecurityEvent):
        """Update health status based on security events"""
        current_time = datetime.utcnow()
        
        # Count recent security events by severity
        recent_events = [
            e for e in self.security_events
            if current_time - e.timestamp < timedelta(hours=1)
        ]
        
        critical_count = len([e for e in recent_events if e.severity == MonitoringLevel.CRITICAL])
        error_count = len([e for e in recent_events if e.severity == MonitoringLevel.ERROR])
        warning_count = len([e for e in recent_events if e.severity == MonitoringLevel.WARNING])
        
        # Determine overall health status
        if critical_count > 0:
            health_status = "critical"
        elif error_count > 5:
            health_status = "degraded"
        elif warning_count > 10:
            health_status = "warning"
        else:
            health_status = "healthy"
        
        self.health_status = {
            "status": health_status,
            "last_updated": current_time.isoformat(),
            "recent_events": {
                "critical": critical_count,
                "error": error_count,
                "warning": warning_count
            },
            "total_events_24h": len([
                e for e in self.security_events
                if current_time - e.timestamp < timedelta(hours=24)
            ])
        }
    
    async def get_comprehensive_health_status(self) -> Dict[str, Any]:
        """Get comprehensive health status"""
        try:
            # Collect current metrics
            current_metrics = await self.collect_system_metrics()
            
            # Determine system health
            system_health = "healthy"
            if current_metrics.cpu_percent > 90:
                system_health = "critical"
            elif current_metrics.cpu_percent > 80:
                system_health = "degraded"
            elif current_metrics.memory_percent > 90:
                system_health = "critical"
            elif current_metrics.memory_percent > 80:
                system_health = "degraded"
            
            return {
                "status": system_health,
                "timestamp": datetime.utcnow().isoformat(),
                "system_metrics": {
                    "cpu_percent": current_metrics.cpu_percent,
                    "memory_percent": current_metrics.memory_percent,
                    "disk_percent": current_metrics.disk_percent,
                    "load_average": current_metrics.load_average
                },
                "performance_metrics": self.performance_metrics,
                "security_status": self.health_status,
                "monitoring_enabled": True,
                "opentelemetry_available": OPENTELEMETRY_AVAILABLE
            }
            
        except Exception as e:
            logger.error(f"Failed to get health status: {e}")
            return {
                "status": "unknown",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "monitoring_enabled": True,
                "opentelemetry_available": OPENTELEMETRY_AVAILABLE
            }
    
    async def get_security_report(self) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        try:
            current_time = datetime.utcnow()
            
            # Get recent security events
            recent_events = [
                e for e in self.security_events
                if current_time - e.timestamp < timedelta(hours=24)
            ]
            
            # Categorize events
            event_types = {}
            severity_counts = {}
            
            for event in recent_events:
                # Count by event type
                event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
                
                # Count by severity
                severity_counts[event.severity.value] = severity_counts.get(event.severity.value, 0) + 1
            
            return {
                "total_events_24h": len(recent_events),
                "event_types": event_types,
                "severity_counts": severity_counts,
                "recent_events": [
                    {
                        "event_type": e.event_type,
                        "severity": e.severity.value,
                        "description": e.description,
                        "source_ip": e.source_ip,
                        "user_id": e.user_id,
                        "timestamp": e.timestamp.isoformat()
                    }
                    for e in recent_events[-10:]  # Last 10 events
                ],
                "security_score": self._calculate_security_score(recent_events)
            }
            
        except Exception as e:
            logger.error(f"Failed to generate security report: {e}")
            return {"error": str(e)}
    
    def _calculate_security_score(self, events: List[SecurityEvent]) -> int:
        """Calculate security score based on events"""
        if not events:
            return 100
        
        # Penalize based on severity and frequency
        penalty = 0
        for event in events:
            if event.severity == MonitoringLevel.CRITICAL:
                penalty += 20
            elif event.severity == MonitoringLevel.ERROR:
                penalty += 10
            elif event.severity == MonitoringLevel.WARNING:
                penalty += 5
            else:
                penalty += 1
        
        return max(0, 100 - penalty)
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        logger.info("🚀 Starting world-class monitoring service...")
        
        while True:
            try:
                # Collect metrics every 30 seconds
                await self.collect_system_metrics()
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait longer on error

# Global monitoring service instance
monitoring_service = WorldClassMonitoringService() 