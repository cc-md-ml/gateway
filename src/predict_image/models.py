from sqlalchemy import Column, String, Integer, ForeignKey, Double

from src.database import Base
from src.auth.models import User

class PredictionResult(Base):
    __tablename__ = 'prediction_results'
    id = Column(String(255), primary_key=True, index=True)
    user_email = Column(String(255))
    disease = Column(String(255))
    probability = Column(Double)
    image_name = Column(String(255))
    description = Column(String(255))
    symptoms = Column(String(255))
    treatment = Column(String(255))
    contagiousness = Column(String(255))
    prevalence = Column(String(255))
    

    def to_dict(self):
        return {
            "id": self.id,
            "user_email": self.user_email,
            "image_name": self.image_name,
            "disease": self.disease,
            "probability": self.probability,
            "description": self.description,
            "symptoms": self.symptoms,
            "treatment": self.treatment,
            "contagiousness": self.contagiousness,
            "prevalence": self.prevalence
        }