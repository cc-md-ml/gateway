from pydantic import BaseModel


class PromptRequest(BaseModel):
    disease: str
    

class PromptResponse(BaseModel):
    description: str
    symptoms: str
    contagiousness: str
    treatment: str
    prevalence: str
