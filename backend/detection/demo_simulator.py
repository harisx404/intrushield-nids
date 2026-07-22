"""Demo Simulator  automatically generates realistic network threats."""

import asyncio
import random
from collections.abc import Callable, Coroutine
from datetime import UTC, datetime
from typing import Any

import structlog

log = structlog.get_logger(__name__)

MOCK_ALERTS = [
    {
        "event_type": "alert",
        "src_ip": "192.168.1.100",
        "dest_ip": "10.0.0.5",
        "alert": {
            "signature": "ET SCAN Nmap OS Detection Probe",
            "severity": 1,
            "category": "Network Scan",
        },
    },
    {
        "event_type": "alert",
        "src_ip": "45.33.32.156",
        "dest_ip": "10.0.0.10",
        "alert": {
            "signature": "Possible SQL Injection (UNION SELECT)",
            "severity": 1,
            "category": "Web Application Attack",
        },
    },
    {
        "event_type": "alert",
        "src_ip": "10.0.0.50",
        "dest_ip": "10.0.0.1",
        "alert": {
            "signature": "Possible Reverse Shell (/bin/bash outbound)",
            "severity": 2,
            "category": "Suspicious Login",
        },
    },
    {
        "event_type": "alert",
        "src_ip": "8.8.8.8",
        "dest_ip": "192.168.1.15",
        "alert": {
            "signature": "Suspicious Large DNS TXT Query",
            "severity": 2,
            "category": "Bad Unknown",
        },
    },
    {
        "event_type": "alert",
        "src_ip": "114.114.114.114",
        "dest_ip": "10.0.0.100",
        "alert": {
            "signature": "Log4Shell JNDI Injection Attempt",
            "severity": 1,
            "category": "Attempted Admin",
        },
    },
]


class DemoSimulator:
    """Injects live fake traffic directly into the alert manager."""

    def __init__(self, callback: Callable[[dict[str, Any]], Coroutine[Any, Any, None]]):
        self.callback = callback
        self._running = False

    async def start(self) -> None:
        """Start the background injection loop."""
        self._running = True
        log.info(
            "demo_simulator_started",
            message="Injecting live threats every 10-20 seconds",
        )
        while self._running:
            await asyncio.sleep(random.uniform(10.0, 20.0))

            # Create a mock alert
            alert = random.choice(MOCK_ALERTS).copy()
            alert["timestamp"] = datetime.now(UTC).isoformat()

            try:
                await self.callback(alert)
            except Exception as e:
                log.error("demo_injection_failed", error=str(e))

    def stop(self) -> None:
        """Stop the simulator."""
        self._running = False
