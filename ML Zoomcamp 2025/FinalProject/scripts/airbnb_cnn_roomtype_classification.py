# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3.10 (tfenv)
#     language: python
#     name: tfenv
# ---

# %% id="XgxqfHiw9O1X"
import os
import ssl
import requests
from io import BytesIO
from urllib import request

from tqdm import tqdm
from PIL import Image

import pandas as pd
import json
import numpy as np
import seaborn as sn
import pickle

from matplotlib import pyplot as plt
from io import StringIO
# %matplotlib inline

# %% id="3bzuJKLx-D2s"
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
import tensorflow_datasets as tfds

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix, classification_report

# %% colab={"base_uri": "https://localhost:8080/"} id="KWhTjjVNb7Zi" outputId="6720e9af-4d42-440d-902b-b839a6bd9553"
import cv2

# %%
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

# %%
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

train_ds = image_dataset_from_directory(
    "../data_room_classifier/train",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

test_ds = image_dataset_from_directory(
    "../data_room_classifier/test",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="categorical"
)

class_names = train_ds.class_names
NUM_CLASSES = len(class_names)
print(class_names)

test_class_names = test_ds.class_names
print(test_class_names)

# %%
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.1),
    tf.keras.layers.RandomContrast(0.1),
])

# %%
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras import layers, models

base_model = EfficientNetB0(
    include_top=False,
    weights="imagenet",
    input_shape=(224, 224, 3)
)

# Freeze base model
base_model.trainable = False

model = models.Sequential([
    data_augmentation,
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(NUM_CLASSES, activation='softmax')  # Now this matches dataset
])



model.summary()

# %%
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',  # Changed from categorical
    metrics=['accuracy']
)


# %%
model.summary()

# %%
EPOCHS = 15

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=EPOCHS
)


# %%
history

# %%
#####Fine tuning the model

# %%
# Unfreeze top layers
base_model.trainable = True

for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

fine_tune_epochs = 10

history_fine = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=fine_tune_epochs
)


# %%
history_fine

# %%
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

y_true = []
y_pred = []

for images, labels in test_ds:
    preds = model.predict(images)
    y_true.extend(np.argmax(labels.numpy(), axis=1))
    y_pred.extend(np.argmax(preds, axis=1))

print(classification_report(y_true, y_pred, target_names=class_names))

# %%
model.save("../_models/cnn_room_classifier_effnet.keras")

# %%
model_test.input_shape

# %%
from tensorflow.keras.preprocessing import image

# %%
IMG_SIZE = (224, 224)

def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array


# %%
class_names = [
    'closet', 'computerroom', 'corridor', 'dining_room', 'elevator', 
     'gameroom', 'garage', 'gym', 'kitchen', 'livingroom', 'lobby', 'meeting_room', 
     'office', 'pantry', 'restaurant', 'restaurant_kitchen', 'tv_studio', 'waitingroom']


# %%
img_path = "../data_room_classifier/living_room.jpg"

img_tensor = preprocess_image(img_path)
pred = model_test.predict(img_tensor)

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print(f"Predicted Room: {predicted_class}")
print(f"Confidence: {confidence:.2%}")

# %%
img_path = "../data_room_classifier/dining_room.jpg"

img_tensor = preprocess_image(img_path)
pred = model_test.predict(img_tensor)

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print(f"Predicted Room: {predicted_class}")
print(f"Confidence: {confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen.jpg"

img_tensor = preprocess_image(img_path)
pred = model_test.predict(img_tensor)

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print(f"Predicted Room: {predicted_class}")
print(f"Confidence: {confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen1.jpg"

img_tensor = preprocess_image(img_path)
pred = model_test.predict(img_tensor)

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print(f"Predicted Room: {predicted_class}")
print(f"Confidence: {confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen2.jpg"

img_tensor = preprocess_image(img_path)
pred = model_test.predict(img_tensor)

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print(f"Predicted Room: {predicted_class}")
print(f"Confidence: {confidence:.2%}")

# %%
import tensorflow as tf
import tf2onnx


model_test = tf.keras.models.load_model("../_models/cnn_room_classifier_effnet.keras")

@tf.function
def serving_default(input_tensor):
    return model_test(input_tensor, training=False) 

input_signature = [tf.TensorSpec(model_test.input_shape, tf.float32, name='input')]

output_path = "../_models/cnn_room_classifier_effnet_fixed.onnx"

model_proto, _ = tf2onnx.convert.from_function(
    serving_default,
    input_signature=input_signature,
    opset=13,
    output_path=output_path
)

print(f"Success! Cleaned model saved to {output_path}")

# %%
import onnxruntime as ort
import numpy as np
from tensorflow.keras.preprocessing import image

session = ort.InferenceSession(
    "../_models/cnn_room_classifier_effnet.onnx",
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


# %%
def preprocess_image_onnx(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
    return img_array.astype(np.float32)


# %%
img_path = "../data_room_classifier/dining_room.jpg"

img_tensor = preprocess_image_onnx(img_path)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

input_feed = {
    'input': img_tensor,  # Or whatever the image input name is
    'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
    'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
}
pred = session.run([output_name], input_feed)[0]

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print("Predicted Room:", predicted_class)
print("Confidence:", f"{confidence:.2%}")

# %%
img_path = "../data_room_classifier/living_room.jpg"

img_tensor = preprocess_image_onnx(img_path)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

input_feed = {
    'input': img_tensor,  
    'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
    'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
}
pred = session.run([output_name], input_feed)[0]

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print("Predicted Room:", predicted_class)
print("Confidence:", f"{confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen.jpg"

img_tensor = preprocess_image_onnx(img_path)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

input_feed = {
    'input': img_tensor,  
    'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
    'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
}
pred = session.run([output_name], input_feed)[0]

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print("Predicted Room:", predicted_class)
print("Confidence:", f"{confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen1.jpg"

img_tensor = preprocess_image_onnx(img_path)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

input_feed = {
    'input': img_tensor,  
    'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
    'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
}
pred = session.run([output_name], input_feed)[0]

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print("Predicted Room:", predicted_class)
print("Confidence:", f"{confidence:.2%}")

# %%
img_path = "../data_room_classifier/Kitchen2.jpg"

img_tensor = preprocess_image_onnx(img_path)
mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1,1,1,3)  
std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1,1,1,3)

input_feed = {
    'input': img_tensor,  
    'sequential_1_1/efficientnetb0_1/normalization_1/Sub/y:0': mean,
    'sequential_1_1/efficientnetb0_1/normalization_1/Sqrt/x:0': std
}
pred = session.run([output_name], input_feed)[0]

predicted_class = class_names[np.argmax(pred)]
confidence = np.max(pred)

print("Predicted Room:", predicted_class)
print("Confidence:", f"{confidence:.2%}")

# %%
