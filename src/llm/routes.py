from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from ..utils import get_env_value
from .schemas import (
    PromptRequest)

chat = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768")
system = "You are a dermatologist."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])


router = APIRouter(
    prefix="/llm",
    responses={ 404: { 
        "message": "Not found" } 
    },
)

@router.post(
    "/get-disease-detail",
    responses={ 
        401: { "description": "Invalid username or password." },
    },
)
async def get_disease_detail(body: PromptRequest):
    # TODO: implement login service
    chain = prompt | chat
    res = chain.invoke({"text": "explain what is melanoma"})
    print(res.content, type(res))
    return body.model_dump(mode='json')
