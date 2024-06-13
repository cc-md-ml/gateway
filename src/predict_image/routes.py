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
    PromptRequest, PromptResponse
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
    response_model=PromptResponse
)
async def predict_disease(image: UploadFile = File(...), user = Depends(firebase.get_user_token)):
    if image.filename == "":
        raise HTTPException(status_code=400, detail="No image provided")
    res : PromptResponse = await service.upload_and_get_detail(image)
    return res.model_dump(mode='json')