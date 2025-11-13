# 🌐 Enterprise Network Automation Suite

> **Automated Network Management Tools for Multi-Site Enterprise Infrastructure**

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Project Status](https://img.shields.io/badge/status-in%20development-yellow.svg)]()

---

## 📋 Project Overview

This project is a comprehensive Python-based automation suite for enterprise network management, designed to simplify and streamline network operations across multi-site infrastructures. It combines traditional infrastructure expertise with modern AI technologies to create intelligent, ethical, and production-ready tools.

**Developed by:** Philipp Prinzen  
**Context:** IHK Certification Project - Fachinformatiker für Anwendungsentwicklung  
**Timeline:** November 2025 - October 2026 (70 hours project scope)  
**Institution:** BBQ Hamburg

---

## 🎯 Project Goals

### Primary Objectives
- **Automate** repetitive network management tasks
- **Integrate AI** for intelligent decision-making and natural language interaction
- **Ensure Ethical AI** principles throughout (transparency, human oversight, audit logging)
- **Provide Production-Ready** tools with proper testing, documentation, and deployment

### Learning Objectives
- Master Python for systems automation
- Integrate Large Language Models (LLMs) into infrastructure workflows
- Apply Ethical AI principles learned from FemAI experience
- Demonstrate full-stack development skills (backend, frontend, AI, database)

---

## 🏗️ Network Infrastructure: "OnPrem"

### Design Overview
Multi-site enterprise network designed in Cisco Packet Tracer with 41 devices across two locations.

**HQ (Headquarters):**
- 1× Router (HQ-R1)
- 1× Distribution Switches (HQ-SW-01)
- 1× Access Switches (HQ-SW-02)
- 6× Servers (DC-01, DC-02, EXC-01, EXC-02, DB-01, FILE-01, WEB-01, APP-01 (...))
- 14× Client PCs
- 5× VLANs (10: Hypervisor, 20: VMs, 30: Backup, 40: Management, 50: Clients)

**Branch (Remote Office):**
- 1× Router (Branch-RT-01)
- 1× Distribution Switch (Branch-SW-01)
- 1× Access Switches (Branch-SW-02)
- 2× Server (Branch-TS-03, Branch-TS-04)
- 8× Client PCs (DHCP)
- 8x Network Printer
- 5× VLANs (same as HQ)

**Routing:** OSPF between HQ and Branch

**Documentation:** Complete topology, IP addressing scheme, and configurations available in `/docs` and `/00-packet-tracer`

---

## 🛠️ The Four Tools

### Tool 1: VLAN Calculator ✅ **COMPLETE**
**Status:** Production-ready  
**Lines of Code:** ~300  
**Completion:** November 2025

Automated subnet calculation tool for enterprise VLAN deployments.

**Features:**
- Calculates network parameters for 5 VLANs (10, 20, 30, 40, 50)
- Supports both HQ and Branch sites
- Computes: Network Address, Broadcast, Subnet Mask (CIDR & Decimal), Usable Host Range, DHCP Range, Default Gateway
- CSV export for documentation
- User-friendly CLI with input validation
- Error handling and logging

**Tech Stack:** Python 3.11+, ipaddress module, csv

**Usage:**
```bash
cd 01-vlan-calculator
python vlan_calculator.py
```

**Example Output:**
```
=== VLAN 10 (Management) - HQ ===
Network Address: 10.0.10.0
Broadcast: 10.0.10.255
Subnet Mask: 255.255.255.0 (/24)
Usable Hosts: 10.0.10.1 - 10.0.10.254 (254 hosts)
DHCP Range: 10.0.10.100 - 10.0.10.200
Default Gateway: 10.0.10.1
```

---

### Tool 2: IP Management System 🔄 **IN DEVELOPMENT**
**Status:** Planned for December 2025 - February 2026  
**Estimated Scope:** 15 hours

Web-based device inventory and IP address management system with automated health monitoring.

**Planned Features:**
- YAML-based device inventory (inspired by Post Agent architecture)
- Automated ping status checks (scheduled with APScheduler)
- Free IP address detection
- Device categorization by VLAN, site, and type
- Web dashboard (Flask + Bootstrap)
- Historical status tracking (SQLite database)
- CSV/Excel export
- REST API for integration

**Tech Stack:** Python, Flask, PyYAML, SQLite, APScheduler, Bootstrap 5, Chart.js

**Architecture:**
```
02-ip-management/
├── data/
│   └── device_inventory.yaml
├── src/
│   ├── scanner.py          # Ping checks & monitoring
│   ├── manager.py          # IP management logic
│   └── db.py               # Database operations
├── templates/
│   ├── dashboard.html      # Main UI
│   └── device_detail.html
├── static/
│   ├── css/
│   └── js/
├── app.py                  # Flask application
└── requirements.txt
```

**Sample YAML Structure:**
```yaml
- hostname: HQ-R1
  ip: 10.0.10.1
  vlan: 10
  site: HQ
  type: Router
  description: "HQ Main Router"
  
- hostname: HQ-SW1
  ip: 10.0.10.2
  vlan: 10
  site: HQ
  type: Switch
  description: "HQ Distribution Switch 1"
```

---

### Tool 3: Config Template Generator 📋 **PLANNED**
**Status:** Planned for March - June 2026  
**Estimated Scope:** 10 hours

Template-based network device configuration generator with validation.

**Planned Features:**
- Jinja2 template engine for device configs
- Templates for: VLANs, OSPF, Access Lists, DHCP, etc.
- Variable substitution (IP addresses, VLAN IDs, hostnames)
- Syntax validation (regex-based)
- Output as .txt files
- Integration with Tools 1 & 2 (auto-populate variables)
- CLI and Web interface

**Tech Stack:** Python, Jinja2, Click (CLI), PyYAML

**Sample Template (switch_vlan.j2):**
```jinja2
! VLAN Configuration for {{ hostname }}
! Generated: {{ timestamp }}

{% for vlan in vlans %}
vlan {{ vlan.id }}
 name {{ vlan.name }}
 
interface {{ vlan.interface }}
 switchport mode access
 switchport access vlan {{ vlan.id }}
 description {{ vlan.description }}
{% endfor %}
```

---

### Tool 4: AI Network Assistant 🎯 **IHK MAIN PROJECT**
**Status:** Planned for July - October 2026  
**Estimated Scope:** 25-30 hours

LLM-powered conversational network management assistant with ethical AI safeguards.

**Core Features:**

1. **Natural Language Understanding**
   - User queries in plain German/English
   - Understands network-specific terminology
   - Context-aware responses

2. **Tool Integration (Function Calling)**
   - Automatically invokes Tools 1-3 based on user intent
   - Example: "Zeig mir alle Geräte in VLAN 20" → calls IP Management
   - Orchestrates multiple tools for complex queries

3. **AI-Powered Config Generation**
   - Generates device configurations via LLM
   - Uses GPT-4o-mini with structured prompts
   - Validates output with Tool 3 templates
   - Human preview & approval required

4. **Documentation Assistant**
   - Explains network concepts in simple language
   - Provides troubleshooting guidance
   - Generates documentation from configs

5. **Intelligent Troubleshooting**
   - Diagnoses connectivity issues
   - Suggests solutions based on network state
   - Checks VLAN, routing, gateway configurations

**Ethical AI Safeguards** (inspired by FemAI Post Agent):
- ✅ **Input Validation:** Prevents shell injection and malicious commands
- ✅ **Output Validation:** Regex checks before config deployment
- ✅ **Human-in-the-Loop:** Critical operations require manual approval
- ✅ **Audit Logging:** All AI queries and decisions logged
- ✅ **Transparency:** Shows which tools were used and why
- ✅ **Explainability:** AI provides reasoning for recommendations

**Tech Stack:** 
- Backend: Python, Flask, OpenAI API (GPT-4o-mini), LangChain (optional)
- Frontend: HTML, Bootstrap 5, JavaScript (Vanilla)
- Database: SQLite (chat history, audit logs)
- AI: Prompt engineering, Function Calling, RAG (Retrieval Augmented Generation)

**Architecture Pattern:**
```
Inspired by FemAI Post Agent:
- External prompt templates (prompts/)
- Structured AI responses (Hook, Analysis, Action)
- YAML-based configuration
- Production logging and error handling
- Environment variable management (.env)
```

**Sample Interaction:**
```
User: "Zeig mir alle Geräte in VLAN 20"

AI Assistant:
🔍 Analyzing query...
📊 Calling IP Management Tool (Tool 2)...

Found 8 devices in VLAN 20 (IT):
- HQ-R1 (10.0.20.1) - Router - Status: ✅ Online
- PC-IT-01 (10.0.20.101) - Client - Status: ✅ Online
- PC-IT-02 (10.0.20.102) - Client - Status: ❌ Offline
...

Would you like to investigate offline devices?
```

---

## 🎓 IHK Project Context

### Certification Details
- **Program:** Fachinformatiker für Anwendungsentwicklung (Application Developer)
- **Institution:** BBQ Hamburg
- **Duration:** June 2025 - June 2027
- **Project Phase:** July - October 2026 (70 hours)
- **Goal:** 100% evaluation (mirroring Linux Essentials: 800/500 points)

### Why This Project?

**Combines Three Core Competencies:**

1. **Infrastructure Expertise (10+ years IT)**
   - System Engineer experience (VMware, Storage, Networking)
   - Linux Professional certification (800/500 points, 100% all areas)
   - Enterprise networking knowledge (CCNA-level concepts)

2. **AI/ML Development (2025 experience)**
   - Production AI Agent (Ethical AI Post Agent @ FemAI)
   - LLM integration (GPT-4, Google Cloud certified)
   - Hackathon participation (LeadWithAIAgents 2025, Silicon Valley)
   - Prompt engineering (elite-level)

3. **Software Development (Current training)**
   - Python, Java (BBQ curriculum)
   - Web frameworks (Flask)
   - Database design (SQL)
   - Testing & CI/CD

**This project demonstrates the evolution from System Engineer → AI/ML Engineer with Application Development certification.**

---

## 📚 Technology Stack

### Backend
- **Python 3.11+** - Primary programming language
- **Flask** - Web framework for Tool 2 & 4
- **OpenAI API** - GPT-4o-mini for AI Assistant
- **LangChain** - Optional agent orchestration framework
- **SQLite** - Database for device history and logs
- **PyYAML** - Configuration management
- **Jinja2** - Template engine for configs

### Frontend
- **HTML5 + Bootstrap 5** - Responsive UI (no React - keeping it simple)
- **JavaScript (Vanilla)** - Client-side interactions
- **Chart.js** - Data visualization (Tool 2 dashboard)

### DevOps & Tools
- **Git/GitHub** - Version control
- **GitHub Actions** - CI/CD pipeline
- **pytest** - Unit and integration testing
- **Docker** - Optional containerization
- **python-dotenv** - Environment variable management
- **Pylint/Black** - Code quality and formatting

### Infrastructure
- **Cisco Packet Tracer** - Network simulation and testing
- **Linux (Ubuntu/Debian)** - Development environment
- **VS Code / PyCharm** - IDE

---

## 🗂️ Repository Structure

```
enterprise-network-automation/
│
├── 00-packet-tracer/              # Network simulation files
│   ├── OnPrem.pkt                 # Main Packet Tracer file
│   ├── screenshots/               # Topology images
│   └── configs/                   # Device configuration exports
│
├── 01-vlan-calculator/            # Tool 1 ✅ COMPLETE
│   ├── vlan_calculator.py
│   ├── README.md
│   ├── requirements.txt
│   └── tests/
│
├── 02-ip-management/              # Tool 2 🔄 IN DEVELOPMENT
│   ├── data/
│   ├── src/
│   ├── templates/
│   ├── static/
│   ├── app.py
│   ├── README.md
│   └── requirements.txt
│
├── 03-config-generator/           # Tool 3 📋 PLANNED
│   ├── templates/                 # Jinja2 config templates
│   ├── src/
│   ├── README.md
│   └── requirements.txt
│
├── 04-ai-assistant/               # Tool 4 🎯 IHK PROJECT
│   ├── prompts/                   # LLM prompt templates
│   ├── src/
│   ├── templates/
│   ├── static/
│   ├── logs/                      # Audit logs
│   ├── app.py
│   ├── README.md
│   └── requirements.txt
│
├── docs/                          # Documentation
│   ├── network-design.md          # Topology documentation
│   ├── ip-address-plan.csv        # IP allocation table
│   ├── project-requirements.md    # IHK project specifications
│   └── ethical-ai-guidelines.md   # AI safety principles
│
├── tests/                         # Integration tests
│
├── .github/
│   └── workflows/                 # CI/CD pipelines
│       └── python-tests.yml
│
├── .gitignore
├── LICENSE
├── README.md                      # This file
└── requirements.txt               # Global dependencies
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git
- (Optional) Cisco Packet Tracer for network simulation

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR_USERNAME/enterprise-network-automation.git
cd enterprise-network-automation
```

2. **Set up virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run Tool 1 (VLAN Calculator):**
```bash
cd 01-vlan-calculator
python vlan_calculator.py
```

5. **For Tool 4 (AI Assistant) - Add OpenAI API Key:**
```bash
# Create .env file in 04-ai-assistant/
echo "OPENAI_API_KEY=your_api_key_here" > 04-ai-assistant/.env
```

---

## 🧪 Testing

Run tests for all tools:
```bash
pytest tests/
```

Run tests for specific tool:
```bash
pytest 01-vlan-calculator/tests/
```

---

## 📖 Documentation

- **[Network Design](docs/network-design.txt)** - Complete topology and architecture
- **[IP Address Plan](docs/ip-address-plan.csv)** - Full IP allocation table
- **[Ethical AI Guidelines](docs/ethical-ai-guidelines.md)** - AI safety principles
- **[Tool 1 README](01-vlan-calculator/README.md)** - VLAN Calculator documentation
- **[Tool 2 README](02-ip-management/README.md)** - IP Management System docs
- **[Tool 4 README](04-ai-assistant/README.md)** - AI Assistant documentation

---

## 🛡️ Ethical AI Principles

This project integrates Ethical AI principles learned during work with **Alexandra Wudel** (AI Person of the Year 2024, Founder FemAI):

### Core Principles

1. **Transparency**
   - All AI decisions are logged and auditable
   - Users can see which tools the AI called and why
   - Source attribution for all recommendations

2. **Human Oversight**
   - Critical operations (config changes, deployments) require human approval
   - "Human-in-the-Loop" design pattern throughout
   - Preview functionality before execution

3. **Bias Awareness**
   - LLMs can provide incorrect or outdated information
   - Validation layers (regex, syntax checks) mitigate AI errors
   - Clear disclaimers: "AI-generated, please review"

4. **Safety & Security**
   - Input sanitization prevents injection attacks
   - Output validation before any config deployment
   - Rate limiting on API calls
   - Secure API key management

5. **Explainability**
   - AI provides reasoning for its recommendations
   - "Explain" button shows decision-making process
   - Educational value: users learn while using the tool

**Reference Project:** [Ethical AI Post Agent](https://github.com/shinanDev/ethical_ai_post_agent) - Production AI system developed at FemAI

---

## 📈 Project Timeline

### Phase 1: Foundation (Nov 2025 - Feb 2026)
- ✅ Tool 1: VLAN Calculator (COMPLETE)
- 🔄 Tool 2: IP Management System (IN DEVELOPMENT)
- 📚 Python & Flask fundamentals
- 🎓 Web development basics (Bootstrap, REST APIs)

### Phase 2: AI Integration (Mar - Jun 2026)
- 📋 Tool 3: Config Template Generator
- 🤖 OpenAI API & LangChain learning
- 🎯 Prompt engineering practice
- 📊 IHK project preparation

### Phase 3: IHK Main Project (Jul - Oct 2026)
- 🎯 Tool 4: AI Network Assistant development
- 📝 IHK documentation
- 🧪 Comprehensive testing & CI/CD
- 🎤 Presentation preparation
- 🏆 **Goal: 100% evaluation**

### Phase 4: Internship (Sep 2026 - Jun 2027)
- 💼 Real-world AI/ML projects
- 🔗 Portfolio expansion
- 🤝 Industry networking

### Phase 5: IHK Certification (Apr - May 2027)
- 📄 Final documentation
- 🎤 Presentation
- 💬 Technical interview
- 🎓 **Target: Certified Application Developer**

---

## 🎯 Success Metrics

### Technical Goals
- ✅ All 4 tools fully functional
- ✅ 80%+ test coverage
- ✅ Production-ready code quality (Pylint >9.0)
- ✅ Complete documentation
- ✅ CI/CD pipeline operational

### IHK Project Goals
- 🎯 70 hours project scope (accurately tracked)
- 🎯 15-20 page documentation
- 🎯 Live demo without errors
- 🎯 Answer all technical questions confidently
- 🎯 **100% evaluation** (mirroring Linux Essentials: 800/500)

### Learning Goals
- 📚 Master Python for systems automation
- 📚 Integrate LLMs into production systems
- 📚 Apply Ethical AI principles consistently
- 📚 Full-stack development proficiency
- 📚 Professional software engineering practices

---

## 👨‍💻 About the Developer

**Philipp Prinzen**  
Junior Developer | AI Agent Developer | 10+ years IT experience

**Background:**
- First Level Support @ 3NET GmbH (2018-2021)
- System Engineer @ Vater Unternehmensgruppe (2021-2024)
- Junior Developer @ FemAI (2025)
- AI Trainer @ Outlier.ai (2025)

**Certifications:**
- 🏆 Linux Professional Institute - Linux Essentials (800/500 points, 100% all areas)
- 🏆 Google Cloud - Introduction to Large Language Models
- 🏆 IBM - Introduction to Software Engineering
- 🏆 LeadWithAIAgents Hackathon 2025 Participant

**Skills:**
- Infrastructure: Linux, VMware, Networking (10+ years)
- AI/ML: LLMs, Prompt Engineering, AI Agents (production experience)
- Development: Python, Java, Flask, Git/GitHub

**Connect:**
- LinkedIn: [Philipp Prinzen](https://www.linkedin.com/in/philipp-prinzen-46a51a166/)
- GitHub: [shinanDev](https://github.com/shinanDev)

---

## 🤝 Acknowledgments

**Special Thanks:**

- **Alexandra Wudel** (FemAI) - Mentor for Ethical AI principles, inspiration for agent architecture
  - AI Person of the Year 2024
  - Deutscher Bundestag Arbeitsgruppe KI
  - Founder of FemAI (Center for Feminist Artificial Intelligence)

- **BBQ Hamburg** - Vocational retraining program instructors and classmates

- **Classmates:** Adrian, Mahmoud, and study group members for collaborative learning

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🔗 Related Projects

- **[FemAI Ethical AI Post Agent](https://github.com/shinanDev/ethical_ai_post_agent)** - Production AI system for LinkedIn content generation with bias awareness
- **[Network Design Documentation](docs/network-design.txt)** - Complete "OnPrem" topology

---

## 📬 Contact & Support

For questions, suggestions, or collaboration:

- **Email:** shinan.dev@proton.me
- **LinkedIn:** [Philipp Prinzen](https://www.linkedin.com/in/philipp-prinzen-46a51a166)
- **GitHub Issues:** [Create an issue](https://github.com/shinanDev/enterprise-network-automation/issues)

---

## 🎓 Academic Integrity Statement

This project is submitted as part of the IHK certification for **Fachinformatiker für Anwendungsentwicklung** at BBQ Hamburg. All code is original work, with proper attribution for external libraries, frameworks, and inspiration sources (e.g., FemAI Post Agent architecture pattern).

**Ethical AI principles are not just implemented in the code - they guide the entire development process.**

---

**Built with ❤️ in Hamburg | Moin! 🌊**

**"Let's make AI fair so that it scales bias-aware."** - Inspired by FemAI
