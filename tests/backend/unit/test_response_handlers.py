"""Unit tests for response-handler gating and severity thresholds."""

from datetime import datetime, timezone

import pytest

from backend.core.constants import severity_at_least
from backend.response.email_handler import EmailHandler
from backend.response.log_handler import LogHandler
from backend.response.webhook_handler import WebhookHandler
from backend.schemas.alert import AlertResponse


def _alert(severity: str) -> AlertResponse:
    now = datetime.now(timezone.utc)
    return AlertResponse(
        id=1,
        timestamp=now,
        severity=severity,
        status="NEW",
        signature="Test signature",
        src_ip="203.0.113.1",
        dst_ip="192.0.2.1",
        created_at=now,
        updated_at=now,
    )


def test_severity_at_least_ranking():
    assert severity_at_least("CRITICAL", "HIGH") is True
    assert severity_at_least("HIGH", "HIGH") is True
    assert severity_at_least("LOW", "HIGH") is False
    # Unknown severities never satisfy a threshold.
    assert severity_at_least("BOGUS", "LOW") is False


def test_log_handler_respects_enable_flag(monkeypatch):
    handler = LogHandler()
    monkeypatch.setattr(
        "backend.response.log_handler.settings.ENABLE_LOG_RESPONSE", True
    )
    assert handler.should_handle(_alert("INFO")) is True
    monkeypatch.setattr(
        "backend.response.log_handler.settings.ENABLE_LOG_RESPONSE", False
    )
    assert handler.should_handle(_alert("CRITICAL")) is False


def test_email_handler_gates_on_flag_and_severity(monkeypatch):
    handler = EmailHandler()
    monkeypatch.setattr(
        "backend.response.email_handler.settings.ENABLE_EMAIL_RESPONSE", True
    )
    monkeypatch.setattr(
        "backend.response.email_handler.settings.EMAIL_MIN_SEVERITY", "HIGH"
    )
    assert handler.should_handle(_alert("CRITICAL")) is True
    assert handler.should_handle(_alert("MEDIUM")) is False

    # Disabled flag overrides severity.
    monkeypatch.setattr(
        "backend.response.email_handler.settings.ENABLE_EMAIL_RESPONSE", False
    )
    assert handler.should_handle(_alert("CRITICAL")) is False


def test_webhook_handler_requires_flag_severity_and_url(monkeypatch):
    handler = WebhookHandler()
    handler.webhook_url = "https://example.com/hook"
    monkeypatch.setattr(
        "backend.response.webhook_handler.settings.ENABLE_WEBHOOK_RESPONSE", True
    )
    monkeypatch.setattr(
        "backend.response.webhook_handler.settings.WEBHOOK_MIN_SEVERITY", "MEDIUM"
    )
    assert handler.should_handle(_alert("HIGH")) is True
    assert handler.should_handle(_alert("LOW")) is False

    # No URL configured -> never fires even when enabled.
    handler.webhook_url = ""
    assert handler.should_handle(_alert("CRITICAL")) is False


@pytest.mark.asyncio
async def test_response_engine_persists_results(db_session, monkeypatch):
    """The engine should record a ResponseLog row for each handler that runs."""
    import sys

    from backend.repositories import response_repo
    from backend.response.response_engine import ResponseEngine

    # The package __init__ binds the `response_engine` instance over the
    # submodule name, so fetch the actual module object from sys.modules.
    engine_module = sys.modules["backend.response.response_engine"]

    # Only the log handler is enabled for this test.
    monkeypatch.setattr(
        "backend.response.log_handler.settings.ENABLE_LOG_RESPONSE", True
    )
    monkeypatch.setattr(
        "backend.response.email_handler.settings.ENABLE_EMAIL_RESPONSE", False
    )
    monkeypatch.setattr(
        "backend.response.webhook_handler.settings.ENABLE_WEBHOOK_RESPONSE", False
    )

    # Route the engine's own-session persistence into the test session.
    class _CtxSession:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, *args):
            return False

    monkeypatch.setattr(engine_module, "AsyncSessionLocal", lambda: _CtxSession())

    engine = ResponseEngine()
    await engine.process_alert(_alert("CRITICAL"))

    rows, total = await response_repo.get_multi(db_session)
    assert total == 1
    assert rows[0].handler_name == "LogHandler"
    assert rows[0].status == "SUCCESS"
