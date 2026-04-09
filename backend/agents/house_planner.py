from typing import List
from backend.models.house_models import HouseRequest, HouseOffer
from backend.tools.web_scraper import scraper
import logging

logger = logging.getLogger(__name__)


class HousePlannerAgent:
    """
    Agent responsible for searching and collecting accommodation offers.
    Uses WebScraper to query Airbnb and Booking.
    """
    
    def __init__(self):
        self.name = "HousePlanner"
        self.scraper = scraper
    
    async def search_accommodations(self, request: HouseRequest) -> List[HouseOffer]:
        """
        Search for accommodations across multiple sources.
        Adjusts to remaining budget after flight selection.
        """
        logger.info(f"[{self.name}] Starting accommodation search for {request.destination_country}")
        
        try:
            # Calculate remaining budget
            remaining_budget = request.max_budget - request.selected_flight_price
            
            if remaining_budget <= 0:
                logger.warning(f"[{self.name}] No budget remaining after flight selection")
                return []
            
            logger.info(f"[{self.name}] Remaining budget: {remaining_budget} {request.max_budget} - {request.selected_flight_price}")
            
            # Use scraper to search accommodations
            raw_offers = await self.scraper.search_accommodations(
                destination=request.destination_city or request.destination_country,
                check_in=request.check_in.isoformat(),
                check_out=request.check_out.isoformat(),
                guests=request.guests,
                max_budget=remaining_budget
            )
            
            # Convert to HouseOffer models and filter by budget
            offers = []
            for raw_offer in raw_offers:
                try:
                    offer = HouseOffer(**raw_offer)
                    # Filter by remaining budget
                    if offer.total_price <= remaining_budget:
                        offers.append(offer)
                except Exception as e:
                    logger.warning(f"[{self.name}] Failed to parse offer: {e}")
                    continue
            
            logger.info(f"[{self.name}] Found {len(offers)} accommodation offers within budget")
            return offers
            
        except Exception as e:
            logger.error(f"[{self.name}] Error searching accommodations: {e}")
            return []
