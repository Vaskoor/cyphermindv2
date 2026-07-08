"""Learning and feedback router."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
from app.db.base import get_db
from app.models.learning import PreferencePair
from app.learning.q_learning import q_orchestrator
from app.learning.bradley_terry import fit_bradley_terry

router = APIRouter(prefix="/learning", tags=["learning"])

class FeedbackRequest(BaseModel):
    query: str
    report_a: str
    report_b: str
    winner: str   # "a" or "b"
    agent_combo_a: Optional[str] = None
    agent_combo_b: Optional[str] = None
    analyst_notes: Optional[str] = None

@router.get("/q-table")
async def get_q_table():
    return q_orchestrator.get_policy_summary()

@router.post("/feedback")
async def submit_feedback(body: FeedbackRequest, db: AsyncSession = Depends(get_db)):
    pair = PreferencePair(
        analyst_id=1,
        **body.model_dump()
    )
    db.add(pair)
    await db.commit()
    await db.refresh(pair)
    return {"id": pair.id, "status": "recorded"}

@router.get("/bradley-terry")
async def get_bt_scores(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PreferencePair))
    pairs = result.scalars().all()
    bt_pairs = [
        (p.agent_combo_a or "unknown_a", p.agent_combo_b or "unknown_b", p.winner)
        for p in pairs
        if p.agent_combo_a and p.agent_combo_b
    ]
    scores = fit_bradley_terry(bt_pairs) if bt_pairs else {}
    return {"scores": scores, "pair_count": len(bt_pairs)}
