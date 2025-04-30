from fastapi import FastAPI, HTTPException
from databases import Database
from config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Itinerary, Day, Accommodation
from schemas import ItineraryCreate, FullItineraryResponse, DayResponse
from datetime import datetime


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
        # Validate total_nights is positive
        if itinerary_data.total_nights <= 0:
            raise HTTPException(status_code=400, detail="total_nights must be positive")

        # Create new itinerary
        new_itinerary = Itinerary(
            name=itinerary_data.name,
            start_date=itinerary_data.start_date,
            total_nights=itinerary_data.total_nights,
            recommended_for_nights=itinerary_data.recommended_for_nights
        )
        session.add(new_itinerary)
        session.flush()  # Get the itinerary ID

        # Create days for the itinerary
        days = [
            Day(itinerary_id=new_itinerary.id, day_number=i + 1, accommodation_id=1)  # Default to accommodation_id 1 for now
            for i in range(itinerary_data.total_nights)
        ]
        session.add_all(days)

        session.commit()
        session.refresh(new_itinerary)

        # Load days for response
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
@app.get("/itineraries", response_model=list[FullItineraryResponse])
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
            total_nights=itinerary.total_nights,
            recommended_for_nights=itinerary.recommended_for_nights,
            days=[DayResponse(id=d.id, day_number=d.day_number, accommodation_id=d.accommodation_id) for d in itinerary.days]
        )
        
@app.get("/recommend/{nights}", response_model=FullItineraryResponse)
async def recommend_itinerary(nights: int):
    with Session(engine) as session:
        # Validate nights is positive
        if nights <= 0:
            raise HTTPException(status_code=400, detail="Number of nights must be positive")

        # Find an itinerary with matching recommended_for_nights
        itinerary = session.query(Itinerary).filter(Itinerary.recommended_for_nights == nights).first()
        if not itinerary:
            raise HTTPException(status_code=404, detail=f"No recommended itinerary found for {nights} nights")

        return FullItineraryResponse(
            id=itinerary.id,
            name=itinerary.name,
            start_date=itinerary.start_date,
            total_nights=itinerary.total_nights,
            recommended_for_nights=itinerary.recommended_for_nights,
            days=[DayResponse(id=d.id, day_number=d.day_number, accommodation_id=d.accommodation_id) for d in itinerary.days]
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)