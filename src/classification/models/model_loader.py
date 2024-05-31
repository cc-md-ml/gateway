import tensorflow as tf
import tensorflow_hub as hub

class ModelLoader:
    @staticmethod
    def load_model():
        model_path = r'assets/best_model.h5'
        model = tf.keras.models.load_model(
            model_path,
            custom_objects={'KerasLayer': hub.KerasLayer}
        )
        return model