from typing import Dict, List, Optional
from datetime import datetime
import logging

from backend.models.flight_models import FlightRequest, FlightOffer
from backend.models.house_models import HouseRequest, HouseOffer
from backend.agents.flight_planner import FlightPlannerAgent
from backend.agents.flight_analyst import FlightAnalystAgent
from backend.agents.house_planner import HousePlannerAgent
from backend.agents.house_analyst import HouseAnalystAgent
from backend.agents.documentalist import DocumentalistAgent
from backend.llm.client import AzureLLMClient
import json

logger = logging.getLogger(__name__)


class TravelOrchestrator:
    """
    Central orchestrator that coordinates all agents in the travel planning system.
    
    Workflow:
    1. FlightPlannerAgent searches for flights
    2. FlightAnalystAgent ranks and selects top 5
    3. User/System selects one flight
    4. HousePlannerAgent searches accommodations with remaining budget
    5. HouseAnalystAgent ranks and selects top 5
    6. User/System selects one accommodation
    7. DocumentalistAgent generates final travel plan
    """
    
    def __init__(self):
        self.flight_planner = FlightPlannerAgent()
        self.flight_analyst = FlightAnalystAgent()
        self.house_planner = HousePlannerAgent()
        self.house_analyst = HouseAnalystAgent()
        self.documentalist = DocumentalistAgent()
        self.llm = AzureLLMClient()
        logger.info("[Orchestrator] Initialized with all agents")
    
    async def create_travel_plan(self, user_request: Dict) -> Dict:
        """
        Main orchestration method that coordinates all agents.
        
        Args:
            user_request: Dictionary containing:
                - origin_airport: str
                - destination_country: str
                - destination_city: Optional[str]
                - departure_date: str (ISO format)
                - return_date: str (ISO format)
                - passengers: int
                - max_budget: float
        
        Returns:
            Dictionary with:
                - flight_options: List of top 5 flights
                - house_options: List of top 5 accommodations (after flight selection)
                - travel_plan: Final markdown document (after both selections)
                - status: 'pending_flight_selection' | 'pending_house_selection' | 'completed'
        """
        logger.info(f"[Orchestrator] Starting travel plan creation for {user_request['destination_country']}")
        
        try:
            # Step 1 & 2: Search and analyze flights
            flight_request = FlightRequest(
                origin_airport=user_request['origin_airport'],
                destination_country=user_request['destination_country'],
                departure_date=datetime.fromisoformat(user_request['departure_date']),
                return_date=datetime.fromisoformat(user_request['return_date']),
                passengers=user_request['passengers'],
                max_budget=user_request['max_budget']
            )
            
            all_flights = await self.flight_planner.search_flights(flight_request)
            
            if not all_flights:
                return {
                    'status': 'error',
                    'message': 'No flights found for your criteria',
                    'flight_options': [],
                    'house_options': [],
                    'travel_plan': None
                }
            
            top_flights = self.flight_analyst.analyze_and_rank(all_flights, max_results=5)
            
            logger.info(f"[Orchestrator] Returning {len(top_flights)} flight options to user")
            
            return {
                'status': 'pending_flight_selection',
                'flight_options': [flight.dict() for flight in top_flights],
                'house_options': [],
                'travel_plan': None
            }
            
        except Exception as e:
            logger.error(f"[Orchestrator] Error creating travel plan: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'flight_options': [],
                'house_options': [],
                'travel_plan': None
            }
    
    async def continue_with_flight_selection(
        self,
        user_request: Dict,
        selected_flight_id: str,
        flight_options: List[Dict]
    ) -> Dict:
        """
        Continue orchestration after user selects a flight.
        
        Args:
            user_request: Original request
            selected_flight_id: ID of the selected flight
            flight_options: Previously returned flight options
        
        Returns:
            Dictionary with accommodation options
        """
        logger.info(f"[Orchestrator] Continuing with flight selection: {selected_flight_id}")
        
        try:
            # Find selected flight
            selected_flight_data = next(
                (f for f in flight_options if f['id'] == selected_flight_id),
                None
            )
            
            if not selected_flight_data:
                # If not found, use the first one (best score)
                selected_flight_data = flight_options[0]
                logger.warning(f"[Orchestrator] Flight {selected_flight_id} not found, using best option")
            
            selected_flight = FlightOffer(**selected_flight_data)
            
            # Step 3 & 4: Search and analyze accommodations
            house_request = HouseRequest(
                destination_country=user_request['destination_country'],
                destination_city=user_request.get('destination_city'),
                check_in=datetime.fromisoformat(user_request['departure_date']),
                check_out=datetime.fromisoformat(user_request['return_date']),
                guests=user_request['passengers'],
                max_budget=user_request['max_budget'],
                selected_flight_price=selected_flight.price
            )
            
            all_houses = await self.house_planner.search_accommodations(house_request)
            
            if not all_houses:
                return {
                    'status': 'error',
                    'message': 'No accommodations found within remaining budget',
                    'flight_options': flight_options,
                    'selected_flight': selected_flight_data,
                    'house_options': [],
                    'travel_plan': None
                }
            
            top_houses = self.house_analyst.analyze_and_rank(all_houses, max_results=5)
            
            logger.info(f"[Orchestrator] Returning {len(top_houses)} accommodation options to user")
            
            return {
                'status': 'pending_house_selection',
                'selected_flight': selected_flight_data,
                'house_options': [house.dict() for house in top_houses],
                'travel_plan': None
            }
            
        except Exception as e:
            logger.error(f"[Orchestrator] Error in flight selection continuation: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'selected_flight': None,
                'house_options': [],
                'travel_plan': None
            }
    
    def finalize_with_house_selection(
        self,
        user_request: Dict,
        selected_flight: Dict,
        selected_house_id: str,
        house_options: List[Dict],
        flight_alternatives: List[Dict] = None
    ) -> Dict:
        """
        Finalize orchestration after user selects accommodation.
        
        Args:
            user_request: Original request
            selected_flight: Previously selected flight
            selected_house_id: ID of the selected accommodation
            house_options: Previously returned accommodation options
            flight_alternatives: Alternative flights for reference
        
        Returns:
            Dictionary with complete travel plan
        """
        logger.info(f"[Orchestrator] Finalizing with house selection: {selected_house_id}")
        
        try:
            # Find selected house
            selected_house_data = next(
                (h for h in house_options if h['id'] == selected_house_id),
                None
            )
            
            if not selected_house_data:
                # If not found, use the first one (best score)
                selected_house_data = house_options[0]
                logger.warning(f"[Orchestrator] House {selected_house_id} not found, using best option")
            
            # Convert to model objects
            flight_offer = FlightOffer(**selected_flight)
            house_offer = HouseOffer(**selected_house_data)
            
            # Get alternatives (excluding selected ones)
            flight_alts = None
            if flight_alternatives:
                flight_alts = [
                    FlightOffer(**f) for f in flight_alternatives 
                    if f['id'] != selected_flight['id']
                ][:3]
            
            house_alts = [
                HouseOffer(**h) for h in house_options 
                if h['id'] != selected_house_id
            ][:3]
            
            # Step 5: Generate final document
            travel_plan_md = self.documentalist.generate_travel_plan(
                user_request=user_request,
                selected_flight=flight_offer,
                selected_house=house_offer,
                flight_alternatives=flight_alts,
                house_alternatives=house_alts
            )
            
            logger.info(f"[Orchestrator] Travel plan completed successfully")
            
            return {
                'status': 'completed',
                'selected_flight': selected_flight,
                'selected_house': selected_house_data,
                'travel_plan': travel_plan_md,
                'total_cost': flight_offer.price + house_offer.total_price
            }
            
        except Exception as e:
            logger.error(f"[Orchestrator] Error in house selection finalization: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'travel_plan': None
            }

    async def review_plan(self, review_type: str, comment: str, context: Dict) -> Dict:
        """
        HITL review logic.
        review_type: "editorial" | "criteria"
        comment: user feedback
        context: {
            user_request,
            selected_flight,
            selected_house
        }
        """
        logger.info(f"[Orchestrator] Review requested. Type: {review_type}")

        try:
            user_request = context.get("user_request")
            selected_flight = context.get("selected_flight")
            selected_house = context.get("selected_house")

            if review_type == "editorial":
                # Regenerate document with comment
                flight_offer = FlightOffer(**selected_flight)
                house_offer = HouseOffer(**selected_house)

                revised_plan = self.documentalist.generate_travel_plan(
                    user_request=user_request,
                    selected_flight=flight_offer,
                    selected_house=house_offer,
                    revision_comment=comment  # Documentalist can optionally use this
                )

                return {
                    "status": "revised",
                    "travel_plan": revised_plan
                }

            elif review_type == "criteria":
                logger.info("[Orchestrator] Re-running search due to criteria change")

                constraints = await self._extract_constraints(comment)
                logger.info(f"[Orchestrator] Parsed constraints object: {constraints}")

                entity = constraints.get("entity")
                if isinstance(entity, str):
                    entity = entity.lower()

                # --- HOUSE constraints ---
                if entity == "house" and selected_flight:
                    flight_offer = FlightOffer(**selected_flight)

                    house_request = HouseRequest(
                        destination_country=user_request['destination_country'],
                        destination_city=user_request.get('destination_city'),
                        check_in=datetime.fromisoformat(user_request['departure_date']),
                        check_out=datetime.fromisoformat(user_request['return_date']),
                        guests=user_request['passengers'],
                        max_budget=user_request['max_budget'],
                        selected_flight_price=flight_offer.price
                    )

                    all_houses = await self.house_planner.search_accommodations(house_request)

                    filtered = all_houses
                    for key, value in constraints.get("constraints", {}).items():
                        if value is not None:
                            filtered = [
                                h for h in filtered
                                if hasattr(h, key) and getattr(h, key) == value
                            ]

                    if not filtered:
                        return {
                            "status": "error",
                            "message": "No accommodations match the requested criteria."
                        }

                    ranked = self.house_analyst.analyze_and_rank(filtered, max_results=5)

                    logger.info(f"[Orchestrator] Returning {len(ranked)} filtered accommodation options to user")

                    return {
                        "status": "pending_house_selection",
                        "selected_flight": selected_flight,
                        "house_options": [h.dict() for h in ranked],
                        "travel_plan": None
                    }

                # --- FLIGHT constraints or fallback ---
                return await self.create_travel_plan(user_request)

            else:
                return {
                    "status": "error",
                    "message": "Invalid review type"
                }

        except Exception as e:
            logger.error(f"[Orchestrator] Error in review process: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def _extract_constraints(self, comment: str) -> Dict:
        """
        Uses LLM to extract structured constraints from user comment.
        Returns dict:
        {
            "entity": "house" | "flight" | None,
            "constraints": { ... }
        }
        """
        system_prompt = """
You are a multilingual constraint extractor for a travel planning system.

The user may write in Spanish or English.

Return ONLY valid JSON with this structure:

{
  "entity": "house" | "flight" | null,
  "constraints": {
    "bathrooms": integer or null,
    "bedrooms": integer or null,
    "beds": integer or null,
    "max_guests": integer or null
  }
}

Interpret both Spanish and English terms:

Spanish examples:
- baño / baños → bathrooms
- dormitorio / dormitorios / habitación / habitaciones → bedrooms
- cama / camas → beds
- personas / huéspedes → max_guests

English examples:
- bathroom(s)
- bedroom(s)
- bed(s)
- guest(s)

Rules:
- If the comment refers to accommodation features, entity = "house".
- If it refers to flights (mañana, morning, directo, direct, barato, cheaper, etc), entity = "flight".
- Extract numeric values whether written as digits or words (e.g., "dos", "two").
- If not applicable, return null values.
- Return ONLY JSON. No explanation. No markdown.
"""

        try:
            logger.info(f"[Orchestrator] Sending comment to LLM: {comment}")
            raw = self.llm.generate(system_prompt=system_prompt, user_prompt=comment)
            logger.info(f"[Orchestrator] Raw LLM response: {raw}")

            # --- Defensive JSON extraction ---
            start = raw.find("{")
            end = raw.rfind("}") + 1

            if start == -1 or end == -1:
                logger.warning("[Orchestrator] No JSON object detected in LLM response")
                return {"entity": None, "constraints": {}}

            json_str = raw[start:end]

            parsed = json.loads(json_str)

            if not isinstance(parsed, dict):
                return {"entity": None, "constraints": {}}

            parsed.setdefault("constraints", {})

            logger.info(f"[Orchestrator] Extracted constraints: {parsed}")

            return parsed

        except Exception as e:
            logger.warning(f"[Orchestrator] Constraint extraction failed: {e}")
            return {"entity": None, "constraints": {}}


# Singleton instance
orchestrator = TravelOrchestrator()
