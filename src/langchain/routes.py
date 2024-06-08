from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.langchain.service import LangChainService


router = APIRouter(
    prefix="/llm",
    responses={ 404: { 
        "message": "Not found" } 
    },
)

SERVICE = LangChainService()


@router.post(
    "/get-disease-detail",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def get_disease_detail(body: str):
    # TODO: implement login service/handler
    # TODO: integrate with prediction results
    res = await SERVICE.send_prompt("Melanoma", 0.95, "Other related diseases example string")
    return JSONResponse(content=res, status_code=200)
