# UltraSteelChallenge/app/main.py

from fastapi import FastAPI
from app.api.endpoints import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="RFID API",
    version="1.0.0"
)

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://inventory-ultrasteel.vercel.app/", "http://localhost:3000", "http://192.168.1.12:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

