from pydantic import BaseModel


class PromptRequest(BaseModel):
    disease: str
    

class PromptResponse(BaseModel):
    description: str
    symptoms: str
    treatment: str
    contagiousness: str
    prevalence: str
