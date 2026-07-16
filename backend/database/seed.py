"""Database seed script for development."""
import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from backend.core.database import async_session_factory
from backend.models import User, Alert
from backend.core.constants import Severity, AlertStatus

async def seed_db() -> None:
    async with async_session_factory() as session:
        # Check if admin user exists
        result = await session.execute(select(User).filter_by(username="admin"))
        admin_user = result.scalars().first()
        
        if not admin_user:
            # Note: In a real app, hash the password using auth_service.
            # Assuming passlib bcrypt hash for "changeme123"
            hashed_pw = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjIQqiRQYq" # changeme123
            
            admin_user = User(
                username="admin",
                email="admin@nids.local",
                hashed_password=hashed_pw,
                role="admin"
            )
            session.add(admin_user)
            await session.commit()
            print("Admin user created.")

        # Check if alerts exist
        result = await session.execute(select(Alert).limit(1))
        existing_alert = result.scalars().first()
        
        if not existing_alert:
            alerts = []
            now = datetime.now(timezone.utc)
            
            # Generate 50 sample alerts
            for i in range(50):
                severity = Severity.INFO
                if i % 10 == 0:
                    severity = Severity.CRITICAL
                elif i % 5 == 0:
                    severity = Severity.HIGH
                elif i % 3 == 0:
                    severity = Severity.MEDIUM
                elif i % 2 == 0:
                    severity = Severity.LOW
                    
                alert = Alert(
                    timestamp=now - timedelta(minutes=i*5),
                    src_ip=f"192.168.1.{10 + (i % 20)}",
                    src_port=10000 + i,
                    dest_ip="10.0.0.5",
                    dest_port=80,
                    protocol="TCP",
                    signature=f"ET SCAN Potential SSH Scan OUTBOUND {i}",
                    signature_id=2001234 + i,
                    severity=severity,
                    category="Attempted Information Leak",
                    status=AlertStatus.NEW,
                    raw_eve={"event_type": "alert", "alert": {"signature": "test"}}
                )
                alerts.append(alert)
                
            session.add_all(alerts)
            await session.commit()
            print(f"Created {len(alerts)} sample alerts.")

if __name__ == "__main__":
    print("Seeding database...")
    asyncio.run(seed_db())
    print("Database seeding complete.")
