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
            score, breakdown = self._calculate_score(offer, offers)
            offer.score = score
            # Attach breakdown for frontend visibility (MVP transparency)
            offer.scoring_breakdown = breakdown
            scored_offers.append(offer)
        
        # Sort by score (higher is better)
        scored_offers.sort(key=lambda x: x.score, reverse=True)
        
        # Return top N
        top_offers = scored_offers[:max_results]
        logger.info(f"[{self.name}] Selected top {len(top_offers)} offers")
        
        return top_offers
    
    def _calculate_score(self, offer: FlightOffer, all_offers: List[FlightOffer]):
        """
        Improved weighted scoring with transparent breakdown.
        Returns (total_score, breakdown_dict)
        """
        prices = [o.price for o in all_offers]
        min_price = min(prices)
        max_price = max(prices)

        # --- PRICE (35%) ---
        if max_price > min_price:
            normalized_price = 1 - (offer.price - min_price) / (max_price - min_price)
        else:
            normalized_price = 1

        price_score = normalized_price * 35

        # --- STOPS (25%) ---
        if offer.stops == 0:
            stops_score = 25
        elif offer.stops == 1:
            stops_score = 18
        else:
            stops_score = 10

        # --- DURATION (20%) ---
        duration_score = 12
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

        # --- BUDGET ALIGNMENT (20%) ---
        # Penalize extreme expensive options
        budget_alignment = 20 * normalized_price

        total_score = price_score + stops_score + duration_score + budget_alignment

        breakdown = {
            "price_score": {
                "value": round(price_score, 2),
                "max": 35
            },
            "stops_score": {
                "value": stops_score,
                "max": 25
            },
            "duration_score": {
                "value": duration_score,
                "max": 20
            },
            "budget_alignment": {
                "value": round(budget_alignment, 2),
                "max": 20
            },
            "total": {
                "value": round(total_score, 2),
                "max": 100
            }
        }

        logger.debug(f"[{self.name}] {offer.id} breakdown: {breakdown}")

        return round(total_score, 2), breakdown
