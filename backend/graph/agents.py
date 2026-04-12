"""
Definición de agentes LLM especializados.

Cada agente:
- Tiene un rol claro
- Puede invocar tools
- Está supervisado por LangGraph (que reemplaza al orquestador clásico)
"""

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

from backend.graph.tools import (
    search_flights_tool,
    search_accommodations_tool,
    generate_travel_plan_tool,
)

# Contexto temporal para fallback si el agente no pasa argumentos
_LAST_USER_REQUEST = None

def set_last_user_request(data: dict):
    global _LAST_USER_REQUEST
    _LAST_USER_REQUEST = data


# -----------------------------
# REGISTRO DE TOOLS PARA LLM
# -----------------------------

@tool
async def search_flights(**kwargs):
    """
    Busca vuelos utilizando la lógica determinista del dominio.
    Acepta argumentos dinámicos del agente y los convierte
    en un FlightRequest real.
    """
    from backend.models.flight_models import FlightRequest
    from datetime import datetime
    import json
    import logging

    logger = logging.getLogger(__name__)
    logger.info(f"[search_flights] kwargs recibidos: {json.dumps(kwargs, default=str)}")

    # El agente puede enviar:
    # 1) Campos planos (origin_airport=...)
    # 2) Un objeto anidado como input_data={...}
    # El agente puede enviar los datos en distintos formatos.
    # Normalizamos aquí de forma robusta.
    if "input_data" in kwargs:
        data = kwargs["input_data"]
    elif len(kwargs) == 1 and isinstance(list(kwargs.values())[0], dict):
        data = list(kwargs.values())[0]
    elif not kwargs and _LAST_USER_REQUEST is not None:
        # Fallback: el agente llamó la tool sin argumentos
        data = _LAST_USER_REQUEST
    else:
        data = kwargs

    flight_request = FlightRequest(
        origin_airport=data["origin_airport"],
        destination_country=data["destination_country"],
        departure_date=datetime.fromisoformat(data["departure_date"]),
        return_date=datetime.fromisoformat(data["return_date"]),
        passengers=data["passengers"],
        max_budget=data["max_budget"],
    )

    return await search_flights_tool(flight_request)


@tool
async def search_accommodations(**kwargs):
    """
    Busca alojamientos utilizando la lógica determinista del dominio.
    Soporta múltiples formatos de entrada del agente y aplica fallback.
    """
    import json
    import logging

    logger = logging.getLogger(__name__)
    logger.info(f"[search_accommodations] kwargs recibidos: {json.dumps(kwargs, default=str)}")

    # Normalización robusta (igual que vuelos)
    if "input_data" in kwargs:
        data = kwargs["input_data"]
    elif len(kwargs) == 1 and isinstance(list(kwargs.values())[0], dict):
        data = list(kwargs.values())[0]
    elif not kwargs and _LAST_USER_REQUEST is not None:
        # Fallback si el agente llama sin argumentos
        data = _LAST_USER_REQUEST
    else:
        data = kwargs

    # Convertimos dict → modelo de dominio (igual que vuelos)
    from backend.models.house_models import HouseRequest
    from datetime import datetime

    house_request = HouseRequest(
        destination_country=data["destination_country"],
        destination_city=data.get("destination_city"),
        departure_date=datetime.fromisoformat(data["departure_date"]),
        return_date=datetime.fromisoformat(data["return_date"]),
        passengers=data["passengers"],
        max_budget=data["max_budget"],
        selected_flight_price=data.get("selected_flight_price"),
    )

    return await search_accommodations_tool(house_request)


@tool
def generate_travel_plan(input_data: dict):
    """
    Genera el documento final del plan de viaje combinando
    request del usuario, vuelo seleccionado y alojamiento.
    """
    return generate_travel_plan_tool(input_data)


tools = [
    search_flights,
    search_accommodations,
    generate_travel_plan,
]


# -----------------------------
# LLM BASE
# -----------------------------

import os

llm = ChatOpenAI(
    base_url="https://genia4as.services.ai.azure.com/api/projects/firstProject/openai/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o",
    temperature=0
)


# -----------------------------
# AGENTES ESPECIALIZADOS
# -----------------------------

def build_flight_agent():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Eres un agente especializado en búsqueda de vuelos. "
            "SIEMPRE debes usar la herramienta 'search_flights' para obtener resultados. "
            "No respondas con texto explicativo. "
            "Devuelve exclusivamente el resultado de la herramienta."
        ),
        ("placeholder", "{messages}")
    ])
    return create_react_agent(llm, tools, prompt=prompt)


def build_house_agent():
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Eres un agente especializado en búsqueda de alojamientos. "
            "Tu única acción permitida es usar la herramienta 'search_accommodations'. "
            "NO puedes responder con texto libre. "
            "NO puedes analizar. "
            "Debes invocar la herramienta inmediatamente."
        ),
        ("placeholder", "{messages}")
    ])
    # Solo le damos acceso a la tool de alojamientos
    return create_react_agent(
        llm,
        [search_accommodations],
        prompt=prompt
    )


def build_finalize_agent():
    return create_react_agent(llm, tools)
