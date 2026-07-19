from fastapi import APIRouter
from backend.core.dependencies import CurrentUser
from backend.schemas.common import ok

router = APIRouter()

@router.get("", summary="Get reports")
async def get_reports(current_user: CurrentUser) -> dict:
    """Retrieve system reports (placeholder)."""
    return ok(data=[], message="Reports retrieved successfully")
