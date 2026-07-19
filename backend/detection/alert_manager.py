"""Alert manager — enrich, deduplicate, persist, and publish parsed alerts."""

import structlog
from backend.api.websocket.manager import ws_manager
from backend.core.constants import PRIORITY_MAP, Severity
from backend.core.database import AsyncSessionLocal
from backend.core.event_bus import event_bus
from backend.detection.eve_parser import AlertEvent
from backend.detection.geoip_enricher import GeoIPEnricher
from backend.repositories import alert_repo
from backend.schemas.alert import AlertCreate, AlertResponse
from cachetools import TTLCache

log = structlog.get_logger(__name__)


class AlertManager:
    """Turns parsed Suricata alert events into persisted, enriched alerts."""

    def __init__(self, geoip_enricher: GeoIPEnricher) -> None:
        self.geoip_enricher = geoip_enricher
        # Deduplicate identical alerts for 60s; cap at 10k keys to bound memory.
        self._recent_alerts: TTLCache = TTLCache(maxsize=10000, ttl=60)

    async def process_parsed_alert(self, event: AlertEvent) -> None:
        """Enrich a parsed alert, persist it, and publish it to the event bus."""
        # Deduplicate on (source, signature) to avoid alert storms.
        dedup_key = f"{event.src_ip}-{event.signature_id}"
        if dedup_key in self._recent_alerts:
            return
        self._recent_alerts[dedup_key] = True

        geo = self.geoip_enricher.lookup(event.src_ip or "")

        alert_create = AlertCreate(
            timestamp=event.timestamp,
            severity=self._map_severity(event.severity),
            category=event.category or None,
            signature_id=event.signature_id,
            signature=event.signature or "Unknown",
            src_ip=event.src_ip or "Unknown",
            src_port=event.src_port,
            dst_ip=event.dst_ip or "Unknown",
            dst_port=event.dst_port,
            protocol=event.protocol,
            flow_id=event.flow_id,
            geo_country=geo.country,
            geo_city=geo.city,
            geo_lat=geo.latitude,
            geo_lon=geo.longitude,
            raw_eve=event.raw,
        )

        async with AsyncSessionLocal() as session:
            db_alert = await alert_repo.create(session, obj_in=alert_create)

        # Serialize once into the same shape the REST API returns, so live feed
        # rows and fetched rows are identical on the frontend.
        alert_response = AlertResponse.model_validate(db_alert)

        # Push the full alert to connected WebSocket clients for the live feed.
        await ws_manager.broadcast_alert(alert_response.model_dump(mode="json"))

        # Notify the response engine (log/webhook/email handlers), which operate
        # on the AlertResponse object directly.
        await event_bus.publish("new_alert", alert_response)
        log.info("alert_processed", alert_id=db_alert.id, severity=db_alert.severity)

    @staticmethod
    def _map_severity(priority: int) -> str:
        """Map a Suricata numeric priority (1=highest) to a Severity string."""
        return PRIORITY_MAP.get(priority, Severity.INFO).value
