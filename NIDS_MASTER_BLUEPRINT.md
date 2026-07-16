# MASTER BLUEPRINT — Network Intrusion Detection System (NIDS)
## `CodeAlpha_NetworkIntrusionDetectionSystem`
### Prepared for: CodeAlpha Cybersecurity Internship
### Author Role: SOC Analyst & Principal Security Architect + Senior Full-Stack Engineer
### Classification: Internal Technical Blueprint — AI Agent Implementation Guide
### Version: 1.0.0

---

> **This document is the authoritative source of truth for building this project.**
> An AI coding agent must follow every section in sequence.
> No implementation decision is left ambiguous.
> Every architecture choice is deliberate and production-grade.

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Software Architecture](#4-software-architecture)
5. [Folder Structure](#5-folder-structure)
6. [Coding Standards](#6-coding-standards)
7. [UI/UX Design System](#7-uiux-design-system)
8. [Dashboard Pages](#8-dashboard-pages)
9. [Features](#9-features)
10. [Alert System](#10-alert-system)
11. [Response Mechanism](#11-response-mechanism)
12. [Database Design](#12-database-design)
13. [API Design](#13-api-design)
14. [Security Practices](#14-security-practices)
15. [Logging Strategy](#15-logging-strategy)
16. [Testing Strategy](#16-testing-strategy)
17. [GitHub Standards](#17-github-standards)
18. [Documentation Plan](#18-documentation-plan)
19. [README Blueprint](#19-readme-blueprint)
20. [GitHub Presentation](#20-github-presentation)
21. [Contributor Experience](#21-contributor-experience)
22. [Deployment](#22-deployment)
23. [Performance](#23-performance)
24. [Future Roadmap](#24-future-roadmap)
25. [Final Development Plan](#25-final-development-plan)
26. [Rules for the AI Coding Agent](#26-rules-for-the-ai-coding-agent)

---

## 1. PROJECT OVERVIEW

### 1.1 What Is This Project?

The **Network Intrusion Detection System (NIDS)** is a production-grade, open-source cybersecurity platform that monitors network traffic in real-time, detects malicious or suspicious activities, generates actionable alerts, and provides a professional SOC-style dashboard for security analysts.

At its core, the system leverages **Suricata** — the industry-standard, multi-threaded intrusion detection engine — as the detection backbone, supplemented by a custom Python-based orchestration layer, a FastAPI REST + WebSocket backend, and a React/Next.js frontend that visualizes network threat intelligence live.

Unlike simple script-based NIDS demonstrations, this project is architected to mirror real-world Security Operations Center (SOC) tooling: modular, scalable, observable, and production-deployable via Docker.

---

### 1.2 Why Does This Project Exist?

Modern networks face increasingly sophisticated threats: port scans, DDoS floods, SQL injection attempts over network layers, botnet communication, malware C2 beacons, ARP poisoning, DNS exfiltration, and lateral movement by attackers. Manual monitoring is impossible at scale.

A NIDS automates this surveillance by:
- Inspecting every packet crossing the network interface
- Matching traffic patterns against known threat signatures
- Raising alerts with full packet context when threats are detected
- Enabling security teams to respond before damage is done

This project exists to demonstrate mastery of network security fundamentals, detection engineering, full-stack application development, and professional software craftsmanship — all aligned with real-world SOC workflows.

---

### 1.3 Real-World Applications

| Application Domain | Example |
|---|---|
| Corporate SOC | Monitoring employee network for insider threats and malware |
| Data Centers | Detecting lateral movement and unauthorized access |
| University Networks | Monitoring student networks for policy violations |
| Industrial Control Systems | Detecting OT/IT boundary attacks |
| ISP Infrastructure | Identifying DDoS patterns and botnet nodes |
| Home Labs | Personal network security monitoring |
| Honeypots | Capturing attacker TTPs for threat intelligence |
| Managed Security Service Providers (MSSPs) | Delivering detection-as-a-service to clients |

---

### 1.4 Who Uses NIDS?

- **Security Operations Center (SOC) Analysts** — primary users of NIDS dashboards
- **Network Security Engineers** — who write and tune detection rules
- **Incident Responders** — who investigate alerts to confirm breaches
- **Threat Hunters** — who proactively search for hidden adversaries
- **Compliance Officers** — who need audit trails of network events
- **DevSecOps Engineers** — who integrate NIDS into CI/CD pipelines
- **CTF Players and Security Learners** — practicing detection skills

---

### 1.5 Project Goals

**Primary Goals:**
1. Deploy and configure Suricata as the core detection engine
2. Write and manage custom Suricata detection rules
3. Parse, store, and display Suricata EVE JSON alerts
4. Build a real-time SOC dashboard with live monitoring
5. Implement automated response mechanisms
6. Provide attack analytics, traffic statistics, and visual reports

**Internship Objectives:**
- Demonstrate understanding of network intrusion detection concepts
- Show ability to integrate industry-standard security tools (Suricata)
- Build a full-stack application around a security core
- Practice documentation, version control, and professional development workflows

**Learning Outcomes:**
- Deep understanding of TCP/IP packet analysis and network protocols
- Hands-on experience with Suricata rule syntax and signature-based detection
- Full-stack development using Python (FastAPI) and React (Next.js)
- Real-time data streaming with WebSockets
- Docker-based deployment and containerization
- Database design for time-series security event data
- Professional GitHub repository management

---

## 2. SYSTEM ARCHITECTURE

### 2.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      TRAFFIC SOURCES                            │
│  [Network Interface] [PCAP File] [Simulated Traffic Generator]  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Raw Packets
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    PACKET CAPTURE LAYER                          │
│   Suricata (libpcap/AF_PACKET) + Python Scapy (supplementary)   │
│   • Live interface sniffing                                      │
│   • PCAP replay support                                          │
│   • Protocol dissection                                          │
└──────────────────────────────┬───────────────────────────────────┘
                               │ Decoded Packets / Flows
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DETECTION ENGINE                              │
│   Suricata Multi-Threaded Engine                                 │
│   • Signature-based detection (ET Rules + Custom Rules)          │
│   • Anomaly detection                                            │
│   • Protocol validation                                          │
│   • Flow tracking                                                │
│   • File extraction                                              │
└────────────────┬─────────────────────────┬───────────────────────┘
                 │                         │
                 ▼                         ▼
┌────────────────────────┐   ┌─────────────────────────────────────┐
│    RULE ENGINE         │   │     EVE JSON OUTPUT                 │
│  • Custom Rules (.rules)│   │  • alerts.json (alert events)       │
│  • Rule Parser         │   │  • dns.json (DNS events)            │
│  • Rule Validator      │   │  • http.json (HTTP events)          │
│  • Rule Reload (SIGHUP)│   │  • stats.json (statistics)          │
└────────────────────────┘   └─────────────────┬───────────────────┘
                                               │
                                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    EVE LOG WATCHER SERVICE                       │
│   Python asyncio file tail (watchdog library)                    │
│   • Monitors eve.json in real-time                               │
│   • Parses each JSON line                                        │
│   • Classifies event types                                       │
│   • Forwards to Alert Manager                                    │
└──────────────────────────────┬───────────────────────────────────┘
                               │ Parsed Alert Objects
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                     ALERT MANAGER                                │
│   • Deduplication logic                                          │
│   • Severity classification (INFO / LOW / MEDIUM / HIGH / CRIT) │
│   • Enrichment (GeoIP lookup, threat intelligence)               │
│   • Alert routing to Response Engine and Database                │
│   • WebSocket broadcast to connected clients                     │
└───────────────────────┬──────────────────────┬───────────────────┘
                        │                      │
                        ▼                      ▼
┌──────────────────────────────┐  ┌────────────────────────────────┐
│     RESPONSE ENGINE          │  │        DATABASE LAYER          │
│  • Log to file               │  │  SQLite (dev) / PostgreSQL     │
│  • Email notification        │  │  • alerts table                │
│  • Desktop push notification │  │  • events table                │
│  • Webhook (Slack/Teams)     │  │  • rules table                 │
│  • Firewall rule (iptables)  │  │  • responses table             │
│  • IP block (temporary ban)  │  │  • statistics table            │
│  • Custom script execution   │  │  • audit_log table             │
└──────────────────────────────┘  └──────────────┬─────────────────┘
                                                 │
                                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                              │
│   • REST API endpoints (CRUD for alerts, rules, settings)        │
│   • WebSocket server (real-time push to dashboard)               │
│   • Authentication (JWT)                                         │
│   • Background task scheduler (alert polling)                    │
│   • Middleware (CORS, auth, rate-limit, logging)                 │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTP REST + WebSocket
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    NEXT.JS DASHBOARD                             │
│   • Live alert feed (WebSocket)                                  │
│   • Traffic analytics charts (Recharts)                          │
│   • Rule management CRUD                                         │
│   • System status monitoring                                     │
│   • Geolocation threat map                                       │
│   • Reports and export                                           │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                        ┌──────▼──────┐
                        │   REPORTS   │
                        │  PDF/CSV    │
                        │  export     │
                        └─────────────┘
```

---

### 2.2 Module Communication Map

| From | To | Method | Data Format |
|---|---|---|---|
| Network Interface | Suricata | libpcap / AF_PACKET | Raw packets |
| Suricata | EVE Log Files | File write | JSON (NDJSON) |
| EVE Log Watcher | Alert Manager | Python function call / asyncio queue | Python dict |
| Alert Manager | Database | SQLAlchemy ORM | Python objects |
| Alert Manager | Response Engine | Event dispatch | Alert DTO |
| Alert Manager | FastAPI WebSocket | asyncio queue | JSON string |
| FastAPI WebSocket | Next.js Dashboard | WebSocket ws:// | JSON messages |
| FastAPI REST | Next.js Dashboard | HTTP/HTTPS | JSON responses |
| Response Engine | External Systems | HTTP POST / iptables / subprocess | Varies |
| Database | FastAPI | SQLAlchemy query | Python objects |
| FastAPI | Frontend | JSON over HTTP | REST API response schema |

---

### 2.3 Data Flow for a Single Alert Event

```
1. Attacker sends port scan packets → Network Interface
2. Suricata detects scan pattern via ET SCAN rules
3. Suricata writes alert to /var/log/suricata/eve.json
4. Python EVE Watcher reads new JSON line
5. Alert Manager classifies: severity=HIGH, category=SCAN
6. Alert Manager enriches: GeoIP → source country = CN
7. Database record created: alerts table, id=42
8. Response Engine fires: log_alert(), send_webhook()
9. FastAPI WebSocket broadcasts: {event: "new_alert", data: {...}}
10. Next.js receives WebSocket message → updates live feed
11. Alert rendered in dashboard with red badge
12. Analyst investigates → marks alert as reviewed
13. Audit log entry created for analyst action
```

---

## 3. TECH STACK

### 3.1 Detection Engine: **Suricata 7.x**

**Reason for Selection over Snort 3:**
- Native multi-threading (uses all CPU cores; Snort 3 still has threading limitations in practice)
- Built-in EVE JSON output format — structured JSON logs are machine-readable with zero parsing overhead
- Active development by OISF with regular CVE rule updates
- Supports AF_PACKET, DPDK, PF_RING for high-performance capture
- Integrated TLS/JA3 fingerprinting and HTTP protocol detection
- Better documentation and community support for Python integration
- Supports `suricatasc` Unix socket for live management without restart

---

### 3.2 Packet Capture: **Scapy 2.5.x + PyShark 0.6.x**

- **Scapy**: Used for traffic simulation and supplementary packet crafting in tests
- **PyShark**: Python wrapper for TShark — used for PCAP file analysis features
- **Libpcap**: Suricata uses this natively for interface capture

---

### 3.3 Backend: **Python 3.11 + FastAPI 0.110.x**

**Reason for Selection:**
- FastAPI is the fastest Python web framework (on par with NodeJS for async workloads)
- Native async/await support — critical for handling WebSocket connections and background alert polling simultaneously
- Automatic OpenAPI documentation generation (`/docs`, `/redoc`)
- Pydantic v2 for strict request/response validation with zero boilerplate
- Built-in dependency injection system
- Type-safe with Python 3.11+ type hints
- Production-tested in large-scale systems (Uber, Microsoft, Netflix use FastAPI internals)

**Key Backend Libraries:**
| Library | Version | Purpose |
|---|---|---|
| `fastapi` | 0.110.x | Web framework |
| `uvicorn` | 0.29.x | ASGI server |
| `sqlalchemy` | 2.0.x | ORM (async) |
| `alembic` | 1.13.x | Database migrations |
| `pydantic` | 2.6.x | Data validation |
| `python-jose` | 3.3.x | JWT authentication |
| `passlib` | 1.7.x | Password hashing |
| `watchdog` | 4.0.x | File system event monitoring (EVE log) |
| `aiofiles` | 23.x | Async file I/O |
| `httpx` | 0.27.x | Async HTTP client (webhooks) |
| `geoip2` | 4.x | MaxMind GeoIP2 lookups |
| `apscheduler` | 3.10.x | Background task scheduling |
| `python-multipart` | 0.0.9 | File upload support |
| `structlog` | 24.x | Structured logging |
| `pytest` | 8.x | Testing |
| `pytest-asyncio` | 0.23.x | Async test support |

---

### 3.4 Frontend: **Next.js 14.x + React 18 + TypeScript**

**Reason for Selection:**
- Next.js 14 App Router provides server components, layouts, and streaming — ideal for a dashboard app
- TypeScript gives compile-time safety across the entire frontend codebase
- Server-side rendering for initial page loads (fast first contentful paint)
- API routes for lightweight BFF (Backend for Frontend) patterns if needed

**Key Frontend Libraries:**
| Library | Version | Purpose |
|---|---|---|
| `next` | 14.x | React framework |
| `react` | 18.x | UI library |
| `typescript` | 5.x | Type safety |
| `tailwindcss` | 3.4.x | Utility-first CSS |
| `@shadcn/ui` | latest | Accessible component system |
| `recharts` | 2.x | Primary charting library |
| `lucide-react` | 0.38.x | Icon system |
| `socket.io-client` | 4.x | WebSocket client |
| `axios` | 1.x | HTTP client |
| `zustand` | 4.x | Global state management |
| `date-fns` | 3.x | Date formatting |
| `react-table` | 8.x (TanStack) | Data tables |
| `framer-motion` | 11.x | Animations |
| `react-hot-toast` | 2.x | Toast notifications |
| `next-themes` | 0.x | Dark/light mode |

---

### 3.5 Database: **SQLite (development) → PostgreSQL 16.x (production)**

**Reasoning:**
- SQLite is zero-configuration and embedded — perfect for development, demo, and internship submission
- PostgreSQL is the production target — scales to millions of alert records with proper indexing
- SQLAlchemy 2.0 async ORM abstracts the difference — switching databases requires only a connection string change
- No need for MongoDB — security event data is inherently relational (alerts → rules → responses → audit_logs)

---

### 3.6 Real-Time Communication: **WebSocket (FastAPI native)**

- FastAPI has native WebSocket support via `starlette`
- No need for Socket.IO overhead — pure WebSocket protocol is sufficient
- Frontend uses browser-native `WebSocket` API wrapped in a custom React hook

---

### 3.7 Containerization: **Docker 24.x + Docker Compose 2.x**

- Every service runs in its own container
- `docker-compose.yml` orchestrates all services with one command
- Suricata runs in privileged mode with host network access (required for packet capture)
- Production: Docker Swarm or Kubernetes manifests provided in `/deploy` directory

---

### 3.8 CI/CD: **GitHub Actions**

- Automated linting (Black, Ruff, ESLint)
- Automated testing (pytest, Jest)
- Docker image build and push to GHCR
- Semantic versioning and changelog generation

---

### 3.9 Logging: **structlog + JSON file rotation**

- Structured JSON logs (machine-parseable)
- `structlog` for Python backend logging
- Log rotation via `logging.handlers.RotatingFileHandler`
- ELK stack integration guide provided (optional advanced setup)

---

## 4. SOFTWARE ARCHITECTURE

### 4.1 Architectural Pattern: Layered + Feature-Based Hybrid

The backend follows a strict **four-layer architecture**:

```
┌─────────────────────────────────────────────┐
│           API / Transport Layer              │  ← FastAPI routes, WebSocket handlers
├─────────────────────────────────────────────┤
│              Service Layer                   │  ← Business logic, orchestration
├─────────────────────────────────────────────┤
│            Repository Layer                  │  ← Database access, query abstraction
├─────────────────────────────────────────────┤
│              Domain Layer                    │  ← Models, schemas, constants, enums
└─────────────────────────────────────────────┘
```

**Plus two cross-cutting layers:**
- **Infrastructure Layer** — Suricata management, log watching, response engine
- **Core Layer** — config, logging, security, middleware

---

### 4.2 SOLID Principles Applied

| Principle | Application |
|---|---|
| **S** — Single Responsibility | Each class/module does exactly one thing: `AlertRepository` only handles DB operations for alerts; `AlertService` only handles alert business logic |
| **O** — Open/Closed | Response handlers are plugin-style — add new response types without modifying existing code |
| **L** — Liskov Substitution | All repository classes implement abstract `BaseRepository` — swap SQLite for PostgreSQL without touching service layer |
| **I** — Interface Segregation | Separate schemas for request vs response vs internal; no fat interfaces |
| **D** — Dependency Inversion | FastAPI dependency injection (`Depends()`) provides repository instances to services; services never instantiate repositories directly |

---

### 4.3 Dependency Injection Map

```python
# FastAPI DI tree
Route Handler
  └── get_alert_service()  [Depends]
        └── AlertService(repo=get_alert_repository())
              └── AlertRepository(db=get_db())
                    └── AsyncSession (SQLAlchemy)
```

No service ever creates its own database session. Sessions are provided by the DI container, ensuring testability (mock injected in tests).

---

### 4.4 Repository Pattern

```
abstract BaseRepository[T]
  ├── create(entity: T) → T
  ├── get_by_id(id: int) → T | None
  ├── get_all(filters, pagination) → List[T]
  ├── update(id: int, data: dict) → T
  └── delete(id: int) → bool

AlertRepository(BaseRepository[Alert])
RuleRepository(BaseRepository[Rule])
EventRepository(BaseRepository[NetworkEvent])
ResponseRepository(BaseRepository[ResponseLog])
```

---

### 4.5 Service Layer Contracts

Each service exposes a typed interface:

```python
class AlertService:
    async def create_alert(self, alert_data: AlertCreate) -> AlertResponse
    async def get_alerts(self, filters: AlertFilter) -> PaginatedResponse[AlertResponse]
    async def get_alert_by_id(self, alert_id: int) -> AlertResponse
    async def acknowledge_alert(self, alert_id: int, analyst_id: int) -> AlertResponse
    async def get_alert_statistics(self) -> AlertStatistics
```

---

### 4.6 Event-Driven Internal Messaging

The Alert Manager uses an asyncio-based internal event bus:

```python
class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None
    async def publish(self, event_type: str, payload: dict) -> None
```

Alert Manager publishes `"new_alert"` events. WebSocket manager and Response Engine subscribe independently — **zero coupling** between them.

---

## 5. FOLDER STRUCTURE

```
CodeAlpha_NetworkIntrusionDetectionSystem/
│
├── 📁 backend/                          # Python FastAPI application
│   ├── 📁 api/                          # HTTP transport layer
│   │   ├── 📁 v1/                       # API version 1
│   │   │   ├── 📁 routes/               # FastAPI routers
│   │   │   │   ├── alerts.py            # /api/v1/alerts endpoints
│   │   │   │   ├── rules.py             # /api/v1/rules endpoints
│   │   │   │   ├── events.py            # /api/v1/events endpoints
│   │   │   │   ├── statistics.py        # /api/v1/statistics endpoints
│   │   │   │   ├── system.py            # /api/v1/system endpoints
│   │   │   │   ├── auth.py              # /api/v1/auth endpoints
│   │   │   │   └── reports.py           # /api/v1/reports endpoints
│   │   │   └── __init__.py
│   │   ├── 📁 websocket/                # WebSocket handlers
│   │   │   ├── manager.py               # Connection manager (broadcast logic)
│   │   │   ├── handlers.py              # WebSocket message handlers
│   │   │   └── __init__.py
│   │   └── __init__.py
│   │
│   ├── 📁 core/                         # Cross-cutting core concerns
│   │   ├── config.py                    # Pydantic Settings (env vars)
│   │   ├── security.py                  # JWT creation/verification
│   │   ├── logging.py                   # structlog configuration
│   │   ├── database.py                  # SQLAlchemy engine, session factory
│   │   ├── dependencies.py              # FastAPI Depends() factories
│   │   ├── exceptions.py                # Custom exception classes
│   │   ├── constants.py                 # System-wide constants
│   │   └── __init__.py
│   │
│   ├── 📁 middleware/                   # ASGI middleware stack
│   │   ├── auth.py                      # JWT bearer token middleware
│   │   ├── cors.py                      # CORS configuration
│   │   ├── rate_limiter.py              # Request rate limiting
│   │   ├── request_logger.py            # HTTP request/response logging
│   │   ├── error_handler.py             # Global exception handler
│   │   └── __init__.py
│   │
│   ├── 📁 models/                       # SQLAlchemy ORM models (database tables)
│   │   ├── base.py                      # Declarative base, TimestampMixin
│   │   ├── alert.py                     # Alert model
│   │   ├── event.py                     # NetworkEvent model
│   │   ├── rule.py                      # DetectionRule model
│   │   ├── response_log.py              # ResponseLog model
│   │   ├── statistics.py                # TrafficStatistics model
│   │   ├── user.py                      # User model (auth)
│   │   ├── audit_log.py                 # AuditLog model
│   │   └── __init__.py
│   │
│   ├── 📁 schemas/                      # Pydantic v2 request/response schemas
│   │   ├── alert.py                     # AlertCreate, AlertResponse, AlertFilter
│   │   ├── event.py                     # EventCreate, EventResponse
│   │   ├── rule.py                      # RuleCreate, RuleResponse, RuleUpdate
│   │   ├── statistics.py                # StatisticsResponse, DashboardStats
│   │   ├── auth.py                      # LoginRequest, TokenResponse, UserCreate
│   │   ├── common.py                    # PaginatedResponse, ErrorResponse
│   │   └── __init__.py
│   │
│   ├── 📁 repositories/                 # Data access layer
│   │   ├── base.py                      # Abstract BaseRepository[T]
│   │   ├── alert_repository.py          # AlertRepository
│   │   ├── event_repository.py          # EventRepository
│   │   ├── rule_repository.py           # RuleRepository
│   │   ├── response_repository.py       # ResponseRepository
│   │   ├── statistics_repository.py     # StatisticsRepository
│   │   ├── user_repository.py           # UserRepository
│   │   └── __init__.py
│   │
│   ├── 📁 services/                     # Business logic layer
│   │   ├── alert_service.py             # Alert lifecycle management
│   │   ├── event_service.py             # Network event management
│   │   ├── rule_service.py              # Rule CRUD and validation
│   │   ├── statistics_service.py        # Aggregation and analytics
│   │   ├── auth_service.py              # Authentication logic
│   │   ├── report_service.py            # Report generation (PDF/CSV)
│   │   └── __init__.py
│   │
│   ├── 📁 detection/                    # Detection engine integration layer
│   │   ├── suricata_manager.py          # Suricata process control (start/stop/reload)
│   │   ├── eve_log_watcher.py           # asyncio file tail for eve.json
│   │   ├── eve_parser.py                # EVE JSON event parser and type classifier
│   │   ├── alert_manager.py             # Alert enrichment, deduplication, routing
│   │   ├── rule_validator.py            # Suricata rule syntax validator
│   │   ├── geoip_enricher.py            # MaxMind GeoIP2 lookup
│   │   ├── threat_intel.py              # Threat intelligence integration
│   │   └── __init__.py
│   │
│   ├── 📁 response/                     # Automated response engine
│   │   ├── base_handler.py              # Abstract ResponseHandler
│   │   ├── log_handler.py               # Log-to-file response
│   │   ├── email_handler.py             # Email notification response
│   │   ├── webhook_handler.py           # Slack/Teams webhook response
│   │   ├── firewall_handler.py          # iptables IP block response
│   │   ├── notification_handler.py      # Desktop push notification
│   │   ├── response_engine.py           # Orchestrates all handlers
│   │   └── __init__.py
│   │
│   ├── 📁 utils/                        # Pure utility functions
│   │   ├── ip_utils.py                  # IP validation, CIDR parsing
│   │   ├── time_utils.py                # Timezone handling, formatting
│   │   ├── hash_utils.py                # Hashing helpers
│   │   ├── file_utils.py                # File I/O helpers
│   │   ├── pagination.py                # Pagination helpers
│   │   └── __init__.py
│   │
│   ├── 📁 database/                     # Database management
│   │   ├── 📁 migrations/               # Alembic migration scripts
│   │   │   ├── env.py                   # Alembic environment
│   │   │   ├── script.py.mako           # Migration template
│   │   │   └── 📁 versions/             # Individual migration files
│   │   ├── seed.py                      # Development seed data
│   │   └── __init__.py
│   │
│   ├── main.py                          # FastAPI application factory
│   ├── requirements.txt                 # Python dependencies (pinned)
│   ├── requirements-dev.txt             # Dev-only dependencies
│   ├── pyproject.toml                   # Project metadata, ruff/black config
│   └── .env.example                     # Environment variable template
│
├── 📁 frontend/                         # Next.js 14 application
│   ├── 📁 app/                          # Next.js 14 App Router
│   │   ├── 📁 (dashboard)/              # Dashboard route group
│   │   │   ├── 📁 dashboard/            # /dashboard
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 monitoring/           # /monitoring
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 alerts/               # /alerts
│   │   │   │   ├── page.tsx
│   │   │   │   └── 📁 [id]/             # /alerts/[id]
│   │   │   │       └── page.tsx
│   │   │   ├── 📁 analytics/            # /analytics
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 rules/                # /rules
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 logs/                 # /logs
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 reports/              # /reports
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 settings/             # /settings
│   │   │   │   └── page.tsx
│   │   │   ├── 📁 system/               # /system
│   │   │   │   └── page.tsx
│   │   │   └── layout.tsx               # Dashboard layout (sidebar + header)
│   │   ├── 📁 auth/                     # /auth route group
│   │   │   └── 📁 login/
│   │   │       └── page.tsx
│   │   ├── layout.tsx                   # Root layout
│   │   ├── globals.css                  # Global CSS + Tailwind directives
│   │   ├── not-found.tsx                # 404 page
│   │   └── error.tsx                    # Error boundary
│   │
│   ├── 📁 components/                   # Reusable React components
│   │   ├── 📁 ui/                       # Shadcn UI base components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── badge.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── table.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── toast.tsx
│   │   │   └── ...
│   │   ├── 📁 layout/                   # Layout components
│   │   │   ├── Sidebar.tsx              # Left navigation sidebar
│   │   │   ├── Header.tsx               # Top header bar
│   │   │   ├── Footer.tsx               # Footer (version, links)
│   │   │   └── PageWrapper.tsx          # Page container with header slot
│   │   ├── 📁 dashboard/                # Dashboard-specific widgets
│   │   │   ├── StatCard.tsx             # KPI statistic card
│   │   │   ├── AlertFeed.tsx            # Live alert stream
│   │   │   ├── ThreatMap.tsx            # Geographic threat visualization
│   │   │   ├── SeverityDonut.tsx        # Severity distribution donut chart
│   │   │   ├── TrafficTimeline.tsx      # Traffic volume area chart
│   │   │   └── TopAttackers.tsx         # Top source IPs table
│   │   ├── 📁 alerts/                   # Alert management components
│   │   │   ├── AlertTable.tsx           # Filterable alerts table
│   │   │   ├── AlertDetail.tsx          # Alert detail modal/drawer
│   │   │   ├── AlertBadge.tsx           # Severity badge component
│   │   │   ├── AlertFilters.tsx         # Search and filter controls
│   │   │   └── AlertActions.tsx         # Acknowledge/dismiss/escalate
│   │   ├── 📁 charts/                   # Chart components
│   │   │   ├── ProtocolPieChart.tsx     # Protocol distribution pie
│   │   │   ├── AlertHistogram.tsx       # Alerts per hour bar chart
│   │   │   ├── NetworkFlowChart.tsx     # Traffic flow line chart
│   │   │   └── AttackCategoryBar.tsx    # Attack categories bar chart
│   │   ├── 📁 rules/                    # Rule management components
│   │   │   ├── RuleEditor.tsx           # Monaco-style rule editor
│   │   │   ├── RuleTable.tsx            # Rules listing table
│   │   │   ├── RuleValidationBadge.tsx  # Valid/invalid indicator
│   │   │   └── RuleForm.tsx             # Create/edit rule form
│   │   ├── 📁 monitoring/               # Live monitoring components
│   │   │   ├── LiveFeed.tsx             # Real-time packet events
│   │   │   ├── ConnectionStatus.tsx     # WebSocket connection indicator
│   │   │   └── MonitoringControls.tsx   # Start/stop/pause controls
│   │   └── 📁 common/                   # Shared utility components
│   │       ├── LoadingSpinner.tsx
│   │       ├── EmptyState.tsx
│   │       ├── ErrorState.tsx
│   │       ├── ConfirmDialog.tsx
│   │       ├── DataTable.tsx
│   │       └── CopyButton.tsx
│   │
│   ├── 📁 hooks/                        # Custom React hooks
│   │   ├── useWebSocket.ts              # WebSocket connection hook
│   │   ├── useAlerts.ts                 # Alert data fetching hook
│   │   ├── useStatistics.ts             # Statistics data hook
│   │   ├── usePagination.ts             # Pagination state hook
│   │   ├── useDebounce.ts               # Input debounce hook
│   │   └── useLocalStorage.ts           # localStorage persistence hook
│   │
│   ├── 📁 stores/                       # Zustand global state stores
│   │   ├── alertStore.ts                # Alert state (live feed, count)
│   │   ├── systemStore.ts               # System status state
│   │   └── settingsStore.ts             # User settings state
│   │
│   ├── 📁 lib/                          # Library configuration
│   │   ├── api.ts                       # Axios instance with interceptors
│   │   ├── utils.ts                     # Shadcn utility (cn function)
│   │   ├── constants.ts                 # Frontend constants
│   │   └── types.ts                     # Shared TypeScript types
│   │
│   ├── 📁 types/                        # TypeScript interface definitions
│   │   ├── alert.ts                     # Alert interfaces
│   │   ├── event.ts                     # Event interfaces
│   │   ├── rule.ts                      # Rule interfaces
│   │   ├── statistics.ts                # Statistics interfaces
│   │   ├── api.ts                       # API response type wrappers
│   │   └── index.ts                     # Barrel export
│   │
│   ├── 📁 public/                       # Static assets
│   │   ├── 📁 images/
│   │   │   ├── logo.svg
│   │   │   └── banner.png
│   │   └── favicon.ico
│   │
│   ├── next.config.ts                   # Next.js configuration
│   ├── tailwind.config.ts               # Tailwind configuration
│   ├── tsconfig.json                    # TypeScript configuration
│   ├── package.json                     # NPM dependencies
│   └── .env.local.example               # Frontend env template
│
├── 📁 suricata/                         # Suricata configuration and rules
│   ├── 📁 config/
│   │   ├── suricata.yaml                # Main Suricata configuration
│   │   └── threshold.config             # Alert threshold configuration
│   ├── 📁 rules/                        # Detection rules
│   │   ├── custom.rules                 # Project-specific custom rules
│   │   ├── local.rules                  # Local environment rules
│   │   └── README.md                    # Rule writing guide
│   └── 📁 scripts/
│       ├── update_rules.sh              # Pull latest ET Open rules
│       └── test_rules.sh                # Test rules against sample PCAP
│
├── 📁 scripts/                          # Utility and automation scripts
│   ├── setup.sh                         # Development environment setup
│   ├── generate_traffic.py              # Traffic simulation for testing
│   ├── seed_db.py                       # Database seeding script
│   ├── export_alerts.py                 # Export alerts to CSV/JSON
│   └── health_check.sh                  # System health verification
│
├── 📁 docker/                           # Docker build files
│   ├── Dockerfile.backend               # Python backend image
│   ├── Dockerfile.frontend              # Next.js frontend image
│   ├── Dockerfile.suricata              # Suricata container
│   └── nginx.conf                       # Nginx reverse proxy config
│
├── 📁 deploy/                           # Deployment configurations
│   ├── docker-compose.yml               # Development compose
│   ├── docker-compose.prod.yml          # Production compose
│   └── 📁 k8s/                         # Kubernetes manifests (future)
│       ├── backend-deployment.yaml
│       ├── frontend-deployment.yaml
│       └── suricata-daemonset.yaml
│
├── 📁 tests/                            # All test files
│   ├── 📁 backend/
│   │   ├── 📁 unit/
│   │   │   ├── test_alert_service.py
│   │   │   ├── test_rule_validator.py
│   │   │   ├── test_eve_parser.py
│   │   │   └── test_geoip_enricher.py
│   │   ├── 📁 integration/
│   │   │   ├── test_alert_api.py
│   │   │   ├── test_rules_api.py
│   │   │   └── test_websocket.py
│   │   └── conftest.py                  # pytest fixtures
│   ├── 📁 frontend/
│   │   ├── test_alert_badge.test.tsx
│   │   ├── test_stat_card.test.tsx
│   │   └── setup.ts
│   └── 📁 pcap/                         # Sample PCAP files for testing
│       ├── port_scan.pcap
│       ├── ssh_bruteforce.pcap
│       └── dns_exfil.pcap
│
├── 📁 docs/                             # Documentation source
│   ├── ARCHITECTURE.md
│   ├── INSTALLATION.md
│   ├── RULE_GUIDE.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── USER_GUIDE.md
│   ├── FAQ.md
│   └── 📁 images/
│       ├── architecture.png
│       ├── dashboard-screenshot.png
│       └── alert-detail.png
│
├── 📁 assets/                           # Project assets
│   ├── banner.png                       # GitHub README banner
│   ├── social-preview.png               # GitHub social preview (1280×640)
│   └── 📁 screenshots/
│       ├── 01-dashboard.png
│       ├── 02-live-monitoring.png
│       ├── 03-alert-detail.png
│       └── 04-analytics.png
│
├── 📁 .github/                          # GitHub-specific files
│   ├── 📁 workflows/
│   │   ├── ci.yml                       # CI: lint, test, build
│   │   ├── release.yml                  # CD: create GitHub release
│   │   └── security-scan.yml            # Security: CodeQL scan
│   ├── 📁 ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── rule_suggestion.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS                       # Code ownership
│   └── dependabot.yml                   # Dependency updates
│
├── README.md                            # Project README
├── CONTRIBUTING.md                      # Contribution guidelines
├── CODE_OF_CONDUCT.md                   # Community standards
├── SECURITY.md                          # Security policy and reporting
├── CHANGELOG.md                         # Version history
├── LICENSE                              # MIT License
├── .gitignore                           # Git ignore rules
├── .editorconfig                        # Editor configuration
└── docker-compose.yml                   # Root-level convenience compose
```

---

**Folder Purpose Summary:**

| Folder | Purpose |
|---|---|
| `backend/api/` | HTTP and WebSocket transport — routes only, no business logic |
| `backend/core/` | Cross-cutting concerns shared by all layers |
| `backend/middleware/` | ASGI middleware applied to every request |
| `backend/models/` | Database table definitions (SQLAlchemy ORM) |
| `backend/schemas/` | Request/response validation (Pydantic v2) |
| `backend/repositories/` | All database queries — no logic, just data access |
| `backend/services/` | Business logic, orchestration of repositories |
| `backend/detection/` | Suricata integration, EVE log watching, alert management |
| `backend/response/` | Automated response handlers |
| `backend/utils/` | Pure functions with no side effects |
| `frontend/app/` | Next.js 14 App Router pages |
| `frontend/components/` | Reusable React component library |
| `frontend/hooks/` | Custom React hooks for state and side effects |
| `frontend/stores/` | Zustand global state management |
| `frontend/lib/` | Third-party library configuration |
| `frontend/types/` | TypeScript interface definitions |
| `suricata/` | Suricata config, rules, and helper scripts |
| `scripts/` | Development and operational automation |
| `docker/` | Dockerfile definitions |
| `deploy/` | Compose and orchestration files |
| `tests/` | All test files (unit, integration, E2E) |
| `docs/` | Extended documentation |
| `.github/` | GitHub workflow automation and templates |

---

## 6. CODING STANDARDS

### 6.1 Naming Conventions

**Python (Backend):**

| Item | Convention | Example |
|---|---|---|
| Module/file | `snake_case` | `alert_service.py` |
| Class | `PascalCase` | `AlertService`, `BaseRepository` |
| Function/method | `snake_case` | `get_alert_by_id()`, `parse_eve_event()` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_ALERT_BATCH_SIZE = 100` |
| Variable | `snake_case` | `alert_count`, `source_ip` |
| Private method | `_snake_case` | `_validate_severity()` |
| Async function | prefix with verbs | `async def fetch_alerts()` |
| Type alias | `PascalCase` | `AlertList = List[AlertResponse]` |
| Enum | `PascalCase` members `UPPER_SNAKE` | `class Severity(Enum): HIGH = "high"` |

**TypeScript (Frontend):**

| Item | Convention | Example |
|---|---|---|
| File (component) | `PascalCase.tsx` | `AlertTable.tsx` |
| File (hook) | `camelCase.ts` | `useAlerts.ts` |
| File (utility) | `camelCase.ts` | `api.ts` |
| Component | `PascalCase` | `AlertFeed`, `StatCard` |
| Interface | `PascalCase` | `AlertResponse`, `WebSocketMessage` |
| Type alias | `PascalCase` | `SeverityLevel` |
| Hook | `usePascalCase` | `useWebSocket`, `useDebounce` |
| Constant | `UPPER_SNAKE_CASE` | `WS_RECONNECT_INTERVAL = 5000` |
| Variable | `camelCase` | `alertCount`, `sourceIp` |
| CSS class | Tailwind utility only — no custom class names |

---

### 6.2 Docstrings (Python)

All Python functions, classes, and modules must have docstrings following Google style:

```python
def create_alert(self, alert_data: AlertCreate) -> AlertResponse:
    """Create a new alert record and trigger response pipeline.

    Validates alert data, persists to database, enriches with GeoIP,
    broadcasts via WebSocket, and dispatches to response engine.

    Args:
        alert_data: Validated alert creation schema containing all
            required fields from the EVE JSON alert event.

    Returns:
        AlertResponse: The created alert with generated ID and timestamps.

    Raises:
        AlertCreationError: If database write fails after 3 retries.
        ValidationError: If alert_data fails Pydantic validation.

    Example:
        >>> alert = await service.create_alert(AlertCreate(
        ...     src_ip="192.168.1.100",
        ...     severity=Severity.HIGH,
        ...     signature="ET SCAN Port Scan Detected"
        ... ))
        >>> print(alert.id)
        42
    """
```

---

### 6.3 TypeScript JSDoc

```typescript
/**
 * Custom hook for managing WebSocket connection to backend alert stream.
 *
 * Automatically reconnects on disconnect with exponential backoff.
 * Publishes received alerts to the global Zustand alert store.
 *
 * @param url - WebSocket endpoint URL (defaults to env variable)
 * @returns Connection status and last received message
 *
 * @example
 * const { isConnected, lastMessage } = useWebSocket();
 */
export function useWebSocket(url?: string): WebSocketHookReturn {
```

---

### 6.4 Error Handling

**Backend — Three-tier error strategy:**

1. **Domain Errors** — Custom exception classes (never expose internals)
```python
class AlertNotFoundError(BaseNIDSError):
    """Raised when requested alert does not exist."""
    status_code = 404
    message = "Alert not found"
```

2. **Global Exception Handler** — Catches all unhandled exceptions, returns structured JSON
```python
@app.exception_handler(BaseNIDSError)
async def nids_exception_handler(request: Request, exc: BaseNIDSError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.__class__.__name__,
            message=exc.message,
            request_id=request.state.request_id
        ).model_dump()
    )
```

3. **Repository Errors** — Database exceptions caught at repository layer, re-raised as domain errors

**Frontend — Boundary pattern:**
- Every page wrapped in `<ErrorBoundary>` component
- API calls use `try/catch` with user-friendly toast notifications
- WebSocket disconnects trigger automatic reconnection with visible status indicator

---

### 6.5 Logging Standards

Every log entry must be structured JSON:

```python
log.info(
    "alert_created",
    alert_id=alert.id,
    src_ip=alert.src_ip,
    severity=alert.severity.value,
    signature=alert.signature,
    duration_ms=elapsed
)
```

Required fields in every log: `timestamp`, `level`, `event_name`, `request_id` (where applicable).

---

### 6.6 Code Quality Tooling

**Python:**
- **Black** — code formatter (line-length=88)
- **Ruff** — fast linter (replaces flake8 + isort + pyupgrade)
- **mypy** — static type checking (strict mode)
- **bandit** — security linting

**TypeScript:**
- **ESLint** — with `next/core-web-vitals` config
- **Prettier** — code formatter
- **TypeScript strict mode** — `"strict": true` in tsconfig

---

### 6.7 Git Commit Standards

All commits follow **Conventional Commits** specification:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `perf`, `security`

**Examples:**
```
feat(detection): add EVE log watcher with asyncio file tailing
fix(api): resolve race condition in WebSocket broadcast manager
docs(rules): add custom rule writing guide with examples
security(auth): implement JWT refresh token rotation
test(alerts): add integration tests for alert creation endpoint
chore(deps): upgrade FastAPI to 0.110.0
```

---

## 7. UI/UX DESIGN SYSTEM

### 7.1 Design Philosophy

The dashboard is designed to evoke a **professional Security Operations Center** — think Splunk Enterprise, Elastic Security, or Microsoft Sentinel — but with modern aesthetics and a developer-first sensibility. Every design decision serves the primary user: a SOC analyst monitoring live network threats.

**Design Principles:**
1. **Information Density** — Show maximum useful data without clutter
2. **Scannable Hierarchy** — Critical alerts must be visually dominant
3. **Low Cognitive Load** — Consistent patterns, predictable interactions
4. **Immediate Feedback** — Every action returns visible confirmation
5. **Dark by Default** — Reduces eye strain in 24/7 operations center environments

---

### 7.2 Color Palette

```css
/* Core Brand Colors */
--color-background:       #0a0f1e;   /* Near-black navy — primary background */
--color-surface:          #0f1629;   /* Slightly lighter — card backgrounds */
--color-surface-elevated: #162040;   /* Elevated surfaces — dropdowns, tooltips */
--color-border:           #1e2d4d;   /* Subtle borders */
--color-border-active:    #2a4080;   /* Active/focused borders */

/* Text Colors */
--color-text-primary:     #e2e8f0;   /* Primary text */
--color-text-secondary:   #94a3b8;   /* Secondary/muted text */
--color-text-disabled:    #475569;   /* Disabled state text */

/* Brand Accent */
--color-accent-primary:   #00d4ff;   /* Electric cyan — primary actions, links */
--color-accent-secondary: #7c3aed;   /* Deep violet — secondary actions */
--color-accent-glow:      rgba(0, 212, 255, 0.15); /* Glow effect */

/* Severity Alert Colors */
--color-severity-info:     #60a5fa;  /* Blue */
--color-severity-low:      #34d399;  /* Green */
--color-severity-medium:   #fbbf24;  /* Amber */
--color-severity-high:     #f97316;  /* Orange */
--color-severity-critical: #ef4444;  /* Red */

/* Severity Backgrounds (15% opacity) */
--color-severity-info-bg:     rgba(96, 165, 250, 0.1);
--color-severity-low-bg:      rgba(52, 211, 153, 0.1);
--color-severity-medium-bg:   rgba(251, 191, 36, 0.1);
--color-severity-high-bg:     rgba(249, 115, 22, 0.1);
--color-severity-critical-bg: rgba(239, 68, 68, 0.1);

/* Status Colors */
--color-status-active:   #10b981;   /* Green — system active */
--color-status-warning:  #f59e0b;   /* Amber — degraded */
--color-status-error:    #ef4444;   /* Red — system error */
--color-status-offline:  #6b7280;   /* Gray — offline */

/* Chart Colors (ordered for visual distinction) */
--chart-1: #00d4ff;
--chart-2: #7c3aed;
--chart-3: #f97316;
--chart-4: #34d399;
--chart-5: #fbbf24;
--chart-6: #a78bfa;
```

---

### 7.3 Typography

```css
/* Font Stack */
--font-mono: "JetBrains Mono", "Fira Code", "Consolas", monospace;
--font-sans: "Inter", "SF Pro Display", "Segoe UI", sans-serif;

/* Scale */
--text-xs:   0.75rem;    /* 12px — timestamps, secondary labels */
--text-sm:   0.875rem;   /* 14px — body text, table cells */
--text-base: 1rem;       /* 16px — primary body */
--text-lg:   1.125rem;   /* 18px — section labels */
--text-xl:   1.25rem;    /* 20px — card titles */
--text-2xl:  1.5rem;     /* 24px — page titles */
--text-3xl:  1.875rem;   /* 30px — KPI numbers */
--text-4xl:  2.25rem;    /* 36px — hero numbers */

/* IP addresses, signatures, rule IDs use monospace */
.font-mono { font-family: var(--font-mono); }
```

---

### 7.4 Glassmorphism Design Language

Cards use frosted glass effect:

```css
.glass-card {
  background: rgba(15, 22, 41, 0.8);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(30, 45, 77, 0.6);
  border-radius: 12px;
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Cyan glow variant for critical elements */
.glass-card-accent {
  box-shadow:
    0 4px 24px rgba(0, 0, 0, 0.4),
    0 0 20px rgba(0, 212, 255, 0.08),
    inset 0 1px 0 rgba(0, 212, 255, 0.1);
  border-color: rgba(0, 212, 255, 0.2);
}
```

---

### 7.5 Sidebar Navigation

**Structure:**
```
┌─────────────────────────────┐
│ 🔷 NIDS-PRO           v1.0  │
├─────────────────────────────┤
│ ● LIVE                      │  ← animated dot for connection status
├─────────────────────────────┤
│                             │
│ 🏠 Dashboard                │
│ 📡 Live Monitoring      ●   │  ← alert badge when active
│ 🚨 Alert Center        12   │  ← unread count badge
│ 📊 Analytics                │
│ 📋 Logs                     │
│                             │
├── CONFIGURATION ────────────┤
│ 📜 Rules                    │
│ ⚙️  Settings                │
│ 🖥️  System Status           │
│                             │
├── INTELLIGENCE ─────────────┤
│ 📈 Reports                  │
│ 🗺️  Threat Map              │
│                             │
├── HELP ─────────────────────┤
│ 📚 Documentation            │
│ ℹ️  About                    │
│                             │
└─────────────────────────────┘
```

**Sidebar specs:**
- Width: 240px (collapsed: 60px icon-only mode)
- Active state: left border `3px solid var(--color-accent-primary)`, background `var(--color-surface-elevated)`
- Hover state: background `rgba(0, 212, 255, 0.05)`, transition 150ms
- Icon + label layout at 16px gap
- Collapse toggle button at bottom

---

### 7.6 Header

```
┌──────────────────────────────────────────────────────────────────────┐
│  [≡ Menu]   Page Title         [Search]  [🔔 3] [❓] [⚙] [Avatar] │
└──────────────────────────────────────────────────────────────────────┘
```

- Height: 64px
- Breadcrumb below title for nested pages
- Search: `⌘K` shortcut → command palette (future feature)
- Notification bell: shows unread alert count
- Avatar: opens user settings dropdown

---

### 7.7 Component Specifications

**StatCard (KPI Widget):**
```
┌──────────────────────────────┐
│ 🚨 Total Alerts              │
│                              │
│     1,247                    │  ← --text-4xl, --color-accent-primary
│                              │
│  ↑ +23% from yesterday       │  ← trend indicator (green=good, red=bad)
└──────────────────────────────┘
```

**Alert Badge Variants:**
```
[INFO]     → blue background, blue text
[LOW]      → green background, green text
[MEDIUM]   → amber background, amber text
[HIGH]     → orange background, orange text
[CRITICAL] → red background, red text, pulse animation
```

**Table Rows:**
- Row height: 52px
- Hover: `background: var(--color-surface-elevated)`
- Selected: left border 2px cyan, background slightly brighter
- Zebra striping: none (too visually noisy on dark backgrounds)

**Buttons:**
```
Primary:    bg-cyan-500 text-black font-semibold hover:bg-cyan-400
Secondary:  border border-slate-600 text-slate-300 hover:border-slate-400
Danger:     bg-red-500/10 text-red-400 border border-red-500/30
Ghost:      text-slate-400 hover:text-white hover:bg-white/5
```

---

### 7.8 Animations

- Page transitions: `framer-motion` fade + slide in 200ms
- Alert appear: slide-in-from-top with fade, 300ms
- Critical alert: `@keyframes pulse-red` border glow animation
- Chart data: `recharts` built-in animation, 800ms ease-out
- Skeleton loading: shimmer animation on gray placeholder blocks
- WebSocket connected indicator: slow pulse green dot
- Sidebar collapse: smooth width transition 250ms cubic-bezier

---

### 7.9 Responsive Design

| Breakpoint | Behavior |
|---|---|
| `< 768px` (mobile) | Sidebar hidden (hamburger menu), single column layout |
| `768–1024px` (tablet) | Sidebar collapsed (icons only), 2-column grid |
| `> 1024px` (desktop) | Full sidebar, multi-column layout |
| `> 1280px` (large) | Wider charts, more data density |

Dashboard designed primarily for **1920×1080** SOC monitors. Mobile is supported but not the primary use case.

---

### 7.10 Accessibility

- All interactive elements have `focus-visible` ring (cyan, 2px offset)
- Color is never the sole indicator (icons + text accompany color)
- ARIA labels on all icon-only buttons
- Alert severity badges have `role="status"` and `aria-label`
- Keyboard navigation for entire dashboard (Tab, Enter, Escape)
- Screen reader tested with NVDA/VoiceOver on key flows
- Minimum contrast ratio: 4.5:1 for normal text, 3:1 for large text

---

## 8. DASHBOARD PAGES

### 8.1 Dashboard (Home) — `/dashboard`

**Purpose:** Executive overview of current network security posture. The first page analysts see when opening the platform.

**Layout:** 4-column grid on desktop

**Widgets (top row — KPI cards):**
1. **Total Alerts Today** — number + trend vs yesterday
2. **Critical/High Alerts** — count + percentage of total
3. **Active Rules** — count of enabled detection rules
4. **Packets Analyzed** — total since last system restart

**Widgets (middle row):**
5. **Live Alert Feed** — scrolling list of last 20 alerts, auto-updating via WebSocket, shows severity badge + source IP + signature name + timestamp
6. **Severity Distribution** — Donut chart showing breakdown: INFO/LOW/MEDIUM/HIGH/CRITICAL
7. **Top Attack Categories** — Horizontal bar chart: SCAN, EXPLOIT, MALWARE, DOS, POLICY, etc.

**Widgets (bottom row):**
8. **Traffic Volume Timeline** — Area chart: packets/alerts over last 24 hours (hourly buckets)
9. **Top Source IPs** — Table: IP | Country | Alert Count | Last Seen | Status (blocked/unblocked)
10. **System Status Mini** — 3 health indicators: Suricata status, Database, WebSocket

**Actions:**
- Click any alert in feed → opens Alert Detail drawer
- Click IP in top attackers → pre-filtered alerts view for that IP
- "View All Alerts" button → navigates to Alert Center

---

### 8.2 Live Monitoring — `/monitoring`

**Purpose:** Real-time packet event stream for active network surveillance.

**Layout:** Single-column primary with sidebar controls

**Widgets:**
1. **WebSocket Status Banner** — shows connection state: `● CONNECTED — ws://localhost:8000/ws/events` or reconnecting spinner
2. **Event Stream** — auto-scrolling log-style feed of raw events:
   - Format: `[HH:MM:SS.mmm] [SEVERITY] [PROTOCOL] SRC_IP:PORT → DST_IP:PORT — signature_name`
   - Color-coded by severity
   - New events fly in from top with slide animation
3. **Filters Panel** — checkboxes for event types (alerts/dns/http/tls/flow), severity filter, protocol filter
4. **Event Counter** — events/second gauge, total events displayed
5. **Pause/Resume Toggle** — stops auto-scroll without disconnecting

**Controls:**
- **Start Monitoring** button — triggers Suricata process start (if stopped)
- **Stop Monitoring** button — graceful Suricata stop
- **Clear Feed** button — clears displayed events (does not delete DB records)
- **Export Current View** — downloads visible events as JSON/CSV

---

### 8.3 Alert Center — `/alerts`

**Purpose:** Complete alert management — browse, filter, investigate, and respond to all detected threats.

**Layout:** Full-width data table with filter panel

**Filter Panel (left column, collapsible):**
- Date range picker (today/last 7d/last 30d/custom)
- Severity multi-select (INFO/LOW/MEDIUM/HIGH/CRITICAL)
- Status filter (new/acknowledged/resolved/false-positive)
- Category filter (scan/exploit/malware/dos/policy)
- Source IP search
- Destination IP search
- Signature keyword search

**Alert Table Columns:**
| # | Severity | Signature | Src IP | Src Country | Dst IP | Protocol | Timestamp | Status | Actions |
|---|---|---|---|---|---|---|---|---|---|

**Bulk Actions:**
- Select multiple → Acknowledge All
- Select multiple → Mark as False Positive
- Select multiple → Export Selected

**Alert Detail View (drawer/modal):**
When clicking an alert row, a right-side drawer opens with:
- Full alert metadata (all EVE JSON fields)
- Raw packet payload (hex + ASCII view)
- GeoIP information with mini-map
- Response history (what automated actions fired)
- Manual actions: Acknowledge, Escalate, Block IP, Add Note
- Related alerts (same source IP, same signature within 1 hour)
- Snort-compatible rule that triggered this alert

---

### 8.4 Traffic Analytics — `/analytics`

**Purpose:** Visual analysis of network traffic patterns, attack trends, and threat statistics.

**Widgets:**
1. **Alerts Over Time** — Line/area chart with time selector (1h/6h/24h/7d/30d), multiple series (by severity)
2. **Protocol Distribution** — Pie chart: TCP/UDP/ICMP/HTTP/DNS/TLS breakdown
3. **Attack Category Timeline** — Stacked bar chart per day: scan vs exploit vs malware vs dos
4. **Top 10 Source Countries** — Horizontal bar chart with flag emojis
5. **Top 10 Attacked Ports** — Bar chart of most targeted destination ports
6. **Detection Rule Effectiveness** — Table: Rule Name | Triggers | False Positive Rate | Last 7d trend
7. **Hourly Heatmap** — Grid of hours (0-23) × days (Mon-Sun), colored by alert intensity

**Filters:**
- Global time range selector at top affects all charts
- Category filter
- Export each chart as PNG button (recharts built-in)

---

### 8.5 Logs — `/logs`

**Purpose:** Raw access to all log files for debugging and forensic analysis.

**Log Types (tabs):**
1. **Detection Logs** — Suricata EVE JSON stream
2. **Application Logs** — FastAPI backend logs
3. **Audit Logs** — User actions (who acknowledged what, when)
4. **System Logs** — Suricata startup/shutdown, rule reload events
5. **Response Logs** — Automated response action history

**Per tab:**
- Search/filter input (real-time filtering)
- Log level filter (DEBUG/INFO/WARNING/ERROR)
- Auto-scroll toggle
- Download as .log file button
- Copy selected lines button

---

### 8.6 Rules — `/rules`

**Purpose:** Manage Suricata detection rules — view, create, edit, enable/disable, and test.

**Widgets:**
1. **Rule Statistics** — Total rules | Active | Inactive | Custom | Official
2. **Rule Table** — Columns: SID | Action | Protocol | Name | Category | Enabled | Last Trigger | Actions
3. **Rule Editor** — Monaco-style editor with Suricata rule syntax highlighting
4. **Rule Validator** — Inline validation with error highlighting

**Rule Table Actions:**
- Toggle enable/disable (immediate SIGHUP to Suricata)
- Edit rule → opens editor
- Delete rule (with confirmation)
- Test rule against sample PCAP

**Create Rule Flow:**
1. Click "+ New Rule" → opens full-screen editor
2. Type rule with syntax highlighting
3. Real-time validation shows errors inline
4. "Validate Rule" → POST to `/api/v1/rules/validate`
5. "Save & Activate" → writes rule file, sends SIGHUP

**Rule Categories shown as filter tabs:**
`SCAN | EXPLOIT | MALWARE | DOS | POLICY | PROTOCOL | CUSTOM`

---

### 8.7 System Status — `/system`

**Purpose:** Monitor health of all system components.

**Widgets:**
1. **Component Status Grid:**
   - Suricata Engine: `● RUNNING` / `⚠ STOPPED` / `✗ ERROR`
   - Database: `● CONNECTED` / `✗ DISCONNECTED`
   - EVE Log Watcher: `● ACTIVE` / `✗ INACTIVE`
   - WebSocket Server: `● ONLINE (N clients)` / `✗ OFFLINE`
   - Response Engine: `● READY` / `⚠ DEGRADED`

2. **Suricata Statistics** (from stats.json EVE events):
   - Packets Received, Decoded, Dropped
   - Alerts Generated
   - Active Flows
   - Memory Usage

3. **System Resource Monitor:**
   - CPU Usage % (sparkline chart)
   - Memory Usage % (sparkline chart)
   - Disk Usage for log directory

4. **Suricata Controls:**
   - "Reload Rules" button (SIGHUP)
   - "Restart Suricata" button
   - "View Suricata Config" link

---

### 8.8 Reports — `/reports`

**Purpose:** Generate and export security reports.

**Report Types:**
1. **Daily Summary** — Today's alert counts, top attackers, top attack types
2. **Weekly Trend Report** — 7-day trend analysis with charts
3. **Monthly Executive Report** — High-level security posture summary
4. **Custom Report** — User-defined date range and metrics

**For Each Report:**
- Preview in-browser (HTML)
- Download as PDF
- Download as CSV (data tables only)
- Schedule (daily/weekly email delivery) — future feature

---

### 8.9 Settings — `/settings`

**Purpose:** Configure system behavior, notifications, and integrations.

**Setting Sections (tabs):**

1. **General** — System name, timezone, log retention period, theme (dark/light)
2. **Notifications** — Enable/disable email notifications, webhook URL (Slack/Teams), notification thresholds (alert severity to trigger notification)
3. **Response Rules** — Which severity levels trigger which automated responses
4. **Network** — Monitored interface selection, capture filter (BPF expression), PCAP storage settings
5. **Authentication** — Change password, API key management
6. **Database** — Database location, backup schedule, data export

---

### 8.10 About — `/about`

**Purpose:** Project information and attribution.

**Content:**
- Project name, version, build date
- Technology stack credits
- GitHub repository link
- Author information (harisx404)
- License information (MIT)
- Acknowledgements (Suricata, ET Open Rules, Shadcn, etc.)
## 9. FEATURES

### 9.1 Mandatory Features (Internship Requirements)

| Feature | Implementation | Status |
|---|---|---|
| Configure Suricata | `suricata/config/suricata.yaml` + `SuricataManager` class | ✅ Required |
| Detect Suspicious Traffic | Suricata engine with ET Open rules + custom rules | ✅ Required |
| Custom Detection Rules | Rule editor in dashboard + `.rules` file management | ✅ Required |
| Alert Generation | EVE JSON parsing → Alert Manager → Database + WebSocket | ✅ Required |
| Continuous Monitoring | EVE log watcher with asyncio + WebSocket live feed | ✅ Required |
| Response Mechanisms | 6 response handler types (log/email/webhook/firewall/block/notify) | ✅ Required |

---

### 9.2 Advanced Features (Exceeds Requirements)

1. **Real-Time WebSocket Dashboard** — Sub-second alert delivery to all connected clients
2. **GeoIP Enrichment** — MaxMind GeoLite2 lookup on every alert's source IP → country, city, org
3. **Alert Deduplication** — Suppresses repeated identical alerts within configurable time window
4. **Severity Classification Engine** — Maps Suricata priority 1–3 to 5-tier severity scale with custom overrides
5. **Rule Syntax Validation** — Server-side Suricata rule validation before saving
6. **Interactive Traffic Charts** — 7 distinct chart types covering all traffic dimensions
7. **Bulk Alert Operations** — Acknowledge/resolve/export multiple alerts simultaneously
8. **Alert Search & Filter** — Multi-dimensional filtering with URL-based state (shareable filter links)
9. **Audit Log** — Every user action recorded (who did what, when)
10. **JWT Authentication** — Secure login, refresh tokens, role-based access (admin/analyst/viewer)
11. **API Rate Limiting** — 100 requests/minute per IP, with 429 responses
12. **Docker Compose Deployment** — One-command start of entire stack
13. **GitHub Actions CI** — Automated linting, testing, and Docker build on every push
14. **OpenAPI Documentation** — Interactive `/docs` endpoint with all API endpoints documented
15. **Dark Mode Dashboard** — Professional SOC aesthetic with glassmorphism

---

### 9.3 Future Scope Features (Roadmap Items)

1. **Machine Learning Anomaly Detection** — Baseline normal traffic, flag statistical deviations
2. **PCAP Replay Analysis** — Upload `.pcap` file, replay through Suricata, analyze results
3. **Threat Intelligence Integration** — AbuseIPDB, VirusTotal, Shodan API enrichment
4. **YARA Rule Integration** — File extraction + YARA scanning for malware detection
5. **Multi-Interface Support** — Monitor multiple network interfaces simultaneously
6. **Network Topology Map** — Visual map of detected hosts and their connections
7. **Email Report Scheduler** — Automated daily/weekly reports via email
8. **Slack/Teams Bot** — Two-way integration (alerts to Slack, commands from Slack)
9. **SIEM Integration** — Splunk/Elastic forward via Syslog
10. **CVE Correlation** — Map alerts to CVE database for vulnerability context
11. **Zeek Integration** — Add Zeek network analysis framework alongside Suricata
12. **Container Security** — Monitor Docker container network traffic

---

### 9.4 Stretch Goals

1. **SaaS Multi-Tenancy** — Multiple organizations, isolated data
2. **Mobile App** — React Native companion for on-call alerts
3. **AI Alert Triage** — LLM-powered alert investigation assistant
4. **Honeytoken Detection** — Detect access to embedded decoy credentials/files

---

## 10. ALERT SYSTEM

### 10.1 Severity Model

The NIDS uses a **5-tier severity model** mapped from Suricata priorities:

| Level | Name | Suricata Priority | Visual | Use Case |
|---|---|---|---|---|
| 0 | **INFO** | 4 | 🔵 Blue | Informational events, policy violations |
| 1 | **LOW** | 3 | 🟢 Green | Reconnaissance, low-confidence indicators |
| 2 | **MEDIUM** | 2 | 🟡 Amber | Suspicious activity, known bad patterns |
| 3 | **HIGH** | 1 | 🟠 Orange | Active exploitation attempts, malware indicators |
| 4 | **CRITICAL** | 0 (custom) | 🔴 Red + pulse | Active breach indicators, critical infrastructure attacks |

**Severity mapping in `AlertManager`:**
```python
SURICATA_TO_SEVERITY = {
    1: Severity.HIGH,
    2: Severity.MEDIUM,
    3: Severity.LOW,
    4: Severity.INFO,
}

# Custom override for specific rule categories
CATEGORY_SEVERITY_OVERRIDE = {
    "ET POLICY": Severity.INFO,
    "ET SCAN": Severity.MEDIUM,
    "ET EXPLOIT": Severity.HIGH,
    "ET MALWARE": Severity.HIGH,
    "ET TROJAN": Severity.CRITICAL,
    "ET DOS": Severity.HIGH,
    "ET CURRENT_EVENTS": Severity.CRITICAL,
}
```

---

### 10.2 Alert Lifecycle

```
NEW → ACKNOWLEDGED → (RESOLVED | FALSE_POSITIVE)
 │
 └──→ ESCALATED → ACKNOWLEDGED → RESOLVED
```

**State Definitions:**
- **NEW**: Alert just created, requires analyst attention
- **ACKNOWLEDGED**: Analyst has seen it, investigation started
- **ESCALATED**: Sent to senior analyst / incident response team
- **RESOLVED**: Confirmed threat, remediation complete
- **FALSE_POSITIVE**: Analyst confirmed benign activity, rule may need tuning

---

### 10.3 Alert Data Model

Every alert contains:

```json
{
  "id": 1247,
  "timestamp": "2024-01-15T14:23:11.456789Z",
  "severity": "HIGH",
  "status": "NEW",
  "category": "EXPLOIT",
  "signature_id": 2030450,
  "signature": "ET EXPLOIT Possible CVE-2021-44228 Log4j RCE Inbound",
  "src_ip": "45.33.32.156",
  "src_port": 49152,
  "dst_ip": "192.168.1.50",
  "dst_port": 8080,
  "protocol": "TCP",
  "flow_id": "1847291847382",
  "geo": {
    "country": "United States",
    "city": "Fremont",
    "latitude": 37.5485,
    "longitude": -121.9886,
    "org": "AS63949 Linode LLC",
    "isp": "Linode"
  },
  "raw_eve": { ... },
  "acknowledged_by": null,
  "acknowledged_at": null,
  "notes": "",
  "created_at": "2024-01-15T14:23:11.456789Z",
  "updated_at": "2024-01-15T14:23:11.456789Z"
}
```

---

### 10.4 Alert Flow — Step by Step

```
1. Suricata writes alert to eve.json
2. EVE Log Watcher reads new line
3. EVE Parser extracts: src_ip, dst_ip, src_port, dst_port, signature, priority, category, flow_id
4. Deduplication check: hash(src_ip + dst_ip + signature_id) → if seen within 60s, drop
5. Severity Classification: map priority → severity, apply category override
6. GeoIP Enrichment: MaxMind lookup on src_ip
7. Create AlertCreate schema object
8. AlertRepository.create() → persist to database
9. EventBus.publish("new_alert", alert_dict)
10. WebSocketManager receives event → broadcast to all connected clients
11. ResponseEngine receives event → execute configured responses
12. Audit log entry: "alert_created"
```

---

### 10.5 Notification Delivery

**WebSocket (Real-time in Dashboard):**
```json
{
  "event": "new_alert",
  "data": {
    "id": 1247,
    "severity": "CRITICAL",
    "signature": "ET TROJAN Zeus Bot Activity",
    "src_ip": "45.33.32.156",
    "timestamp": "2024-01-15T14:23:11Z"
  }
}
```

**Toast Notification (In Dashboard):**
- CRITICAL/HIGH → red toast, persistent (must be dismissed)
- MEDIUM → amber toast, auto-dismiss after 10 seconds
- LOW/INFO → blue/green toast, auto-dismiss after 5 seconds

**Browser Notification (Push):**
- Requests `Notification.requestPermission()` on first visit
- On CRITICAL alert: `new Notification("⚠ CRITICAL Alert", { body: "Zeus Bot Activity from 45.33.32.156" })`

---

## 11. RESPONSE MECHANISM

### 11.1 Architecture

The Response Engine follows a **chain-of-responsibility** pattern. Each handler is independently registered and executed. Failure of one handler does not block others.

```python
class ResponseEngine:
    def __init__(self, handlers: List[BaseResponseHandler]):
        self.handlers = handlers

    async def execute(self, alert: AlertResponse) -> List[ResponseResult]:
        results = []
        for handler in self.handlers:
            if handler.should_handle(alert):
                result = await handler.handle(alert)
                results.append(result)
        return results
```

---

### 11.2 Response Handlers

**Handler 1 — LogHandler**
- Triggered: All alerts
- Action: Append alert to `logs/responses/response_{date}.log` in structured JSON format
- Config: `LOG_RESPONSES=true`

**Handler 2 — EmailHandler**
- Triggered: Alerts with severity HIGH or CRITICAL
- Action: Sends email via SMTP with alert details formatted in HTML template
- Config: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `ALERT_EMAIL_TO`
- Template: HTML email with alert details, severity badge, GeoIP data, direct link to dashboard alert

**Handler 3 — WebhookHandler**
- Triggered: Alerts with severity MEDIUM or above
- Action: HTTP POST to configured webhook URL (Slack/Teams/Discord/custom)
- Payload: Formatted JSON message with alert data
- Slack payload example:
```json
{
  "text": "🚨 *HIGH Alert Detected*",
  "attachments": [{
    "color": "#f97316",
    "fields": [
      {"title": "Signature", "value": "ET SCAN Port Scan", "short": false},
      {"title": "Source IP", "value": "45.33.32.156 (US)", "short": true},
      {"title": "Destination", "value": "192.168.1.1:22", "short": true}
    ]
  }]
}
```
- Config: `WEBHOOK_URL`, `WEBHOOK_MIN_SEVERITY`
- Retry: 3 attempts with exponential backoff

**Handler 4 — FirewallHandler**
- Triggered: Alerts with severity CRITICAL, or source IP in blocklist
- Action: Executes `iptables -A INPUT -s {src_ip} -j DROP` via subprocess
- Requires: Run with appropriate privileges (or via sudo wrapper script)
- Safety: Whitelist check before blocking (never block private RFC1918 IPs)
- Config: `ENABLE_FIREWALL_RESPONSE=true`, `FIREWALL_WHITELIST`

```python
FIREWALL_WHITELIST = [
    "127.0.0.1",
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
]
```

**Handler 5 — IPBlockHandler**
- Triggered: Source IP generates 5+ HIGH alerts within 5 minutes
- Action: Adds IP to `blocked_ips` database table with configurable TTL (default: 24 hours)
- Effect: Firewall rule added, IP flagged in dashboard with 🚫 indicator
- Auto-expiry: Scheduler removes expired blocks every 15 minutes

**Handler 6 — NotificationHandler**
- Triggered: Alerts with severity HIGH or CRITICAL
- Action: `POST /api/v1/notifications` → pushes to WebSocket clients → browser `Notification` API
- Non-blocking async

---

### 11.3 Response Configuration

Response behavior is fully configurable via Settings UI and `.env`:

```env
# Response Engine Config
ENABLE_LOG_RESPONSE=true
ENABLE_EMAIL_RESPONSE=false
ENABLE_WEBHOOK_RESPONSE=true
ENABLE_FIREWALL_RESPONSE=false
ENABLE_IP_BLOCK_RESPONSE=false

# Thresholds
EMAIL_MIN_SEVERITY=HIGH
WEBHOOK_MIN_SEVERITY=MEDIUM
FIREWALL_MIN_SEVERITY=CRITICAL
IP_BLOCK_THRESHOLD_COUNT=5
IP_BLOCK_THRESHOLD_MINUTES=5
IP_BLOCK_DURATION_HOURS=24
```

---

### 11.4 Response Log Schema

Every response action creates an audit entry:

```json
{
  "id": 89,
  "alert_id": 1247,
  "handler": "WebhookHandler",
  "action": "slack_notification_sent",
  "status": "SUCCESS",
  "details": {"webhook_url": "https://hooks.slack.com/...", "http_status": 200},
  "executed_at": "2024-01-15T14:23:11.892Z"
}
```

---

## 12. DATABASE DESIGN

### 12.1 Entity Relationship Diagram (Text)

```
┌───────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    users      │     │     alerts      │     │  response_logs  │
│───────────────│     │─────────────────│     │─────────────────│
│ id (PK)       │─┐   │ id (PK)         │──┐  │ id (PK)         │
│ username      │ │   │ timestamp       │  │  │ alert_id (FK)───┘
│ email         │ │   │ severity        │  └──│ handler         │
│ password_hash │ │   │ status          │     │ action          │
│ role          │ │   │ category        │     │ status          │
│ is_active     │ │   │ signature_id    │     │ details (JSON)  │
│ created_at    │ │   │ signature       │     │ executed_at     │
│ last_login    │ └───│ acknowledged_by │     └─────────────────┘
└───────────────┘     │ (FK→users.id)   │
                      │ src_ip          │     ┌─────────────────┐
                      │ src_port        │     │ detection_rules │
                      │ dst_ip          │     │─────────────────│
                      │ dst_port        │     │ id (PK)         │
                      │ protocol        │     │ sid (UNIQUE)    │
                      │ flow_id         │     │ action          │
                      │ geo_country     │     │ protocol        │
                      │ geo_city        │     │ name            │
                      │ geo_lat         │     │ category        │
                      │ geo_lon         │     │ content         │
                      │ geo_org         │     │ is_enabled      │
                      │ raw_eve (JSON)  │     │ is_custom       │
                      │ notes           │     │ trigger_count   │
                      │ acknowledged_at │     │ last_triggered  │
                      │ created_at      │     │ created_by (FK) │
                      │ updated_at      │     │ created_at      │
                      └─────────────────┘     │ updated_at      │
                                              └─────────────────┘
┌─────────────────────┐     ┌──────────────────────┐
│  network_events     │     │   traffic_statistics  │
│─────────────────────│     │──────────────────────│
│ id (PK)             │     │ id (PK)               │
│ event_type          │     │ bucket_start          │
│ timestamp           │     │ bucket_end            │
│ src_ip              │     │ packets_received      │
│ src_port            │     │ packets_dropped       │
│ dst_ip              │     │ alerts_total          │
│ dst_port            │     │ alerts_by_severity    │
│ protocol            │     │  (JSON)               │
│ flow_id             │     │ alerts_by_category    │
│ http_hostname       │     │  (JSON)               │
│ http_url            │     │ top_src_ips (JSON)    │
│ http_method         │     │ protocol_dist (JSON)  │
│ dns_query           │     │ created_at            │
│ dns_type            │     └──────────────────────┘
│ tls_sni             │
│ tls_version         │     ┌──────────────────────┐
│ raw_eve (JSON)      │     │    blocked_ips        │
│ created_at          │     │──────────────────────│
└─────────────────────┘     │ id (PK)               │
                            │ ip_address (UNIQUE)   │
┌─────────────────────┐     │ reason                │
│    audit_logs       │     │ alert_count           │
│─────────────────────│     │ blocked_at            │
│ id (PK)             │     │ expires_at            │
│ user_id (FK)        │     │ is_permanent          │
│ action              │     │ created_by (FK)       │
│ resource_type       │     └──────────────────────┘
│ resource_id         │
│ old_value (JSON)    │
│ new_value (JSON)    │
│ ip_address          │
│ user_agent          │
│ created_at          │
└─────────────────────┘
```

---

### 12.2 Table Definitions

**`alerts` table — Primary alert records:**

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK, AUTO_INCREMENT | Unique alert identifier |
| `timestamp` | DATETIME(6) | NOT NULL, INDEX | Alert detection time (microsecond precision) |
| `severity` | VARCHAR(10) | NOT NULL, INDEX | INFO/LOW/MEDIUM/HIGH/CRITICAL |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'NEW' | Alert lifecycle status |
| `category` | VARCHAR(50) | INDEX | Attack category from Suricata |
| `signature_id` | INTEGER | INDEX | Suricata rule SID |
| `signature` | VARCHAR(512) | NOT NULL | Human-readable rule name |
| `src_ip` | VARCHAR(45) | NOT NULL, INDEX | Source IP (IPv4 or IPv6) |
| `src_port` | SMALLINT | NULLABLE | Source port |
| `dst_ip` | VARCHAR(45) | NOT NULL | Destination IP |
| `dst_port` | SMALLINT | NULLABLE, INDEX | Destination port |
| `protocol` | VARCHAR(10) | INDEX | Network protocol |
| `flow_id` | VARCHAR(32) | INDEX | Suricata flow correlation ID |
| `geo_country` | VARCHAR(100) | NULLABLE | Source IP country |
| `geo_city` | VARCHAR(100) | NULLABLE | Source IP city |
| `geo_lat` | FLOAT | NULLABLE | Latitude |
| `geo_lon` | FLOAT | NULLABLE | Longitude |
| `geo_org` | VARCHAR(255) | NULLABLE | ASN organization |
| `raw_eve` | JSON | NULLABLE | Full raw Suricata EVE event |
| `notes` | TEXT | DEFAULT '' | Analyst investigation notes |
| `acknowledged_by` | INTEGER | FK → users.id | Who acknowledged |
| `acknowledged_at` | DATETIME | NULLABLE | When acknowledged |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Record creation |
| `updated_at` | DATETIME | NOT NULL, DEFAULT NOW | Last modification |

**Indexes on `alerts`:**
- `idx_alerts_timestamp` — for time-range queries
- `idx_alerts_severity` — for severity filtering
- `idx_alerts_src_ip` — for IP-based queries
- `idx_alerts_status` — for status filtering
- `idx_alerts_category` — for category analytics
- Composite: `idx_alerts_timestamp_severity` — for dashboard KPI queries

---

**`detection_rules` table:**

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PK | Internal rule ID |
| `sid` | INTEGER | UNIQUE, NOT NULL | Suricata rule SID (1000001+ for custom) |
| `action` | VARCHAR(10) | NOT NULL | alert/drop/pass/reject |
| `protocol` | VARCHAR(10) | NOT NULL | tcp/udp/icmp/http/dns/tls/any |
| `name` | VARCHAR(512) | NOT NULL | Rule signature message |
| `category` | VARCHAR(50) | NOT NULL | Rule category classification |
| `content` | TEXT | NOT NULL | Full Suricata rule text |
| `is_enabled` | BOOLEAN | DEFAULT TRUE | Whether rule is active |
| `is_custom` | BOOLEAN | DEFAULT FALSE | Custom vs official ET rule |
| `trigger_count` | INTEGER | DEFAULT 0 | Total times rule has fired |
| `last_triggered` | DATETIME | NULLABLE | Last time rule fired an alert |
| `created_by` | INTEGER | FK → users.id | Who created (NULL for official rules) |
| `created_at` | DATETIME | NOT NULL | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL | Last modification |

---

### 12.3 Migrations Strategy

- **Alembic** manages all schema changes
- Every schema change = one migration file (never modify existing migrations)
- Migration naming: `{revision}_{description}.py` e.g., `001_create_alerts_table.py`
- Test migrations both up and down before committing
- Production: Run `alembic upgrade head` on container startup

---

## 13. API DESIGN

### 13.1 Base URL and Versioning

```
Base: http://localhost:8000
API: http://localhost:8000/api/v1
WebSocket: ws://localhost:8000/ws/events
Documentation: http://localhost:8000/docs
```

All API responses follow a consistent envelope:

```json
{
  "success": true,
  "data": { ... },
  "message": "Alerts retrieved successfully",
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 1247,
    "total_pages": 63
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": "AlertNotFoundError",
  "message": "Alert with ID 999 not found",
  "detail": null,
  "request_id": "req_abc123"
}
```

---

### 13.2 Authentication Endpoints

```
POST /api/v1/auth/login
  Body: { "username": "admin", "password": "secure123" }
  Response: { "access_token": "...", "refresh_token": "...", "token_type": "bearer", "expires_in": 3600 }

POST /api/v1/auth/refresh
  Body: { "refresh_token": "..." }
  Response: { "access_token": "...", "expires_in": 3600 }

POST /api/v1/auth/logout
  Headers: Authorization: Bearer {token}
  Response: { "message": "Logged out successfully" }

GET /api/v1/auth/me
  Headers: Authorization: Bearer {token}
  Response: { "id": 1, "username": "admin", "email": "...", "role": "admin" }
```

---

### 13.3 Alert Endpoints

```
GET /api/v1/alerts
  Query params:
    page (int, default=1)
    per_page (int, default=20, max=100)
    severity (enum: INFO|LOW|MEDIUM|HIGH|CRITICAL)
    status (enum: NEW|ACKNOWLEDGED|RESOLVED|FALSE_POSITIVE|ESCALATED)
    category (str)
    src_ip (str)
    dst_ip (str)
    signature (str, partial match)
    start_date (ISO8601)
    end_date (ISO8601)
    sort_by (str, default=created_at)
    sort_order (enum: asc|desc, default=desc)
  Response: PaginatedResponse[AlertResponse]
  Auth: Required

GET /api/v1/alerts/{alert_id}
  Response: AlertResponse (with full raw_eve, geo, and response history)
  Auth: Required

POST /api/v1/alerts/{alert_id}/acknowledge
  Body: { "notes": "Investigated, confirmed malicious activity" }
  Response: AlertResponse
  Auth: Required (analyst+)

POST /api/v1/alerts/{alert_id}/resolve
  Body: { "resolution": "RESOLVED | FALSE_POSITIVE", "notes": "..." }
  Response: AlertResponse
  Auth: Required (analyst+)

POST /api/v1/alerts/{alert_id}/escalate
  Body: { "notes": "Escalating to incident response team" }
  Response: AlertResponse
  Auth: Required (analyst+)

DELETE /api/v1/alerts/{alert_id}
  Response: { "message": "Alert deleted" }
  Auth: Required (admin only)

POST /api/v1/alerts/bulk-acknowledge
  Body: { "alert_ids": [1, 2, 3], "notes": "..." }
  Response: { "updated_count": 3, "alerts": [...] }
  Auth: Required (analyst+)

GET /api/v1/alerts/export
  Query: format (csv|json), filters same as GET /alerts
  Response: File download (Content-Disposition: attachment)
  Auth: Required
```

---

### 13.4 Statistics Endpoints

```
GET /api/v1/statistics/dashboard
  Response: {
    "total_alerts_today": 1247,
    "total_alerts_week": 8432,
    "critical_alerts_today": 12,
    "high_alerts_today": 89,
    "active_rules_count": 342,
    "packets_analyzed": 8472938,
    "alerts_by_severity": { "INFO": 234, "LOW": 567, ... },
    "alerts_by_category": { "SCAN": 234, "EXPLOIT": 12, ... },
    "top_src_ips": [{"ip": "45.33.32.156", "count": 234, "country": "US"}, ...],
    "alerts_trend_24h": [{"hour": "14:00", "count": 23}, ...]
  }
  Auth: Required

GET /api/v1/statistics/timeline
  Query: range (1h|6h|24h|7d|30d), interval (5m|1h|1d)
  Response: { "buckets": [{"timestamp": "...", "count": 12, "by_severity": {...}}] }
  Auth: Required

GET /api/v1/statistics/top-attackers
  Query: limit (int, default=10), period (24h|7d|30d)
  Response: { "attackers": [{"ip": "...", "country": "...", "count": 234, "last_seen": "..."}] }
  Auth: Required

GET /api/v1/statistics/protocols
  Query: period (24h|7d|30d)
  Response: { "protocols": [{"protocol": "TCP", "count": 8472, "percentage": 67.4}] }
  Auth: Required

GET /api/v1/statistics/categories
  Query: period (24h|7d|30d)
  Response: { "categories": [{"category": "SCAN", "count": 234, ...}] }
  Auth: Required
```

---

### 13.5 Rules Endpoints

```
GET /api/v1/rules
  Query: is_enabled (bool), is_custom (bool), category (str), search (str)
  Response: PaginatedResponse[RuleResponse]
  Auth: Required

POST /api/v1/rules
  Body: { "content": "alert tcp any any -> any any (msg:\"...\"; sid:1000001; rev:1;)" }
  Response: RuleResponse
  Auth: Required (admin+)

GET /api/v1/rules/{rule_id}
  Response: RuleResponse (with trigger history)
  Auth: Required

PUT /api/v1/rules/{rule_id}
  Body: { "content": "...", "is_enabled": true }
  Response: RuleResponse
  Auth: Required (admin+)

DELETE /api/v1/rules/{rule_id}
  Response: { "message": "Rule deleted and Suricata reloaded" }
  Auth: Required (admin only)

POST /api/v1/rules/validate
  Body: { "content": "alert tcp any any -> any any (msg:\"...\"; sid:1000001; rev:1;)" }
  Response: { "valid": true, "errors": [], "warnings": ["No content match specified"] }
  Auth: Required

POST /api/v1/rules/{rule_id}/toggle
  Response: { "is_enabled": false, "message": "Rule disabled and Suricata reloaded" }
  Auth: Required (analyst+)

POST /api/v1/rules/reload
  Response: { "message": "Rules reloaded (SIGHUP sent to Suricata)", "rule_count": 342 }
  Auth: Required (admin only)
```

---

### 13.6 System Endpoints

```
GET /api/v1/system/health
  Response: {
    "status": "healthy",
    "components": {
      "suricata": {"status": "running", "pid": 1234, "uptime_seconds": 3600},
      "database": {"status": "connected", "latency_ms": 1.2},
      "eve_watcher": {"status": "active", "last_event_at": "..."},
      "websocket": {"status": "online", "connected_clients": 3}
    }
  }
  Auth: None (health check endpoint)

GET /api/v1/system/suricata/stats
  Response: { "packets_received": 1234567, "alerts": 1247, "flows": 8923, ... }
  Auth: Required

POST /api/v1/system/suricata/start
  Response: { "message": "Suricata started", "pid": 5678 }
  Auth: Required (admin only)

POST /api/v1/system/suricata/stop
  Response: { "message": "Suricata stopped gracefully" }
  Auth: Required (admin only)

POST /api/v1/system/suricata/restart
  Response: { "message": "Suricata restarted", "pid": 5679 }
  Auth: Required (admin only)

GET /api/v1/system/blocked-ips
  Response: PaginatedResponse[BlockedIP]
  Auth: Required

DELETE /api/v1/system/blocked-ips/{ip}
  Response: { "message": "IP unblocked and firewall rule removed" }
  Auth: Required (admin only)
```

---

### 13.7 WebSocket Protocol

**Connection:** `ws://localhost:8000/ws/events?token={jwt_token}`

**Server → Client Messages:**

```json
// New alert
{
  "type": "new_alert",
  "timestamp": "2024-01-15T14:23:11Z",
  "data": { /* AlertResponse object */ }
}

// System stats update (every 30 seconds)
{
  "type": "stats_update",
  "timestamp": "2024-01-15T14:23:11Z",
  "data": {
    "packets_per_second": 1247,
    "alerts_per_minute": 12,
    "active_flows": 8923
  }
}

// System status change
{
  "type": "system_status",
  "timestamp": "2024-01-15T14:23:11Z",
  "data": {
    "component": "suricata",
    "status": "stopped",
    "reason": "Manual stop via API"
  }
}

// Ping (server sends every 30s)
{ "type": "ping", "timestamp": "..." }
```

**Client → Server Messages:**

```json
// Pong response
{ "type": "pong" }

// Subscribe to specific severity only
{ "type": "subscribe", "filters": { "severity": ["HIGH", "CRITICAL"] } }

// Request current stats
{ "type": "get_stats" }
```

---

### 13.8 HTTP Status Codes

| Code | Usage |
|---|---|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE |
| 400 | Bad request (validation error) |
| 401 | Unauthenticated (missing/invalid token) |
| 403 | Unauthorized (insufficient role) |
| 404 | Resource not found |
| 409 | Conflict (duplicate SID, etc.) |
| 422 | Unprocessable entity (Pydantic validation failed) |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Service unavailable (Suricata not running) |

---

## 14. SECURITY PRACTICES

### 14.1 Authentication & Authorization

- **JWT tokens** with 1-hour expiry + refresh token (7 days)
- Refresh token stored in `httpOnly` cookie (not localStorage)
- Role-based access control: `admin > analyst > viewer`
- All API endpoints require valid JWT (except `/health` and `/docs`)
- JWT secret: 256-bit random key from environment variable `JWT_SECRET_KEY`
- Password hashing: `bcrypt` with work factor 12

```python
# Role permissions table
PERMISSIONS = {
    "viewer": ["GET /api/v1/alerts", "GET /api/v1/statistics"],
    "analyst": [*viewer_perms, "POST /api/v1/alerts/{id}/acknowledge", "POST /api/v1/alerts/{id}/resolve"],
    "admin": [*analyst_perms, "POST /api/v1/rules", "DELETE /api/v1/rules/{id}", "POST /api/v1/system/*"]
}
```

---

### 14.2 Input Validation

- All API inputs validated by Pydantic v2 schemas
- IP addresses validated with `ipaddress.ip_address()` before processing
- SQL injection impossible due to SQLAlchemy ORM parameterized queries
- Suricata rule content sanitized before writing to disk
- File path inputs validated against allowlist (no path traversal)
- Max request body size: 1MB (configured in Uvicorn)

---

### 14.3 Security Headers

Applied via middleware to all responses:
```python
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
}
```

---

### 14.4 Environment Variables

**Never hardcode secrets. Never commit `.env` files.**

Required environment variables:

```env
# Application
APP_NAME=NIDS-Pro
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=false

# Security
JWT_SECRET_KEY=<256-bit-random-key-change-in-production>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=sqlite+aiosqlite:///./database/nids.db
# Production: postgresql+asyncpg://user:pass@localhost/nids

# Suricata
SURICATA_LOG_PATH=/var/log/suricata/eve.json
SURICATA_CONFIG_PATH=/etc/suricata/suricata.yaml
SURICATA_RULES_PATH=/etc/suricata/rules/custom.rules

# GeoIP
GEOIP_DB_PATH=/opt/geoip/GeoLite2-City.mmdb

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW_SECONDS=60

# Response Engine
ENABLE_EMAIL_RESPONSE=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
ALERT_EMAIL_TO=

ENABLE_WEBHOOK_RESPONSE=false
WEBHOOK_URL=
WEBHOOK_MIN_SEVERITY=MEDIUM

ENABLE_FIREWALL_RESPONSE=false
ENABLE_IP_BLOCK_RESPONSE=false
```

`.env.example` is committed to repository. `.env` is in `.gitignore`.

---

### 14.5 Dependency Security

- **Dependabot** enabled via `.github/dependabot.yml` — weekly PR for dependency updates
- **GitHub Actions CodeQL** scan on every push
- **pip-audit** run in CI pipeline to check for known vulnerable dependencies
- **npm audit** run in frontend CI pipeline
- All Python packages pinned to exact versions in `requirements.txt`

---

### 14.6 CORS Configuration

```python
CORS_CONFIG = {
    "allow_origins": settings.CORS_ORIGINS.split(","),
    "allow_credentials": True,
    "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    "allow_headers": ["Authorization", "Content-Type", "X-Request-ID"],
    "max_age": 3600,
}
```

Wildcard `*` is explicitly forbidden in all environments.

---

## 15. LOGGING STRATEGY

### 15.1 Log Architecture

Five distinct log streams, each with separate files:

| Log Type | File | Rotation | Retention |
|---|---|---|---|
| Application | `logs/app/app_{date}.log` | Daily | 30 days |
| Detection | `logs/detection/detection_{date}.log` | Daily | 90 days |
| API Access | `logs/access/access_{date}.log` | Daily | 30 days |
| Error | `logs/errors/error_{date}.log` | Daily | 90 days |
| Audit | `logs/audit/audit_{date}.log` | Daily | 365 days |
| Response | `logs/responses/response_{date}.log` | Daily | 30 days |

---

### 15.2 Log Format (Structured JSON)

All log entries are JSON objects on a single line (NDJSON):

```json
{
  "timestamp": "2024-01-15T14:23:11.456789Z",
  "level": "INFO",
  "event": "alert_created",
  "request_id": "req_abc123def456",
  "service": "alert_service",
  "alert_id": 1247,
  "severity": "HIGH",
  "src_ip": "45.33.32.156",
  "signature": "ET EXPLOIT CVE-2021-44228",
  "duration_ms": 12.4
}
```

---

### 15.3 Log Levels

| Level | Usage |
|---|---|
| DEBUG | Detailed internal state (only in development) |
| INFO | Normal operations (alert created, rule loaded, API request) |
| WARNING | Non-fatal issues (GeoIP lookup failed, webhook retry) |
| ERROR | Failed operations requiring investigation (DB write failed) |
| CRITICAL | System-level failures (Suricata crashed, database unreachable) |

---

### 15.4 Access Log Format

```
[2024-01-15 14:23:11] req_abc123 GET /api/v1/alerts 200 12ms user=analyst1 ip=192.168.1.100
```

---

### 15.5 Audit Log Schema

Audit logs record every user action affecting system state:

```json
{
  "timestamp": "2024-01-15T14:23:11Z",
  "event": "alert_acknowledged",
  "user_id": 2,
  "username": "analyst1",
  "resource_type": "alert",
  "resource_id": 1247,
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "changes": {
    "status": { "from": "NEW", "to": "ACKNOWLEDGED" },
    "notes": { "from": "", "to": "Confirmed malicious activity" }
  }
}
```

---

## 16. TESTING STRATEGY

### 16.1 Test Coverage Requirements

- **Backend overall**: Minimum 80% line coverage
- **Services**: Minimum 90% (core business logic)
- **Repositories**: Minimum 85%
- **API routes**: 100% happy path + common error cases
- **EVE Parser**: 100% (critical path)
- **Rule Validator**: 100% (critical path)

---

### 16.2 Backend Unit Tests

**`tests/backend/unit/test_eve_parser.py`:**
```python
def test_parse_alert_event():
    """Test parsing of Suricata EVE JSON alert event."""
    sample_eve = {
        "timestamp": "2024-01-15T14:23:11.456789+0000",
        "flow_id": 1847291847382,
        "in_iface": "eth0",
        "event_type": "alert",
        "src_ip": "45.33.32.156",
        "src_port": 49152,
        "dest_ip": "192.168.1.50",
        "dest_port": 8080,
        "proto": "TCP",
        "alert": {
            "action": "allowed",
            "gid": 1,
            "signature_id": 2030450,
            "rev": 1,
            "signature": "ET EXPLOIT Test Rule",
            "category": "A Network Trojan was Detected",
            "severity": 1
        }
    }
    result = EVEParser.parse(sample_eve)
    assert result.event_type == "alert"
    assert result.src_ip == "45.33.32.156"
    assert result.signature_id == 2030450
    assert result.priority == 1

def test_parse_dns_event(): ...
def test_parse_http_event(): ...
def test_parse_tls_event(): ...
def test_parse_stats_event(): ...
def test_parse_unknown_event_type(): ...
```

**`tests/backend/unit/test_alert_service.py`:**
```python
@pytest.mark.asyncio
async def test_create_alert_success(alert_service, mock_alert_repository, mock_event_bus):
    """Test alert creation with all dependencies mocked."""
    mock_alert_repository.create.return_value = make_alert(id=1)
    alert = await alert_service.create_alert(make_alert_create())
    assert alert.id == 1
    mock_event_bus.publish.assert_called_once_with("new_alert", ANY)

@pytest.mark.asyncio
async def test_create_alert_deduplication(alert_service):
    """Test that duplicate alerts within 60s window are suppressed."""
    ...

@pytest.mark.asyncio
async def test_acknowledge_alert_changes_status(alert_service, mock_repo):
    ...

@pytest.mark.asyncio
async def test_acknowledge_alert_not_found_raises_error(alert_service):
    ...
```

---

### 16.3 Backend Integration Tests

**`tests/backend/integration/test_alert_api.py`:**
```python
@pytest.mark.asyncio
async def test_get_alerts_returns_paginated_list(client, auth_headers, seed_alerts):
    """Integration test: GET /api/v1/alerts returns alerts from real DB."""
    response = await client.get("/api/v1/alerts", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "data" in data
    assert "meta" in data
    assert data["meta"]["total"] == 10  # from seed_alerts fixture

@pytest.mark.asyncio
async def test_get_alerts_filter_by_severity(client, auth_headers, seed_alerts):
    response = await client.get("/api/v1/alerts?severity=CRITICAL", headers=auth_headers)
    alerts = response.json()["data"]
    assert all(a["severity"] == "CRITICAL" for a in alerts)

@pytest.mark.asyncio
async def test_unauthorized_access_returns_401(client):
    response = await client.get("/api/v1/alerts")
    assert response.status_code == 401
```

**`tests/backend/integration/test_websocket.py`:**
```python
@pytest.mark.asyncio
async def test_websocket_receives_new_alert(client, alert_service, auth_token):
    """Test that creating an alert broadcasts via WebSocket."""
    async with client.websocket_connect(f"/ws/events?token={auth_token}") as ws:
        await alert_service.create_alert(make_alert_create(severity="CRITICAL"))
        message = await asyncio.wait_for(ws.receive_json(), timeout=2.0)
        assert message["type"] == "new_alert"
        assert message["data"]["severity"] == "CRITICAL"
```

---

### 16.4 Rule Tests

**`tests/backend/unit/test_rule_validator.py`:**
```python
VALID_RULES = [
    'alert tcp any any -> any 80 (msg:"Test HTTP"; content:"GET"; sid:1000001; rev:1;)',
    'drop udp any any -> any 53 (msg:"DNS Query"; dns.query; content:"evil.com"; sid:1000002; rev:1;)',
]

INVALID_RULES = [
    'alert tcp any any -> (msg:"Missing dest port";)',  # syntax error
    'alert tcp any any -> any any (msg:"No SID";)',      # missing required sid
    'alert tcp any any -> any any (msg:"Duplicate"; sid:1000001; rev:1;)',  # duplicate sid
]

@pytest.mark.parametrize("rule", VALID_RULES)
def test_valid_rule_passes_validation(rule):
    result = RuleValidator.validate(rule)
    assert result.is_valid == True
    assert result.errors == []

@pytest.mark.parametrize("rule", INVALID_RULES)
def test_invalid_rule_fails_validation(rule):
    result = RuleValidator.validate(rule)
    assert result.is_valid == False
    assert len(result.errors) > 0
```

---

### 16.5 Frontend Tests

**Component tests with React Testing Library:**

```typescript
// tests/frontend/test_alert_badge.test.tsx
describe("AlertBadge", () => {
  it("renders CRITICAL badge with correct styles", () => {
    render(<AlertBadge severity="CRITICAL" />);
    const badge = screen.getByText("CRITICAL");
    expect(badge).toBeInTheDocument();
    expect(badge).toHaveClass("bg-red-500/10", "text-red-400");
  });

  it.each(["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"])(
    "renders %s severity correctly",
    (severity) => {
      render(<AlertBadge severity={severity as SeverityLevel} />);
      expect(screen.getByText(severity)).toBeInTheDocument();
    }
  );
});
```

---

### 16.6 Performance Tests

Test that the system can handle realistic load:

```python
# tests/backend/performance/test_alert_throughput.py
@pytest.mark.performance
async def test_alert_creation_throughput():
    """System should handle 100 alerts/second without degradation."""
    alerts = [make_alert_create() for _ in range(1000)]
    start = time.monotonic()
    await asyncio.gather(*[service.create_alert(a) for a in alerts])
    elapsed = time.monotonic() - start
    assert elapsed < 10.0, f"1000 alerts took {elapsed:.2f}s (>10s threshold)"

@pytest.mark.performance
async def test_websocket_broadcast_latency():
    """WebSocket broadcast should complete in <100ms for 10 connected clients."""
    ...
```

---

## 17. GITHUB STANDARDS

### 17.1 Branch Strategy

```
main ─────────────────────────────────────── Production-ready code
  └── develop ──────────────────────────────── Integration branch
        ├── feature/detection-engine ──────────── Feature branches
        ├── feature/dashboard-charts ──────────── 
        ├── fix/websocket-reconnection ────────── Bug fix branches
        └── docs/api-documentation ────────────── Documentation branches
```

**Rules:**
- Direct push to `main` is **forbidden** — requires PR with at least 1 review
- `develop` is the integration branch — all features merge here first
- `main` is only updated from `develop` via merge commit (no fast-forward)
- Feature branches named: `feature/{short-description}`
- Bug fixes: `fix/{short-description}`
- Documentation: `docs/{short-description}`
- Releases: `release/v{major}.{minor}.{patch}`

---

### 17.2 GitHub Actions Workflows

**`.github/workflows/ci.yml`** — Triggered on every push and PR:
```yaml
name: CI
on: [push, pull_request]
jobs:
  lint-backend:
    - runs: ruff check backend/ && black --check backend/ && mypy backend/
  lint-frontend:
    - runs: npx eslint frontend/ && npx tsc --noEmit
  test-backend:
    - runs: pytest tests/backend/ --cov=backend --cov-report=xml
  test-frontend:
    - runs: npx jest --coverage
  build-docker:
    - builds Docker images to verify build succeeds
  security-scan:
    - runs: pip-audit && npm audit
```

**`.github/workflows/release.yml`** — Triggered on version tag push:
```yaml
on:
  push:
    tags: ['v*.*.*']
jobs:
  release:
    - builds Docker images
    - pushes to GitHub Container Registry (ghcr.io)
    - creates GitHub Release with changelog
    - uploads release artifacts
```

---

### 17.3 Issue Templates

**Bug Report Template:**
```markdown
## Bug Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1. 
2. 
3. 

## Expected Behavior
<!-- What should happen -->

## Actual Behavior
<!-- What actually happens -->

## Environment
- OS:
- Python version:
- Docker version:
- Browser (if UI bug):

## Logs
```
paste relevant logs here
```

## Screenshots
<!-- If applicable -->
```

**Feature Request Template:**
```markdown
## Feature Summary
<!-- One-line description -->

## Problem Statement
<!-- What problem does this solve? -->

## Proposed Solution
<!-- How should it work? -->

## Alternatives Considered
<!-- Other approaches you thought about -->

## Additional Context
<!-- Any other relevant information -->
```

---

### 17.4 Labels

| Label | Color | Usage |
|---|---|---|
| `bug` | `#d73a4a` | Something isn't working |
| `feature` | `#0075ca` | New feature request |
| `enhancement` | `#a2eeef` | Improvement to existing feature |
| `documentation` | `#0075ca` | Documentation changes |
| `security` | `#e11d48` | Security-related issue |
| `good first issue` | `#7057ff` | Good for newcomers |
| `help wanted` | `#008672` | Extra attention needed |
| `detection-rules` | `#f9d0c4` | Related to detection rules |
| `frontend` | `#d4edda` | Dashboard/UI related |
| `backend` | `#cfe2ff` | API/backend related |
| `performance` | `#fff3cd` | Performance improvement |
| `duplicate` | `#cfd3d7` | Duplicate issue |
| `wontfix` | `#ffffff` | Will not be fixed |
| `in-progress` | `#fbca04` | Currently being worked on |
| `needs-review` | `#e4e669` | PR awaiting review |
| `priority: high` | `#b60205` | High priority |
| `v1.0` | `#0e8a16` | Milestone tag |

---

### 17.5 Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

- `MAJOR` — Breaking changes (API incompatibility, architectural overhaul)
- `MINOR` — New features added (backward-compatible)
- `PATCH` — Bug fixes and security patches

Examples:
- `v1.0.0` — Initial release
- `v1.1.0` — Added PCAP replay feature
- `v1.1.1` — Fixed WebSocket reconnection bug
- `v2.0.0` — Migrated to PostgreSQL, breaking configuration change

---

## 18. DOCUMENTATION PLAN

### 18.1 Documentation Index

| Document | Location | Audience |
|---|---|---|
| `README.md` | Root | All visitors |
| `CONTRIBUTING.md` | Root | Contributors |
| `CODE_OF_CONDUCT.md` | Root | Community |
| `SECURITY.md` | Root | Security researchers |
| `CHANGELOG.md` | Root | All users |
| `LICENSE` | Root | All |
| `docs/ARCHITECTURE.md` | docs/ | Developers |
| `docs/INSTALLATION.md` | docs/ | Users |
| `docs/RULE_GUIDE.md` | docs/ | Security engineers |
| `docs/API.md` | docs/ | API consumers |
| `docs/DEPLOYMENT.md` | docs/ | DevOps |
| `docs/USER_GUIDE.md` | docs/ | End users |
| `docs/FAQ.md` | docs/ | All |
| `docs/ROADMAP.md` | docs/ | All |
| `suricata/rules/README.md` | suricata/rules/ | Rule authors |
| FastAPI `/docs` | Runtime | API consumers |

---

### 18.2 Key Document Contents

**`docs/INSTALLATION.md`** must cover:
1. Prerequisites (OS, Python, Node.js, Docker versions)
2. Quick Start (Docker Compose — single command)
3. Manual Installation (step by step)
4. Suricata Configuration
5. First Login credentials
6. Verifying installation with health check

**`docs/RULE_GUIDE.md`** must cover:
1. Suricata rule syntax reference
2. Rule action types (alert/drop/pass/reject)
3. Protocol options
4. Detection keywords (content, pcre, flow)
5. Custom SID numbering convention (1000001+)
6. Rule categories used in this project
7. Example rules (port scan, brute force, DNS exfil, HTTP injection)
8. Rule testing procedure
9. Rule performance considerations

**`docs/API.md`** must cover:
- Authentication flow
- All endpoint specifications (auto-generated from FastAPI OpenAPI)
- WebSocket protocol
- SDK code examples (Python, JavaScript)
- Rate limiting behavior
- Error reference

---

## 19. README BLUEPRINT

### 19.1 README Structure

```markdown
<!-- HERO BANNER -->
<p align="center">
  <img src="assets/banner.png" width="100%" alt="NIDS-Pro Banner">
</p>

<h1 align="center">
  🛡️ Network Intrusion Detection System
</h1>

<p align="center">
  <strong>Professional SOC-Grade NIDS • Real-Time Threat Detection • Built with Suricata + FastAPI + Next.js</strong>
</p>

<!-- BADGES ROW -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.110-green?logo=fastapi" />
  <img src="https://img.shields.io/badge/Next.js-14-black?logo=next.js" />
  <img src="https://img.shields.io/badge/Suricata-7.x-orange?logo=suricata" />
  <img src="https://img.shields.io/badge/Docker-ready-blue?logo=docker" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
  <img src="https://img.shields.io/github/stars/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=social" />
</p>

---

## 📸 Screenshots

| Dashboard | Live Monitoring | Alert Detail |
|---|---|---|
| ![Dashboard](assets/screenshots/01-dashboard.png) | ![Monitoring](assets/screenshots/02-live-monitoring.png) | ![Alert](assets/screenshots/03-alert-detail.png) |

---

## ✨ Features

- 🔍 **Real-Time Detection** — Suricata 7.x powered detection with ET Open + custom rules
- 📊 **Live Dashboard** — WebSocket-driven SOC dashboard with live alert feed
- 🚨 **5-Tier Alert System** — INFO/LOW/MEDIUM/HIGH/CRITICAL severity classification
- 🌍 **GeoIP Enrichment** — MaxMind GeoLite2 lookup on every source IP
- ⚡ **Automated Response** — Email/webhook/firewall/IP-block response pipeline
- 📈 **Attack Analytics** — 7 chart types covering all traffic dimensions
- 🔧 **Rule Management** — Create/edit/validate Suricata rules from the UI
- 🐳 **Docker Ready** — One-command deployment with Docker Compose
- 🔐 **Secure API** — JWT authentication, RBAC, rate limiting

---

## 🏗️ Architecture

[Architecture diagram image]

---

## 🚀 Quick Start

### Prerequisites
- Docker 24.x and Docker Compose 2.x
- OR: Python 3.11+, Node.js 20+, Suricata 7.x

### 1. Clone the Repository
\`\`\`bash
git clone https://github.com/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem.git
cd CodeAlpha_NetworkIntrusionDetectionSystem
\`\`\`

### 2. Configure Environment
\`\`\`bash
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
# Edit .env files with your settings
\`\`\`

### 3. Launch with Docker Compose
\`\`\`bash
docker-compose up -d
\`\`\`

### 4. Access the Dashboard
- Dashboard: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Default login: admin / changeme123

---

## 📁 Project Structure

[Condensed folder tree]

---

## 🛡️ Detection Rules

[Example custom rule snippet and link to RULE_GUIDE.md]

---

## 📖 Documentation

| Doc | Description |
|---|---|
| [Installation Guide](docs/INSTALLATION.md) | Full setup instructions |
| [Rule Writing Guide](docs/RULE_GUIDE.md) | Write custom detection rules |
| [API Reference](docs/API.md) | REST API documentation |
| [Architecture](docs/ARCHITECTURE.md) | System design details |
| [Deployment Guide](docs/DEPLOYMENT.md) | Docker and production setup |

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 👤 Author

**Muhammad Haris (harisx404)**
- GitHub: [@harisx404](https://github.com/harisx404)
- LinkedIn: [linkedin.com/in/harisx404](https://linkedin.com/in/harisx404)

---

## 🙏 Acknowledgements

- [Suricata IDS](https://suricata.io/) — Detection engine
- [Emerging Threats Open Rules](https://rules.emergingthreats.net/) — Rule signatures
- [Shadcn UI](https://ui.shadcn.com/) — UI component library
- [MaxMind GeoLite2](https://www.maxmind.com/) — GeoIP database
- [FastAPI](https://fastapi.tiangolo.com/) — Python web framework

---

*Built with ❤️ for CodeAlpha Cybersecurity Internship*
```
## 20. GITHUB PRESENTATION

### 20.1 Repository Banner

The banner (`assets/banner.png`) must be created at **1280×400px** and include:

- **Left side:** Shield/radar icon in electric cyan on dark navy background
- **Center text:**
  - Line 1: `NIDS-PRO` in large bold JetBrains Mono font, cyan color
  - Line 2: `Network Intrusion Detection System` in slate-300
  - Line 3: `Suricata • FastAPI • Next.js • Real-Time SOC Dashboard` in smaller text
- **Right side:** Subtle network graph / packet wave visual element
- **Bottom bar:** A thin cyan gradient bar across the full width
- **Aesthetic:** Dark glassmorphism, same palette as the dashboard

Design tool recommendation: Canva Pro or Figma. Export as `.png` at 2x resolution for retina screens.

---

### 20.2 Social Preview Image

**File:** `assets/social-preview.png`
**Dimensions:** 1280×640px (GitHub Open Graph standard)

Content:
- Large shield + radar icon center-left
- Project name and subtitle right side
- Three mini screenshot thumbnails of the dashboard in a row
- Technology logos in footer (Python, FastAPI, React, Suricata)
- Dark background matching dashboard theme

This image appears when the repository link is shared on LinkedIn, Twitter/X, Slack, and other platforms.

---

### 20.3 Repository Screenshots

Capture and store these in `assets/screenshots/`:

| File | Content | Dimensions |
|---|---|---|
| `01-dashboard.png` | Main dashboard with KPI cards, live feed, charts | 1920×1080 |
| `02-live-monitoring.png` | Live monitoring page with active event stream | 1920×1080 |
| `03-alert-detail.png` | Alert detail drawer open with full metadata | 1920×1080 |
| `04-analytics.png` | Analytics page showing traffic charts | 1920×1080 |
| `05-rules-editor.png` | Rules page with editor and rule table | 1920×1080 |
| `06-system-status.png` | System status page with component health | 1920×1080 |

Screenshots should be captured in dark mode, at 1920×1080, with realistic but safe fake data (fabricated IP addresses only, no real-world sensitive information).

---

### 20.4 Demo GIF

Create an animated GIF (`assets/demo.gif`) showing:
1. Dashboard loading with live alert feed populating
2. Critical alert appearing with red flash animation
3. Clicking alert → detail drawer opening
4. Switching to analytics page → charts rendering

Capture with **LICEcap** or **ScreenToGif** (Windows) or **Kap** (macOS).
Target: <5MB, 1280×720, 15fps, 30 seconds duration.

---

### 20.5 Shields.io Badges

**Static badges to include in README:**
```markdown
<!-- Technology badges -->
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![Suricata](https://img.shields.io/badge/Suricata-7.x-F0562F?style=flat-square)

<!-- Repository badges -->
![License](https://img.shields.io/github/license/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=flat-square)
![Stars](https://img.shields.io/github/stars/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=flat-square)
![Issues](https://img.shields.io/github/issues/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)

<!-- CI status badge -->
![CI](https://github.com/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem/actions/workflows/ci.yml/badge.svg)

<!-- Code quality (optional via Codecov) -->
![Coverage](https://img.shields.io/codecov/c/github/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem?style=flat-square)
```

---

### 20.6 Repository Topics (GitHub Tags)

Set these topics on the repository settings page:

```
network-security  intrusion-detection  suricata  fastapi  nextjs
python  react  typescript  cybersecurity  soc-dashboard  nids
threat-detection  packet-analysis  docker  real-time  websocket
internship  codeAlpha  open-source  security-tools  tailwindcss
```

Topics drive GitHub search discoverability. A security engineer searching `suricata fastapi` or `nids dashboard` must find this project on the first page.

---

### 20.7 Pinned Repository Strategy

On the GitHub profile (`github.com/harisx404`):
- Pin this repository in the top 6 pinned repositories slot
- Pin alongside: MedicaLink HMS (MERN flagship), TourMate (FYP), SC-200 prep materials
- The combination demonstrates: full-stack engineering + cybersecurity + infrastructure

The NIDS repository should be the **#1 pinned project** given the internship context.

---

### 20.8 GitHub Releases Strategy

| Tag | Name | Contents |
|---|---|---|
| `v0.1.0` | Alpha — Core Detection | Suricata integration + basic alert logging |
| `v0.5.0` | Beta — Dashboard | Dashboard with live monitoring |
| `v1.0.0` | Production Release | All features, Docker, full documentation |

Each release includes:
- Compiled release notes from `CHANGELOG.md`
- Docker images published to GHCR
- `Source code (zip)` and `Source code (tar.gz)` auto-generated by GitHub
- SHA256 checksum file for verification

---

## 21. CONTRIBUTOR EXPERIENCE

### 21.1 CONTRIBUTING.md Structure

```markdown
# Contributing to NIDS-Pro

Thank you for your interest in contributing! This document explains how to
contribute effectively to this project.

## Table of Contents
1. Code of Conduct
2. Getting Started
3. Development Setup
4. How to Contribute
5. Pull Request Process
6. Coding Standards
7. Writing Detection Rules
8. Reporting Security Vulnerabilities

## Getting Started

### Prerequisites
[...]

### Fork & Clone
1. Fork this repository on GitHub
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/...`
3. Add upstream: `git remote add upstream https://github.com/harisx404/...`
4. Create a branch: `git checkout -b feature/your-feature-name`

### Development Setup
[Step by step setup with exact commands]

## Types of Contributions Welcome

| Type | Description |
|---|---|
| 🐛 Bug fixes | Found a bug? Please fix it! |
| ✨ New features | Add features from the roadmap |
| 📜 Detection rules | Write new Suricata detection rules |
| 📖 Documentation | Improve or correct documentation |
| 🧪 Tests | Add missing test coverage |
| 🎨 UI improvements | Enhance the dashboard |
| 🔒 Security | Report and fix security issues |

## Good First Issues

Look for issues tagged `good first issue` — these are deliberately chosen
as appropriate starting points for new contributors:
- Add a new chart to the analytics page
- Write a detection rule for [attack type]
- Add a missing API test
- Improve error messages in the UI

## Pull Request Checklist

Before submitting your PR, confirm all of these:

- [ ] Code follows the project's coding standards
- [ ] All existing tests pass (`pytest` and `jest`)
- [ ] New code has appropriate test coverage
- [ ] Docstrings added to all new Python functions
- [ ] JSDoc added to all new TypeScript functions
- [ ] No hardcoded secrets or sensitive data
- [ ] `CHANGELOG.md` updated with your change
- [ ] PR description explains what, why, and how
- [ ] Screenshots attached if UI was changed
```

---

### 21.2 Pull Request Template

**`.github/PULL_REQUEST_TEMPLATE.md`:**

```markdown
## Summary

<!-- One paragraph explaining what this PR does and why. -->

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] ✨ New feature (non-breaking change adding functionality)
- [ ] 💥 Breaking change (fix or feature causing existing functionality to break)
- [ ] 📖 Documentation update
- [ ] 🧹 Refactor (code change with no functional change)
- [ ] 🧪 Test (adding or improving tests)
- [ ] 🔒 Security fix

## Related Issue

Closes #<!-- issue number -->

## Changes Made

<!-- Bullet list of specific changes -->
- 
- 
- 

## Testing

<!-- How was this tested? -->

- [ ] Unit tests pass (`pytest tests/backend/unit/`)
- [ ] Integration tests pass (`pytest tests/backend/integration/`)
- [ ] Frontend tests pass (`npx jest`)
- [ ] Manually tested in browser

## Screenshots (if UI changed)

| Before | After |
|---|---|
| screenshot | screenshot |

## Checklist

- [ ] My code follows the project's coding standards
- [ ] I have added docstrings/JSDoc to new functions
- [ ] I have updated `CHANGELOG.md`
- [ ] No console.log or print() debugging left in code
- [ ] No hardcoded secrets or sensitive data
```

---

### 21.3 Discussion Board Configuration

Enable GitHub Discussions with these categories:

| Category | Emoji | Description |
|---|---|---|
| Announcements | 📢 | Project news and releases |
| General | 💬 | General project discussion |
| Q&A | ❓ | Ask questions about setup and usage |
| Rule Sharing | 🛡️ | Share and discuss detection rules |
| Ideas | 💡 | Propose new features |
| Show and Tell | 🎉 | Share your deployment or customization |
| Security | 🔐 | Security discussions (public, non-sensitive) |

---

### 21.4 First Good Issue Guidelines

When opening an issue intended for new contributors, the issue must:
1. Have label `good first issue`
2. Describe the exact file(s) to modify
3. Explain the expected behavior with a code example
4. List the exact test to add or modify
5. Link to the relevant section of documentation
6. Offer to clarify in comments

**Example good first issue:**
```
Title: Add "Copy IP" button to alert detail view

Description:
The alert detail drawer shows the source IP address as plain text.
We want a small copy button next to it that copies the IP to clipboard.

File to modify: frontend/components/alerts/AlertDetail.tsx

Expected behavior:
- Add a CopyButton component (already exists at frontend/components/common/CopyButton.tsx)
- Render it next to the src_ip field
- On click, copy the IP string and show "Copied!" toast

Test to add: frontend/tests/test_alert_detail.test.tsx
- Test that CopyButton renders next to src_ip
- Test that clicking it calls navigator.clipboard.writeText()

This is a great first issue as it requires minimal code changes and
teaches you how components are structured in this project.
```

---

## 22. DEPLOYMENT

### 22.1 Docker Compose Architecture

```yaml
# docker-compose.yml (development)
version: "3.9"

services:

  suricata:
    build:
      context: .
      dockerfile: docker/Dockerfile.suricata
    container_name: nids-suricata
    restart: unless-stopped
    network_mode: host          # REQUIRED: host network for packet capture
    privileged: true            # REQUIRED: raw socket access
    cap_add:
      - NET_ADMIN
      - NET_RAW
    volumes:
      - ./suricata/config:/etc/suricata:ro
      - ./suricata/rules:/etc/suricata/rules:ro
      - suricata_logs:/var/log/suricata
    environment:
      - SURICATA_INTERFACE=eth0
    command: suricata -c /etc/suricata/suricata.yaml -i ${SURICATA_INTERFACE:-eth0}

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend
    container_name: nids-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - suricata_logs:/var/log/suricata:ro  # shared read-only log access
      - ./backend:/app                       # dev hot-reload
      - ./database:/app/database
      - ./logs:/app/logs
      - ./suricata/rules:/app/rules
    env_file:
      - ./backend/.env
    depends_on:
      - suricata
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/system/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: ../docker/Dockerfile.frontend
    container_name: nids-frontend
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app                      # dev hot-reload
      - /app/node_modules                    # exclude from bind mount
      - /app/.next                           # exclude build cache
    env_file:
      - ./frontend/.env.local
    depends_on:
      - backend

  nginx:
    image: nginx:1.25-alpine
    container_name: nids-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend

volumes:
  suricata_logs:          # shared between suricata and backend containers
```

---

### 22.2 Dockerfile Specifications

**`docker/Dockerfile.backend`:**
```dockerfile
# Stage 1: Dependencies
FROM python:3.11-slim AS deps
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpcap-dev curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim AS production
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpcap0.8 curl && rm -rf /var/lib/apt/lists/*
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin
COPY . .
RUN adduser --disabled-password --gecos "" nidsuser \
    && chown -R nidsuser:nidsuser /app
USER nidsuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/system/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`docker/Dockerfile.frontend`:**
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --frozen-lockfile

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS production
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:3000 || exit 1
CMD ["node", "server.js"]
```

**`docker/Dockerfile.suricata`:**
```dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    suricata suricata-update curl && rm -rf /var/lib/apt/lists/*
RUN suricata-update update-sources \
    && suricata-update enable-source et/open \
    && suricata-update
COPY suricata/config/suricata.yaml /etc/suricata/suricata.yaml
COPY suricata/rules/ /etc/suricata/rules/
VOLUME ["/var/log/suricata"]
EXPOSE 0
ENTRYPOINT ["suricata"]
CMD ["-c", "/etc/suricata/suricata.yaml", "-i", "eth0"]
```

---

### 22.3 Manual Installation (Linux)

**Prerequisites:**
```bash
# Python 3.11+
sudo apt-get install python3.11 python3.11-venv python3-pip

# Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Suricata 7.x
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt-get update && sudo apt-get install suricata

# GeoIP dependencies
sudo apt-get install libmaxminddb0 libmaxminddb-dev
```

**Backend Setup:**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
alembic upgrade head           # Run database migrations
python -m database.seed        # Seed initial data (admin user)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend Setup:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local with backend URL
npm run dev                    # Development server on port 3000
```

**Suricata Setup:**
```bash
# Configure Suricata
sudo cp suricata/config/suricata.yaml /etc/suricata/suricata.yaml
sudo cp suricata/rules/custom.rules /etc/suricata/rules/custom.rules

# Download ET Open rules
sudo suricata-update

# Start Suricata (replace eth0 with your interface)
sudo suricata -c /etc/suricata/suricata.yaml -i eth0

# Verify it's running
sudo tail -f /var/log/suricata/eve.json
```

---

### 22.4 Suricata Configuration Key Settings

**`suricata/config/suricata.yaml` critical settings:**

```yaml
# Network interface
af-packet:
  - interface: eth0
    cluster-id: 99
    cluster-type: cluster_flow
    defrag: yes
    use-mmap: yes
    tpacket-v3: yes

# EVE JSON output (REQUIRED for this project)
outputs:
  - eve-log:
      enabled: yes
      filetype: regular
      filename: /var/log/suricata/eve.json
      types:
        - alert:
            payload: yes
            payload-buffer-size: 4kb
            payload-printable: yes
            packet: yes
            metadata: yes
            tagged-packets: yes
        - http:
            extended: yes
        - dns:
            query: yes
            answer: yes
        - tls:
            extended: yes
        - files:
            force-magic: yes
        - flow
        - stats:
            threads: yes

# Rule files
rule-files:
  - /etc/suricata/rules/emerging-all.rules
  - /etc/suricata/rules/custom.rules
  - /etc/suricata/rules/local.rules

# Threading (tune to available CPUs)
threading:
  set-cpu-affinity: no
  detect-thread-ratio: 1.0

# Logging
logging:
  default-log-level: notice
  outputs:
    - console:
        enabled: no
    - file:
        enabled: yes
        level: info
        filename: /var/log/suricata/suricata.log
```

---

### 22.5 Windows Installation

Windows support via **WSL2 (Ubuntu 22.04)**:

1. Enable WSL2: `wsl --install`
2. Install Ubuntu 22.04 from Microsoft Store
3. Follow Linux installation guide inside WSL2
4. Network interface: Use `eth0` inside WSL2 (maps to Windows adapter)
5. Note: Full packet capture may require additional Windows drivers in WSL2

Native Windows is **not supported** for Suricata packet capture. Docker Desktop on Windows uses WSL2 backend and works correctly.

---

### 22.6 Production Hardening

For production deployment, beyond the base Docker Compose:

1. **Replace SQLite with PostgreSQL:**
   ```env
   DATABASE_URL=postgresql+asyncpg://nids_user:securepass@db:5432/nids
   ```

2. **Enable HTTPS via Let's Encrypt** in nginx.conf

3. **Set strong JWT secret:**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```

4. **Disable debug mode:**
   ```env
   DEBUG=false
   APP_ENV=production
   ```

5. **Enable firewall** on the host machine — only expose ports 80, 443

6. **Regular backups:** Daily PostgreSQL dump to encrypted S3/remote storage

7. **Log forwarding:** Ship logs to ELK or Splunk if available

8. **Monitoring:** Add Prometheus + Grafana sidecar for infrastructure metrics

---

## 23. PERFORMANCE

### 23.1 Packet Processing Performance

**Target:** Handle 1Gbps network traffic on a 4-core VM without dropping packets.

**Suricata tuning:**
- Use `AF_PACKET` with `cluster_flow` mode for zero-copy packet reception
- Enable `tpacket-v3` for batch packet reading
- Set `use-mmap: yes` for memory-mapped I/O
- Tune `detect-thread-ratio` to match available CPUs
- Disable unused protocol parsers in `suricata.yaml` `app-layer` section
- Configure `defrag: yes` for proper IP reassembly

---

### 23.2 EVE Log Watcher Performance

The EVE log watcher must process logs with sub-second latency:

```python
class EVELogWatcher:
    """
    Asyncio-based file tail that processes Suricata EVE JSON events.

    Performance design decisions:
    - Uses asyncio for non-blocking I/O (no threading overhead)
    - Reads in chunks of 8192 bytes (OS page size multiple)
    - Processes events in batches when load is high
    - Uses a semaphore to prevent DB write queue overflow
    - Sleep interval: 0.1s (100ms) when file has no new data
    """

    CHUNK_SIZE = 8192
    POLL_INTERVAL = 0.1  # seconds
    BATCH_SIZE = 50      # process up to 50 events per read cycle

    async def tail(self, filepath: str) -> None:
        async with aiofiles.open(filepath, mode="r") as f:
            await f.seek(0, 2)  # seek to end on startup
            while True:
                lines = await f.readlines()
                if lines:
                    await self._process_batch(lines[:self.BATCH_SIZE])
                else:
                    await asyncio.sleep(self.POLL_INTERVAL)
```

---

### 23.3 Database Performance

**Indexing strategy** (most important for query performance on large alert tables):

```sql
-- Most frequent query: alerts by time range + severity
CREATE INDEX CONCURRENTLY idx_alerts_timestamp_severity
    ON alerts (timestamp DESC, severity);

-- Filtering by IP (common in investigation workflows)
CREATE INDEX CONCURRENTLY idx_alerts_src_ip_hash
    ON alerts USING HASH (src_ip);

-- Status filtering
CREATE INDEX CONCURRENTLY idx_alerts_status
    ON alerts (status) WHERE status != 'RESOLVED';  -- partial index
```

**Query optimization:**
- Dashboard KPI queries use pre-aggregated `traffic_statistics` table (updated by background job every 60 seconds) — never compute live aggregations on millions of alert rows
- Alert listing uses cursor-based pagination (keyset) for tables > 100k rows, not offset-based pagination
- Use `SELECT specific_columns` instead of `SELECT *` — never retrieve `raw_eve` JSON on list queries

---

### 23.4 Backend Concurrency

FastAPI + Uvicorn runs on asyncio event loop:
- All I/O operations (DB reads, file reads, HTTP requests) are `async/await`
- **Never block the event loop** with synchronous operations
- CPU-bound operations (rule parsing, large report generation) offloaded to `ProcessPoolExecutor`
- Database operations use SQLAlchemy 2.0 async engine with connection pool (min=5, max=20)

```python
# Connection pool configuration
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,      # Verify connections before use
    pool_recycle=3600,       # Recycle connections every hour
    echo=False,              # Never log SQL in production
)
```

---

### 23.5 Frontend Performance

- **Next.js 14 App Router** with server components — reduces JavaScript bundle size
- **Static rendering** for non-dynamic pages (About, Help)
- **Dynamic imports** for heavy components (charts): `const Chart = dynamic(() => import('./Chart'), { ssr: false })`
- **Recharts virtualization** — `virtualized` prop on large data tables via TanStack Virtual
- **WebSocket debouncing** — If alerts arrive faster than 10/second, batch DOM updates to prevent jank
- **Image optimization** — All images via Next.js `<Image>` component for automatic WebP conversion and lazy loading
- **React Query / SWR** pattern — Not used (Zustand + axios is sufficient for this project's scale)
- **Bundle analysis** — Run `ANALYZE=true npm run build` to identify oversized bundles

---

### 23.6 Caching Strategy

| Data | Cache Method | TTL |
|---|---|---|
| Dashboard KPI stats | In-memory (Python dict in service) | 30 seconds |
| GeoIP lookups | `functools.lru_cache` (max 10,000 entries) | Session lifetime |
| Rule list | In-memory cache invalidated on rule change | Until SIGHUP |
| Top attackers | Pre-aggregated in `traffic_statistics` table | 60 seconds |
| Static frontend assets | Next.js build cache + CDN headers | 1 year (immutable) |

---

## 24. FUTURE ROADMAP

### 24.1 Version 1.0.0 — Initial Production Release (Current Target)

**Theme:** Professional SOC NIDS Dashboard

**Deliverables:**
- ✅ Suricata 7.x integration with EVE JSON pipeline
- ✅ FastAPI REST API + WebSocket backend
- ✅ Next.js 14 SOC dashboard with 10 pages
- ✅ 5-tier alert severity system with real-time feed
- ✅ GeoIP enrichment on all alerts
- ✅ Automated response engine (6 handlers)
- ✅ Full rule management CRUD
- ✅ JWT authentication with RBAC
- ✅ Docker Compose deployment
- ✅ GitHub Actions CI pipeline
- ✅ Full documentation suite
- ✅ 80%+ test coverage

---

### 24.2 Version 1.1.0 — Intelligence Upgrade

**Theme:** Threat Intelligence Integration

**New Features:**
- **AbuseIPDB Integration** — Automatically check source IPs against abuse database
- **VirusTotal Hash Lookup** — Check extracted file hashes against VirusTotal
- **PCAP Replay Mode** — Upload `.pcap` file, replay through Suricata, view results in dashboard
- **Threat Hunting Query Builder** — SQL-like interface for querying historical events
- **Alert Correlation Engine** — Group related alerts into incidents automatically
- **Email Report Scheduler** — Automated daily/weekly PDF reports via email
- **Improved GeoIP Map** — Interactive world map with click-to-filter by country

---

### 24.3 Version 1.2.0 — Detection Enhancement

**Theme:** Advanced Detection Capabilities

**New Features:**
- **YARA Rule Integration** — Scan extracted files from Suricata with YARA rules
- **JA3/JA3S TLS Fingerprinting** — Display JA3 hashes for TLS connections, compare against known-bad list
- **SSH/RDP Brute Force Detection** — Built-in detection for credential stuffing attacks
- **DNS Exfiltration Detection** — Custom rule set for DNS tunneling and exfiltration
- **Baseline Traffic Profiler** — Learn normal traffic patterns, alert on deviations
- **Multi-Interface Support** — Monitor multiple network interfaces simultaneously
- **Suricata Stats Dashboard** — Dedicated page for Suricata engine telemetry

---

### 24.4 Version 2.0.0 — Enterprise Grade

**Theme:** Multi-Tenant SOC Platform

**New Features:**
- **PostgreSQL as Default** — SQLite fully replaced, migration tooling provided
- **Multi-Tenancy** — Isolated organizations, each with their own rules and alerts
- **SAML/SSO Integration** — Enterprise identity provider support
- **Kubernetes Manifests** — Helm chart for production K8s deployment
- **Horizontal Scaling** — Multiple backend instances behind load balancer
- **Message Queue** — Redis/RabbitMQ replacing direct asyncio queues for reliability
- **Machine Learning Anomaly Detection** — Isolation Forest model for traffic anomalies
- **SIEM Integration** — Syslog forwarding to Splunk/Elastic/QRadar
- **Two-Way Slack Bot** — Receive alerts in Slack, acknowledge/block from Slack
- **API Key Management** — Per-user API keys for programmatic access

---

### 24.5 Version 3.0.0 — AI-Powered Security

**Theme:** Intelligent Threat Analysis

**New Features:**
- **LLM Alert Triage** — AI assistant that explains what an alert means in plain English
- **Attack Chain Visualization** — Visual kill chain diagram from correlated alerts
- **Predictive Blocking** — ML model predicts high-risk IPs before they attack
- **Natural Language Rule Generation** — "Detect SSH brute force" → generates Suricata rule
- **Automated Incident Reports** — LLM-written incident report from alert cluster
- **Threat Intelligence Graph** — Network graph of attacker infrastructure relationships
- **Container Network Monitoring** — Monitor Docker/K8s pod-to-pod traffic
- **CVE Alert Enrichment** — Map detected exploits to CVE database automatically

---

## 25. FINAL DEVELOPMENT PLAN

### Phase 0: Repository Bootstrap (Day 1)
**Objectives:** Create the professional GitHub repository structure before writing any code.

**Tasks:**
1. Create `CodeAlpha_NetworkIntrusionDetectionSystem` repository on GitHub (public)
2. Configure repository settings: topics, social preview, website link
3. Create all folders from the folder structure section (using `mkdir -p`)
4. Add `.gitignore`, `.editorconfig`, `LICENSE` (MIT)
5. Create `README.md` stub with hero banner placeholder
6. Create all GitHub template files: issue templates, PR template, CODEOWNERS
7. Configure branch protection rules (require PR for `main`)
8. Enable GitHub Discussions, Issues, Dependabot
9. Create GitHub Actions workflow stubs (will fill in Phase 7)
10. Push initial commit: `chore(init): initialize repository structure`

**Acceptance Criteria:**
- Repository is public and visible
- Folder structure exists (empty files with `.gitkeep` where needed)
- All GitHub templates in place
- Branch protection configured

---

### Phase 1: Development Environment (Day 1–2)
**Objectives:** Configure the complete development environment and tooling.

**Tasks:**
1. Create `backend/pyproject.toml` with Black, Ruff, mypy configuration
2. Create `backend/requirements.txt` and `backend/requirements-dev.txt` with all pinned packages
3. Create `frontend/package.json` with all npm dependencies
4. Create `frontend/tsconfig.json` (strict mode)
5. Create `frontend/tailwind.config.ts` with complete design system colors/fonts
6. Create `backend/core/config.py` — Pydantic Settings loading all env vars
7. Create `backend/core/logging.py` — structlog configuration
8. Create `backend/core/constants.py` — system-wide constants
9. Create all `__init__.py` files (empty) for proper Python packaging
10. Create `backend/.env.example` and `frontend/.env.local.example`
11. Test: `ruff check backend/` passes, `tsc --noEmit` passes

**Acceptance Criteria:**
- `pip install -r requirements.txt` succeeds
- `npm install` succeeds
- Linting tools report no errors on empty files
- `pyproject.toml` configured with correct tool settings

---

### Phase 2: Database Layer (Day 2–3)
**Objectives:** Build the complete database model and migration system.

**Tasks:**
1. Create `backend/core/database.py` — SQLAlchemy async engine + session factory
2. Create `backend/models/base.py` — Declarative base with `TimestampMixin`
3. Create all model files: `alert.py`, `event.py`, `rule.py`, `response_log.py`, `statistics.py`, `user.py`, `audit_log.py`, `blocked_ip.py`
4. Initialize Alembic: `alembic init backend/database/migrations`
5. Configure `alembic.ini` and `env.py` for async SQLAlchemy
6. Create initial migration: `alembic revision --autogenerate -m "create_initial_schema"`
7. Create `backend/database/seed.py` — seeds admin user + 50 sample alerts for development
8. Write unit tests for every model (field types, constraints, relationships)
9. Run migration and seed: `alembic upgrade head && python -m database.seed`
10. Verify schema in SQLite browser

**Acceptance Criteria:**
- All 8 tables created by migration
- Seed script creates admin user (`admin` / `changeme123`) and 50 sample alerts
- `pytest tests/backend/unit/test_models.py` passes
- Foreign key relationships enforced

---

### Phase 3: Repository + Service Layers (Day 3–4)
**Objectives:** Build the data access and business logic layers.

**Tasks:**
1. Create `backend/repositories/base.py` — Generic async `BaseRepository[T]`
2. Implement all repository classes: `AlertRepository`, `RuleRepository`, `EventRepository`, `ResponseRepository`, `StatisticsRepository`, `UserRepository`
3. Create `backend/schemas/` — all Pydantic v2 schemas for requests, responses, and filters
4. Create `backend/schemas/common.py` — `PaginatedResponse[T]`, `ErrorResponse`
5. Create `backend/services/auth_service.py` — JWT token creation, password hashing, user auth
6. Create `backend/services/alert_service.py` — full alert lifecycle logic
7. Create `backend/services/rule_service.py` — rule CRUD + file writing + SIGHUP trigger
8. Create `backend/services/statistics_service.py` — aggregation queries
9. Create `backend/services/report_service.py` — CSV/PDF generation
10. Create `backend/core/exceptions.py` — all custom exception classes
11. Create `backend/core/dependencies.py` — all FastAPI `Depends()` factories
12. Write comprehensive unit tests for all service methods (mock repositories)

**Acceptance Criteria:**
- All service methods have unit tests
- Services compile without import errors
- `pytest tests/backend/unit/test_*_service.py` — all pass
- Minimum 90% coverage on service layer

---

### Phase 4: Detection Engine Integration (Day 4–5)
**Objectives:** Build the Suricata integration and real-time alert pipeline.

**Tasks:**
1. Create `backend/detection/eve_parser.py` — parses all EVE event types into typed Python objects
2. Create `backend/detection/eve_log_watcher.py` — asyncio file tail with watchdog
3. Create `backend/detection/alert_manager.py` — deduplication, severity classification, enrichment, event bus publish
4. Create `backend/detection/geoip_enricher.py` — MaxMind GeoLite2 lookup with LRU cache
5. Create `backend/detection/rule_validator.py` — Suricata rule syntax validation
6. Create `backend/detection/suricata_manager.py` — start/stop/restart/SIGHUP via subprocess
7. Create `backend/detection/threat_intel.py` — stub for AbuseIPDB (v1.0 no-op, v1.1 implements)
8. Create `backend/core/event_bus.py` — asyncio internal publish/subscribe
9. Wire: `EVELogWatcher → EVEParser → AlertManager → EventBus`
10. Write comprehensive unit tests for EVEParser (all event types, edge cases, malformed JSON)
11. Write integration test: mock eve.json file → verify alerts appear in DB

**Acceptance Criteria:**
- EVE parser handles all 10+ Suricata event types without crashing
- Malformed JSON lines are logged and skipped (no crash)
- Alert created within 500ms of EVE log write
- Deduplication suppresses identical alerts within 60-second window
- `pytest tests/backend/unit/test_eve_parser.py` — 100% coverage

---

### Phase 5: Response Engine (Day 5)
**Objectives:** Build all automated response handlers.

**Tasks:**
1. Create `backend/response/base_handler.py` — abstract `BaseResponseHandler` with `should_handle()` + `handle()`
2. Create `backend/response/log_handler.py` — structured JSON file logging
3. Create `backend/response/email_handler.py` — SMTP email via `smtplib` + HTML template
4. Create `backend/response/webhook_handler.py` — HTTP POST with retry logic
5. Create `backend/response/firewall_handler.py` — `iptables` subprocess wrapper with whitelist check
6. Create `backend/response/ip_block_handler.py` — DB record + firewall rule + TTL management
7. Create `backend/response/notification_handler.py` — WebSocket push notification
8. Create `backend/response/response_engine.py` — orchestrator that reads config and executes applicable handlers
9. Subscribe `ResponseEngine` to `EventBus` `"new_alert"` events
10. Write unit tests for each handler with mocked dependencies
11. Create background scheduler job to clean up expired IP blocks

**Acceptance Criteria:**
- Each handler can be independently enabled/disabled via config
- Handlers fail gracefully (log error, continue to next handler)
- Email handler includes proper HTML template
- Firewall handler never blocks RFC1918 IPs
- IP block expires automatically after configured TTL

---

### Phase 6: FastAPI Application (Day 5–7)
**Objectives:** Build the complete REST API and WebSocket server.

**Tasks:**
1. Create `backend/main.py` — FastAPI app factory with lifespan, middleware stack, router registration
2. Create `backend/middleware/` — CORS, auth, rate_limiter, request_logger, error_handler
3. Create all route files: `alerts.py`, `rules.py`, `events.py`, `statistics.py`, `system.py`, `auth.py`, `reports.py`
4. Create `backend/api/websocket/manager.py` — `WebSocketManager` with connection pool and broadcast
5. Create `backend/api/websocket/handlers.py` — WebSocket endpoint handler
6. Implement every API endpoint listed in Section 13 with full request/response validation
7. Configure Uvicorn startup: bind to `0.0.0.0:8000`, log level `info`
8. Start background tasks in `lifespan`: EVELogWatcher, statistics aggregator, IP block cleanup scheduler
9. Write integration tests for every API endpoint (happy path + all error cases)
10. Verify OpenAPI schema at `/docs` — all endpoints documented with examples

**Acceptance Criteria:**
- All API endpoints return correct HTTP status codes
- Authentication enforced on all protected endpoints
- Rate limiting returns 429 after limit exceeded
- WebSocket broadcasts alert within 200ms of creation
- `pytest tests/backend/integration/test_*_api.py` — all pass
- FastAPI `/docs` page fully functional with all endpoints

---

### Phase 7: Next.js Dashboard (Day 7–12)
**Objectives:** Build the complete frontend SOC dashboard.

**Sub-phases:**

**7a: Infrastructure (Day 7)**
- Install all npm dependencies
- Configure `tailwind.config.ts` with complete design system
- Install and configure Shadcn UI components
- Create `frontend/lib/api.ts` — Axios instance with base URL, interceptors, JWT header injection
- Create `frontend/lib/constants.ts` — API endpoints, WebSocket URL
- Create all TypeScript type definitions in `frontend/types/`
- Create root layout with ThemeProvider (dark mode default)
- Create dashboard layout with Sidebar + Header components
- Create `frontend/hooks/useWebSocket.ts` with reconnect logic

**7b: Core Components (Day 8)**
- Build all `frontend/components/ui/` Shadcn components
- Build `Sidebar.tsx`, `Header.tsx`, `PageWrapper.tsx`
- Build `StatCard.tsx`, `AlertBadge.tsx`, `LoadingSpinner.tsx`, `EmptyState.tsx`, `ErrorState.tsx`
- Build `DataTable.tsx` using TanStack Table
- Build `CopyButton.tsx`, `ConfirmDialog.tsx`

**7c: Dashboard Page (Day 9)**
- Build `/dashboard` page with all 10 widgets
- Implement `AlertFeed.tsx` with WebSocket integration
- Implement `SeverityDonut.tsx`, `TrafficTimeline.tsx`, `TopAttackers.tsx`
- Connect all widgets to backend API endpoints
- Implement real-time stat counter updates

**7d: Alert Center (Day 9–10)**
- Build `/alerts` page with full-featured data table
- Build `AlertFilters.tsx` with all filter controls
- Build `AlertDetail.tsx` drawer with full metadata view
- Implement bulk selection and bulk actions
- Implement export functionality

**7e: Analytics, Monitoring, Rules (Day 10–11)**
- Build `/analytics` page with all 7 chart types
- Build `/monitoring` page with live event stream
- Build `/rules` page with rule editor and validator
- Build `/system` page with component health grid

**7f: Remaining Pages (Day 11–12)**
- Build `/logs`, `/reports`, `/settings`, `/about` pages
- Build auth `/login` page with JWT flow
- Add 404 and error pages
- Add Framer Motion page transitions
- Complete responsive breakpoints for all pages

**Acceptance Criteria:**
- All 10+ pages render without console errors
- Live alert feed updates in real-time via WebSocket
- Charts display data from API
- All forms validate input before submission
- Auth flow: login → JWT stored → protected routes require auth
- Responsive on 768px, 1024px, 1920px viewports
- No TypeScript compilation errors (`tsc --noEmit`)

---

### Phase 8: Docker & Deployment (Day 12–13)
**Objectives:** Containerize all services and test full-stack deployment.

**Tasks:**
1. Write `docker/Dockerfile.backend` with multi-stage build
2. Write `docker/Dockerfile.frontend` with multi-stage build
3. Write `docker/Dockerfile.suricata`
4. Write `docker/nginx.conf` — reverse proxy backend to `/api`, frontend to `/`
5. Write `docker-compose.yml` (development)
6. Write `deploy/docker-compose.prod.yml` (production hardening)
7. Write `scripts/setup.sh` — automates environment setup from scratch
8. Write `suricata/scripts/update_rules.sh` — pulls latest ET Open rules
9. Test: `docker-compose up -d` → verify all 4 containers start successfully
10. Test: Dashboard accessible at `http://localhost:3000`
11. Test: API accessible at `http://localhost:8000/docs`
12. Test: Suricata generating EVE logs → alerts appearing in dashboard

**Acceptance Criteria:**
- `docker-compose up -d` starts all services without errors
- Dashboard fully functional via Docker Compose
- Suricata capturing traffic in Docker environment
- `scripts/setup.sh` runs end-to-end without manual steps

---

### Phase 9: Testing & Quality (Day 13–14)
**Objectives:** Achieve target coverage and fix all quality issues.

**Tasks:**
1. Run full test suite: `pytest tests/ --cov=backend --cov-report=html`
2. Identify coverage gaps → add missing tests
3. Run `mypy backend/` — fix all type errors
4. Run `ruff check backend/` — fix all linting issues
5. Run `npx eslint frontend/` — fix all ESLint warnings
6. Run `bandit -r backend/` — fix any security findings
7. Run `pip-audit` — address any vulnerable dependencies
8. Performance test: verify 1000 alerts created in <10 seconds
9. Load test WebSocket: 10 concurrent clients receiving alerts simultaneously
10. Manual QA: test all 10 dashboard pages in Chrome, Firefox, Safari
11. Fix all bugs found during QA

**Acceptance Criteria:**
- Backend coverage ≥ 80% overall, ≥ 90% on services
- Zero mypy errors in strict mode
- Zero ruff errors
- Zero bandit HIGH/CRITICAL findings
- All manual QA test cases passing

---

### Phase 10: Documentation (Day 14–15)
**Objectives:** Complete all documentation to production standard.

**Tasks:**
1. Write `README.md` following blueprint in Section 19
2. Write `docs/INSTALLATION.md` — test every command
3. Write `docs/RULE_GUIDE.md` with example rules for all categories
4. Write `docs/API.md` — synchronized with FastAPI OpenAPI spec
5. Write `docs/ARCHITECTURE.md` with system diagram
6. Write `docs/DEPLOYMENT.md` covering Docker + manual + production
7. Write `docs/USER_GUIDE.md` with screenshots
8. Write `docs/FAQ.md` with 20+ common questions
9. Write `CONTRIBUTING.md` following Section 21
10. Write `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CHANGELOG.md`
11. Write `suricata/rules/README.md` — rule writing guide
12. Create all screenshots for documentation
13. Create demo GIF
14. Create banner and social preview images

**Acceptance Criteria:**
- README renders correctly on GitHub
- All documentation links work (no 404s)
- Installation guide tested on clean Ubuntu 22.04 VM
- All images display correctly

---

### Phase 11: Release (Day 15–16)
**Objectives:** Professional v1.0.0 GitHub release.

**Tasks:**
1. Final review of all code, documentation, and tests
2. Ensure all 26 sections of this blueprint are implemented
3. Update `CHANGELOG.md` with v1.0.0 entry
4. Create release branch: `git checkout -b release/v1.0.0`
5. Final commit: `chore(release): prepare v1.0.0`
6. Merge to `main` via PR
7. Create and push git tag: `git tag v1.0.0 && git push origin v1.0.0`
8. GitHub Actions release workflow fires automatically
9. Verify Docker images published to GHCR
10. Write release notes on GitHub Releases page
11. Add repository to GitHub profile pinned repos
12. Share on LinkedIn (portfolio post)

**Acceptance Criteria:**
- `v1.0.0` tag created and visible on GitHub
- Release notes published on GitHub Releases
- Docker images available on `ghcr.io/harisx404/`
- Repository pinned on GitHub profile
- All CI checks passing on `main`

---

## 26. RULES FOR THE AI CODING AGENT

These are **absolute, non-negotiable implementation rules**. Violating any of these rules is not permitted under any circumstances.

---

### Rule 1 — NEVER skip reading this blueprint
Before writing a single line of code, re-read the relevant section of this blueprint. Do not rely on prior knowledge or assumptions. Every architectural decision is documented here. Follow it.

---

### Rule 2 — STRICT folder structure enforcement
All files must be created in their designated folder exactly as specified in Section 5. Never create files in the wrong location. Never create files at the root level that belong in subfolders. Never deviate from the naming convention.

```
# WRONG
backend/alert_service.py         ← breaks folder structure
backend/api/routes/alertservice.py ← wrong name format

# CORRECT
backend/services/alert_service.py
backend/api/v1/routes/alerts.py
```

---

### Rule 3 — ZERO hardcoded secrets
Never hardcode passwords, API keys, JWT secrets, database URLs, SMTP credentials, or any sensitive value in code. Every secret is loaded from environment variables via `backend/core/config.py`.

```python
# WRONG
JWT_SECRET = "super-secret-key-123"
DATABASE_URL = "postgresql://admin:password123@localhost/nids"

# CORRECT
JWT_SECRET_KEY: str = Field(..., env="JWT_SECRET_KEY")
DATABASE_URL: str = Field(..., env="DATABASE_URL")
```

---

### Rule 4 — NEVER break the layered architecture
The dependency direction is strictly one-way: `Route → Service → Repository → Model`. No layer may import from a higher layer.

```python
# WRONG — service importing from route
from backend.api.v1.routes.alerts import AlertRouter

# WRONG — repository importing from service
from backend.services.alert_service import AlertService

# CORRECT — dependency flows downward only
# In service: from backend.repositories.alert_repository import AlertRepository
# In route: from backend.services.alert_service import AlertService
```

---

### Rule 5 — EVERY function must be documented
No function, method, or class may exist without a docstring (Python) or JSDoc comment (TypeScript). One-line utilities may use a single-line docstring. Complex functions require full Args/Returns/Raises documentation.

```python
# WRONG
def calculate_severity(priority: int) -> Severity:
    return PRIORITY_MAP.get(priority, Severity.INFO)

# CORRECT
def calculate_severity(priority: int) -> Severity:
    """Map Suricata alert priority to NIDS severity level.

    Args:
        priority: Suricata priority integer (1=highest, 4=lowest).

    Returns:
        Severity: Corresponding NIDS severity enum value.
    """
    return PRIORITY_MAP.get(priority, Severity.INFO)
```

---

### Rule 6 — EVERY feature needs a test
For every function written, a corresponding test must be written. No feature is "done" without a test. Minimum test requirements:
- Happy path test
- Edge case test (empty input, None, boundary values)
- Error case test (what happens when it fails)

---

### Rule 7 — NO duplicate code
If the same logic appears twice, extract it. Utility functions live in `backend/utils/`. Shared React components live in `frontend/components/common/`. Never copy-paste logic between modules.

---

### Rule 8 — ASYNC consistency in backend
All Python backend code that performs I/O must be `async/await`. Never use `time.sleep()` (use `asyncio.sleep()`). Never use synchronous file I/O (use `aiofiles`). Never use synchronous HTTP clients (use `httpx.AsyncClient`). Never use synchronous database queries (use SQLAlchemy 2.0 async).

```python
# WRONG
def get_alerts():
    return db.execute("SELECT * FROM alerts").fetchall()

# CORRECT
async def get_alerts():
    result = await db.execute(select(Alert))
    return result.scalars().all()
```

---

### Rule 9 — TypeScript strict mode is non-negotiable
`tsconfig.json` must have `"strict": true`. Every TypeScript file must be properly typed. `any` is forbidden (use `unknown` if truly necessary, with proper type narrowing). No TypeScript compilation errors are acceptable.

```typescript
// WRONG
const handleAlert = (data: any) => { ... }

// CORRECT
const handleAlert = (data: AlertResponse) => { ... }
```

---

### Rule 10 — Meaningful commit messages
Every `git commit` must follow the Conventional Commits specification from Section 17. No commits with messages like "fix", "update", "changes", or "working now".

```bash
# WRONG
git commit -m "fix"
git commit -m "added stuff"

# CORRECT
git commit -m "feat(detection): add GeoIP enrichment to alert manager"
git commit -m "fix(api): resolve pagination offset calculation error for large datasets"
```

---

### Rule 11 — Security first
Before implementing any user-facing input handling:
1. Validate all inputs with Pydantic schemas
2. Check for SQL injection via parameterized queries (SQLAlchemy)
3. Check for path traversal on file paths
4. Sanitize before writing to disk (especially Suricata rule content)
5. Never log sensitive data (passwords, tokens, raw packet payloads in app logs)

---

### Rule 12 — Error handling is mandatory
No function may let an exception propagate unhandled to the user. Every exception must either:
- Be caught and re-raised as a typed domain exception, OR
- Be caught at the route level by the global exception handler

```python
# WRONG — unhandled exception reaches user
async def create_alert(self, data: AlertCreate) -> AlertResponse:
    return await self.repository.create(data)

# CORRECT — caught and re-raised with context
async def create_alert(self, data: AlertCreate) -> AlertResponse:
    try:
        return await self.repository.create(data)
    except IntegrityError as e:
        raise AlertCreationError(
            f"Failed to create alert: duplicate detection"
        ) from e
```

---

### Rule 13 — Environment-aware configuration
Code must behave differently based on `APP_ENV`:
- `development`: verbose logging, hot reload, detailed error messages, SQLite
- `production`: minimal logging, no reload, generic error messages, connection pooling

```python
if settings.APP_ENV == "development":
    log_level = "DEBUG"
    app.add_middleware(DetailedErrorMiddleware)
else:
    log_level = "WARNING"
```

---

### Rule 14 — Database migrations only via Alembic
Never modify the database schema directly. Never use `Base.metadata.create_all()` in production code (only in tests). All schema changes go through an Alembic migration file with both `upgrade()` and `downgrade()` implementations.

---

### Rule 15 — Component reusability in frontend
Before creating a new React component, check if an existing component can be reused or extended. Components in `frontend/components/common/` are universal — use them. Never duplicate component logic. Prefer composition over custom variants.

---

### Rule 16 — API contract enforcement
The API response format is fixed (Section 13). Every API endpoint must return a response matching the envelope `{ success, data, message, meta }`. Never return raw objects from routes. Never break the contract without a major version bump.

---

### Rule 17 — No `console.log` in production code
All debugging output must use the logging system:
- Python: `log.debug(...)`, `log.info(...)` via structlog
- TypeScript: `console.error(...)` for errors only, never `console.log` in components

Remove all debugging statements before committing.

---

### Rule 18 — Suricata must be config-file driven
Never call `suricata` with inline rule strings or ad-hoc arguments. All Suricata configuration lives in `suricata/config/suricata.yaml`. All rules live in `suricata/rules/`. Never modify Suricata behavior via subprocess arguments when the equivalent config setting exists.

---

### Rule 19 — WebSocket connections must handle disconnection
The WebSocket manager must:
- Track all connected clients in a set
- Remove clients on disconnect (clean up the set)
- Not raise exceptions when broadcasting to a disconnecting client
- Handle reconnection from the frontend with exponential backoff

```python
async def broadcast(self, message: str) -> None:
    disconnected = set()
    for connection in self.active_connections:
        try:
            await connection.send_text(message)
        except WebSocketDisconnect:
            disconnected.add(connection)
    # Clean up disconnected clients
    self.active_connections -= disconnected
```

---

### Rule 20 — The project must run from a clean clone
After all code is committed, test this exact sequence on a fresh machine:

```bash
git clone https://github.com/harisx404/CodeAlpha_NetworkIntrusionDetectionSystem.git
cd CodeAlpha_NetworkIntrusionDetectionSystem
docker-compose up -d
```

If the project does not run after these 3 commands, the implementation is incomplete.

---

### Rule 21 — Never commit generated or sensitive files
`.gitignore` must exclude:
```
.env
.env.local
*.pyc
__pycache__/
.venv/
venv/
node_modules/
.next/
database/*.db
logs/
*.log
*.mmdb        # GeoIP database files
GeoLite2-*.mmdb
dist/
build/
coverage/
.mypy_cache/
.ruff_cache/
```

---

### Rule 22 — Pagination on all list endpoints
No API endpoint may return an unbounded list of results. Every endpoint that returns a list must implement cursor-based or offset-based pagination with `page`, `per_page` (max 100), and `total` in the response meta.

---

### Rule 23 — Maintain `CHANGELOG.md` throughout development
Every feature addition, bug fix, or breaking change must be added to `CHANGELOG.md` in [Keep a Changelog](https://keepachangelog.com/) format as it is developed — not retroactively at release time.

---

### Rule 24 — All Suricata rules must be tested
Every custom rule written for `suricata/rules/custom.rules` must be validated with:
1. Rule syntax validation (via `suricata -T -c suricata.yaml`)
2. PCAP replay test with `suricata -r test.pcap` using a relevant test PCAP
3. Documentation in `suricata/rules/README.md` explaining what the rule detects

---

### Rule 25 — Code must look human-built
This project is for a professional portfolio reviewed by human engineers. Code must:
- Be naturally readable
- Avoid AI-patterned generic naming (`process_data`, `handle_stuff`)
- Use domain-appropriate terminology (`enrich_alert_with_geoip`, `broadcast_alert_to_analysts`)
- Have realistic, thoughtful comments that explain *why*, not *what*
- Show engineering judgment in architecture decisions (not just "it works")

---

*End of Master Blueprint — Version 1.0.0*

---

> **Agent Implementation Note:**
> Follow phases in order. Do not skip ahead.
> Each phase has explicit acceptance criteria that must pass before moving to the next.
> When in doubt about any implementation detail, refer to the relevant section of this blueprint.
> This blueprint is the single source of truth.
> Build it like you are shipping to a Fortune 500 SOC team.
