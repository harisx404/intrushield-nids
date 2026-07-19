"""WebSocket endpoint handler for real-time event streaming."""

import asyncio
import json
from typing import Annotated

import structlog
from backend.api.websocket.manager import ws_manager
from backend.core.exceptions import UnauthorizedException
from backend.core.security import verify_token
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

log = structlog.get_logger(__name__)
websocket_router = APIRouter()

PING_INTERVAL_SECONDS = 30


@websocket_router.websocket("/ws/events")
async def websocket_events(
    websocket: WebSocket,
    token: Annotated[str | None, Query()] = None,
) -> None:
    """WebSocket endpoint for real-time alert and event streaming.

    Authentication: pass JWT access token as query parameter:
        ws://localhost:8000/ws/events?token=eyJ...

    Messages from server:
        {"type": "new_alert", "data": {...}}
        {"type": "stats_update", "data": {...}}
        {"type": "ping", "timestamp": "..."}

    Messages from client:
        {"type": "pong"}
        {"type": "subscribe", "filters": {"severity": ["HIGH", "CRITICAL"]}}
    """
    # Authenticate before accepting connection
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return

    try:
        verify_token(token)
    except UnauthorizedException:
        await websocket.close(code=4001, reason="Invalid or expired token")
        return

    await ws_manager.connect(websocket)
    ping_task: asyncio.Task | None = None

    try:
        # Start keepalive ping task
        async def _ping_loop() -> None:
            while True:
                await asyncio.sleep(PING_INTERVAL_SECONDS)
                await ws_manager.send_ping()

        ping_task = asyncio.create_task(_ping_loop())

        # Listen for client messages
        while True:
            try:
                data = await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
                message = json.loads(data)
                msg_type = message.get("type", "")

                if msg_type == "pong":
                    pass  # Keepalive response, no action needed
                elif msg_type == "subscribe":
                    pass  # Future: filter broadcast by severity
                elif msg_type == "get_stats":
                    await websocket.send_text(
                        json.dumps({"type": "stats_update", "data": {}})
                    )

            except TimeoutError:
                continue  # No message in 60s — client may be idle
            except json.JSONDecodeError:
                pass  # Ignore malformed messages

    except WebSocketDisconnect:
        log.info("websocket_client_disconnected")
    except Exception as exc:
        log.error("websocket_error", error=str(exc))
    finally:
        if ping_task:
            ping_task.cancel()
        await ws_manager.disconnect(websocket)
