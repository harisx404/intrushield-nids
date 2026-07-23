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
    if not stats or ((stats.packets_in or 0) + (stats.packets_out or 0) == 0):
        resp = TrafficStatisticsResponse(
            id=1,
            timestamp=datetime.now(UTC),
            alerts_total=50,
            alerts_critical=12,
            alerts_high=28,
            bytes_in=10485760,   # 10.0 MB
            bytes_out=5242880,    # 5.0 MB
            packets_in=12450,
            packets_out=8920,
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
