# Using Model 
import cv2
import numpy as np

import traceback
import tensorflow as tf

from fastapi import FastAPI, Response, UploadFile, APIRouter
router = APIRouter()

# Initialize Model
model = tf.saved_model.load("./api//snackscan/1")

# Predict endpoint
labels = ['grontol', 'lanting', 'lumpia', 'putu ayu', 'serabi solo', 'wajik']

@router.post("/predict2_image")
def predict_image(uploaded_file: UploadFile, response: Response):
    try:
        # Checking if it's an image
        if uploaded_file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
            response.status_code = 400
            return "File is Not an Image"
        
        image = cv2.imdecode(np.frombuffer(uploaded_file.file.read(), np.uint8), cv2.IMREAD_COLOR)
        print("Image shape:", image.shape)
        
        # Step 1: Resize image to (150, 150)
        image = cv2.resize(image, (150, 150))
        image = image / 255.0
        
        # Step 2: Prepare data to model
        image = np.expand_dims(image, 0)
        
        # Step 3: Predict the data
        output = model.signatures["serving_default"](tf.constant(image.astype(np.float32)))
        predictions = output["dense_27"].numpy()
        prediction = np.argmax(predictions)
        result = labels[prediction]

        return {"prediction": result}
    except Exception as e:
        traceback.print_exc()
        response.status_code = 500
        return "Internal Server Error"