# API Reference

The NIDS Backend exposes a RESTful API and a real-time WebSocket connection.

## REST Endpoints (v1)

Base Path: `/api/v1`

### Authentication (`/auth`)
- `POST /auth/login`: Authenticate and receive JWT.
- `POST /auth/refresh`: Refresh JWT access token.

### Alerts (`/alerts`)
- `GET /alerts`: Retrieve paginated alerts.
  - Query Params: `page`, `limit`, `severity`, `source_ip`
- `GET /alerts/{id}`: Get detailed alert by ID.
- `PATCH /alerts/{id}/status`: Acknowledge or resolve an alert.

### Rules (`/rules`)
- `GET /rules`: List all loaded Suricata rules.
- `POST /rules`: Add a custom rule to `custom.rules` (Requires Admin).
- `POST /rules/reload`: Trigger Suricata to hot-reload rule signatures.

### System (`/system`)
- `GET /system/health`: Readiness/Liveness probe.
- `GET /system/metrics`: Export Prometheus metrics.

---

## WebSocket Stream

Endpoint: `ws://localhost:8000/api/v1/ws/alerts`

**Authentication**: Pass JWT via query parameter `?token=...`

**Payload Format (Server to Client)**:
```json
{
  "type": "NEW_ALERT",
  "data": {
    "id": "uuid",
    "timestamp": "2026-07-16T12:00:00Z",
    "src_ip": "192.168.1.10",
    "dst_ip": "10.0.0.5",
    "signature": "ET SCAN Nmap OS Detection Probe",
    "severity": "HIGH",
    "action": "allowed"
  }
}
```
