import pickle
import xgboost as xgb
import pandas as pd
from fastapi import FastAPI, Body
from AirbnbProperty import AirbnbProperty
from AirbnbSuperhost import AirbnbSuperhost

from tensorflow.keras.preprocessing import image as keras_image
import onnxruntime as ort

import tensorflow as tf
import numpy as np
from io import BytesIO

app = FastAPI()

IMG_SIZE = (224, 224)
class_names = [
    'closet', 'computerroom', 'corridor', 'dining_room', 'elevator', 
     'gameroom', 'garage', 'gym', 'kitchen', 'livingroom', 'lobby', 'meeting_room', 
     'office', 'pantry', 'restaurant', 'restaurant_kitchen', 'tv_studio', 'waitingroom']

with open('../_models/classification_model.bin', 'rb') as f_in: # very important to use 'rb' here, it means read-binary 
    model_classification, dv_classification = pickle.load(f_in)

model_regression = xgb.XGBRegressor()
model_regression.load_model('../_models/regression_model.json')

model_room_keras = tf.keras.models.load_model("../_models/cnn_room_classifier_effnet.keras")

ort_session = ort.InferenceSession(
    "../_models/cnn_room_classifier_effnet.onnx",
    providers=["CPUExecutionProvider"]
)
input_name = ort_session.get_inputs()[0].name
output_name = ort_session.get_outputs()[0].name


def preprocess_image(image_bytes: bytes):
    img = keras_image.load_img(BytesIO(image_bytes), target_size=IMG_SIZE)
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict_property_price")
async def predict_property_price(request: AirbnbProperty):
    X_input = pd.DataFrame([request.dict()])
    expected_features = model_regression.get_booster().feature_names
    X_input = X_input[expected_features]
    y_pred = model_regression.predict(X_input)
    return {"property_price": float(y_pred)}


@app.post("/predict_superhost")
async def predict_hit(request: AirbnbSuperhost):
    print(request.dict())
    x = dv_classification.transform([request.dict()])
    y_pred = model_classification.predict_proba(x)[0, 1]
    return {"probability": float(y_pred)}


@app.post("/predict_room_keras")
async def predict_room_keras(image: bytes = Body(..., media_type="application/octet-stream")):
    image_bytes = image
    img = preprocess_image(image_bytes)
    x = model_room_keras.predict(img)
    predicted_class = class_names[np.argmax(x)]
    confidence = np.max(x)
    return {"room_type": str(predicted_class), "confidence": float(confidence)}


@app.post("/predict_room_onnx")
async def predict_room_onnx(image: bytes = Body(..., media_type="application/octet-stream")):
    image_bytes = image
    img_tensor = preprocess_image(image_bytes)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

    input_feed = {
        'input': img_tensor,  # Or whatever the image input name is
        'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
        'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
    }
    pred = ort_session.run([output_name], input_feed)[0]

    predicted_class = class_names[np.argmax(pred)]
    confidence = np.max(pred)
    return {"room_type_onnx": str(predicted_class), "confidence_onnx": float(confidence)}