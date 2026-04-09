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
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

from travel_itinerary_mvp.graph.orchestrator import ItineraryOrchestrator


app = FastAPI(title="Travel Itinerary MVP API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = ItineraryOrchestrator()


# -----------------------------
# Request / Response Schemas
# -----------------------------

class TravelRequestDTO(BaseModel):
    origin_airport: str
    destination_country: str
    departure_date: str
    return_date: str
    passengers: int
    budget: float


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

    # Convert structured data to natural language for the agents
    user_input = f"""
    Quiero planificar un viaje con las siguientes características:
    - Origen: Aeropuerto {request.origin_airport}
    - Destino: {request.destination_country}
    - Fecha de ida: {request.departure_date}
    - Fecha de vuelta: {request.return_date}
    - Número de pasajeros: {request.passengers}
    - Presupuesto: {request.budget}€
    """.strip()

    state = orchestrator.process_request(
        user_input=user_input,
        constraints={
            "budget": request.budget,
            "origin_airport": request.origin_airport,
            "destination_country": request.destination_country,
            "departure_date": request.departure_date,
            "return_date": request.return_date,
            "passengers": request.passengers
        }
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
