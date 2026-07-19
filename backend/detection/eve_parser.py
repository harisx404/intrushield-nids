"""
Suricata EVE JSON event parser.

Converts raw EVE JSON dict into typed Python objects.
Handles all event types: alert, dns, http, tls, flow, stats, fileinfo, anomaly.
Never raises exceptions on malformed data — returns None instead.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


@dataclass
class EVEEvent:
    """Base parsed EVE event."""
    event_type: str
    timestamp: datetime
    src_ip: Optional[str] = None
    src_port: Optional[int] = None
    dst_ip: Optional[str] = None
    dst_port: Optional[int] = None
    protocol: Optional[str] = None
    flow_id: Optional[str] = None
    in_iface: Optional[str] = None
    raw: dict = field(default_factory=dict)


@dataclass
class AlertEvent(EVEEvent):
    """Parsed Suricata alert event."""
    signature_id: int = 0
    signature: str = ""
    category: str = ""
    severity: int = 3        # Suricata severity: 1=high, 4=low
    action: str = "allowed"
    rev: int = 1
    gid: int = 1


class EVEParser:
    """Parse raw Suricata EVE JSON events into typed objects."""

    @staticmethod
    def parse(raw: dict[str, Any]) -> Optional[EVEEvent]:
        """Parse a raw EVE JSON dict into a typed EVEEvent.
        
        Args:
            raw: Raw dictionary from JSON-parsed EVE log line.
            
        Returns:
            Typed EVEEvent subclass or None if event cannot be parsed
            or is an unrecognised event type.
        """
        try:
            event_type = raw.get("event_type", "")
            timestamp = EVEParser._parse_timestamp(raw.get("timestamp", ""))

            base_kwargs: dict[str, Any] = {
                "event_type": event_type,
                "timestamp": timestamp,
                "src_ip": raw.get("src_ip"),
                "src_port": raw.get("src_port"),
                "dst_ip": raw.get("dest_ip"),
                "dst_port": raw.get("dest_port"),
                "protocol": raw.get("proto"),
                "flow_id": str(raw.get("flow_id", "")) or None,
                "in_iface": raw.get("in_iface"),
                "raw": raw,
            }

            if event_type == "alert":
                return EVEParser._parse_alert(raw, base_kwargs)
            else:
                return EVEEvent(**base_kwargs)

        except Exception:
            return None  # Never crash on malformed events

    @staticmethod
    def _parse_alert(raw: dict, base_kwargs: dict) -> AlertEvent:
        """Parse an alert event specifically."""
        alert_data = raw.get("alert", {})
        return AlertEvent(
            **base_kwargs,
            signature_id=alert_data.get("signature_id", 0),
            signature=alert_data.get("signature", "Unknown"),
            category=alert_data.get("category", ""),
            severity=alert_data.get("severity", 3),
            action=alert_data.get("action", "allowed"),
            rev=alert_data.get("rev", 1),
            gid=alert_data.get("gid", 1),
        )

    @staticmethod
    def _parse_timestamp(ts_str: str) -> datetime:
        """Parse Suricata timestamp string to aware datetime.
        
        Suricata format: "2024-01-15T14:23:11.456789+0000"
        """
        if not ts_str:
            return datetime.now(timezone.utc)
        try:
            # Handle Suricata's +0000 suffix
            ts_str = ts_str.replace("+0000", "+00:00")
            return datetime.fromisoformat(ts_str)
        except ValueError:
            return datetime.now(timezone.utc)
