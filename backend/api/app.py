from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Nuevo sistema basado en LangGraph
from backend.graph.graph_builder import build_travel_graph
from backend.graph.nodes import (
    start_node,
    flight_node,
    house_node,
    finalize_node,
    review_node,
    error_node,
)

travel_graph = build_travel_graph(
    start_node=start_node,
    flight_node=flight_node,
    house_node=house_node,
    finalize_node=finalize_node,
    review_node=review_node,
    error_node=error_node,
)

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
    Ejecuta el grafo LangGraph desde el nodo start.
    """
    result = await travel_graph.ainvoke({
        "user_request": request
    })
    return result


@app.post("/travel/select-flight")
async def select_flight(payload: dict):
    """
    Step 2:
    Actualiza estado y continúa grafo.
    """
    state = {
        "user_request": payload["user_request"],
        "selected_flight": next(
            (f for f in payload["flight_options"]
             if f["id"] == payload["selected_flight_id"]),
            None
        )
    }

    result = await travel_graph.ainvoke(state)
    return result


@app.post("/travel/select-house")
async def select_house(payload: dict):
    """
    Step 3:
    Ejecuta nodo finalize.
    """
    state = {
        "user_request": payload["user_request"],
        "selected_flight": payload["selected_flight"],
        "selected_house": next(
            (h for h in payload["house_options"]
             if h["id"] == payload["selected_house_id"]),
            None
        )
    }

    result = await travel_graph.ainvoke(state)
    return result


@app.post("/travel/review")
async def review_plan(payload: dict):
    """
    HITL Step integrado en grafo.
    """
    state = {
        "user_request": payload["context"]["user_request"],
        "selected_flight": payload["context"].get("selected_flight"),
        "selected_house": payload["context"].get("selected_house"),
        "review_type": payload["type"],
        "review_comment": payload["comment"],
    }

    result = await travel_graph.ainvoke(state)
    return result
