
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

@app.get("/" , tags=["Root"])
async def read_root():
    return {"Hello": "World"}