from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict

# Existing models
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

class ItineraryResponse(BaseModel):
    id: int
    name: str
    start_date: datetime
    total_nights: int
    recommended_for_nights: Optional[int]

    class Config:
        orm_mode = True

class DayResponse(BaseModel):
    id: int
    day_number: int
    accommodation_id: int

    class Config:
        orm_mode = True

class FullItineraryResponse(ItineraryResponse):
    days: List[DayResponse]

# New models for detailed itinerary response
class ItineraryDetail(BaseModel):
    day: int
    activities: List[str]
    accommodations: Dict[str, str]
    dining: List[str]
    transportation: str

class DetailedItineraryResponse(BaseModel):
    duration: int
    location: str
    itinerary: List[ItineraryDetail]

    class Config:
        schema_extra = {
            "example": {
                "duration": 2,
                "location": "phuket",
                "itinerary": [
                    {
                        "day": 1,
                        "activities": ["Morning: Stroll along Patong Beach, enjoy water activities like snorkeling", "Afternoon: Explore Phuket Old Town, visit colorful Sino-Portuguese buildings", "Evening: Dinner at Nikita’s (seafood restaurant)"],
                        "accommodations": {"luxury": "The Nai Harn", "mid-range": "Selina Phuket", "budget": "Roost Glamping"},
                        "dining": ["Nikita’s (seafood, ~500 THB per person)", "One Chun Cafe (local Thai, ~200 THB per person)"],
                        "transportation": "Use Grab or Bolt for taxis (~100-200 THB per ride)"
                    },
                    {
                        "day": 2,
                        "activities": ["Morning: Visit Big Buddha for panoramic views", "Afternoon: Relax at Kata Beach, try paddleboarding", "Evening: Explore Bangla Road for nightlife"],
                        "accommodations": {"luxury": "The Nai Harn", "mid-range": "Selina Phuket", "budget": "Roost Glamping"},
                        "dining": ["Three Monkeys (Thai fusion, ~300 THB per person)", "Banzaan Market (street food, ~100 THB per person)"],
                        "transportation": "Rent a motorbike for flexibility (~300 THB per day)"
                    }
                ]
            }
        }