from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class FlightRequest(BaseModel):
    """Structured flight search request"""
    origin_airport: str = Field(..., description="IATA code or airport name")
    destination_country: str = Field(..., description="Destination country")
    departure_date: date = Field(..., description="Departure date")
    return_date: date = Field(..., description="Return date")
    passengers: int = Field(..., ge=1, le=9, description="Number of passengers")
    max_budget: float = Field(..., gt=0, description="Maximum budget per person")


class FlightOffer(BaseModel):
    """Single flight offer from scraping"""
    id: str
    airline: str
    origin: str
    destination: str
    departure_date: str
    departure_time: str
    arrival_date: str
    arrival_time: str
    duration: str
    stops: int
    price: float
    currency: str = "EUR"
    source: str  # Skyscanner, Google Flights, etc.
    booking_url: Optional[str] = None
    score: Optional[float] = None  # Quality-price score


class FlightSearchResult(BaseModel):
    """Response from flight search"""
    phase: str  # "all_flights", "top_flights", "no_flights"
    message: Optional[str] = None
    data: list[FlightOffer] = []
    total_found: int = 0
