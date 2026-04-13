# Eliminadas dependencias deterministas directas.
# Toda ejecución real pasa por tools invocadas por agentes.

import logging
import re

logger = logging.getLogger(__name__)


def _filter_houses_by_review_comment(houses, comment):
    """
    Ranking inteligente (Opción B):
    - No elimina completamente opciones
    - Penaliza estructuralmente si no cumple requisitos
    - Ordena por proximidad a los criterios del usuario
    """

    if not comment:
        return houses

    beds_pattern = re.search(r"(\d+)\s*(?:camas?|beds?)", comment, re.IGNORECASE)
    bedrooms_pattern = re.search(r"(\d+)\s*(?:dormitorios?|habitaciones?|rooms?)", comment, re.IGNORECASE)
    bathrooms_pattern = re.search(r"(\d+)\s*(?:bañ?os?|bathrooms?)", comment, re.IGNORECASE)

    target_beds = int(beds_pattern.group(1)) if beds_pattern else None
    target_bedrooms = int(bedrooms_pattern.group(1)) if bedrooms_pattern else None
    target_bathrooms = int(bathrooms_pattern.group(1)) if bathrooms_pattern else None

    if not any([target_beds, target_bedrooms, target_bathrooms]):
        return houses

    scored = []

    for house in houses:
        beds = house.get("beds") or 0
        bedrooms = house.get("bedrooms") or 0
        bathrooms = house.get("bathrooms") or 0

        penalty = 0

        if target_beds is not None:
            penalty += abs(beds - target_beds) * 15

        if target_bedrooms is not None:
            penalty += abs(bedrooms - target_bedrooms) * 20

        if target_bathrooms is not None:
            penalty += abs(bathrooms - target_bathrooms) * 25

        base_score = house.get("score", 0)
        adjusted_score = base_score - penalty

        house_copy = dict(house)
        house_copy["score"] = max(adjusted_score, 0)
        house_copy["hitl_penalty"] = penalty

        scored.append(house_copy)

    scored.sort(key=lambda x: x["score"], reverse=True)

    logger.info(
        f"[house_node] Ranking HITL aplicado -> beds={target_beds}, bedrooms={target_bedrooms}, bathrooms={target_bathrooms}"
    )

    return scored


async def start_node(state):
    return state


async def flight_node(state):
    """
    Nodo determinista temporal para vuelos.
    Ejecuta la tool estructurada en lugar del agente ReAct
    para devolver opciones listas para el frontend.
    """
    from backend.graph.agents import set_last_user_request
    from backend.graph.tools import search_flights_tool
    from backend.models.flight_models import FlightRequest
    from datetime import date
    import logging

    user_request = state["user_request"]
    set_last_user_request(user_request)

    try:
        flight_request = FlightRequest(
            origin_airport=user_request["origin_airport"],
            destination_country=user_request["destination_country"],
            departure_date=date.fromisoformat(user_request["departure_date"]),
            return_date=date.fromisoformat(user_request["return_date"]),
            passengers=user_request["passengers"],
            max_budget=user_request["max_budget"],
        )
    except Exception as exc:
        return {
            "status": "error",
            "error_message": f"Invalid flight request payload: {exc}",
        }

    flights = await search_flights_tool(flight_request.dict())

    logger = logging.getLogger(__name__)
    logger.info(f"[flight_node] Flights returned: {len(flights)}")

    return {
        "flight_options": flights,
        "status": "pending_flight_selection",
    }


