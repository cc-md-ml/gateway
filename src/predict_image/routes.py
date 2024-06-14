from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException
)

from src.auth import firebase
from src.predict_image.service import PredictImageService
from src.langchain.schemas import (
    PromptResponse
)
from src.predict_image.schemas import (
    PredictImageResponse
)


router = APIRouter(
    prefix="/predict-image",
    responses={ 
        404: { "message": "Not found" } 
    },
)
service = PredictImageService()
@router.post(
    "/upload",
    response_model=PredictImageResponse
)
async def predict_disease(image: UploadFile = File(...), user = Depends(firebase.get_user_token)):
    if image.filename == "":
        raise HTTPException(status_code=400, detail="No image provided")

    res : PredictImageResponse = await service.upload_and_get_detail(image, user)
    return res.model_dump(mode='json')

@router.get(
    "/prediction-history-list",
    response_model=list
)
async def get_prediction_history(user = Depends(firebase.get_user_token)):
    results: list = await service.get_prediction_history(user)
    return results

@router.get(
    "/prediction-history/{id}",
    response_model=PredictImageResponse
)
async def get_prediction_by_id(id: str, user = Depends(firebase.get_user_token)):
    result: PredictImageResponse = await service.get_prediction_by_id(id, user)
    return result.model_dump(mode='json')