from typing import List
from backend.models.house_models import HouseOffer
import logging

logger = logging.getLogger(__name__)


class HouseAnalystAgent:
    """
    Agent responsible for analyzing accommodation offers and selecting the best ones.
    Calculates quality-price scores and returns top 5.
    """
    
    def __init__(self):
        self.name = "HouseAnalyst"
    
    def analyze_and_rank(self, offers: List[HouseOffer], max_results: int = 5) -> List[HouseOffer]:
        """
        Analyze accommodation offers and return top N based on quality-price score.
        
        Score calculation considers:
        - Price (lower is better)
        - Rating (higher is better)
        - Number of reviews (more is better, indicates reliability)
        - Amenities (more is better)
        """
        logger.info(f"[{self.name}] Analyzing {len(offers)} accommodation offers")
        
        if not offers:
            return []
        
        # Calculate score for each offer
        scored_offers = []
        for offer in offers:
            score, breakdown = self._calculate_score(offer, offers)
            offer.score = score
            offer.scoring_breakdown = breakdown
            scored_offers.append(offer)
        
        # Sort by score (higher is better)
        scored_offers.sort(key=lambda x: x.score, reverse=True)
        
        # Return top N
        top_offers = scored_offers[:max_results]
        logger.info(f"[{self.name}] Selected top {len(top_offers)} offers")
        
        return top_offers
    
    def _calculate_score(self, offer: HouseOffer, all_offers: List[HouseOffer]):
        """
        Improved weighted scoring with transparent breakdown.
        Returns (total_score, breakdown_dict)
        """
        prices = [o.total_price for o in all_offers]
        min_price = min(prices)
        max_price = max(prices)

        # --- PRICE (30%) ---
        if max_price > min_price:
            normalized_price = 1 - (offer.total_price - min_price) / (max_price - min_price)
        else:
            normalized_price = 1

        price_score = normalized_price * 30

        # --- RATING (25%) ---
        rating_score = (offer.rating / 5.0) * 25 if offer.rating else 0

        # --- REVIEWS (15%) ---
        import math
        if offer.reviews_count:
            normalized_reviews = min(offer.reviews_count / 500.0, 1.0)
            reviews_score = 15 * math.sqrt(normalized_reviews)
        else:
            reviews_score = 0

        # --- AMENITIES (15%) ---
        amenities_count = len(offer.amenities) if offer.amenities else 0
        amenities_score = min(amenities_count / 10.0, 1.0) * 15

        # --- BUDGET ALIGNMENT (15%) ---
        budget_alignment = normalized_price * 15

        total_score = price_score + rating_score + reviews_score + amenities_score + budget_alignment

        breakdown = {
            "price_score": {
                "value": round(price_score, 2),
                "max": 30
            },
            "rating_score": {
                "value": round(rating_score, 2),
                "max": 25
            },
            "reviews_score": {
                "value": round(reviews_score, 2),
                "max": 15
            },
            "amenities_score": {
                "value": round(amenities_score, 2),
                "max": 15
            },
            "budget_alignment": {
                "value": round(budget_alignment, 2),
                "max": 15
            },
            "total": {
                "value": round(total_score, 2),
                "max": 100
            }
        }

        logger.debug(f"[{self.name}] {offer.id} breakdown: {breakdown}")

        return round(total_score, 2), breakdown
