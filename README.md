# IntruShield NIDS — Autonomous Network Intrusion Detection & Threat Telemetry Platform

<div align="center">

  <img src="https://img.shields.io/badge/version-1.3.0-blue.svg" alt="Version" />
  <a href="https://github.com/harisx404/intrushield-nids/actions/workflows/ci.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/harisx404/intrushield-nids/ci.yml?branch=main&label=CI" alt="CI Status" />
  </a>
  <img src="https://img.shields.io/badge/python-3.12-blue.svg" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/next.js-14-black.svg" alt="Next.js 14" />
  <img src="https://img.shields.io/badge/suricata-7.0-red.svg" alt="Suricata 7.0" />
  <img src="https://img.shields.io/badge/deployed-Vercel-000000?logo=vercel" alt="Deployed on Vercel" />
  <img src="https://img.shields.io/badge/docker-compose-2496ED.svg?logo=docker&logoColor=white" alt="Docker Compose" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />

</div>

<br/>

**IntruShield NIDS** is an **enterprise-grade Security Operations Center (SOC) platform and threat telemetry engine** designed and built by **[Muhammad Haris](https://github.com/harisx404)**.

It seamlessly orchestrates **Suricata 7** (deep packet inspection engine) with a high-performance async **FastAPI** backend and a responsive **Next.js 14** analytics dashboard — delivering instant threat visibility from raw network wire traffic to analyst screens over WebSockets with zero polling latency.

> 🌐 **Live Production Demo:** [https://intrushield-nids.vercel.app](https://intrushield-nids.vercel.app)

---

## 🔑 Quick Login

| Field | Value |
|-------|-------|
| **URL** | [https://intrushield-nids.vercel.app](https://intrushield-nids.vercel.app) |
| **Username** | `admin` |
| **Password** | `admin` |
| **API Docs** | `/docs` |

> ⚠️ Change credentials before deploying to a real production environment.

---

## 📸 Platform Screenshots

<div align="center">
  <h3>Security Command — Real-Time SOC Dashboard</h3>
  <img src="docs/screenshots/intrushield-nids-dashboard.png" alt="Security Command SOC Dashboard" width="100%" />

  <br/><br/>

  <h3>Alert Center — Live Incident Log & Filtering</h3>
  <img src="docs/screenshots/intrushield-nids-alerts.png" alt="Alert Center Incident Log" width="100%" />

  <br/><br/>

  <h3>Detection Rules — Suricata Signature Management</h3>
  <img src="docs/screenshots/intrushield-nids-rules.png" alt="Suricata Detection Rules" width="100%" />

  <br/><br/>

  <h3>System Monitoring — Traffic Throughput & Component Metrics</h3>
  <img src="docs/screenshots/intrushield-nids-monitoring.png" alt="System Monitoring Metrics" width="100%" />
</div>

---

## 🎯 What This Project Demonstrates

| Engineering Domain | Highlights & Capabilities |
|--------------------|---------------------------|
| **Async Python** | FastAPI, SQLAlchemy async sessions, `aiofiles` log-tailing pipeline |
| **Real-Time Delivery** | Zero-latency WebSocket broadcast manager & auto-reconnecting clients |
| **Security Engineering** | Suricata IDS integration, signature rulesets, JWT authentication, audit logging |
| **Data Pipeline** | EVE JSON stream parsing, GeoIP2 enrichment, sliding-window deduplication |
| **Frontend Architecture** | Next.js 14, Zustand state management, Recharts analytics |
| **DevOps & CI/CD** | Multi-stage Docker builds, Vercel Serverless, GitHub Actions CI |

---

## ⚡ Quick Start (30 Seconds)

### Run via Docker Compose

```bash
git clone https://github.com/harisx404/intrushield-nids.git
cd intrushield-nids

# Build and launch containers (database seeds automatically)
docker compose up --build -d

# View live backend logs
docker compose logs -f backend
```

Access the SOC Dashboard live at **`http://localhost`**.

---

## 📚 Documentation Directory

Complete technical documentation, architecture deep dives, deployment blueprints, and SIEM integration guides are organized inside the [`docs/`](docs/) directory:

| Guide | Description | Link |
|-------|-------------|------|
| 🏗️ **System Architecture** | Domain-Driven Design, packet pipeline, & async data flow | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 🔌 **API Reference** | REST endpoints, WebSocket schema, & authentication | [docs/API.md](docs/API.md) |
| 🌐 **Deployment Guide** | Docker Host Mode, NGINX proxy, & Vercel deployment | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| 🛡️ **Detection Rules Guide** | Writing custom Suricata signatures & hot-reloading | [docs/RULE_GUIDE.md](docs/RULE_GUIDE.md) |
| 📖 **User Operations Manual** | SOC analyst dashboard usage & incident response workflow | [docs/USER_GUIDE.md](docs/USER_GUIDE.md) |
| ❓ **Enterprise FAQ** | Network SPAN/TAP setup, persistent telemetry & SIEM ingestion | [docs/FAQ.md](docs/FAQ.md) |

---

## 🛡️ Enterprise SIEM Integration

IntruShield NIDS supports native log forwarding and integration with enterprise SIEM platforms:

* **File-Based**: Tailing `suricata/logs/eve.json` via Filebeat, Logstash, Splunk Universal Forwarder, or Wazuh Agent.
* **REST API Polling**: Polling `/api/v1/alerts` from Cortex XSOAR, Shuffle, or Splunk Phantom.
* **WebSocket Stream**: Pushing real-time alert JSON payloads directly to SIEM webhooks.

> Detailed SIEM setup instructions are available in [docs/FAQ.md](docs/FAQ.md).

---

## 👤 Author & License

Designed and engineered by **[Muhammad Haris](https://github.com/harisx404)**.  
Distributed under the **MIT License**.
