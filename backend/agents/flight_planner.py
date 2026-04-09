from typing import List
from backend.models.flight_models import FlightRequest, FlightOffer
from backend.tools.web_scraper import scraper
import logging

logger = logging.getLogger(__name__)


class FlightPlannerAgent:
    """
    Agent responsible for searching and collecting flight offers.
    Uses WebScraper to query multiple sources.
    """
    
    def __init__(self):
        self.name = "FlightPlanner"
        self.scraper = scraper
    
    async def search_flights(self, request: FlightRequest) -> List[FlightOffer]:
        """
        Search for flights across multiple sources.
        Returns empty list if no flights found.
        """
        logger.info(f"[{self.name}] Starting flight search for {request.origin_airport} -> {request.destination_country}")
        
        try:
            # Use scraper to search flights
            raw_offers = await self.scraper.search_flights(
                origin=request.origin_airport,
                destination=request.destination_country,
                departure_date=request.departure_date.isoformat(),
                return_date=request.return_date.isoformat(),
                passengers=request.passengers,
                max_budget=request.max_budget
            )
            
            # Convert to FlightOffer models
            offers = []
            for raw_offer in raw_offers:
                try:
                    offer = FlightOffer(**raw_offer)
                    offers.append(offer)
                except Exception as e:
                    logger.warning(f"[{self.name}] Failed to parse offer: {e}")
                    continue
            
            logger.info(f"[{self.name}] Found {len(offers)} flight offers")
            return offers
            
        except Exception as e:
            logger.error(f"[{self.name}] Error searching flights: {e}")
            return []
