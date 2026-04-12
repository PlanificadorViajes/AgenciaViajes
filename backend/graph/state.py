from typing import TypedDict, Optional, List, Dict, Any


class TravelState(TypedDict, total=False):
    """
    Estado compartido del grafo LangGraph.

    Este estado reemplaza la lógica implícita del TravelOrchestrator.
    Cada nodo del grafo leerá y modificará este diccionario.
    """

    # Entrada inicial
    user_request: Dict[str, Any]

    # Resultados intermedios
    flight_options: Optional[List[Dict[str, Any]]]
    selected_flight: Optional[Dict[str, Any]]

    house_options: Optional[List[Dict[str, Any]]]
    selected_house: Optional[Dict[str, Any]]

    # Resultado final
    travel_plan: Optional[str]

    # Control de flujo
    status: Optional[str]
    error_message: Optional[str]

    # Contexto de revisión
    review_type: Optional[str]
    review_comment: Optional[str]
