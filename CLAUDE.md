# OPNsense MCP — learning project

## What I'm building
An MCP (Model Context Protocol) server that lets Claude query my homelab router.

- **Router:** OPNsense (talked to over its REST API at `https://<router>/api/...`, API key + secret via HTTP Basic auth)
- **Server:** Python + FastAPI, with the official MCP Python SDK (`FastMCP`) mounted inside it at `/mcp`
- **Hosting:** container image, deployed to my **k3s** cluster (Traefik ingress)
- **Client:** Claude Code / Claude Desktop connecting over HTTP with a bearer token

Target architecture:
```
Claude ──HTTP──► Traefik Ingress (k3s) ──► Service ──► FastAPI pod :8000 ──HTTPS──► OPNsense :443 /api/...
```

## How I want to learn (read this first, Claude)
- **I'm new to FastAPI.** Go slow, one small piece at a time.
- **I type the code myself.** Explain a few lines, let me write them, then move on. Don't dump whole files on me.
- **Explain the networking too** — requests, ports, HTTP, TCP, how traffic flows through k3s.
- **I write the Kubernetes manifests myself** (Deployment, Service, Secret, Ingress). Claude reviews them, doesn't write them for me.
- Plain language. Define terms the first time they come up.
- Short checks/questions are welcome to make sure things stuck.

## Lesson plan
1. **Minimal FastAPI app** — `app`, routes, uvicorn, request/response, `/healthz`  ← **current**
2. OPNsense API client with `httpx` (API key setup, self-signed certs, GET vs POST)
3. Mount the MCP server in FastAPI and write read-only tools
4. Bearer token auth middleware
5. Dockerfile + build/push image (GHCR)
6. **I write** the k3s manifests; Claude reviews

## Where I'm at
- Lesson 1 in progress.
- Covered so far: what a web API is, URL parts (protocol/host/port/path), HTTP request/response, status codes, uvicorn vs FastAPI, `127.0.0.1` vs `0.0.0.0`.
- **Next step:** create `app/practice.py` and type the first two lines (`from fastapi import FastAPI`, `app = FastAPI()`), then add a first route and run it.
- Open question to answer: in `http://192.168.1.1:443/api/core/firmware/status`, which part is the host, the port, and the path a route matches?
- `app/main.py` is Claude's example file for reference; it has a `TODO(human)` for a `/healthz` route.
- Git/GitHub set up (repo is **public**). Still to do: set `git config --global user.email`.

## Environment
- Windows 11, but I run commands in **WSL (Ubuntu) bash** from `/mnt/c/Users/imkyo/OneDrive/Documents/opnsense-mcp`. Give terminal commands in bash.
- Python 3.12. uvicorn isn't on PATH on the Windows side → use `python -m uvicorn app.main:app --reload --port 8000`.
- `gh` CLI installed and logged in inside WSL.

## Rules for this repo
- **Public repo: never commit secrets.** OPNsense key/secret and the MCP token live in `.env` (gitignored) locally and in a Kubernetes Secret in the cluster.
- Start with **read-only** tools. Anything that changes the router comes later, deliberately.
- Keep the MCP endpoint LAN-only; don't expose it to the internet.
- Update the "Where I'm at" section as lessons progress.
