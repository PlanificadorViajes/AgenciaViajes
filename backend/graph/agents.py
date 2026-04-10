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
        # Caso: {'input': {...}} o similar
        data = list(kwargs.values())[0]
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
async def search_accommodations(input_data: dict):
    """
    Busca alojamientos utilizando la lógica determinista del dominio.
    Recibe un diccionario con los parámetros del alojamiento y devuelve
    una lista de opciones rankeadas.
    """
    return await search_accommodations_tool(input_data)


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
    return create_react_agent(llm, tools)


def build_finalize_agent():
    return create_react_agent(llm, tools)
