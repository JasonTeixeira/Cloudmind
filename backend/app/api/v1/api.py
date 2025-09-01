"""
Main API Router - Includes all sub-routers
"""

from fastapi import APIRouter

# Import available routers
from app.api.v1.auth.router import router as auth_router
from app.api.v1.projects.router import router as projects_router
from app.api.v1.cost.router import router as cost_router
from app.api.v1.security.router import router as security_router
from app.api.v1.ai.router import router as ai_router
from app.api.v1.infrastructure.router import router as infrastructure_router
from app.api.v1.reports.router import router as reports_router
from app.api.v1.monitoring.router import router as monitoring_router
from app.api.v1.auto_healing.router import router as auto_healing_router
from app.api.v1.data_feeds.router import router as data_feeds_router
from app.api.v1.websocket import router as websocket_router
from app.api.v1.editor import router as editor_router
from app.api.v1.explorer import router as explorer_router
from app.api.v1.terminal import router as terminal_router
from app.api.v1.debugger import router as debugger_router
from app.api.v1.extension import router as extension_router
from app.api.v1.ui import router as ui_router
from app.api.v1.integration import router as integration_router
from app.api.v1.scanner import router as scanner_router
from app.api.v1.project_storage import router as project_storage_router
from app.api.v1.pricing.router import router as pricing_router

# Create main API router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(
    auth_router,
    tags=["Authentication"]
)

api_router.include_router(
    projects_router,
    prefix="/projects",
    tags=["Projects"]
)

api_router.include_router(
    cost_router,
    prefix="/cost",
    tags=["Cost Analysis"]
)

api_router.include_router(
    security_router,
    prefix="/security",
    tags=["Security"]
)

api_router.include_router(
    ai_router,
    prefix="/ai",
    tags=["AI/ML"]
)

api_router.include_router(
    infrastructure_router,
    prefix="/infrastructure",
    tags=["Infrastructure"]
)

api_router.include_router(
    reports_router,
    prefix="/reports",
    tags=["Reports & Analytics"]
)

api_router.include_router(
    monitoring_router,
    prefix="/monitoring",
    tags=["Monitoring & Observability"]
)

api_router.include_router(
    auto_healing_router,
    prefix="/auto-healing",
    tags=["Auto-Healing & Recovery"]
)

api_router.include_router(
    data_feeds_router,
    prefix="/data-feeds",
    tags=["Data Feeds & Integrations"]
)

api_router.include_router(
    websocket_router,
    tags=["WebSocket & Real-time Communication"]
)

api_router.include_router(
    editor_router,
    tags=["Code Editor & IDE"]
)

api_router.include_router(
    explorer_router,
    tags=["File Explorer"]
)

api_router.include_router(
    terminal_router,
    tags=["Integrated Terminal"]
)

api_router.include_router(
    debugger_router,
    tags=["Advanced Debugging"]
)

api_router.include_router(
    extension_router,
    tags=["Advanced Extensions"]
)

api_router.include_router(
    ui_router,
    tags=["Advanced UI"]
)

api_router.include_router(
    integration_router,
    tags=["Final System Integration"]
)

api_router.include_router(
    scanner_router,
    tags=["Enterprise Scanner"]
)

api_router.include_router(
    project_storage_router,
    tags=["Project Storage"]
)

api_router.include_router(
    pricing_router,
    tags=["Tokenized Pricing & Consulting"]
) 