async def house_node(state):
    """
    Nodo agentic real para alojamientos.
    Usa create_react_agent con formato messages.
    """
    if not state.get("selected_flight"):
        return state

    from backend.graph.agents import build_house_agent, set_last_user_request
    from langchain_core.messages import HumanMessage

    agent = build_house_agent()

    user_request = state["user_request"]
    selected_flight = state["selected_flight"]
    review_type = state.get("review_type")
    review_comment = state.get("review_comment")

    # Registramos request para fallback
    set_last_user_request(user_request)

    payload = {
        "destination_country": user_request["destination_country"],
        "destination_city": user_request.get("destination_city"),
        "departure_date": user_request["departure_date"],
        "return_date": user_request["return_date"],
        "passengers": user_request["passengers"],
        "max_budget": user_request["max_budget"],
        "selected_flight_price": selected_flight["price"],
    }

    # ⚠ Bypass temporal del agente para evitar recursión ReAct
    # Ejecutamos la lógica determinista directamente (igual que hicimos con vuelos)
    from backend.graph.tools import search_accommodations_tool
    from backend.models.house_models import HouseRequest
    from datetime import datetime

    house_request = HouseRequest(
        destination_country=payload["destination_country"],
        destination_city=payload.get("destination_city"),
        check_in=datetime.fromisoformat(payload["departure_date"]),
        check_out=datetime.fromisoformat(payload["return_date"]),
        guests=payload["passengers"],
        max_budget=payload["max_budget"],
        selected_flight_price=payload.get("selected_flight_price"),
    )

    houses = await search_accommodations_tool(house_request)

    if review_type == "house_criteria":
        houses = _filter_houses_by_review_comment(houses, review_comment)

    # 🔎 DEBUG: Ver exactamente qué devuelve el planner
    logger.info(f"[house_node] Houses returned: {len(houses)} opciones")

    return {
        "house_options": houses,
        "status": "pending_house_selection",
        "review_type": None,
    }


async def finalize_node(state):
    """
    Nodo de generación final (determinista).
    Llama directamente a la tool generate_travel_plan.
    """
    if not state.get("selected_house"):
        return state

    from backend.graph.tools import generate_travel_plan_tool

    from types import SimpleNamespace

    # Construimos objetos completos con los atributos que el domain espera
    flight_data = state["selected_flight"]
    house_data = state["selected_house"]
    user_request = state["user_request"]

    flight_obj = SimpleNamespace(**flight_data)
    house_obj = SimpleNamespace(**house_data)

    # Normalizamos todos los campos que usa Documentalist
    flight_obj.origin = getattr(flight_obj, "origin", user_request.get("origin_airport"))
    flight_obj.destination = getattr(flight_obj, "destination", user_request.get("destination_country"))
    flight_obj.departure_date = getattr(flight_obj, "departure_date", user_request.get("departure_date"))
    flight_obj.arrival_date = getattr(flight_obj, "arrival_date", user_request.get("return_date"))
    flight_obj.departure_time = getattr(flight_obj, "departure_time", "N/A")
    flight_obj.arrival_time = getattr(flight_obj, "arrival_time", "N/A")
    flight_obj.duration = getattr(flight_obj, "duration", "N/A")
    flight_obj.stops = getattr(flight_obj, "stops", 0)
    flight_obj.score = getattr(flight_obj, "score", 0)
    flight_obj.source = getattr(flight_obj, "source", "unknown")
    flight_obj.booking_url = getattr(flight_obj, "booking_url", "https://example.com/flight")

    house_obj.name = getattr(house_obj, "name", "Selected Accommodation")
    house_obj.type = getattr(house_obj, "type", "Apartment")
    house_obj.location = getattr(house_obj, "location", house_data.get("city") or user_request.get("destination_country"))
    house_obj.city = getattr(house_obj, "city", user_request.get("destination_country"))
    house_obj.rating = getattr(house_obj, "rating", 0)
    house_obj.reviews_count = getattr(house_obj, "reviews_count", 0)
    house_obj.bedrooms = getattr(house_obj, "bedrooms", 1)
    house_obj.beds = getattr(house_obj, "beds", 1)
    house_obj.bathrooms = getattr(house_obj, "bathrooms", 1)
    house_obj.max_guests = getattr(house_obj, "max_guests", user_request.get("passengers", 1))
    house_obj.amenities = getattr(house_obj, "amenities", [])
    house_obj.score = getattr(house_obj, "score", 0)
    house_obj.source = getattr(house_obj, "source", "unknown")
    house_obj.booking_url = getattr(house_obj, "booking_url", "https://example.com/accommodation")

    payload = {
        "user_request": state["user_request"],
        "selected_flight": flight_obj,
        "selected_house": house_obj,
    }

    travel_plan = generate_travel_plan_tool(payload)

    return {
        "travel_plan": travel_plan,
        "status": "completed"
    }


async def review_node(state):
    return state


async def error_node(state):
    return state
