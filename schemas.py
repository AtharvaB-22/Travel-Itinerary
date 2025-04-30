from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Input model for creating an itinerary
class ItineraryCreate(BaseModel):
    name: str
    start_date: datetime
    total_nights: int
    recommended_for_nights: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Custom Phuket Trip",
                "start_date": "2023-12-01T00:00:00",
                "total_nights": 3,
                "recommended_for_nights": 3
            }
        }

# Output model for an itinerary
class ItineraryResponse(BaseModel):
    id: int
    name: str
    start_date: datetime
    total_nights: int
    recommended_for_nights: Optional[int]

    class Config:
        orm_mode = True

# Day response model (nested in itinerary)
class DayResponse(BaseModel):
    id: int
    day_number: int
    accommodation_id: int

    class Config:
        orm_mode = True

# Full itinerary with days
class FullItineraryResponse(ItineraryResponse):
    days: List[DayResponse]