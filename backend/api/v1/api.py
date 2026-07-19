from backend.api.v1.routes.alerts import router as alerts_router
from backend.api.v1.routes.auth import router as auth_router
from backend.api.v1.routes.events import router as events_router
from backend.api.v1.routes.reports import router as reports_router
from backend.api.v1.routes.rules import router as rules_router
from backend.api.v1.routes.statistics import router as statistics_router
from backend.api.v1.routes.system import router as system_router
from backend.api.websocket.manager import router as websockets_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth_router, tags=["login"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
api_router.include_router(rules_router, prefix="/rules", tags=["rules"])
api_router.include_router(statistics_router, prefix="/statistics", tags=["statistics"])
api_router.include_router(system_router, prefix="/system", tags=["system"])
api_router.include_router(reports_router, prefix="/reports", tags=["reports"])
api_router.include_router(websockets_router, tags=["websocket"])
