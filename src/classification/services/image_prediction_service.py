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
        self.img_size = 240

    async def predict(self, file: UploadFile) -> str:
        image = await file.read()
        img = self.load_and_preprocess_image(image)
        pred = self.model.predict(tf.expand_dims(img, axis=0))
        pred_class_encoded = np.argmax(pred)
        pred_label = self.label_mapping[pred_class_encoded]
        return pred_label

    def load_and_preprocess_image(self, image_data: bytes) -> tf.Tensor:
        img = tf.io.decode_image(image_data, channels=3)
        img = tf.image.resize(img, (self.img_size, self.img_size))
        img = img / 255.0
        return img
