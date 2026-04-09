from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.orchestrator.travel_orchestrator import orchestrator

app = FastAPI(title="Travel Planner Backend")

# CORS configuration (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/travel/start")
async def start_travel_plan(request: dict):
    """
    Step 1:
    Returns top flight options.
    """
    return await orchestrator.create_travel_plan(request)


@app.post("/travel/select-flight")
async def select_flight(payload: dict):
    """
    Step 2:
    User selects a flight.
    """
    return await orchestrator.continue_with_flight_selection(
        user_request=payload["user_request"],
        selected_flight_id=payload["selected_flight_id"],
        flight_options=payload["flight_options"],
    )


@app.post("/travel/select-house")
def select_house(payload: dict):
    """
    Step 3:
    User selects accommodation and final document is generated.
    """
    return orchestrator.finalize_with_house_selection(
        user_request=payload["user_request"],
        selected_flight=payload["selected_flight"],
        selected_house_id=payload["selected_house_id"],
        house_options=payload["house_options"],
        flight_alternatives=payload.get("flight_alternatives"),
    )
