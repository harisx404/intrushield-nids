from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from backend.repositories import statistics_repo
from backend.models.statistics import TrafficStatistics

class StatisticsService:
    async def get_current_stats(self, session: AsyncSession) -> Optional[TrafficStatistics]:
        return await statistics_repo.get_latest(session)

statistics_service = StatisticsService()
