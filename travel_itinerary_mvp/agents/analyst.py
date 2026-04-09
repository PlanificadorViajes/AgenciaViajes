"""
Analyst Agent.
Interprets user input and produces StructuredTravelSpec.
"""

import re
from typing import List, Optional

from travel_itinerary_mvp.domain.models import StructuredTravelSpec
from travel_itinerary_mvp.llm.client import AzureLLMClient
import json


class AnalystAgent:
    """
    Uses LLM to transform raw input into StructuredTravelSpec.
    """

    def __init__(self):
        self.llm = AzureLLMClient()

    def analyze(self, user_input: str, budget: Optional[int] = None) -> StructuredTravelSpec:
        system_prompt = "Extract destination, duration_days, preferences as JSON."
        user_prompt = user_input

        response = self.llm.generate(system_prompt, user_prompt)

        try:
            parsed = json.loads(response)
        except Exception:
            parsed = {
                "destination": self._extract_destination(user_input),
                "duration_days": self._extract_duration(user_input),
                "preferences": self._extract_preferences(user_input)
            }

        return StructuredTravelSpec(
            destination=parsed.get("destination", "Europe"),
            duration_days=int(parsed.get("duration_days", 7)),
            budget=budget,
            preferences=parsed.get("preferences", []),
            constraints=[]
        )

    def _extract_duration(self, text: str) -> int:
        match = re.search(r"(\\d+)\\s*days?", text.lower())
        return int(match.group(1)) if match else 7

    def _extract_destination(self, text: str) -> str:
        known_destinations = ["japan", "tokyo", "paris", "rome", "london"]
        text_lower = text.lower()
        for d in known_destinations:
            if d in text_lower:
                return d.capitalize()
        return "Europe"

    def _extract_preferences(self, text: str) -> List[str]:
        preferences = []
        keywords = ["food", "culture", "nature", "luxury", "budget"]
        text_lower = text.lower()
        for k in keywords:
            if k in text_lower:
                preferences.append(k)
        return preferences
