from pydantic import BaseModel


class PromptRequest(BaseModel):
    disease: str
    