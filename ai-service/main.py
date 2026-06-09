from fastapi import FastAPI
from routes.routing import router as ai_router

app = FastAPI(
    title="AppVerse AI Service",
    description="AI microservice for AppVerse AI Lite",
    version="1.0.0"
)

app.include_router(ai_router)

@app.get("/")
def health():
    return {"message": "AI service is running✅"}
