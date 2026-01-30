from fastapi import FastAPI,File,UploadFile,HTTPException
import numpy as np
import tensorflow as tf
from io import BytesIO
from PIL import Image
import os

app=FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "leafguard_model.h5")
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
class_names=["Early Blight","Late Blight","Healthy"]

suggestions = {
    "Early Blight": [
        "Remove infected leaves immediately to prevent spreading.",
        "Avoid overhead watering; water at the base of the plant.",
        "Apply fungicide if infection is severe."
    ],
    "Late Blight": [
        "Remove and destroy infected leaves; do not compost.",
        "Use protective fungicides early and repeatedly.",
        "Ensure proper spacing between plants for better air circulation."
    ],
    "Healthy": [
        "Check leaves periodically for early signs of disease.",
        "Maintain good soil and water management.",
        "Rotate crops to prevent disease buildup in the soil."
    ]
}

ALLOWED_EXTENSION={"jpg","jpeg","png"}
MAX_SIZE=5*1024*1024
IMAGE_SIZE=(224,224)
CONFIDENCE_THRESHOLD=0.6


def read_file_as_image(data)->np.ndarray:
    try:
        image= np.array(Image.open(BytesIO(data)).convert("RGB"))
        return image
    except:
        raise HTTPException(status_code=400, detail="Invalid image file")
    
def validate_file(file:UploadFile,content:bytes):
    ext=file.filename.split(".")[-1].lower()
    if ext not in ALLOWED_EXTENSION:
        raise HTTPException(status_code=400,detail="Only JPG and PNG images allowed")
    
    if len(content)>MAX_SIZE:
        raise HTTPException(status_code=400,detail="File size exceeds 5MB")

def preprocess_image(image:np.ndarray)->np.ndarray:
    img = Image.fromarray(image)
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    return img_batch


def check_brightness(image:np.ndarray):
    gray=np.mean(image)
    if gray<40:
        raise HTTPException(status=400,detail="Image too dark")
    if gray>220:
        raise HTTPException(status_code=400,detail="Image too bright")
    
def check_image_size(image:np.ndarray):
    h,w=image.shape[:2]
    if h<100 or w<100:
        raise HTTPException(status_code=400,detail="Image resolution too low")
    if h*w>500_000:
        return "Warning: multiple leaves detected, accuracy may reduce"
    return None

@app.get("/")
async def hello():
    return "Hello, I'm Alive"

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        validate_file(file,contents)

        image=read_file_as_image(contents)

        check_brightness(image)
        multi_leaf_warning=check_image_size(image)

        img_batch = np.expand_dims(image, 0)
        img_batch = tf.convert_to_tensor(img_batch, dtype=tf.float32)

        # For regular Keras model
        pred_array = model.predict(img_batch)  # returns a NumPy array


        predicted_class = class_names[np.argmax(pred_array[0])]
        confidence = float(np.max(pred_array[0]))

        if confidence<CONFIDENCE_THRESHOLD:
            return {
                "class": "Uncertain",
                "confidence": confidence,
                "message":"Low confidence. Please upload a clearer image."
            }
        result={
            "class":predicted_class,
            "confidence":confidence,
            "suggestions":suggestions[predicted_class]
        }
        if multi_leaf_warning:
            result["warning"]=multi_leaf_warning
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
        