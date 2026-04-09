"""
FastAPI application implementing target MVP architecture.

Architecture:
Frontend
 ↓
FastAPI
 ↓
Orchestrator
 ↓
Analyst → Planner → Critic
 ↓
HITL
 ↓
PostgreSQL (future integration layer prepared)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

from travel_itinerary_mvp.graph.orchestrator import ItineraryOrchestrator


app = FastAPI(title="Travel Itinerary MVP API")

orchestrator = ItineraryOrchestrator()


# -----------------------------
# Request / Response Schemas
# -----------------------------

class TravelRequestDTO(BaseModel):
    user_input: str
    budget: Optional[int] = None


class TravelPlanResponse(BaseModel):
    session_id: str
    status: str
    approved: bool
    score: float
    plan: Optional[dict]


# -----------------------------
# Endpoints
# -----------------------------

@app.post("/travel-request", response_model=TravelPlanResponse)
def create_travel_request(request: TravelRequestDTO):
    session_id = str(uuid4())

    state = orchestrator.process_request(
        user_input=request.user_input,
        constraints={"budget": request.budget} if request.budget else None
    )

    return TravelPlanResponse(
        session_id=state.session_id,
        status=state.status,
        approved=state.approved,
        score=state.get_current_score(),
        plan=state.current_plan
    )


@app.get("/travel-plan/{session_id}", response_model=TravelPlanResponse)
def get_travel_plan(session_id: str):
    raise HTTPException(status_code=501, detail="PostgreSQL integration pending")


@app.post("/travel-plan/{session_id}/refine", response_model=TravelPlanResponse)
def refine_travel_plan(session_id: str):
    raise HTTPException(status_code=501, detail="Refinement flow pending")


@app.post("/travel-plan/{session_id}/human-review")
def human_review(session_id: str):
    raise HTTPException(status_code=501, detail="HITL module pending")
