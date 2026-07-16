import pytest
from backend.detection.eve_parser import EveParser

def test_parse_valid_json():
    json_str = '{"timestamp": "2023-10-01T12:00:00.000000Z", "event_type": "alert"}'
    parsed = EveParser.parse_line(json_str)
    assert parsed is not None
    assert parsed["event_type"] == "alert"

def test_parse_invalid_json():
    json_str = '{"timestamp": "2023-10-01T12:00:00.000000Z", "event_type": "alert"' # Missing brace
    parsed = EveParser.parse_line(json_str)
    assert parsed is None

def test_extract_alert_data():
    eve_event = {
        "timestamp": "2023-10-01T12:00:00.000000Z",
        "event_type": "alert",
        "src_ip": "192.168.1.100",
        "dest_ip": "8.8.8.8",
        "proto": "UDP",
        "alert": {
            "signature": "ET INFO DNS Query to .cc domain",
            "signature_id": 2023883,
            "severity": 3,
            "category": "Potentially Bad Traffic"
        }
    }
    alert_data = EveParser.extract_alert_data(eve_event)
    
    assert alert_data is not None
    assert alert_data["src_ip"] == "192.168.1.100"
    assert alert_data["signature"] == "ET INFO DNS Query to .cc domain"
    assert alert_data["severity"] == "MEDIUM" # mapped from 3
