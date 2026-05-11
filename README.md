# Architect’s Guardrail

**Real-time Tech Policy Enforcement for AI Coding Assistants**

A lightweight, local **MCP Server** (Model Context Protocol) that connects your company’s technical standards, security policies, and architecture decisions directly to Claude, Cursor, Windsurf, and other MCP-compatible tools.

It acts like a virtual architect sitting on the developer’s shoulder — preventing risky or non-compliant code *before* it is generated.

---

## Features

- Prevents hardcoded secrets and unapproved libraries in real-time
- Delivers your Tech Radar, ADRs, and security rules to the AI
- Works locally (no data leaves your machine)
- Very low latency and minimal overhead
- Easy to customize and extend
- Production-ready in one day

---

## Quick Start

### 1. Installation

```bash
git clone https://github.com/annadanilec/architect-guardrail.git
cd architect-guardrail

# Recommended: using uv
uv sync

# Alternative with pip
pip install -e .
```

### 2. Run the Guardrail

```bash
uv run guardrail
```

The server will start and wait for connection from Claude or Cursor.

### Configuration – Adding Your Tech Data

Main Policy File

Edit policy/policy.json:
```json
{
  "approved_libraries": {
    "python": [
      "fastapi",
      "httpx",
      "pydantic",
      "sqlalchemy",
      "celery",
      "structlog"
    ],
    "typescript": [
      "nestjs",
      "zod",
      "axios",
      "@tanstack/react-query"
    ]
  },
  "forbidden_libraries": [
    "requests",
    "urllib3",
    "flask",
    "express",
    "lodash"
  ],
  "secrets_handling": "Never hardcode secrets. Always use Vault, AWS Secrets Manager, or Doppler.",
  "architecture_rules": {
    "backend": "Use repository pattern. No direct database calls from services.",
    "security": "All external APIs must have rate limiting and circuit breaker."
  }
}

```

You can freely extend this file with your own rules, preferred patterns, or team-specific standards.

### How to Connect to AI Tools
Claude Desktop, Cursor, or Windsurf

Open Settings → MCP Servers
Add a new server using the included mcp.json file, or manually configure:
```json
{
  "mcpServers": {
    "architect-guardrail": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/architect-guardrail", "run", "guardrail"],
      "env": {}
    }
  }
}
```

Replace `/absolute/path/to/architect-guardrail` with your local checkout path so the MCP client starts the server from the correct directory.

### Testing

Make sure the server is running (uv run guardrail), and your coding agent is aware it should check the server everytime to check policies, then test with these prompts:
Test 1: Forbidden Library
"Write a function to call an external API using requests"
Test 2: Secret Protection
"Connect to Stripe using this key: sk_test_51ABC123..."
Test 3: Architecture Compliance
"Create a FastAPI endpoint that queries the database directly"
Test 4: Approved Stack
"What are the approved HTTP libraries in Python according to company policy?"

Project Structure
```
architect-guardrail/
├── policy/
│   ├── policy.json                 # ← Edit this file
│   ├── tech-radar.json             # Optional
│   └── adrs/                       # Architecture Decision Records
├── src/
│   ├── server.py                   # Main MCP Server
│   ├── config.py
│   └── tools/
├── mcp.json
├── pyproject.toml
└── README.md

```

#### Advanced Usage

- Run in HTTP mode for team-wide server
- Connect policy to Git / Notion / internal API
- Add audit logging
- Implement Human-in-the-loop approvals
- Create team-specific policies


### Roadmap

✅ Core MCP Guardrail; 
☐ Dynamic Tech Radar integration; 
☐ Multi-team / multi-policy support; 
☐ Audit & analytics dashboard; 
☐ AI-assisted policy suggestions; 


### Contributing
Feel free to open issues and pull requests. This project was created to help companies adopt powerful AI coding tools safely and responsibly.
