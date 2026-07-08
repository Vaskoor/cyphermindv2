"""CypherMind FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.base import init_db
from app.api.routers import (
    agents,
    auth,
    bug_bounty,
    chat,
    dashboard,
    engagements,
    findings,
    knowledge,
    learning,
    reports,
    selfplay,
    settings,
    tools,
    ws,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting CypherMind backend...")
    await init_db()
    yield
    logger.info("Shutting down CypherMind backend.")


app = FastAPI(
    title="CypherMind API",
    description="Self-Learning AI Penetration Testing Copilot",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in [
    auth.router,
    bug_bounty.router,
    engagements.router,
    agents.router,
    chat.router,
    knowledge.router,
    selfplay.router,
    reports.router,
    learning.router,
    dashboard.router,
    findings.router,
    settings.router,
    tools.router,
]:
    app.include_router(router, prefix="/api/v1")

app.include_router(ws.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "CypherMind"}
