# 🛡️ CypherMind — Self-Learning AI Penetration Testing Copilot

> **An autonomous, multi-agent AI framework for ethical penetration testing, threat modeling, vulnerability research, and bug bounty automation powered by Reinforcement Learning, Hybrid RAG, Taint Analysis, and Red vs Blue Self-Play.**

<p align="center">

![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue.svg)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

</p>

---

## 📖 Overview

CypherMind is an AI-native penetration testing platform that combines **Large Language Models**, **Reinforcement Learning**, **Hybrid Retrieval-Augmented Generation (RAG)**, **Static Code Analysis**, **Taint Tracking**, and **Multi-Agent Collaboration** to automate security assessments.

Unlike traditional vulnerability scanners, CypherMind continuously learns from previous engagements and analyst feedback to improve future testing strategies.

It is designed for:

- 🛡️ Ethical Hackers
- 🎯 Bug Bounty Hunters
- 🔍 Security Researchers
- 👨‍💻 Application Security Engineers
- 🏢 Security Teams
- 🎓 Cybersecurity Education

---

# ✨ Features

## 🤖 AI Multi-Agent Security Swarm

Multiple specialized AI agents collaborate together.

| Agent | Responsibility |
|---------|---------------|
| 🔎 Recon Agent | Asset discovery, DNS enumeration, HTTP fingerprinting |
| 🧪 SAST Agent | Static Application Security Testing |
| 💥 Exploit Agent | Payload generation & vulnerability verification |
| 🔐 Post-Exploit Agent | Privilege escalation & impact analysis |
| 🐞 Bug Bounty Agent | Autonomous bug bounty workflow |

---

## 🧠 Reinforcement Learning Orchestrator

CypherMind uses **Q-Learning** to determine which security agents should execute for each engagement.

### State

```
(Target Type,
Technology Stack,
Programming Language,
Open Ports,
Detected Services)
```

### Action

```
Bitmask representing
Recon
SAST
Exploit
Post Exploit
```

### Reward

```
Reward =
(Vulnerability Count
× Average Severity
× Novelty Score)
/ Execution Time
```

Over time the orchestrator learns the most efficient testing strategy.

---

## 📚 Hybrid Retrieval-Augmented Generation (Hybrid RAG)

CypherMind combines multiple retrieval strategies.

- ✅ Dense Vector Search (ChromaDB)
- ✅ BM25 Keyword Retrieval
- ✅ Reciprocal Rank Fusion
- ✅ Cross Encoder Re-ranking

This dramatically improves LLM context quality.

---

## 🔍 Taint Analysis Engine

Automatically constructs source-to-sink data flow graphs.

Detects:

- SQL Injection
- Command Injection
- Path Traversal
- XSS
- Unsafe Deserialization
- Missing Sanitization

Powered by

- Python AST
- tree-sitter
- NetworkX

---

## ⚔️ Red vs Blue Self-Play

A continuous learning environment where

### 🔴 Red Team

- Generates exploits
- Creates payloads
- Finds attack paths

### 🔵 Blue Team

- Produces secure patches
- Suggests mitigations
- Improves code

Novel attacks are automatically stored inside the knowledge base for future retrieval.

---

## 📊 Interactive Dashboard

Real-time monitoring includes

- Live agent execution
- Vulnerability timeline
- Severity distribution
- Knowledge Base growth
- RL statistics
- WebSocket streaming
- Taint graph visualization

---

## 💬 Tool-Augmented AI Security Chat

The assistant can call tools during conversations.

Supported tools include

- Web Search
- CVE Lookup
- HTTP Probe
- Knowledge Base Search
- Nuclei
- Nmap
- DNS Lookup
- WHOIS
- URL Analysis

Every answer supports citations and reasoning traces.

---

## 🐞 Autonomous Bug Bounty Copilot

The Bug Bounty Agent can autonomously perform:

- Scope validation
- Reconnaissance
- Technology fingerprinting
- Payload generation
- Vulnerability verification
- Report generation

All while respecting defined scope restrictions.

---

# 🏗️ System Architecture

```
                    ┌────────────────────────────┐
                    │       User Interface        │
                    │  Dashboard / Chat / Hunt    │
                    └──────────────┬──────────────┘
                                   │
                     REST API / WebSockets
                                   │
                    ┌──────────────▼──────────────┐
                    │      FastAPI Backend         │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
 RL Orchestrator            Multi-Agent Swarm         Hybrid RAG Engine
 (Q-Learning)          Recon • SAST • Exploit        ChromaDB + BM25
                        PostExploit • BugBounty      Cross Encoder
        │                          │                          │
        └──────────────┬───────────┴──────────────┬──────────┘
                       ▼                          ▼
               Taint Analysis             Self-Play Arena
                NetworkX AST          Red Team ↔ Blue Team
                       │
                       ▼
             Knowledge Base Updates
                       │
                       ▼
                Continuous Learning
```

---

# 🚀 Quick Start

Clone the repository

```bash
git clone https://github.com/yourusername/cyphermind.git

cd cyphermind
```

Install everything

```bash
bash scripts/install.sh
```

Start backend and frontend

```bash
bash scripts/start.sh
```

Open

```
Frontend
http://localhost:3000

Backend
http://localhost:8000

API Docs
http://localhost:8000/docs
```

---

# ⚙️ Manual Setup

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH=.

uvicorn app.main:app \
--reload \
--host 0.0.0.0 \
--port 8000
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# ⚙️ Environment Variables

Create

```
.env
```

