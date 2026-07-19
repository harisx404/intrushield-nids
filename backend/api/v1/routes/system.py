from fastapi import APIRouter
from typing import Any
import asyncio

from backend.core.dependencies import AdminRole
from backend.schemas.common import ok

router = APIRouter()

@router.post("/suricata/restart", summary="Restart Suricata", dependencies=[AdminRole])
async def restart_suricata() -> dict:
    """Simulate restarting Suricata engine."""
    await asyncio.sleep(2)  # Simulate delay
    return ok(data=None, message="Suricata engine restarted successfully")

@router.post("/suricata/reload", summary="Reload Suricata rules", dependencies=[AdminRole])
async def reload_suricata_rules() -> dict:
    """Simulate reloading Suricata rules."""
    await asyncio.sleep(1)  # Simulate delay
    return ok(data=None, message="Suricata rules reloaded successfully")

@router.get("/health", summary="Health Check")
async def health_check() -> dict:
    """Health check endpoint for Docker."""
    return {"status": "ok"}
