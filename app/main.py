from fastapi import FastAPI, Request
from app.api.endpoints import router as inventory_router

app = FastAPI()

app.include_router(inventory_router, prefix="/inventory")

@app.get("/")
def root():
    return {"status": "RFID FastAPI server running"}
