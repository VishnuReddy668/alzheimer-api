from fastapi import FastAPI, UploadFile, File
import shutil
import os
from model_utils import predict_from_image

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # save uploaded image to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # send file path to model
    prediction = predict_from_image(file_path)

    return {"prediction": prediction}
