# Eliminadas dependencias deterministas directas.
# Toda ejecución real pasa por tools invocadas por agentes.


async def start_node(state):
    return state


async def flight_node(state):
    """
    Nodo agentic real usando create_react_agent.
    Enviamos formato 'messages' como espera LangGraph.
    """
    from backend.graph.agents import build_flight_agent
    from langchain_core.messages import HumanMessage

    agent = build_flight_agent()

    user_request = state["user_request"]

    # Registramos el último request para fallback de la tool
    from backend.graph.agents import set_last_user_request
    set_last_user_request(user_request)

    result = await agent.ainvoke({
        "messages": [
            HumanMessage(
                content=f"Busca vuelos con estos datos: {user_request}"
            )
        ]
    })

    # El agente ReAct devuelve estructura tipo:
    # {"messages": [...]} donde el último mensaje contiene el output
    messages = result.get("messages", [])
    if not messages:
        return {
            "status": "error",
            "error_message": "Flight agent returned no messages"
        }

    final_message = messages[-1]
    return {
        "flight_options": final_message.content,
        "status": "pending_flight_selection"
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

    # 🔎 DEBUG: Ver exactamente qué devuelve el planner
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[house_node] Houses returned: {houses}")

    return {
        "house_options": houses,
        "status": "pending_house_selection"
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

    flight_obj = SimpleNamespace(
        id=flight_data.get("id"),
        price=flight_data.get("price"),
        airline=flight_data.get("airline", "Unknown Airline"),
        origin=user_request.get("origin_airport"),
        destination=user_request.get("destination_country"),
        departure_date=user_request.get("departure_date"),
        return_date=user_request.get("return_date"),
        departure_time=flight_data.get("departure_time", "N/A"),
        arrival_time=flight_data.get("arrival_time", "N/A")
    )

    house_obj = SimpleNamespace(
        id=house_data.get("id"),
        price_per_night=house_data.get("price_per_night"),
        total_price=house_data.get("total_price"),
        name=house_data.get("name", "Selected Accommodation"),
        location=house_data.get("location", user_request.get("destination_country"))
    )

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
