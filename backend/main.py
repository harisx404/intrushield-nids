"""
NIDS FastAPI Application Factory.

Configures the application with lifespan management, middleware stack,
and router registration for all API endpoints.
"""
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.routes import alerts, auth, events, reports, rules, statistics, system
from backend.api.websocket.handlers import websocket_router
from backend.core.config import settings
from backend.core.database import create_tables
from backend.core.logging import setup_logging
from backend.detection.eve_log_watcher import EVELogWatcher
from backend.detection.alert_manager import AlertManager
from backend.detection.geoip_enricher import GeoIPEnricher
from backend.middleware.error_handler import register_exception_handlers
from backend.middleware.rate_limiter import RateLimiterMiddleware
from backend.middleware.request_logger import RequestLoggerMiddleware
from backend.response.response_engine import ResponseEngine
from backend.services.statistics_service import StatisticsService

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager — startup and shutdown."""
    setup_logging()
    log.info("nids_starting", version="1.0.0", env=settings.APP_ENV)

    # Initialize core components
    await create_tables()
    geoip = GeoIPEnricher(settings.GEOIP_DB_PATH)
    from backend.detection.threat_intel import ThreatIntel
    threat_intel = ThreatIntel()
    alert_manager = AlertManager(geoip_enricher=geoip, threat_intel=threat_intel)
    response_engine = ResponseEngine()
    stats_service = StatisticsService()

    # Wire response engine to event bus
    response_engine.start()

    # Start EVE log watcher as background task
    watcher = EVELogWatcher(
        filepath=settings.SURICATA_LOG_PATH,
        alert_manager=alert_manager.process_parsed_alert,
    )
    import asyncio
    watcher_task = asyncio.create_task(watcher.start(), name="eve_watcher")

    # Start stats aggregator (runs every 60 seconds)
    # TODO: Implement run_aggregator_loop in StatisticsService

    log.info("nids_started")
    yield  # Application is running

    # Graceful shutdown
    log.info("nids_shutting_down")
    watcher.stop()
    watcher_task.cancel()
    try:
        await asyncio.gather(watcher_task, return_exceptions=True)
    except Exception:
        pass
    log.info("nids_stopped")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="NIDS-Pro API",
        description="Network Intrusion Detection System — Professional SOC Platform",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # ── Middleware (order matters: outermost first) ──────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
        max_age=3600,
    )
    app.add_middleware(RateLimiterMiddleware)
    app.add_middleware(RequestLoggerMiddleware)

    # ── Exception handlers ───────────────────────────────────────────────
    register_exception_handlers(app)

    # ── Routers ──────────────────────────────────────────────────────────
    prefix = "/api/v1"
    app.include_router(auth.router,       prefix=f"{prefix}/auth", tags=["Authentication"])
    app.include_router(alerts.router,     prefix=f"{prefix}/alerts", tags=["Alerts"])
    app.include_router(rules.router,      prefix=f"{prefix}/rules", tags=["Detection Rules"])
    app.include_router(events.router,     prefix=f"{prefix}/events", tags=["Network Events"])
    app.include_router(statistics.router, prefix=f"{prefix}/statistics", tags=["Statistics"])
    app.include_router(system.router,     prefix=f"{prefix}/system", tags=["System"])
    app.include_router(reports.router,    prefix=f"{prefix}/reports", tags=["Reports"])
    app.include_router(websocket_router)  # WebSocket at /ws/events

    return app


app = create_app()
