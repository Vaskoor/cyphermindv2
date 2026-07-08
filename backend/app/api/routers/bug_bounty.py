"""Standalone autonomous bug bounty hunt API."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field

from app.services.agent_loop import run_agent_loop

router = APIRouter(prefix="/bug-bounty", tags=["bug-bounty"])


class HuntRequest(BaseModel):
    target_url: str
    scope_domains: list[str] = Field(default_factory=list)
    max_iterations: int = Field(15, ge=1, le=30)
    notes: str = ""


class HuntStatus(BaseModel):
    job_id: str
    status: str


# In-memory job store (dev); use Redis/DB in production
_jobs: dict[str, dict] = {}


@router.post("/hunt")
async def start_hunt(body: HuntRequest, background_tasks: BackgroundTasks):
    import uuid
    job_id = str(uuid.uuid4())[:8]
    scope = body.scope_domains or []
    if not scope:
        from urllib.parse import urlparse
        host = urlparse(body.target_url).hostname
        if host:
            scope = [host]

    _jobs[job_id] = {"status": "running", "target": body.target_url}

    async def run():
        goal = (
            f"Bug bounty hunt on {body.target_url}. Scope: {', '.join(scope)}. "
            f"{body.notes}\nFind and report all vulnerabilities."
        )
        try:
            result = await run_agent_loop(
                goal,
                context={"scope_domains": scope, "target_url": body.target_url},
                max_iterations=body.max_iterations,
            )
            _jobs[job_id] = {
                "status": "completed",
                "target": body.target_url,
                "findings": result.findings,
                "tool_calls": result.tool_calls_made,
                "summary": result.final_answer,
                "iterations": result.iterations,
            }
        except Exception as exc:
            _jobs[job_id] = {"status": "failed", "error": str(exc)}

    background_tasks.add_task(run)
    return {"job_id": job_id, "status": "running", "target": body.target_url}


@router.get("/hunt/{job_id}")
async def hunt_status(job_id: str):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Hunt job not found")
    return {"job_id": job_id, **job}
