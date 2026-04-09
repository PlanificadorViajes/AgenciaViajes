"""
Travel Itinerary Generator Agent.
"""
import json
import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from ..config.settings import SYSTEM_SETTINGS
from travel_itinerary_mvp.llm.client import AzureLLMClient
import json

logger = logging.getLogger(__name__)

class PlannerAgent:
    """Planner agent that generates a TravelPlan from StructuredTravelSpec."""
    
    def __init__(self):
        self.prompt_template = self._load_prompt_template()
        self.llm = AzureLLMClient()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    def _load_prompt_template(self) -> str:
        try:
            with open(SYSTEM_SETTINGS.GENERATOR_PROMPT_FILE, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Generate a detailed travel itinerary based on requirements."
    
    def generate_plan(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate travel plan using LLM.
        """
        self.logger.info("Starting LLM-based planning")

        system_prompt = "Generate a structured travel plan as JSON."
        user_prompt = json.dumps(spec)

        response = self.llm.generate(system_prompt, user_prompt)

        try:
            parsed = json.loads(response)
            return parsed
        except Exception:
            return self._generate_mock_plan_from_spec(spec)
    
    def _generate_mock_plan_from_spec(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        days = spec.get("duration_days", 7)
        destination = spec.get("destination", "Europe")
        budget = spec.get("budget") or 1500

        return {
            "destination": destination,
            "duration_days": days,
            "budget": budget,
            "days": self._generate_daily_itinerary(days, destination),
            "justification": f"Generated plan for {destination} within budget {budget}",
            "status": "draft"
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
