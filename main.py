from fastapi import FastAPI, HTTPException
from databases import Database
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Itinerary, Day
from schemas import ItineraryCreate, FullItineraryResponse, DetailedItineraryResponse
from itineraries import itineraries
from typing import List

app = FastAPI()
database = Database(DATABASE_URL)

# Create the tables in the database
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Endpoint to create a new itinerary
@app.post("/itineraries", response_model=FullItineraryResponse)
async def create_itinerary(itinerary_data: ItineraryCreate):
    with Session(engine) as session:
        if itinerary_data.total_nights <= 0:
            raise HTTPException(status_code=400, detail="total_nights must be positive")

        new_itinerary = Itinerary(
            name=itinerary_data.name,
            start_date=itinerary_data.start_date,
            total_nights=itinerary_data.total_nights,
            recommended_for_nights=itinerary_data.recommended_for_nights
        )
        session.add(new_itinerary)
        session.flush()

        days = [
            Day(itinerary_id=new_itinerary.id, day_number=i + 1, accommodation_id=1)
            for i in range(itinerary_data.total_nights)
        ]
        session.add_all(days)

        session.commit()
        session.refresh(new_itinerary)

        return FullItineraryResponse(
            id=new_itinerary.id,
            name=new_itinerary.name,
            start_date=new_itinerary.start_date,
            total_nights=new_itinerary.total_nights,
            recommended_for_nights=new_itinerary.recommended_for_nights,
            days=[DayResponse(id=d.id, day_number=d.day_number, accommodation_id=d.accommodation_id) for d in new_itinerary.days]
        )

# Endpoint to list all itineraries
@app.get("/itineraries", response_model=List[FullItineraryResponse])
async def get_itineraries():
    with Session(engine) as session:
        itineraries = session.query(Itinerary).all()
        return [
            FullItineraryResponse(
                id=it.id,
                name=it.name,
                start_date=it.start_date,
                total_nights=it.total_nights,
                recommended_for_nights=it.recommended_for_nights,
                days=[DayResponse(id=d.id, day_number=d.day_number, accommodation_id=d.accommodation_id) for d in it.days]
            )
            for it in itineraries
        ]

# Endpoint to get a specific itinerary by ID
@app.get("/itineraries/{itinerary_id}", response_model=FullItineraryResponse)
async def get_itinerary(itinerary_id: int):
    with Session(engine) as session:
        itinerary = session.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return FullItineraryResponse(
            id=itinerary.id,
            name=itinerary.name,
            start_date=itinerary.start_date,
            total_nights=it.total_nights,
            recommended_for_nights=it.recommended_for_nights,
            days=[DayResponse(id=d.id, day_number=d.day_number, accommodation_id=d.accommodation_id) for d in it.days]
        )

# Updated endpoint for recommended itineraries with detailed data
@app.get("/recommend/{nights}", response_model=DetailedItineraryResponse)
async def recommend_itinerary(nights: int):
    if nights < 2 or nights > 8:
        raise HTTPException(status_code=400, detail="Duration must be between 2 and 8 nights")

    nights_str = str(nights)
    if nights_str not in itineraries:
        raise HTTPException(status_code=404, detail=f"No recommended itinerary found for {nights} nights")

    itinerary_data = itineraries[nights_str]
    location = "combined" if "combined" in itinerary_data else "phuket" if nights <= 3 else "krabi"
    return DetailedItineraryResponse(
        duration=nights,
        location=location,
        itinerary=itinerary_data[location]
    )

# New endpoint for detailed itineraries
@app.get("/itineraries/detailed/{nights}", response_model=DetailedItineraryResponse)
async def get_detailed_itinerary(nights: int):
    if nights < 2 or nights > 8:
        raise HTTPException(status_code=400, detail="Duration must be between 2 and 8 nights")

    nights_str = str(nights)
    if nights_str not in itineraries:
        raise HTTPException(status_code=404, detail=f"No itinerary found for {nights} nights")

    itinerary_data = itineraries[nights_str]
    location = "combined" if "combined" in itinerary_data else "phuket" if nights <= 3 else "krabi"
    return DetailedItineraryResponse(
        duration=nights,
        location=location,
        itinerary=itinerary_data[location]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)