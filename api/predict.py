# Using api on api
import cv2
import numpy as np
import requests
import json

import traceback
import tensorflow as tf

from fastapi import FastAPI, Response, UploadFile, APIRouter
from .utils import load_image_into_numpy_array
router = APIRouter()

# Predict endpoint
labels = ['grontol', 'lanting', 'lumpia', 'putu ayu', 'serabi solo', 'wajik']

@router.post("/predict_image")
def predict_image(uploaded_file: UploadFile, response: Response):
    try:
        # Checking if it's an image
        if uploaded_file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            response.status_code = 400
            return "File is Not an Image"
        
        image = load_image_into_numpy_array(uploaded_file.file.read())
        print("Image shape:", image.shape)
        
        # Step 1: Resize image to (150, 150)
        image = cv2.resize(image, (150, 150))
        image = image / 255.0
        
        # Step 2: Prepare data to model
        image = np.expand_dims(image, 0)
        
        # Step 3: Predict the data
        json_data = json.dumps({"instances": image.tolist()})
        endpoint = "http://34.128.89.110:8080/v1/models/snackscan:predict"
        response = requests.post(endpoint, data=json_data)
        
        # Step 4: Change the result your determined API output
        prediction = tf.argmax(response.json()["predictions"], 1).numpy()
        result = labels[prediction[0]]
        
        return {"prediction": result}
    
    except Exception as e:
        traceback.print_exc()
        response.status_code = 500
        return "Internal Server Error"

