"""
Travel Itinerary MVP System

A Python system for generating, reviewing, and refining travel itineraries iteratively
using an agent-based architecture (Generator + Critic) with state management.
"""

__version__ = "1.0.0"
__author__ = "Travel Itinerary MVP"
__description__ = "Iterative travel itinerary generation system with agent-based architecture"

from .graph.orchestrator import ItineraryOrchestrator
from .graph.state import PlanState
from .agents.generator import GeneratorAgent
from .agents.critic import CriticAgent
from .persistence.repository import ItineraryRepository
from .memory.session_store import SessionStore

__all__ = [
    "ItineraryOrchestrator",
    "PlanState", 
    "GeneratorAgent",
    "CriticAgent",
    "ItineraryRepository",
    "SessionStore"
]
