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
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
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

    review_type = payload["type"]
    logging.info(f"[REVIEW] review_type recibido: {review_type}")
    context = payload["context"]
    user_request = context["user_request"]
    selected_flight = context.get("selected_flight")
    selected_house = context.get("selected_house")

    # ✅ Caso HITL: cambiar SOLO alojamiento
    if review_type == "house_criteria":
        from backend.graph.nodes import house_node
        logging.info(f"[REVIEW] house_criteria recibido. selected_flight={bool(selected_flight)}")

        state = {
            "user_request": user_request,
            "selected_flight": selected_flight,
            "review_type": review_type,
            "review_comment": payload["comment"],
        }

        # ⚠️ Forzamos llamada directa a house_node SIEMPRE
        return await house_node(state)

    # ✅ Caso HITL: recalcular SOLO vuelo y mantener alojamiento
    if review_type == "flight_criteria":
        from backend.graph.nodes import flight_node, finalize_node

        # 1️⃣ Recalcular vuelos
        flight_result = await flight_node({
            "user_request": user_request
        })

        flight_options = flight_result.get("flight_options", [])
        if not flight_options:
            return flight_result

        # 2️⃣ Elegimos el mejor vuelo automáticamente (top score)
        new_flight = flight_options[0]

        # 3️⃣ Mantener alojamiento actual y regenerar plan final
        state = {
            "user_request": user_request,
            "selected_flight": new_flight,
            "selected_house": selected_house,
        }

        result = await finalize_node(state)

        # ✅ Devolver también el nuevo vuelo al frontend
        result["selected_flight"] = new_flight

        return result

    # ✅ Caso HITL: reinicio completo (legacy)
    if review_type == "criteria":
        state = {
            "user_request": user_request,
        }
        return await travel_graph.ainvoke(state)

    # ✅ Caso HITL: aprobación → devolver archivo descargable (.md)
    if review_type == "approve":
        from fastapi.responses import Response
        from datetime import datetime

        travel_plan = payload.get("context", {}).get("final_plan")

        if not travel_plan:
            # fallback: regenerar con datos actuales
            from backend.graph.nodes import finalize_node
            result = await finalize_node({
                "user_request": user_request,
                "selected_flight": selected_flight,
                "selected_house": selected_house,
            })
            travel_plan = result.get("travel_plan")

        filename = f"travel_itinerary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

        return Response(
            content=travel_plan,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    # ✅ Caso editorial u otros → flujo normal
    state = {
        "user_request": user_request,
        "selected_flight": selected_flight,
        "selected_house": selected_house,
        "review_type": review_type,
        "review_comment": payload["comment"],
    }

    return await travel_graph.ainvoke(state)
