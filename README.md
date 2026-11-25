# OPNsense MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server that lets AI assistants like Claude read information from an **OPNsense** firewall/router — built with **FastAPI** and designed to run in a **k3s** homelab cluster.

> 🚧 **Work in progress / learning project.** I'm building this step by step to learn FastAPI, the OPNsense API, MCP, and Kubernetes deployment. Expect things to change.

## What it does

MCP is a standard way for AI assistants to call "tools" on a server. This project exposes OPNsense data as MCP tools, so you can ask Claude things like:

- *"What devices are on my network right now?"*
- *"Is my firewall up to date?"*
- *"How much CPU and memory is the router using?"*
- *"Which services are running?"*

Claude calls this server → this server calls the OPNsense REST API → the answer comes back as JSON for Claude to explain.

## How it works

```
Claude ──HTTP──► Traefik Ingress (k3s) ──► Service ──► FastAPI pod :8000 ──HTTPS──► OPNsense :443 /api/...
                                                          └─ MCP endpoint at /mcp
```

| Piece | Role |
|---|---|
| **FastAPI** | Python web framework that receives requests and routes them to code |
| **uvicorn** | The server that actually listens on a port and hands requests to FastAPI |
| **MCP Python SDK (FastMCP)** | Turns Python functions into tools an AI assistant can discover and call |
| **httpx** | HTTP client used to talk to the OPNsense API |
| **k3s** | Lightweight Kubernetes that runs the container in my homelab |

## Planned tools (read-only first)

| Tool | OPNsense API | Status |
|---|---|---|
| Firmware / update status | `core/firmware/status` | planned |
| System resources (CPU, RAM, disk) | `diagnostics/system/systemResources` | planned |
| ARP table (devices on the network) | `diagnostics/interface/getArp` | planned |
| Service list | `core/service/search` | planned |

Tools that *change* the router (firewall rules, restarting services) will only come later, deliberately, with tightly scoped API permissions.

## Roadmap

- [ ] **1. Minimal FastAPI app** — routes, uvicorn, health check *(in progress)*
- [ ] 2. OPNsense API client with `httpx`
- [ ] 3. Mount the MCP server and add read-only tools
- [ ] 4. Bearer-token authentication
- [ ] 5. Dockerfile and container image
- [ ] 6. k3s manifests (Deployment, Service, Secret, Ingress)

## Running locally

Requires Python 3.12+.

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Then open:
- http://localhost:8000/ — basic JSON response
- http://localhost:8000/docs — auto-generated interactive API docs

## Project layout

```
opnsense-mcp/
├── app/
│   ├── __init__.py      # marks "app" as a Python package
│   └── main.py          # the FastAPI application
├── requirements.txt     # Python dependencies
├── CLAUDE.md            # context for Claude Code sessions
└── README.md
```

## Security notes

- **No secrets in this repo.** The OPNsense API key/secret and the MCP access token are provided through environment variables (a gitignored `.env` locally, a Kubernetes Secret in the cluster).
- The OPNsense API user is given only the privileges these tools need.
- The MCP endpoint is meant for the LAN only and should not be exposed to the internet.
