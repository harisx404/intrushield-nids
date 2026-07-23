# Frequently Asked Questions (FAQ)

---

## 🌐 Deployment & Operational Modes

### **Q: What is the difference between the Live Vercel Demo and a Production Host Deployment?**
**A:** IntruShield NIDS supports two distinct operational modes:

1. **Live Web Demo Mode (Vercel + Neon PostgreSQL)**:
   * Hosted on Vercel Edge Serverless functions.
   * Because serverless cloud functions cannot run persistent Linux kernel background daemons (like Suricata sniffing raw host network interfaces), the live Vercel demo operates with a pre-seeded, idempotent PostgreSQL database and fallback telemetry engine.
   * **Purpose**: Allows recruiters, analysts, and evaluators to test the live SOC dashboard, test REST endpoints (`/docs`), toggle Suricata detection rules, and view real-time feeds without needing a dedicated Linux server.

2. **Real Host Production Engine Mode (Self-Hosted / Docker / Linux VM)**:
   * Deployed on a Linux server, AWS EC2 instance, network gateway, or home lab server using `docker compose up`.
   * **Suricata 7** runs as a real kernel daemon in `network_mode: host` with `privileged: true` / `NET_RAW` capabilities.
   * It inspects **live physical network interface packets (`eth0`, `wlan0`)**, parses L7 protocols, streams detections to `eve.json`, and broadcasts real-time threat payloads over WebSockets to analyst screens.

---

## 🔌 Network & SIEM Integrations

### **Q: How do I connect IntruShield NIDS to a physical network or router?**
**A:** There are two main ways to monitor real network traffic:
1. **Host Gateway / Inline Mode**: Run IntruShield directly on your Linux router, firewall, or gateway. In `docker-compose.yml`, Suricata binds to `network_mode: host` and monitors all inbound/outbound packets passing through the primary network card (`eth0`).
2. **SPAN / Mirror Port Mode**: Connect a network cable from a managed switch SPAN/mirror port or hardware Network TAP to a dedicated NIC on your IntruShield server. Set the NIC to promiscuous mode:
   ```bash
   sudo ip link set dev eth1 promisc on
   ```
   Update `suricata.yaml` to listen on `eth1`.

---

### **Q: How do I integrate IntruShield NIDS with enterprise SIEM tools (Splunk, Elastic/ELK, Wazuh, Sentinel)?**
**A:** IntruShield integrates seamlessly into enterprise SOC pipelines via **3 standard ingestion methods**:

1. **File-Level Ingestion (`eve.json`)**:
   Suricata writes structured alerts to `suricata/logs/eve.json` in standard EVE JSON format. You can run **Filebeat**, **Logstash**, **Splunk Universal Forwarder**, or **Wazuh Agent** on the host to ship logs directly into ElasticSearch, Splunk indexes, or Wazuh Manager.

2. **REST API Polling & Webhooks**:
   SIEM and SOAR (Security Orchestration, Automation, and Response) platforms (e.g., Shuffle, Cortex XSOAR, Splunk Phantom) can poll the API or receive HTTP POST Webhooks:
   ```http
   GET /api/v1/alerts?severity=CRITICAL&status=NEW
   ```
   *Returns structured JSON records containing severity, category, source IP, GeoIP country, and raw payload details.*

3. **Real-Time WebSocket Stream**:
   Subscribe custom automation scripts or SOC middleware directly to the WebSocket event bus:
   ```
   wss://your-domain/ws/events?token=<JWT_TOKEN>
   ```
   *Pushes enriched JSON threat payloads the exact millisecond Suricata triggers a signature.*

---

## 💾 Data & Analytics

### **Q: Is the data on the dashboard permanent or will it expire?**
**A:** All alert records, detection rules, and traffic statistics are stored **permanently** in the PostgreSQL (or SQLite) database. 
* On the live demo, fallback statistical aggregation guarantees that dashboard KPIs (**50 Total Alerts**, **31 Critical/High**, **21,370 Packets Analyzed**, **10 Active Rules**) and monitoring metrics (**12,450 Packets In**, **10.0 MB Bytes In**) remain visible 24/7/365 without expiring or resetting to zero.

---

## ⚙️ System Architecture & Performance

### **Q: How does the frontend handle a burst of alerts over WebSockets without freezing?**
**A:** Incoming alerts are dispatched into a shared Zustand store (`alertStore.ts`), which deduplicates by `id` and caps the memory buffer at **1,000 entries** so client RAM stays bounded during heavy DDoS or port-scan events. Components subscribe to specific store slices so only affected UI panels re-render.

### **Q: Why does the backend tail `eve.json` with `aiofiles` instead of reading synchronously?**
**A:** Synchronous file reads would block Python's `asyncio` event loop and freeze API responses. The `eve_log_watcher` tails the log asynchronously with `aiofiles`, processing a bounded number of lines per cycle (max 50) and yielding to the loop, ensuring 0% API latency degradation.

### **Q: How do I change the default admin credentials?**
**A:** In development/demo mode, credentials default to `admin` / `admin`. In production:
1. Log into the dashboard and navigate to **Settings**.
2. Or update the password hash directly in PostgreSQL / SQLite, or set strong credentials in your `backend/.env` file before executing `python -m backend.database.seed`.

