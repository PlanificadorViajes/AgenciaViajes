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
    Nodo especializado en alojamientos.
    Flujo controlado por el grafo.
    """
    if not state.get("selected_flight"):
        return state

    from backend.graph.agents import build_house_agent
    agent = build_house_agent()

    user_request = state["user_request"]
    selected_flight = state["selected_flight"]

    payload = {
        "destination_country": user_request["destination_country"],
        "destination_city": user_request.get("destination_city"),
        "departure_date": user_request["departure_date"],
        "return_date": user_request["return_date"],
        "passengers": user_request["passengers"],
        "max_budget": user_request["max_budget"],
        "selected_flight_price": selected_flight["price"],
    }

    result = await agent.ainvoke({
        "input": f"Busca alojamientos con estos datos: {payload}"
    })

    if not result or "output" not in result:
        return {
            "status": "no_accommodation_budget",
            "error_message": "House agent failed"
        }

    return {
        "house_options": result["output"],
        "status": "pending_house_selection"
    }


async def finalize_node(state):
    """
    Nodo de generación final.
    """
    if not state.get("selected_house"):
        return state

    from backend.graph.agents import build_finalize_agent
    agent = build_finalize_agent()

    payload = {
        "user_request": state["user_request"],
        "selected_flight": state["selected_flight"],
        "selected_house": state["selected_house"],
    }

    result = await agent.ainvoke({
        "input": f"Genera el plan final con estos datos: {payload}"
    })

    if not result or "output" not in result:
        return {
            "status": "error",
            "error_message": "Finalize agent failed"
        }

    return {
        "travel_plan": result["output"],
        "status": "completed"
    }


async def review_node(state):
    return state


async def error_node(state):
    return state
