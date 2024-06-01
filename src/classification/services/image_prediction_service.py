from typing import Union
import numpy as np
import tensorflow as tf
from fastapi import UploadFile
from ..models.model_loader import ModelLoader

class ImagePredictionService:
    def __init__(self):
        self.model = ModelLoader.load_model()
        self.label_mapping = {
            0: 'Atopic Dermatitis ',
            1: 'Basal Cell Carcinoma (BCC) ',
            2: 'Benign Keratosis',
            3: 'Eczema ',
            4: 'Melanocytic Nevi (NV) ',
            5: 'Melanoma ',
            6: 'Psoriasis pictures Lichen Planus and related diseases ',
            7: 'Seborrheic Keratoses and other Benign Tumors ',
            8: 'Tinea Ringworm Candidiasis and other Fungal Infections ',
            9: 'Warts Molluscum and other Viral Infections '
        }

        self.tresh_dict = {
            'Atopic Dermatitis ': 0.9199999999999999,
            'Basal Cell Carcinoma (BCC) ': 0.87,
            'Benign Keratosis': 0.6399999999999999,
            'Eczema ': 0.6699999999999999,
            'Melanocytic Nevi (NV) ': 0.8099999999999999,
            'Melanoma ': 0.71,
            'Psoriasis pictures Lichen Planus and related diseases ': 0.5199999999999999,
            'Seborrheic Keratoses and other Benign Tumors ': 0.6399999999999999,
            'Tinea Ringworm Candidiasis and other Fungal Infections ': 0.84,
            'Warts Molluscum and other Viral Infections ': 0.88
        }
                    
        self.img_size = 240

    async def predict(self, file: UploadFile) -> Union[str, dict]:
        image = await file.read()
        img = self.load_and_preprocess_image(image)
        pred = self.model.predict(tf.expand_dims(img, axis=0))

        pred_class_encoded = np.argmax(pred)
        pred_label = self.label_mapping[pred_class_encoded]
        pred_class_prob = float(pred[0][pred_class_encoded])  # Convert to native Python float
        class_probabilities = {self.label_mapping[i]: float(prob) for i, prob in enumerate(pred[0])}

        if pred_class_prob >= self.tresh_dict.get(pred_label, 1):  # Default threshold of 1
            return {"label": pred_label, "probability": pred_class_prob, "classes_probability": class_probabilities}

        return {"message": "Sorry, we don't have the data yet"}

    def load_and_preprocess_image(self, image_data: bytes) -> tf.Tensor:
        img = tf.io.decode_image(image_data, channels=3)
        img = tf.image.resize(img, (self.img_size, self.img_size))
        img = img / 255.0
        return img
