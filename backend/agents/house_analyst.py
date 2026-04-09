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
            score = self._calculate_score(offer, offers)
            offer.score = score
            scored_offers.append(offer)
        
        # Sort by score (higher is better)
        scored_offers.sort(key=lambda x: x.score, reverse=True)
        
        # Return top N
        top_offers = scored_offers[:max_results]
        logger.info(f"[{self.name}] Selected top {len(top_offers)} offers")
        
        return top_offers
    
    def _calculate_score(self, offer: HouseOffer, all_offers: List[HouseOffer]) -> float:
        """
        Calculate quality-price score for an accommodation offer.
        Score ranges from 0 to 100 (higher is better).
        """
        # Get price range
        prices = [o.total_price for o in all_offers]
        min_price = min(prices)
        max_price = max(prices)
        
        # Normalize price (0-40 points, lower price = higher score)
        if max_price > min_price:
            price_score = 40 * (1 - (offer.total_price - min_price) / (max_price - min_price))
        else:
            price_score = 40
        
        # Rating score (0-30 points)
        rating_score = 0
        if offer.rating:
            # Scale from 0-5 to 0-30
            rating_score = (offer.rating / 5.0) * 30
        
        # Reviews count score (0-15 points) - logarithmic scale
        reviews_score = 0
        if offer.reviews_count:
            # More reviews = more reliable
            # 0 reviews = 0, 10 reviews = 7.5, 100 reviews = 11.25, 500+ reviews = 15
            import math
            normalized = min(offer.reviews_count / 500.0, 1.0)
            reviews_score = 15 * math.sqrt(normalized)
        
        # Amenities score (0-15 points)
        amenities_count = len(offer.amenities) if offer.amenities else 0
        # Assume max 10 amenities for normalization
        amenities_score = min(amenities_count / 10.0, 1.0) * 15
        
        total_score = price_score + rating_score + reviews_score + amenities_score
        
        logger.debug(
            f"[{self.name}] {offer.id}: price={price_score:.1f}, "
            f"rating={rating_score:.1f}, reviews={reviews_score:.1f}, "
            f"amenities={amenities_score:.1f}, total={total_score:.1f}"
        )
        
        return round(total_score, 2)
