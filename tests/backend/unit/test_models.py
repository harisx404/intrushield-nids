import pytest
from datetime import datetime, timezone
from backend.models import User, Alert
from backend.core.constants import Severity

def test_user_model_creation():
    user = User(username="testuser", email="test@example.com", hashed_password="hash", role="analyst")
    assert user.username == "testuser"
    assert user.role == "analyst"
    assert user.is_active is True

def test_alert_model_creation():
    alert = Alert(
        timestamp=datetime.now(timezone.utc),
        src_ip="1.1.1.1",
        dest_ip="2.2.2.2",
        protocol="TCP",
        signature="Test alert",
        signature_id=12345,
        severity=Severity.HIGH,
        raw_eve={}
    )
    assert alert.src_ip == "1.1.1.1"
    assert alert.severity == Severity.HIGH
    assert alert.status == "NEW"
