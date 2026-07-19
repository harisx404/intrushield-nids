from backend.models.statistics import TrafficStatistics
from backend.repositories.base import BaseRepository
from backend.schemas.statistics import TrafficStatisticsBase, TrafficStatisticsCreate
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession


class StatisticsRepository(
    BaseRepository[TrafficStatistics, TrafficStatisticsCreate, TrafficStatisticsBase]
):
    async def get_latest(self, session: AsyncSession) -> TrafficStatistics | None:
        result = await session.execute(
            select(self.model).order_by(desc(self.model.timestamp)).limit(1)
        )
        return result.scalars().first()


statistics_repo = StatisticsRepository(TrafficStatistics)
