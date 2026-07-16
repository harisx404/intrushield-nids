from typing import Dict, Any, Optional
from datetime import datetime
from backend.core.event_bus import event_bus
from backend.detection.geoip_enricher import GeoIPEnricher
from backend.detection.threat_intel import ThreatIntel
from backend.schemas.alert import AlertCreate
from backend.core.database import async_session_factory

class AlertManager:
    def __init__(self, geoip_enricher: GeoIPEnricher, threat_intel: ThreatIntel):
        self.geoip_enricher = geoip_enricher
        self.threat_intel = threat_intel
        self._recent_alerts = {}  # Deduplication stub

    async def process_parsed_alert(self, parsed_alert: Dict[str, Any]) -> None:
        """Process an alert, enrich it, save to DB, and publish to EventBus."""
        if not parsed_alert:
            return

        # Deduplication
        dedup_key = f"{parsed_alert.get('src_ip')}-{parsed_alert.get('signature_id')}"
        now = datetime.now().timestamp()
        if dedup_key in self._recent_alerts:
            if now - self._recent_alerts[dedup_key] < 60:
                return # Skip duplicate within 60 seconds
        self._recent_alerts[dedup_key] = now

        # Enrichment
        src_country = self.geoip_enricher.lookup_country(parsed_alert.get("src_ip", ""))
        parsed_alert["src_country"] = src_country

        try:
            timestamp = datetime.fromisoformat(parsed_alert["timestamp"].replace("Z", "+00:00"))
        except (ValueError, TypeError, KeyError):
            timestamp = datetime.now()

        alert_create = AlertCreate(
            timestamp=timestamp,
            src_ip=parsed_alert.get("src_ip", "Unknown"),
            src_port=parsed_alert.get("src_port"),
            dest_ip=parsed_alert.get("dest_ip", "Unknown"),
            dest_port=parsed_alert.get("dest_port"),
            protocol=parsed_alert.get("protocol", "UNKNOWN"),
            signature=parsed_alert.get("signature", "Unknown"),
            signature_id=parsed_alert.get("signature_id", 0),
            severity=parsed_alert.get("severity", "INFO"),
            category=parsed_alert.get("category"),
            flow_id=parsed_alert.get("flow_id"),
            src_country=src_country,
            raw_eve=parsed_alert.get("raw_eve", {})
        )

        async with async_session_factory() as session:
            from backend.repositories import alert_repo
            db_alert = await alert_repo.create(session, obj_in=alert_create)
            
            # Publish to event bus for WebSockets and Response Engine
            await event_bus.publish("new_alert", {"alert_id": db_alert.id, "alert": parsed_alert})
