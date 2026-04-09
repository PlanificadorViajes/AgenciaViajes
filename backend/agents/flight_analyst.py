from typing import List
from backend.models.flight_models import FlightOffer
import logging

logger = logging.getLogger(__name__)


class FlightAnalystAgent:
    """
    Agent responsible for analyzing flight offers and selecting the best ones.
    Calculates quality-price scores and returns top 5.
    """
    
    def __init__(self):
        self.name = "FlightAnalyst"
    
    def analyze_and_rank(self, offers: List[FlightOffer], max_results: int = 5) -> List[FlightOffer]:
        """
        Analyze flight offers and return top N based on quality-price score.
        
        Score calculation considers:
        - Price (lower is better)
        - Number of stops (fewer is better)
        - Duration (shorter is better - if available)
        """
        logger.info(f"[{self.name}] Analyzing {len(offers)} flight offers")
        
        if not offers:
            return []
        
        # Calculate score for each offer
        scored_offers = []
        for offer in offers:
            score = self._calculate_score(offer, offers)
            offer.score = score
            scored_offers.append(offer)
        
        # Sort by score (higher is better)
        scored_offers.sort(key=lambda x: x.score, reverse=True)
        
        # Return top N
        top_offers = scored_offers[:max_results]
        logger.info(f"[{self.name}] Selected top {len(top_offers)} offers")
        
        return top_offers
    
    def _calculate_score(self, offer: FlightOffer, all_offers: List[FlightOffer]) -> float:
        """
        Calculate quality-price score for a flight offer.
        Score ranges from 0 to 100 (higher is better).
        """
        # Get price range
        prices = [o.price for o in all_offers]
        min_price = min(prices)
        max_price = max(prices)
        
        # Normalize price (0-50 points, lower price = higher score)
        if max_price > min_price:
            price_score = 50 * (1 - (offer.price - min_price) / (max_price - min_price))
        else:
            price_score = 50
        
        # Stops score (0-30 points)
        # 0 stops = 30 points, 1 stop = 20 points, 2+ stops = 10 points
        if offer.stops == 0:
            stops_score = 30
        elif offer.stops == 1:
            stops_score = 20
        else:
            stops_score = 10
        
        # Duration score (0-20 points) - simple heuristic
        # Parse duration if available
        duration_score = 15  # Default mid-range score
        try:
            if 'h' in offer.duration:
                hours = int(offer.duration.split('h')[0].strip())
                if hours <= 2:
                    duration_score = 20
                elif hours <= 5:
                    duration_score = 15
                elif hours <= 10:
                    duration_score = 10
                else:
                    duration_score = 5
        except:
            pass
        
        total_score = price_score + stops_score + duration_score
        
        logger.debug(f"[{self.name}] {offer.id}: price={price_score:.1f}, stops={stops_score}, duration={duration_score}, total={total_score:.1f}")
        
        return round(total_score, 2)
