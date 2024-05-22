from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import custom_object_scope
import tensorflow_hub as hub
from PIL import Image
import numpy as np
import io
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

custom_objects = {'KerasLayer': hub.KerasLayer}

try:
    logger.info("Loading model...")
    with custom_object_scope(custom_objects):
        model = load_model("assets/best_model.h5")
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {e}")

def preprocess_image(image: Image.Image, imgsize: int = 240) -> np.ndarray:
    """
    Preprocess the input image to be suitable for prediction.
    """
    image = image.resize((imgsize, imgsize))
    image = np.array(image) / 255.0 
    image = image.astype(np.float32)
    return np.expand_dims(image, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        processed_image = preprocess_image(image)

        logger.info("Making prediction...")
        prediction = model.predict(processed_image)
        logger.info("Prediction made successfully.")

        predicted_class = np.argmax(prediction, axis=1).tolist()
        confidence = np.max(prediction, axis=1).tolist()

        return JSONResponse(content={
            "predicted_class": predicted_class,
            "confidence": confidence
        })

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
