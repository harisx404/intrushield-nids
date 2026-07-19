"""Seed the database with a default admin user and sample alerts for development.

Idempotent: running it repeatedly will not create duplicate users or pile up
extra alerts. Intended for local development and demos only.
"""

import asyncio
import random
from datetime import UTC, datetime, timedelta

from backend.core.constants import AlertStatus, Severity
from backend.core.database import AsyncSessionLocal
from backend.core.security import get_password_hash
from backend.models import Alert, User
from sqlalchemy import func, select

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@nids.local"
DEFAULT_ADMIN_PASSWORD = (
    "changeme123"  # noqa: S105 - dev-only default, documented in README
)
SAMPLE_ALERT_COUNT = 50

_SIGNATURES = [
    ("ET SCAN Potential SSH Scan OUTBOUND", "Attempted Information Leak", Severity.LOW),
    (
        "ET MALWARE Cobalt Strike Beacon Observed",
        "A Network Trojan was Detected",
        Severity.CRITICAL,
    ),
    (
        "ET EXPLOIT Possible SQL Injection Attempt",
        "Web Application Attack",
        Severity.HIGH,
    ),
    (
        "ET POLICY DNS Query to .onion Domain",
        "Potentially Bad Traffic",
        Severity.MEDIUM,
    ),
    (
        "ET INFO Observed DNS Query to Public Resolver",
        "Not Suspicious Traffic",
        Severity.INFO,
    ),
    (
        "ET DOS Possible NTP Amplification Attack",
        "Attempted Denial of Service",
        Severity.HIGH,
    ),
]
_PROTOCOLS = ["TCP", "UDP", "ICMP"]


async def _seed_admin(session) -> None:
    """Create the default admin user if it does not already exist."""
    existing = await session.scalar(
        select(User).where(User.username == DEFAULT_ADMIN_USERNAME)
    )
    if existing:
        print(f"Admin user '{DEFAULT_ADMIN_USERNAME}' already exists — skipping.")
        return

    session.add(
        User(
            username=DEFAULT_ADMIN_USERNAME,
            email=DEFAULT_ADMIN_EMAIL,
            hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
            role="admin",
            is_active=True,
        )
    )
    await session.commit()
    print(
        f"Admin user created — username: {DEFAULT_ADMIN_USERNAME} / password: {DEFAULT_ADMIN_PASSWORD}"
    )


async def _seed_alerts(session) -> None:
    """Populate a fixed number of sample alerts if the table is empty."""
    existing_count = await session.scalar(select(func.count()).select_from(Alert))
    if existing_count:
        print(f"Alerts table already has {existing_count} rows — skipping sample data.")
        return

    now = datetime.now(UTC)
    rng = random.Random(42)  # deterministic sample data across runs
    alerts = []
    for i in range(SAMPLE_ALERT_COUNT):
        signature, category, severity = rng.choice(_SIGNATURES)
        alerts.append(
            Alert(
                timestamp=now - timedelta(minutes=i * 5),
                severity=severity.value,
                status=AlertStatus.NEW.value,
                category=category,
                signature_id=2001234 + i,
                signature=f"{signature} #{i}",
                src_ip=f"203.0.113.{10 + (i % 40)}",
                src_port=rng.randint(1024, 65535),
                dst_ip=f"10.0.0.{5 + (i % 10)}",
                dst_port=rng.choice([80, 443, 22, 3389, 53]),
                protocol=rng.choice(_PROTOCOLS),
                geo_country=rng.choice(["US", "RU", "CN", "DE", "BR", "IN"]),
                raw_eve={"event_type": "alert", "alert": {"signature": signature}},
            )
        )

    session.add_all(alerts)
    await session.commit()
    print(f"Created {len(alerts)} sample alerts.")


async def seed_db() -> None:
    """Seed the database with default data, creating tables first if needed."""
    from backend.core.database import create_tables

    await create_tables()
    async with AsyncSessionLocal() as session:
        await _seed_admin(session)
        await _seed_alerts(session)


if __name__ == "__main__":
    print("Seeding database...")
    asyncio.run(seed_db())
    print("Database seeding complete.")
