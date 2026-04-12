# 🛡️ Adaptive File System Honeypot Agent

**Authors:** Aryan Jakkal & Dhirayshil Sarwade  
**Project Type:** Diploma Final Year Project  
**Domain:** Cybersecurity — Intrusion Detection & Deception Technology

---

## 📌 Overview

The Adaptive File System Honeypot Agent is a proactive cybersecurity system that monitors file systems in real-time, detects suspicious behavior using an intelligent threat scoring algorithm, and automatically deploys decoy files to trap attackers.

Unlike traditional reactive security tools, this system **adapts its defense strategy** based on the current threat level — deploying convincing fake files when suspicious activity is detected, then alerting administrators the moment an attacker touches them.

---

## 🎯 Key Features

- **Real-Time File Monitoring** — Watches directories continuously using the watchdog library
- **Intelligent Threat Scoring** — Multi-rule algorithm (0–100 scale) with 4 detection rules
- **Adaptive Decoy Deployment** — Automatically deploys fake credential and document files when threat score ≥ 51
- **Attack Tracking** — Records forensic data (timestamp, file, action, threat level) for every decoy access
- **Alert System** — Structured alerts with 4 severity levels (Low, Medium, High, Critical)
- **Live Web Dashboard** — Real-time monitoring UI with threat visualization, event feed, and attack log
- **Windows Service** — Runs as a background service, auto-starts on boot

---

## 🔗 How It Works

```
File Event Detected
        ↓
ThreatDetector scores it (0–100)
        ↓
Score ≥ 51 → DecoyManager deploys fake files
        ↓
Attacker accesses a decoy file
        ↓
AttackTracker records forensic data
AlertManager fires Critical alert
        ↓
Dashboard updates in real-time 🚨
```

### Threat Scoring Rules

| Rule | Condition | Points |
|------|-----------|--------|
| Rapid Access | 5+ files in 10 seconds | +20 |
| Unusual Time | Activity midnight–5AM | +15 |
| Sensitive Files | Keywords: password, key, token, secret | +25 |
| Mass Deletion | 3+ deletions in 30 seconds | +30 |

### Threat Levels

| Score | Level | Action |
|-------|-------|--------|
| 0–30 | 🟢 Normal | Monitor only |
| 31–50 | 🟡 Elevated | Log warning |
| 51–70 | 🟠 Suspicious | Deploy 2 decoys |
| 71–100 | 🔴 Critical | Deploy 4 decoys + alert |

---

## 🏗️ Architecture

This project follows **Clean Architecture** principles:

```
src/
├── agent/                  # Entry point + Windows service
├── dashboard/              # Flask web dashboard
│   └── templates/          # HTML/CSS/JS frontend
├── monitor/                # Core monitoring layer
│   ├── file_monitor.py     # Real-time file system watcher
│   ├── threat_detector.py  # Scoring algorithm
│   ├── decoy_manager.py    # Decoy deployment bridge
│   ├── attack_tracker.py   # Forensic attack logging
│   └── logger.py           # Event logging
├── alert/
│   └── manager.py          # Alert system
└── domain/                 # Clean Architecture layers
    ├── entities/            # Core business objects
    ├── interfaces/          # Abstract contracts
    ├── application/         # Business logic (use cases)
    └── infrastructure/      # External dependencies (Faker)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/ARYANJAKKAL123/Adaptive-Honeypot-Security-Agent.git
cd Adaptive-Honeypot-Security-Agent

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -e ".[dev]"
pip install flask flask-socketio pywin32
```

### Configuration

Edit `config/config.yaml` to set your watch directory:

```yaml
monitoring:
  watch_directories:
    - "path/to/your/directory"

threat_detection:
  threshold: 50
```

### Running

**Option 1 — Dashboard (recommended):**
```bash
python src/dashboard/app.py
# Open http://localhost:5000
```

**Option 2 — Agent only (terminal):**
```bash
python src/agent/main.py
```

**Option 3 — Windows Service:**
```bash
python src/agent/service.py install
python src/agent/service.py start
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

**Results: 20/20 tests passing ✅**

| Test File | Tests | Status |
|-----------|-------|--------|
| simple_test.py | 4 | ✅ |
| test_alert_manager.py | 6 | ✅ |
| test_alert_integration.py | 2 | ✅ |
| test_decoy_deployment.py | 4 | ✅ |
| test_decoy_tracking.py | 3 | ✅ |
| test_full_system.py | 1 | ✅ |

---

## 📊 Dashboard

The web dashboard provides real-time visibility into the honeypot system:

- **Threat Score Gauge** — Live 0–100 score with color-coded levels
- **Live Event Feed** — Every file creation, modification, deletion
- **Security Alerts** — Structured alerts when decoys are accessed
- **Deployed Decoys Panel** — Shows active decoy files with type and timestamp
- **Attack Log Table** — Forensic record of every attacker interaction
- **Reset Button** — Clear state for a fresh demo

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Core language |
| watchdog | File system monitoring |
| Faker | Realistic decoy content generation |
| Flask | Web dashboard backend |
| Flask-SocketIO | Real-time WebSocket updates |
| PyYAML | Configuration management |
| pytest | Testing framework |
| pywin32 | Windows service support |

---

## 📁 Project Structure

```
Adaptive-Honeypot-Security-Agent/
├── src/                    # Source code
├── tests/                  # Test suite (20 tests)
├── config/                 # Configuration files
├── docs/                   # Learning documentation
├── decoys/                 # Deployed decoy files (auto-generated)
├── logs/                   # Event, alert, and attack logs
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

---

## 🔒 Security Concepts Demonstrated

- **Honeypot Technology** — Deception-based intrusion detection
- **Behavioral Analysis** — Pattern recognition over time windows
- **Threat Intelligence** — Scoring algorithms for risk assessment
- **Forensic Logging** — Structured JSON attack records
- **Defense in Depth** — Multiple detection layers working together

---

## 👥 Authors

- **Aryan Jakkal** — [GitHub](https://github.com/ARYANJAKKAL123)
- **Dhirayshil Sarwade**

---

*Diploma Final Year Project — Cybersecurity*
