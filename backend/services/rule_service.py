from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import os

from backend.repositories import rule_repo
from backend.models.rule import DetectionRule
from backend.schemas.rule import DetectionRuleCreate, DetectionRuleUpdate
from backend.core.exceptions import NotFoundError

RULES_FILE = "/etc/suricata/rules/custom.rules"

def _append_to_file(content: str):
    try:
        with open(RULES_FILE, "a") as f:
            f.write(f"\n{content}\n")
    except Exception as e:
        print(f"Failed to write to rules file: {e}")

class RuleService:
    async def get_rules(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> tuple[List[DetectionRule], int]:
        return await rule_repo.get_multi(session, skip=skip, limit=limit)

    async def create_rule(self, session: AsyncSession, rule_in: DetectionRuleCreate) -> DetectionRule:
        rule = await rule_repo.create(session, obj_in=rule_in)
        if rule_in.enabled:
            _append_to_file(rule_in.content)
        return rule

    async def update_rule(self, session: AsyncSession, rule_id: int, rule_in: DetectionRuleUpdate) -> DetectionRule:
        rule = await rule_repo.get(session, rule_id)
        if not rule:
            raise NotFoundError("Rule not found")
        return await rule_repo.update(session, db_obj=rule, obj_in=rule_in)

rule_service = RuleService()
