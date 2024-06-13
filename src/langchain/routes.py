from fastapi import (
    APIRouter,
    Depends
)

from src.auth import firebase
from src.langchain.schemas import (
    PromptRequest, PromptResponse
)
from src.langchain.service import LangChainService


service = LangChainService()
router = APIRouter(
    prefix="/llm",
    responses={ 
        404: { "message": "Not found" } 
    },
)

@router.post(
    "/get-disease-detail",
    response_model=PromptResponse
)
async def get_disease_detail(body: PromptRequest, user = Depends(firebase.get_user_token)):
    res: PromptResponse = await service.send_prompt(body)
    return res.model_dump(mode='json')
