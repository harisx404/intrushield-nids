from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from backend.repositories import alert_repo
from backend.models.alert import Alert
from backend.schemas.alert import AlertUpdate
from backend.core.exceptions import NotFoundError

class AlertService:
    async def get_alerts(
        self, session: AsyncSession, skip: int = 0, limit: int = 50, severity: Optional[str] = None
    ) -> tuple[List[Alert], int]:
        if severity:
            alerts = await alert_repo.get_recent_alerts(session, limit=limit, severity=severity)
            return alerts, len(alerts)
        return await alert_repo.get_multi(session, skip=skip, limit=limit)

    async def update_status(self, session: AsyncSession, alert_id: int, status: str) -> Alert:
        alert = await alert_repo.get(session, alert_id)
        if not alert:
            raise NotFoundError(detail="Alert not found")
        
        alert_update = AlertUpdate(status=status)
        return await alert_repo.update(session, db_obj=alert, obj_in=alert_update)

alert_service = AlertService()
