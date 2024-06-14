from fastapi import UploadFile
from pydantic import BaseModel
from src.langchain.schemas import PromptResponse

class PredictImageResponse(PromptResponse):
    """
    Response model for image prediction.
    """
    disease: str
    probability: float
    image_name: str
    id: str
    user_email: str    