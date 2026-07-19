from backend.models.rule import DetectionRule
from backend.repositories.base import BaseRepository
from backend.schemas.rule import DetectionRuleCreate, DetectionRuleUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class RuleRepository(
    BaseRepository[DetectionRule, DetectionRuleCreate, DetectionRuleUpdate]
):
    async def get_by_sid(
        self, session: AsyncSession, *, sid: int
    ) -> DetectionRule | None:
        result = await session.execute(select(self.model).filter(self.model.sid == sid))
        return result.scalars().first()


rule_repo = RuleRepository(DetectionRule)
