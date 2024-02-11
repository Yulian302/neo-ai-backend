import numpy as np
from keras.models import load_model
from time import time
from apps.builtin_model.source.classifiers.ClModel import ClModel
from apps.builtin_model.utils.Image import Image


def init_model(model_name: str, img_height: int, img_width: int) -> any:
    model_name_lower = model_name.lower()
    if model_name_lower == "clmodel":
        return ClModel
    else:
        raise Exception("No models found")


def use_model(model_path: str, model_name: str, base64data, im_h=512, im_w=512):
    try:
        cl_model = init_model(model_name, im_h, im_w)
        model = load_model(model_path, custom_objects={model_name: cl_model})
        img_ = Image(data=base64data)
        img_.augment()
        img_.preprocess()
        start = time()
        predictions = model.predict(img_.image)
        infer_time = time() - start
        predictions = np.argmax(predictions, axis=1)
        prediction_label = get_prediction_label(cl_model, int(predictions[0]))
        return prediction_label, infer_time

    except FileNotFoundError as e:
        raise Exception(f"Model file not found at path: {model_path}") from e

    except Exception as e:
        raise Exception(f"An error using model occurred: {str(e)}") from e


def get_prediction_label(model_class, prediction_value: int) -> str:
    return model_class.predictions[prediction_value]
