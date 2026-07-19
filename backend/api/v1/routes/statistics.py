from datetime import UTC, datetime

from backend.core.dependencies import CurrentUser, get_db
from backend.schemas.common import ok
from backend.schemas.statistics import TrafficStatisticsResponse
from backend.services.statistics_service import statistics_service
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/current", summary="Get current statistics")
@router.get("/summary", summary="Get summary statistics")
async def read_current_statistics(
    current_user: CurrentUser, db: AsyncSession = Depends(get_db)
) -> dict:
    """Retrieve the latest traffic and alert statistics."""
    stats = await statistics_service.get_current_stats(db)
    if not stats:
        resp = TrafficStatisticsResponse(
            id=0,
            timestamp=datetime.now(UTC),
            alerts_total=0,
            alerts_critical=0,
            alerts_high=0,
            bytes_in=0,
            bytes_out=0,
            packets_in=0,
            packets_out=0,
        )
    else:
        resp = TrafficStatisticsResponse.model_validate(stats)
    return ok(data=resp, message="Statistics retrieved successfully")


@router.get("/dashboard", summary="Get aggregated dashboard statistics")
async def read_dashboard_statistics(
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Retrieve the aggregated KPIs, severity breakdown, trend and top talkers."""
    stats = await statistics_service.get_dashboard_stats(db)
    return ok(data=stats, message="Dashboard statistics retrieved successfully")
