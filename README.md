```markdown
#  HTTPxray - X-ray Vision for HTTP Responses # COMMING SOON Please Try -MINI⚡ 

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/ssecgroup/httpxray)
[![Python](https://img.shields.io/badge/python-3.7%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Donate](https://img.shields.io/badge/donate-ETH-orange.svg)](#donations)

HTTPxray is a **professional-grade HTTP analysis tool** that gives you X-ray vision into web applications. It streams results live to disk with **zero RAM usage**, making it capable of scanning millions of URLs on any machine.

```
 Live Streaming     Multi-threading      Zero RAM Usage
 Tech Detection     Security Headers     Sensitive Data
 HTML Reports       SQL/NoSQL DB         REST API
 Web Dashboard      ML Anomaly Detection
```

---

##  Features

###  **Core Capabilities**
- **Live Streaming** - Results hit disk immediately, watch with `tail -f`
- **Zero RAM Usage** - Handles millions of URLs on low-end hardware
- **Multi-threading** - Configurable threads for maximum speed
- **Resume Support** - Pick up interrupted scans where they left off
- **Smart Rate Limiting** - Per-domain adaptive throttling

###  **Deep Inspection**
- **Technology Detection** - Identify 50+ web technologies, frameworks, and servers
- **Security Header Analysis** - Check HSTS, CSP, CORS, and 20+ security headers
- **Sensitive Data Discovery** - Find API keys, passwords, PII, and secrets
- **CVE Scanning** - Check for known vulnerabilities
- **WAF Detection** - Identify Web Application Firewalls
- **CMS Fingerprinting** - Detect WordPress, Drupal, Joomla, and more

###  **Output & Reporting**
- **Live JSONL Output** - Perfect for piping to other tools
- **Beautiful HTML Reports** - Charts, tables, and executive summaries
- **PDF Reports** - Professional documentation for clients
- **CSV Export** - Easy import into Excel/Google Sheets
- **SQLite/PostgreSQL/MySQL/MongoDB** - Structured storage

###  **Integration**
- **REST API** - Control scans programmatically
- **Web Dashboard** - Real-time monitoring
- **Plugin System** - Extend functionality with custom plugins
- **Webhooks** - Slack, email, and custom notifications
- **Distributed Scanning** - Master/worker cluster support

###  **Advanced**
- **ML Anomaly Detection** - Identify unusual responses with machine learning
- **Pattern Recognition** - Cluster similar responses
- **Content Classification** - Auto-categorize endpoints
- **Feature Extraction** - Rich feature set for analysis

---

##  Quick Start

### Installation

```bash
# Install from PyPI
pip install httpxray[full]

# Or install from source
git clone https://github.com/ssecgroup/httpxray.git
cd httpxray
pip install -e .[full]
```

### Basic Usage

```bash
# Scan a single URL
httpxray -u https://example.com

# Scan a domain with common paths
httpxray -d example.com

# Scan a list of URLs (millions supported!)
httpxray -l urls.txt

# Watch results live in another terminal
tail -f outputs/*/scan_results.jsonl | jq '.status'
```

### Advanced Examples

```bash
# Full-featured scan
httpxray -l targets.txt \
  --threads 50 \
  --rate-limit 10 \
  --tech --security --sensitive --ml \
  --db sqlite \
  --report --pdf \
  --verbose

# POST requests with JSON
httpxray -u https://api.example.com/login \
  --post \
  --json '{"username":"admin","password":"test"}' \
  -H "Authorization: Bearer token"

# API server mode
httpxray --api --port 8000

# Web dashboard
httpxray --dashboard --port 5000

# Distributed scanning (master)
httpxray --distributed --master

# Distributed scanning (worker)
httpxray --distributed --worker --master-host 192.168.1.100
```

---

##  Documentation

### Command Line Options

| Option | Description |
|--------|-------------|
| `-u, --url URL` | Single URL to scan |
| `-d, --domain DOMAIN` | Single domain to scan |
| `-l, --list FILE` | File with URLs (one per line) |
| `--threads N` | Number of threads (default: 20) |
| `--rate-limit N` | Requests per second per domain (default: 10) |
| `--timeout N` | Request timeout in seconds (default: 10) |
| `--verbose, -v` | Verbose output with colors |

#### Detectors
| Option | Description |
|--------|-------------|
| `--tech / --no-tech` | Technology detection |
| `--security / --no-security` | Security headers |
| `--sensitive / --no-sensitive` | Sensitive data |
| `--cve / --no-cve` | CVE scanning |
| `--waf / --no-waf` | WAF detection |
| `--cms / --no-cms` | CMS scanning |
| `--ml / --no-ml` | ML anomaly detection |

#### Output
| Option | Description |
|--------|-------------|
| `--output-dir DIR` | Output directory (default: outputs/) |
| `--report / --no-report` | Generate HTML report |
| `--pdf / --no-pdf` | Generate PDF report |
| `--db TYPE` | Database type (sqlite/postgresql/mysql/mongodb) |
| `--save-responses` | Save response bodies |

#### Server Modes
| Option | Description |
|--------|-------------|
| `--api` | Start API server |
| `--api-port PORT` | API server port (default: 8000) |
| `--dashboard` | Start web dashboard |
| `--dashboard-port PORT` | Dashboard port (default: 5000) |

### Output Format

Results are streamed as JSONL (JSON Lines):

```json
{"url":"https://example.com","status":200,"method":"GET","time":0.234,"size":45200,"technologies":[{"technology":"nginx","confidence":"high"}],"security":{"security_score":65,"rating":"C - Fair"},"sensitive_data":{"count":2,"findings":[{"type":"email","severity":"medium"}]}}
```

---

##  Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   Input     │ -> │   Scanner    │ -> │   Output    │
│ - URL       │    │ - Threads    │    │ - JSONL     │
│ - Domain    │    │ - Detectors  │    │ - Database  │
│ - File      │    │ - Rate Limit │    │ - Reports   │
└─────────────┘    └──────────────┘    └─────────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
            ┌───────────┐ ┌───────────┐
            │  Plugins  │ │    API    │
            │  Webhook  │ │ Dashboard │
            └───────────┘ └───────────┘
```

---

##  Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Start for Contributors

```bash
# Fork the repository
git clone https://github.com/yourusername/httpxray.git
cd httpxray

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install in development mode
pip install -e .[full,dev]

# Run tests
pytest tests/

# Run your changes
httpxray --version
```

---

##  Donations

If HTTPxray saves you time and money, consider supporting continued development:

**ETH**: `0x8242f0f25c5445F7822e80d3C9615e57586c6639`

Your support helps maintain and improve this tool for everyone! 🙏

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2024 ssecgroup

---

##  Disclaimer

This tool is for **authorized security testing only**. Users are responsible for compliance with applicable laws. The authors assume no liability for misuse.

---

##  Acknowledgments

- Thanks to all contributors and users
- Built with Python, Requests, Click, and many other amazing libraries

---

**Made with ❤️ by [ssecgroup](https://github.com/ssecgroup)**
```
