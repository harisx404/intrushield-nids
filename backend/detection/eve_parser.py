import json
from typing import Dict, Any, Optional

class EveParser:
    @staticmethod
    def parse_line(line: str) -> Optional[Dict[str, Any]]:
        """Parse a single line of EVE JSON log."""
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            return None

    @staticmethod
    def extract_alert_data(eve_event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract relevant fields for an alert from an EVE event."""
        if eve_event.get("event_type") != "alert":
            return None
            
        alert_info = eve_event.get("alert", {})
        
        return {
            "timestamp": eve_event.get("timestamp"),
            "src_ip": eve_event.get("src_ip"),
            "src_port": eve_event.get("src_port"),
            "dest_ip": eve_event.get("dest_ip"),
            "dest_port": eve_event.get("dest_port"),
            "protocol": eve_event.get("proto", "UNKNOWN"),
            "signature": alert_info.get("signature", "Unknown Signature"),
            "signature_id": alert_info.get("signature_id", 0),
            "severity": EveParser._map_severity(alert_info.get("severity", 3)),
            "category": alert_info.get("category", "Unknown"),
            "flow_id": eve_event.get("flow_id"),
            "raw_eve": eve_event,
        }
        
    @staticmethod
    def _map_severity(priority: int) -> str:
        """Map Suricata priority (1=highest, 4=lowest) to NIDS severity."""
        mapping = {
            1: "CRITICAL",
            2: "HIGH",
            3: "MEDIUM",
            4: "LOW"
        }
        return mapping.get(priority, "INFO")
