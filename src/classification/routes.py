from fastapi import File, HTTPException, UploadFile, APIRouter
from fastapi.responses import JSONResponse

from classification.services.image_prediction_service import ImagePredictionService

router = APIRouter(
    responses={ 404: { 
        "message": "Not found" } 
    },
)

# Initialize the prediction service
prediction_service = ImagePredictionService()

@router.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    try:
        prediction = await prediction_service.predict(file)
        return JSONResponse(content={"prediction": prediction}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))