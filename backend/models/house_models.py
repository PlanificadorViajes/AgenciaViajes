from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class HouseRequest(BaseModel):
    """Structured accommodation search request"""
    destination_country: str
    destination_city: Optional[str] = None
    check_in: date
    check_out: date
    guests: int = Field(..., ge=1, le=16)
    max_budget: float = Field(..., gt=0, description="Maximum budget for entire stay")
    selected_flight_price: float = Field(..., description="Price of selected flight to calculate remaining budget")


class HouseOffer(BaseModel):
    """Single accommodation offer from scraping"""
    id: str
    name: str
    type: str  # Apartment, House, Hotel, etc.
    location: str
    city: str
    country: str
    price_per_night: float
    total_price: float
    currency: str = "EUR"
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    bedrooms: Optional[int] = None
    beds: Optional[int] = None
    bathrooms: Optional[int] = None
    max_guests: int
    amenities: list[str] = []
    source: str  # Airbnb, Booking
    booking_url: Optional[str] = None
    image_url: Optional[str] = None
    score: Optional[float] = None  # Quality-price score


class HouseSearchResult(BaseModel):
    """Response from accommodation search"""
    phase: str  # "all_houses", "top_houses"
    message: Optional[str] = None
    data: list[HouseOffer] = []
    total_found: int = 0
