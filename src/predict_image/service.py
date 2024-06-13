from google.cloud import storage
from google.oauth2 import service_account
import uuid
import os
import requests
from PIL import Image
from io import BytesIO
import time
from functools import wraps

from fastapi import UploadFile, HTTPException
from src.langchain.schemas import (
    PromptRequest, PromptResponse
)
from src.langchain.service import LangChainService
from src.config import (
    setup_env, get_env_value
)
setup_env()



class PredictImageService():
    def __init__(self):
        self.BUCKET_NAME = get_env_value('BUCKET_NAME')
        self.langchain_service = LangChainService()
        self.BUCKET_FOLDER = get_env_value('BUCKET_FOLDER')
        bucket_service_account_path = f'{os.getcwd()}/bucket_service_account_key.json'
        credentials = service_account.Credentials.from_service_account_file(bucket_service_account_path)
        self.client = storage.Client(credentials=credentials)

    def timer(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)  # Assuming the function is async
            end_time = time.time()
            print(f"{func.__name__} executed in {end_time - start_time} seconds")
            return result
        return wrapper
    
    @timer
    async def _upload_image(self, image: UploadFile) -> str:
        """
        Uploads image to Google Cloud Storage.
        """
        bucket = self.client.bucket(self.BUCKET_NAME)
        img_unique_name = f'{uuid.uuid4().hex}-{image.filename}'
        blob = bucket.blob(f'{self.BUCKET_FOLDER}/{img_unique_name}')

         # Resize the image
        original_image = Image.open(image.file)
        resized_image = original_image.resize((800, 600))  # Example size, adjust as needed

    # Save resized image to BytesIO object
        image_bytes = BytesIO()
        resized_image.save(image_bytes, format=original_image.format)
        image_bytes.seek(0)  # Move to the start of the BytesIO object

    # Upload from BytesIO object
        blob.upload_from_file(image_bytes, content_type=image.content_type)


        if not blob.exists():
            raise Exception("Upload failed, file does not exist in bucket.")
        return img_unique_name
    
    @timer
    async def upload_and_get_detail(self, image: UploadFile) -> PromptResponse:
        """
        Uploads image to Google Cloud Storage and returns its details.
        """
        try:
            image_name = await self._upload_image(image)
        except Exception as e:
        # Handle upload to bucket failure
            raise HTTPException(status_code=500, detail=f"Failed to upload image to bucket: {str(e)}")

        try:
            model_response = await self._call_model_api(image_name)
        except Exception as e:
            # Handle call to model API failure
            raise HTTPException(status_code=500, detail=f"Failed to get prediction from model API: {str(e)}")

        if model_response.get('label') is None:
            # Handle label not found in model API response
            if 'message' in model_response:
                message = model_response.get('message')
                raise HTTPException(status_code=422, detail="Model unable to predict the disease")
            else:
                message = model_response.get('detail')
                raise HTTPException(status_code=400, detail=message)
            

        prediction_result = model_response.get('label')
        prompt = PromptRequest(disease=prediction_result)
        try:
            disease_detail = await self.langchain_service.send_prompt(prompt)
        except Exception as e:
        # Handle any errors from langchain_service
            raise HTTPException(status_code=500, detail=f"Failed to get disease detail: {str(e)}")
        return disease_detail

    @timer
    async def _call_model_api(self, image_name: str):
        """
        Calls the model API to get the prediction.
        """
        model_api_url = get_env_value('MODEL_API_URL')
        response = requests.post(model_api_url, json={"filename": image_name})
        if response.status_code != 200:
            raise Exception("Model API call failed.")
        return response.json()