```env
####################################
# NVIDIA NIM
####################################

NVIDIA_API_KEY=

NVIDIA_API_BASE=https://integrate.api.nvidia.com/v1

LLM_MODEL=moonshotai/kimi-k2.6

LLM_TIMEOUT_SECONDS=180

####################################
# Google Search (Optional)
####################################

GOOGLE_API_KEY=

GOOGLE_CSE_ID=

####################################
# Bug Bounty
####################################

BUG_BOUNTY_MAX_ITERATIONS=15

####################################
# Embeddings
####################################

EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

# 📦 Usage

## 🐞 Bug Bounty Copilot

Navigate to

```
/bug-bounty
```

Provide

- Target URL
- Scope
- Program Notes

Click

```
Launch Autonomous Hunt
```

The AI will

- Validate scope
- Fingerprint technologies
- Search CVEs
- Probe services
- Generate payloads
- Verify vulnerabilities
- Produce reports

---

## 💬 AI Security Chat

Navigate to

```
/chat
```

Ask questions like

```
Explain CVE-2024-12345

Analyze this code

Search recent vulnerabilities

Generate SQL Injection payloads

Explain this exploit
```

---

## ⚔️ Self Play Arena

Navigate to

```
/selfplay
```

Paste vulnerable code.

The Red Team attacks.

The Blue Team patches.

New knowledge is automatically stored.

---

## 📚 Knowledge Base

Upload

- Python
- JavaScript
- TypeScript
- Java

Files are chunked, embedded and indexed.

Natural language search is supported.

---

## 🔍 Taint Analysis

Upload a Python file.

CypherMind visualizes

```
Source
    ↓
Propagation
    ↓
Sink
```

Highlighting vulnerable execution paths.

---

# 🌐 REST API

| Endpoint | Description |
|------------|------------|
| GET /health | Health Check |
| GET /api/v1/dashboard/stats | Dashboard Statistics |
| POST /api/v1/engagements | Create Engagement |
| POST /api/v1/agents/execute | Execute Security Agents |
| POST /api/v1/chat | AI Security Chat |
| POST /api/v1/knowledge/query | Hybrid RAG Query |
| POST /api/v1/selfplay/start | Start Self Play |
| POST /api/v1/bug-bounty/hunt | Launch Bug Bounty |
| WS /ws/engagements/{id} | Live Events |

---

# 🧪 Testing

```bash
cd backend

source .venv/bin/activate

pytest ../tests -v
```

Covered components include

- RL Orchestrator
- Agent Routing
- Taint Analysis
- Hybrid Search
- Tool Registry
- API Endpoints

---

# 📁 Project Structure

```
cyphermind
│
├── backend
│   ├── app
│   │   ├── agents
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── learning
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   ├── tools
│   │   ├── utils
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend
│   ├── src
│   │   ├── app
│   │   ├── components
│   │   ├── hooks
│   │   ├── lib
│   │   └── store
│   │
│   ├── package.json
│   └── tailwind.config.js
│
├── data
│
├── scripts
│   ├── install.sh
│   └── start.sh
│
├── tests
│
├── .env.example
│
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- NVIDIA NIM API
- Sentence Transformers
- ChromaDB
- BM25
- Cross Encoder
- NetworkX
- tree-sitter
- Jinja2

---

## Frontend

- Next.js 14
- React
- TailwindCSS
- Zustand
- Axios
- Recharts
- React Force Graph

---

## AI & Machine Learning

- Large Language Models
- Reinforcement Learning
- Q-Learning
- Bradley-Terry Preference Learning
- Hybrid RAG
- Dense Retrieval
- Sparse Retrieval
- Cross Encoder Ranking

---

# 🎯 Roadmap

- [x] Multi-Agent Security Swarm
- [x] Hybrid RAG
- [x] RL Agent Selection
- [x] Autonomous Bug Bounty
- [x] Tool Calling
- [x] Taint Analysis
- [x] Self Play Arena
- [ ] Docker Deployment
- [ ] Kubernetes Support
- [ ] Multi-user Authentication
- [ ] Cloud Deployment
- [ ] CVSS Scoring AI
- [ ] Attack Graph Generation
- [ ] Browser Automation Agent
- [ ] Active Learning Loop
- [ ] MCP Tool Support

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/amazing-feature
```

3. Commit your changes.

```bash
git commit -m "Add amazing feature"
```

4. Push to GitHub.

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request.

---

# 📜 License

This project is licensed under the **MIT License**.

See the **LICENSE** file for details.

---

# ⚠️ Ethical Use

CypherMind is intended **only for authorized security testing, research, education, and bug bounty programs**.

Users are solely responsible for ensuring that all assessments are performed on systems they own or have explicit permission to test.

Unauthorized access or misuse of this software may violate applicable laws and regulations.

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🍴 Fork it
- 🐛 Report issues
- 💡 Suggest new features
- 🤝 Contribute improvements

---

<p align="center">

**🛡️ Built with AI for the future of Ethical Hacking and Autonomous Security Research**

</p>

## Database Architecture

This project uses a relational database (PostgreSQL-compatible). The full
schema DDL is in [`database/schema.sql`](database/schema.sql).

### Tables & Linkage

| Table | Purpose | Key FKs |
|-------|---------|---------|
| `users` | User accounts, auth, roles | root entity |
| (domain tables) | App-specific data | `user_id → users(id)` ON DELETE CASCADE |

### Table Linkage (ERD)

```
users (1) ──< (N) domain_tables
  │ id (PK)                      │ user_id (FK → users.id)
  │ email (UQ)                   │ created_at
  │ role
```

- **users** is the root; domain tables reference `users(id)` with `ON DELETE CASCADE`.
- **Indexes** on all FK columns + frequently-filtered columns (date, status, category).
- **Timestamps** (`created_at`) on all tables for auditability.
- See [`database/schema.sql`](database/schema.sql) for the complete DDL.

