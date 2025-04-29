from fastapi import FastAPI
from databases import Database
from config import DATABASE_URL
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

app = FastAPI()
database = Database(DATABASE_URL)
metadata = MetaData()

# Define a simple test table
test_table = Table(
    "test_table",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

# Create the table in the database
engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# Database connection events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Test endpoint to insert a record
@app.get("/test")
async def test():
    query = test_table.insert().values(name="test")
    await database.execute(query)
    return {"message": "Test record inserted"}

# Test endpoint to read records
@app.get("/test/read")
async def read_test():
    query = test_table.select()
    result = await database.fetch_all(query)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)