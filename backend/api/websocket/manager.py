"""WebSocket connection manager for real-time alert broadcasting."""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from typing import Any

import structlog
from fastapi import WebSocket, WebSocketDisconnect

log = structlog.get_logger(__name__)


class WebSocketManager:
    """Manages all active WebSocket connections and broadcasts messages.

    Thread-safe via asyncio.Lock for mutations to the connection set.
    Gracefully handles disconnecting clients during broadcast.
    """

    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._lock = asyncio.Lock()

    @property
    def connection_count(self) -> int:
        """Current number of connected clients."""
        return len(self._connections)

    async def connect(self, websocket: WebSocket) -> None:
        """Accept a new WebSocket connection and register it."""
        await websocket.accept()
        async with self._lock:
            self._connections.add(websocket)
        log.info("websocket_connected", total=self.connection_count)

    async def disconnect(self, websocket: WebSocket) -> None:
        """Remove a WebSocket connection from the registry."""
        async with self._lock:
            self._connections.discard(websocket)
        log.info("websocket_disconnected", total=self.connection_count)

    async def broadcast(self, message: dict[str, Any]) -> None:
        """Broadcast a JSON message to all connected clients.

        Automatically removes stale connections that raise errors during send.
        """
        if not self._connections:
            return

        text = json.dumps(message, default=str)
        stale: set[WebSocket] = set()

        # Snapshot the set to avoid concurrent modification issues
        async with self._lock:
            connections_snapshot = set(self._connections)

        for ws in connections_snapshot:
            try:
                await ws.send_text(text)
            except (WebSocketDisconnect, RuntimeError, Exception):
                stale.add(ws)

        if stale:
            async with self._lock:
                self._connections -= stale
            log.info("websocket_removed_stale", count=len(stale))

    async def broadcast_alert(self, alert_data: dict[str, Any]) -> None:
        """Broadcast a new alert event to all clients."""
        await self.broadcast(
            {
                "type": "new_alert",
                "timestamp": datetime.now(UTC).isoformat(),
                "data": alert_data,
            }
        )

    async def broadcast_stats(self, stats: dict[str, Any]) -> None:
        """Broadcast statistics update (called every 30 seconds)."""
        await self.broadcast(
            {
                "type": "stats_update",
                "timestamp": datetime.now(UTC).isoformat(),
                "data": stats,
            }
        )

    async def send_ping(self) -> None:
        """Send keepalive ping to all clients."""
        await self.broadcast(
            {
                "type": "ping",
                "timestamp": datetime.now(UTC).isoformat(),
            }
        )


# Singleton instance shared across the application
ws_manager = WebSocketManager()
