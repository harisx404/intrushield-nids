"""
Vercel Serverless entrypoint for the NIDS FastAPI backend.

Vercel requires a top-level `app` variable to be present in this file.
We import the FastAPI `app` from backend.main at module level and provide
a safe fallback if the import fails so that the error is visible in logs.
"""
import os
import sys
import traceback

# Signal to the backend that we are running in Vercel's serverless environment.
os.environ.setdefault("VERCEL", "1")

# Vercel requires a top-level `app` symbol — define a safe placeholder first,
# then try to replace it with the real FastAPI application.
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

_placeholder = FastAPI()

@_placeholder.get("/{path:path}")
async def _startup_error(path: str):
    return PlainTextResponse(
        "Application failed to start. Check function logs.", status_code=503
    )

app = _placeholder

# Now attempt to import the real application.
try:
    from backend.main import app  # noqa: F811  — intentional re-assignment
except Exception:
    # The placeholder above will handle all requests and surface the traceback
    # in Vercel's runtime logs so developers can diagnose import errors.
    _tb = traceback.format_exc()
    _error_app = FastAPI()

    @_error_app.get("/{path:path}")
    async def _error(path: str):
        return PlainTextResponse(_tb, status_code=503)

    app = _error_app
