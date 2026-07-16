# Architecture Deep Dive: CodeAlpha NIDS

The CodeAlpha Network Intrusion Detection System is engineered using a strictly **Layered Domain-Driven Design (DDD)** combined with an **event-driven asynchronous pipeline**. This architecture is designed specifically to handle high-throughput network events (e.g., volumetric DDoS, SYN floods) without exhausting system resources or causing the browser UI to lock up.

## 1. The Detection Layer (Suricata)

At the edge of the system sits **Suricata 7.0**. Suricata operates in IPS/IDS mode, bound directly to the host network interface via Docker `network_mode: host` and `privileged: true`.

- **Packet Inspection**: Suricata evaluates raw packets against loaded signatures (`custom.rules`, `local.rules`, Emerging Threats).
- **Output (EVE JSON)**: Instead of writing directly to a database (which introduces massive latency and locks), Suricata streams detections via Unix pipes to `/var/log/suricata/eve.json`.

## 2. The Ingestion Pipeline (Python / asyncio)

To ingest logs at speeds exceeding 10,000 events per second, we avoid synchronous reads.

- **`aiofiles` Tailing**: A background `asyncio` task (`eve_log_watcher.py`) tails the `eve.json` file asynchronously. 
- **The Queue Buffer**: Parsed lines are instantly dumped into an `asyncio.Queue`. The file tailer never waits for the database.
- **The Batch Worker**: A separate consumer pulls from the queue. It groups events into batches of 100 or when a 50ms flush interval is hit.

## 3. The Core Backend (FastAPI / SQLAlchemy)

The Python backend is strictly segmented:

- **Routers (`backend/api/v1/routes/`)**: Handles incoming HTTP requests. Zero business logic.
- **Services (`backend/services/`)**: The "Domain" layer. Contains the rules for routing alerts, calculating threat scores, and triggering response handlers.
- **Repositories (`backend/repositories/`)**: The data access layer. Implements the Unit of Work pattern using SQLAlchemy `AsyncSession`. Database errors are trapped and mapped to clean `BaseNIDSError` exceptions.

## 4. The Real-Time Broadcast (WebSockets)

When the `AlertService` commits a new threat to the database, it fires an event to the `ConnectionManager`.
The `ConnectionManager` maintains an active registry of connected Next.js clients. It serializes the `Alert` Pydantic model into JSON and pushes it across the socket.

## 5. The Frontend (Next.js & Zustand)

To prevent React from crashing under the weight of 1,000 socket messages per second:
1. **Debouncing / Buffering**: The `useWebSocket.ts` hook intercepts incoming messages and pushes them to a local Javascript array buffer.
2. **Scheduled Flushes**: Every 100ms, the buffer is flushed and deeply merged into the global **Zustand** state (`alertStore.ts`).
3. **Optimized Re-renders**: React components subscribe only to specific Zustand slices (e.g., `useAlertStore(state => state.alerts)`), meaning the DOM updates efficiently exactly 10 times a second, remaining perfectly smooth to the human eye.
