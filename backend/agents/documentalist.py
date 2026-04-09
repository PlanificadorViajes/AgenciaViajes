from typing import List
from backend.models.flight_models import FlightOffer
from backend.models.house_models import HouseOffer
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DocumentalistAgent:
    """
    Agent responsible for generating the final travel plan document in Markdown format.
    Compiles all selected offers into a readable, structured document.
    """
    
    def __init__(self):
        self.name = "Documentalist"
    
    def generate_travel_plan(
        self,
        user_request: dict,
        selected_flight: FlightOffer,
        selected_house: HouseOffer,
        flight_alternatives: List[FlightOffer] = None,
        house_alternatives: List[HouseOffer] = None,
        revision_comment: str = None
    ) -> str:
        """
        Generate a comprehensive travel plan document in Markdown format.
        
        Args:
            user_request: Original user request data
            selected_flight: The chosen flight offer
            selected_house: The chosen accommodation offer
            flight_alternatives: Alternative flight options (optional)
            house_alternatives: Alternative accommodation options (optional)
        
        Returns:
            Markdown-formatted travel plan document
        """
        logger.info(f"[{self.name}] Generating travel plan document")
        
        # Build the document sections
        doc_parts = []
        
        # Header
        doc_parts.append(self._generate_header(user_request))
        
        # Summary
        doc_parts.append(self._generate_summary(user_request, selected_flight, selected_house))
        
        # Flight details
        doc_parts.append(self._generate_flight_section(selected_flight, flight_alternatives))
        
        # Accommodation details
        doc_parts.append(self._generate_accommodation_section(selected_house, house_alternatives))
        
        # Budget breakdown
        doc_parts.append(self._generate_budget_section(user_request, selected_flight, selected_house))
        
        # Next steps
        doc_parts.append(self._generate_next_steps())
        
        # Optional revision section
        if revision_comment:
            doc_parts.append(self._generate_revision_section(revision_comment))

        # Footer
        doc_parts.append(self._generate_footer())
        
        # Combine all parts
        document = "\n\n".join(doc_parts)
        
        logger.info(f"[{self.name}] Travel plan document generated ({len(document)} characters)")
        return document
    
    def _generate_header(self, user_request: dict) -> str:
        """Generate document header"""
        destination = user_request.get('destination_country', 'Unknown')
        return f"# ✈️ Travel Plan to {destination}\n\n*Generated on {datetime.now().strftime('%B %d, %Y')}*"
    
    def _generate_summary(self, user_request: dict, flight: FlightOffer, house: HouseOffer) -> str:
        """Generate trip summary"""
        destination = user_request.get('destination_country', 'Unknown')
        departure_date = user_request.get('departure_date', '')
        return_date = user_request.get('return_date', '')
        total_cost = flight.price + house.total_price
        
        summary = f"""## 📋 Trip Summary

- **Destination:** {destination}
- **Dates:** {departure_date} to {return_date}
- **Duration:** {(datetime.fromisoformat(return_date) - datetime.fromisoformat(departure_date)).days} nights
- **Total Cost:** €{total_cost:.2f}
- **Flight:** €{flight.price:.2f}
- **Accommodation:** €{house.total_price:.2f}"""
        
        return summary
    
    def _generate_flight_section(self, flight: FlightOffer, alternatives: List[FlightOffer] = None) -> str:
        """Generate flight details section"""
        section = f"""## ✈️ Selected Flight

**{flight.airline}** - {flight.origin} → {flight.destination}

- **Departure:** {flight.departure_date} at {flight.departure_time}
- **Arrival:** {flight.arrival_date} at {flight.arrival_time}
- **Duration:** {flight.duration}
- **Stops:** {flight.stops} {'stop' if flight.stops == 1 else 'stops'}
- **Price:** €{flight.price:.2f}
- **Quality Score:** {flight.score:.1f}/100
- **Source:** {flight.source}
- **[Book this flight]({flight.booking_url})**"""
        
        # Add alternatives if provided
        if alternatives and len(alternatives) > 0:
            section += "\n\n### Alternative Flight Options\n"
            for i, alt in enumerate(alternatives[:3], 1):
                section += f"\n{i}. **{alt.airline}** - €{alt.price:.2f} - {alt.stops} stops - Score: {alt.score:.1f}/100"
        
        return section
    
    def _generate_accommodation_section(self, house: HouseOffer, alternatives: List[HouseOffer] = None) -> str:
        """Generate accommodation details section"""
        amenities_str = ", ".join(house.amenities[:8]) if house.amenities else "N/A"
        if len(house.amenities) > 8:
            amenities_str += f", +{len(house.amenities) - 8} more"
        
        section = f"""## 🏠 Selected Accommodation

**{house.name}**

- **Type:** {house.type}
- **Location:** {house.location}, {house.city}
- **Rating:** {'⭐' * int(house.rating or 0)} {house.rating:.1f}/5.0 ({house.reviews_count} reviews)
- **Capacity:** {house.bedrooms} bedroom(s), {house.beds} bed(s), {house.bathrooms} bathroom(s)
- **Max Guests:** {house.max_guests}
- **Price per Night:** €{house.price_per_night:.2f}
- **Total Price:** €{house.total_price:.2f}
- **Quality Score:** {house.score:.1f}/100
- **Amenities:** {amenities_str}
- **Source:** {house.source}
- **[Book this accommodation]({house.booking_url})**"""
        
        # Add alternatives if provided
        if alternatives and len(alternatives) > 0:
            section += "\n\n### Alternative Accommodation Options\n"
            for i, alt in enumerate(alternatives[:3], 1):
                section += f"\n{i}. **{alt.name}** - €{alt.total_price:.2f} total - Rating: {alt.rating:.1f}/5 - Score: {alt.score:.1f}/100"
        
        return section
    
    def _generate_budget_section(self, user_request: dict, flight: FlightOffer, house: HouseOffer) -> str:
        """Generate budget breakdown"""
        max_budget = user_request.get('max_budget', 0)
        total_cost = flight.price + house.total_price
        remaining = max_budget - total_cost
        percentage = (total_cost / max_budget * 100) if max_budget > 0 else 0
        
        section = f"""## 💰 Budget Breakdown

- **Maximum Budget:** €{max_budget:.2f}
- **Flight Cost:** €{flight.price:.2f}
- **Accommodation Cost:** €{house.total_price:.2f}
- **Total Cost:** €{total_cost:.2f}
- **Remaining Budget:** €{remaining:.2f}
- **Budget Usage:** {percentage:.1f}%"""
        
        if remaining > 0:
            section += f"\n\n*You have €{remaining:.2f} remaining for activities, meals, and other expenses.*"
        elif remaining < 0:
            section += f"\n\n*⚠️ This plan exceeds your budget by €{abs(remaining):.2f}. Consider adjusting your selections.*"
        
        return section
    
    def _generate_next_steps(self) -> str:
        """Generate next steps section"""
        return """## 📝 Next Steps

1. **Review** the flight and accommodation options
2. **Book** your flight using the provided link
3. **Book** your accommodation using the provided link
4. **Plan** your activities and daily itinerary
5. **Check** visa requirements and travel insurance
6. **Pack** according to the weather and activities planned

*Have a great trip!* 🎉"""
    
    def _generate_revision_section(self, comment: str) -> str:
        """Generate revision section if user requested changes"""
        return f"""## 🔄 Revision Requested

The user requested the following modification:

> {comment}

This updated version incorporates the requested improvements while maintaining the selected flight and accommodation."""

    def _generate_footer(self) -> str:
        """Generate document footer"""
        return """---

*This travel plan was automatically generated by the Travel Itinerary AI System. Prices and availability are subject to change. Please verify all details before booking.*"""
