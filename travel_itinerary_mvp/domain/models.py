"""
Domain models for clean architecture layer.
Implements structured models replacing raw dict usage.
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# -----------------------------
# Core Domain Entities
# -----------------------------

class TravelRequest(BaseModel):
    id: str
    user_input: str
    created_at: datetime


class StructuredTravelSpec(BaseModel):
    destination: str
    duration_days: int
    budget: Optional[int] = None
    preferences: Optional[List[str]] = []
    constraints: Optional[List[str]] = []


class Activity(BaseModel):
    name: str
    location: str
    estimated_cost: float
    duration: str


class DayPlan(BaseModel):
    date: str
    activities: List[Activity]


class TravelPlan(BaseModel):
    id: str
    request_id: str
    destination: str
    total_cost: float
    days: List[DayPlan]
    justification: Optional[str] = None
    status: str


class ValidationReport(BaseModel):
    score: float
    approved: bool
    issues: List[str]
    improvements: List[str]
    requires_human_review: bool = False


class PlanVersion(BaseModel):
    plan_id: str
    version_number: int
    created_at: datetime
    plan_snapshot: dict
