import onnx
import numpy as np
from io import BytesIO
from urllib import request
from PIL import Image
from onnx.reference import ReferenceEvaluator
import onnxruntime as ort
import ssl

#model = onnx.load("hair_classifier_empty.onnx")
model = onnx.load("hair_classifier_v1.onnx")
img_url = 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'
ref = ReferenceEvaluator(model)

def download_image_from_url(url):
    context = ssl._create_unverified_context()
    with request.urlopen(url, context=context) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img

def load_image_from_file(path):
    img = Image.open(path)
    return img

def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img

def preprocess_image(img):
     img_array = np.array(img, dtype=np.float32)
     img_array = img_array.astype('float32') / 255
     img_array = (img_array - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
     return img_array


def predict_output_evaluator(img_normalized):
    input_data = np.transpose(img_normalized, (2, 0, 1))  # CHW
    input_data = np.expand_dims(input_data, axis=0).astype(np.float32)  # NCHW
    
    #session = ort.InferenceSession("hair_classifier_empty.onnx")
    session = ort.InferenceSession("hair_classifier_v1.onnx")
    prediction = session.run(["output"], {"input": input_data})[0][0][0]
  
    print(f"Model output: {prediction:.4f}")
    print(f"Prediction: {'Curly' if prediction > 0.5 else 'Straight'} hair")

def handler():
    img = download_image_from_url(img_url)
    resized_img =  prepare_image(img, (200,200))
    img_array = preprocess_image(resized_img)
    predict_output_evaluator(img_array)


handler()