from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from classification.services.image_prediction_service import ImagePredictionService

from .routes import global_router
# from auth.router import router as auth_router


app = FastAPI(
    title="Cooleet Back-End API"
)

app.include_router(global_router, prefix="/api/v1")

@app.get("/")
async def root():
    return { "message": "Hello World" }
