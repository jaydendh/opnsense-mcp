# Lesson 1: the smallest useful FastAPI app.
#
# Run it from the opnsense-mcp folder with:
#   uvicorn app.main:app --reload --port 8000
#
# "app.main:app" means: in the package "app", open the module "main.py",
# and use the variable named "app" inside it.

from fastapi import FastAPI

# This object IS your web application. Every route you add hangs off it.
app = FastAPI(title="OPNsense MCP")


# A "route": when someone sends GET /  ...run this function.
# Whatever you return (a dict here) FastAPI turns into JSON automatically.
@app.get("/")
def root():
    return {"service": "opnsense-mcp", "status": "learning"}


# A route can take a "path parameter". The {name} in the URL is passed
# into the function, and the type hint (str) tells FastAPI to validate it.
# Try: http://localhost:8000/hello/jayden
@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello, {name}!"}


# TODO(human): add a GET /healthz route that returns {"ok": True}

