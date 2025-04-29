from fastapi import FastAPI
from databases import Database
from config import DATABASE_URL
from sqlalchemy import create_engine
from models import metadata

app = FastAPI()
database = Database(DATABASE_URL)

# Create the tables in the database
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Temporary endpoint to confirm tables are created
@app.get("/check_tables")
async def check_tables():
    return {"message": "Tables created successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)