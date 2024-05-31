from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from classification.services.image_prediction_service import ImagePredictionService


app = FastAPI()

# Initialize the prediction service
prediction_service = ImagePredictionService()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    try:
        prediction = await prediction_service.predict(file)
        return JSONResponse(content={"prediction": prediction}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
