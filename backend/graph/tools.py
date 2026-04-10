"""
Definición de Tools accesibles por los agentes.

Los agentes NO son tools.
Los agentes son entidades LLM que pueden invocar estas tools.
"""

from typing import Dict, Any, List
from backend.domain.flight_planner import FlightPlannerAgent
from backend.domain.house_planner import HousePlannerAgent
from backend.domain.flight_analyst import FlightAnalystAgent
from backend.domain.house_analyst import HouseAnalystAgent
from backend.domain.documentalist import DocumentalistAgent


# Instancias reales (lógica determinista existente)
flight_planner = FlightPlannerAgent()
house_planner = HousePlannerAgent()
flight_analyst = FlightAnalystAgent()
house_analyst = HouseAnalystAgent()
documentalist = DocumentalistAgent()


# -------------------------
# TOOLS DISPONIBLES
# -------------------------

async def search_flights_tool(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool: Buscar vuelos según request estructurado.
    """
    flights = await flight_planner.search_flights(input_data)
    ranked = flight_analyst.analyze_and_rank(flights, max_results=5)
    return [f.dict() for f in ranked]


async def search_accommodations_tool(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Tool: Buscar alojamientos según request estructurado.
    """
    houses = await house_planner.search_accommodations(input_data)
    ranked = house_analyst.analyze_and_rank(houses, max_results=5)
    return [h.dict() for h in ranked]


def generate_travel_plan_tool(input_data: Dict[str, Any]) -> str:
    """
    Tool: Generar documento final.
    """
    return documentalist.generate_travel_plan(**input_data)
