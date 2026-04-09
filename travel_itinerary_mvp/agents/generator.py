"""
Travel Itinerary Generator Agent.
"""
import json
import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from ..config.settings import SYSTEM_SETTINGS

logger = logging.getLogger(__name__)

class GeneratorAgent:
    """Travel itinerary generator agent."""
    
    def __init__(self):
        self.prompt_template = self._load_prompt_template()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def _load_prompt_template(self) -> str:
        """Load the generator prompt template from file."""
        try:
            with open(SYSTEM_SETTINGS.GENERATOR_PROMPT_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Generator prompt file not found")
            return "Generate a detailed travel itinerary based on requirements."
    
    def generate_plan(self, user_input: str, constraints: Optional[Dict[str, Any]] = None, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a travel itinerary plan."""
        self.logger.info("Starting plan generation")
        
        try:
            plan = self._generate_mock_plan(user_input, constraints, feedback)
            self.logger.info("Plan generation completed successfully")
            return plan
        except Exception as e:
            self.logger.error(f"Error generating plan: {str(e)}")
            raise
    
    def _generate_mock_plan(self, user_input: str, constraints: Optional[Dict[str, Any]] = None, feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a mock travel plan for demonstration."""
        days = self._extract_days(user_input)
        destination = self._extract_destination(user_input)
        budget = self._extract_budget(user_input, constraints)
        
        return {
            "plan": {
                "title": f"{days}-Day Trip to {destination}",
                "duration": f"{days} days",
                "destination": destination,
                "budget_estimate": {
                    "total": budget,
                    "currency": "EUR",
                    "breakdown": {
                        "accommodation": int(budget * 0.4),
                        "transportation": int(budget * 0.2),
                        "activities": int(budget * 0.25),
                        "food": int(budget * 0.1),
                        "miscellaneous": int(budget * 0.05)
                    }
                },
                "itinerary": self._generate_daily_itinerary(days, destination),
                "practical_info": {
                    "best_time_to_visit": "Spring and Fall",
                    "weather_considerations": "Pack layers and rain jacket",
                    "cultural_notes": "Respect local customs",
                    "language": self._get_language(destination),
                    "currency": "EUR",
                    "time_zone": "UTC+1"
                }
            },
            "justification": f"Balanced itinerary within {budget}€ budget, activities grouped geographically.",
            "assumptions": ["Mid-season pricing", "Public transport", "Moderate fitness level"],
            "alternatives": ["Extend stay for relaxed pace", "Budget accommodations available"],
            "risks": ["Weather may affect activities", "Peak pricing possible", "Advance booking needed"]
        }
    
    def _extract_days(self, user_input: str) -> int:
        """Extract number of days from user input."""
        match = re.search(r'(\d+)\s*days?', user_input.lower())
        return int(match.group(1)) if match else 7
    
    def _extract_destination(self, user_input: str) -> str:
        """Extract destination from user input."""
        destinations = {'japan': 'Japan', 'tokyo': 'Tokyo', 'paris': 'Paris', 'london': 'London', 'rome': 'Rome'}
        user_lower = user_input.lower()
        for key, value in destinations.items():
            if key in user_lower:
                return value
        return "Europe"
    
    def _extract_budget(self, user_input: str, constraints: Optional[Dict[str, Any]] = None) -> int:
        """Extract budget from input."""
        if constraints and 'budget' in constraints:
            return constraints['budget']
        match = re.search(r'(\d+).*euro|€(\d+)', user_input.lower())
        return int(match.group(1) or match.group(2)) if match else 1500
    
    def _generate_daily_itinerary(self, days: int, destination: str) -> list:
        """Generate daily itinerary."""
        itinerary = []
        for day in range(1, days + 1):
            date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
            itinerary.append({
                "day": day,
                "date": date,
                "location": destination,
                "activities": [
                    {"time": "09:00", "activity": f"Morning activity in {destination}", "duration": "3 hours", "cost": 50, "notes": "Popular attraction"},
                    {"time": "14:00", "activity": f"Afternoon exploration", "duration": "2 hours", "cost": 30, "notes": "Cultural site"}
                ],
                "accommodation": {"name": f"Hotel {destination}", "type": "hotel", "cost_per_night": 80, "location": "City center"},
                "transportation": {"method": "walking/metro", "cost": 10, "duration": "1 hour", "notes": "Public transport"},
                "meals": {
                    "breakfast": {"location": "Hotel", "estimated_cost": 15},
                    "lunch": {"location": "Local restaurant", "estimated_cost": 25},
                    "dinner": {"location": "Traditional restaurant", "estimated_cost": 35}
                }
            })
        return itinerary
    
    def _get_language(self, destination: str) -> str:
        """Get primary language for destination."""
        languages = {'Japan': 'Japanese', 'Tokyo': 'Japanese', 'Paris': 'French', 'London': 'English', 'Rome': 'Italian'}
        return languages.get(destination, 'Local language')
