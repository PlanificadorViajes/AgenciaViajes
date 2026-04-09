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


# Singleton instance
orchestrator = TravelOrchestrator()
