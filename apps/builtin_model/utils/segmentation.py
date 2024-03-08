import numpy as np
import cv2
from time import time

import matplotlib.pyplot as plt

from apps.builtin_model.source.segmentators.UNetBrainTumorSeg import SEGMENT_CLASSES, init_model
from apps.builtin_model.utils.Image import Image

VOLUME_SLICES = 100


def predict_single_image(model, image, img_size):
    X = np.empty((VOLUME_SLICES, img_size, img_size, 2))
    ce = image
    print(img_size)
    for j in range(VOLUME_SLICES):
        X[j, :, :, 0] = cv2.resize(image, (img_size, img_size))
        X[j, :, :, 1] = cv2.resize(ce, (img_size, img_size))

    return model.predict(X / np.max(X), verbose=1)


def show_predicts_for_single_image(model, image, img_size, start_slice=0):
    gt = np.zeros((img_size, img_size))  # Mock ground truth for a single image
    p = predict_single_image(model, image, img_size)

    core = p[:, :, :, 1]
    edema = p[:, :, :, 2]
    enhancing = p[:, :, :, 3]

    plt.figure(figsize=(18, 50))
    f, axarr = plt.subplots(1, 6, figsize=(18, 50))

    for i in range(6):  # for each image, add brain background
        axarr[i].imshow(cv2.resize(image, (img_size, img_size)), cmap="gray", interpolation='none')

    axarr[0].imshow(cv2.resize(image, (img_size, img_size)), cmap="gray")
    axarr[0].title.set_text('Original image')
    curr_gt = cv2.resize(gt, (img_size, img_size), interpolation=cv2.INTER_NEAREST)
    axarr[2].imshow(p[start_slice, :, :, 1:4], cmap="Reds", interpolation='none', alpha=0.3)
    axarr[2].title.set_text('All classes')
    axarr[3].imshow(edema[start_slice, :, :], cmap="OrRd", interpolation='none', alpha=0.3)
    axarr[3].title.set_text(f'{SEGMENT_CLASSES[1]} predicted')
    axarr[4].imshow(core[start_slice, :, :], cmap="OrRd", interpolation='none', alpha=0.3)
    axarr[4].title.set_text(f'{SEGMENT_CLASSES[2]} predicted')
    axarr[5].imshow(enhancing[start_slice, :, :], cmap="OrRd", interpolation='none', alpha=0.3)
    axarr[5].title.set_text(f'{SEGMENT_CLASSES[3]} predicted')
    plt.show()


def use_unet_model(model_path: str, base64data, img_size):
    try:
        model = init_model(img_size)
        start = time()
        img_ = Image(data=base64data)
        img_.preprocess(required_shape=(128, 128), channels=1)
        predictions = 'pred'
        show_predicts_for_single_image(model, img_.image, img_size)
        infer_time = time() - start
        predictions = np.argmax(predictions, axis=1)
        # prediction_label = get_prediction_label(cl_model, int(predictions[0]))
        prediction_label = 'good'
        return prediction_label, infer_time

    except FileNotFoundError as e:
        raise Exception(f"Model file not found at path: {model_path}") from e

    except Exception as e:
        raise Exception(f"An error using model occurred: {str(e)}") from e
