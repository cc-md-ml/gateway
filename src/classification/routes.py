from fastapi import File, HTTPException, UploadFile, APIRouter
from fastapi.responses import JSONResponse

from src.langchain.service import LangChainService
from src.classification.services.image_prediction_service import ImagePredictionService

router = APIRouter(
    responses={ 404: { 
        "message": "Not found" } 
    },
)

# Initialize the prediction service
prediction_service = ImagePredictionService()
llm_service = LangChainService()

@router.post("/api/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid image file")
    
    try:
        # Get prediction results
        prediction = await prediction_service.predict(file)
        
        # Extract the main disease and top 3 other diseases
        main_disease = prediction['label']
        main_probability = prediction['probability']
        other_diseases = sorted(prediction['classes_probability'].items(), key=lambda x: x[1], reverse=True)[1:4]
        other_diseases_str = ", ".join([f"{disease}: {prob:.2%}" for disease, prob in other_diseases])
        
        # Get the treatment recommendations from LLM
        treatment_recommendation = await llm_service.send_prompt(main_disease, main_probability, other_diseases_str)
        
        # Format the response
        response = {
            "prediction": {
                "main_disease": main_disease,
                "main_probability": main_probability,
                "other_diseases": {disease: prob for disease, prob in other_diseases}
            },
            "treatment_recommendation": treatment_recommendation
        }
        
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
