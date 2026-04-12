from langgraph.graph import StateGraph, END
from backend.graph.state import TravelState


def build_travel_graph(
    start_node,
    flight_node,
    house_node,
    finalize_node,
    review_node,
    error_node,
):
    """
    Construye el StateGraph equivalente al flujo actual del TravelOrchestrator.
    Mantiene exactamente el mismo comportamiento funcional.
    """

    builder = StateGraph(TravelState)

    # Registrar nodos
    builder.add_node("start", start_node)
    builder.add_node("flight", flight_node)
    builder.add_node("house", house_node)
    builder.add_node("finalize", finalize_node)
    builder.add_node("review", review_node)
    builder.add_node("error", error_node)

    # Entrada
    builder.set_entry_point("start")

    # Flujo principal
    builder.add_edge("start", "flight")
    builder.add_edge("flight", "house")
    builder.add_edge("house", "finalize")
    builder.add_edge("finalize", END)

    # -----------------------------
    # FLUJO HITL CONDICIONAL
    # -----------------------------

    def review_router(state):
        review_type = state.get("review_type")
        if review_type == "editorial":
            return "finalize"
        if review_type == "house_criteria":
            state.pop("selected_house", None)
            state.pop("house_options", None)
            return "house"
        if review_type in {"criteria", "flight_criteria"}:
            state.pop("selected_house", None)
            state.pop("selected_flight", None)
            state.pop("house_options", None)
            state.pop("flight_options", None)
            return "flight"
        return END

    builder.add_conditional_edges(
        "review",
        review_router,
        {
            "finalize": "finalize",
            "house": "house",
            "flight": "flight",
            END: END,
        },
    )

    # Flujo de error
    builder.add_edge("error", END)

    return builder.compile()
