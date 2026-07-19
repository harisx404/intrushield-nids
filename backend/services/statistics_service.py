"""Service layer for traffic/alert statistics and dashboard aggregation."""
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.alert import Alert
from backend.models.rule import DetectionRule
from backend.models.statistics import TrafficStatistics
from backend.repositories import statistics_repo


class StatisticsService:
    async def get_current_stats(self, session: AsyncSession) -> Optional[TrafficStatistics]:
        return await statistics_repo.get_latest(session)

    async def get_dashboard_stats(self, session: AsyncSession) -> dict:
        """Aggregate the KPIs, severity breakdown, 24h trend and top talkers.

        Shape matches the frontend DashboardStats interface in
        frontend/app/(dashboard)/dashboard/page.tsx.
        """
        now = datetime.now(timezone.utc)
        day_ago = now - timedelta(hours=24)

        total_today = await session.scalar(
            select(func.count()).select_from(Alert).where(Alert.timestamp >= day_ago)
        ) or 0

        critical_high_today = await session.scalar(
            select(func.count())
            .select_from(Alert)
            .where(Alert.timestamp >= day_ago, Alert.severity.in_(("CRITICAL", "HIGH")))
        ) or 0

        active_rules = await session.scalar(
            select(func.count()).select_from(DetectionRule).where(DetectionRule.is_active.is_(True))
        ) or 0

        latest_stats = await statistics_repo.get_latest(session)
        packets_analyzed = 0
        if latest_stats:
            packets_analyzed = (latest_stats.packets_in or 0) + (latest_stats.packets_out or 0)

        # Severity breakdown across the last 24h.
        severity_rows = await session.execute(
            select(Alert.severity, func.count())
            .where(Alert.timestamp >= day_ago)
            .group_by(Alert.severity)
        )
        alerts_by_severity = {sev: count for sev, count in severity_rows.all()}
        for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"):
            alerts_by_severity.setdefault(level, 0)

        # Hourly trend for the last 24h, zero-filled so the chart is continuous.
        trend_rows = await session.execute(
            select(Alert.timestamp, Alert.id).where(Alert.timestamp >= day_ago)
        )
        buckets = {i: 0 for i in range(24)}
        for ts, _ in trend_rows.all():
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            hours_ago = int((now - ts).total_seconds() // 3600)
            if 0 <= hours_ago < 24:
                buckets[23 - hours_ago] += 1
        alerts_trend_24h = [
            {
                "hour": (now - timedelta(hours=23 - i)).strftime("%H:00"),
                "count": buckets[i],
            }
            for i in range(24)
        ]

        # Top source IPs by alert volume in the last 24h.
        top_rows = await session.execute(
            select(Alert.src_ip, Alert.geo_country, func.count().label("cnt"))
            .where(Alert.timestamp >= day_ago)
            .group_by(Alert.src_ip, Alert.geo_country)
            .order_by(func.count().desc())
            .limit(5)
        )
        top_src_ips = [
            {"ip": ip, "country": country, "count": cnt}
            for ip, country, cnt in top_rows.all()
        ]

        return {
            "total_alerts_today": total_today,
            "critical_alerts_today": critical_high_today,
            "active_rules_count": active_rules,
            "packets_analyzed": packets_analyzed,
            "alerts_by_severity": alerts_by_severity,
            "alerts_trend_24h": alerts_trend_24h,
            "top_src_ips": top_src_ips,
        }


statistics_service = StatisticsService()
