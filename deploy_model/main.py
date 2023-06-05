import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import io
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image

from flask import Flask, request, jsonify

model = keras.models.load_model("my_model.h5")


def transform_image(pillow_image):
    pillow_image = pillow_image.convert('RGB')  # Convert image to RGB
    data = np.asarray(pillow_image)
    data = data / 255.0
    data = tf.image.resize(data, [224, 224])
    data = np.expand_dims(data, axis=0)  # Add a batch dimension
    return data


def predict(x):
    predictions = model(x)
    pred0 = predictions[0]
    label0 = np.argmax(pred0)
    return label0

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            pillow_img = Image.open(io.BytesIO(image_bytes)).convert('L')
            tensor = transform_image(pillow_img)
            prediction = predict(tensor)
            data = {"prediction": int(prediction)}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)