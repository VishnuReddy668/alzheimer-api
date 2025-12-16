import joblib
import numpy as np
import cv2

model = joblib.load("alzheimer_model.pkl")
feature_means = joblib.load("feature_means.pkl")

def extract_features_from_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not loaded")

    img = cv2.resize(img, (200, 200))

    mean_pixel = np.mean(img)
    std_pixel = np.std(img)

    return np.array([mean_pixel, std_pixel])


def predict_from_image(image_path):
    extracted = extract_features_from_image(image_path)

    # fill missing features using mean values
    full_features = np.array(feature_means)
    full_features[:len(extracted)] = extracted

    full_features = full_features.reshape(1, -1)

    # 🔴 WRITE THESE TWO LINES HERE
    prediction = model.predict(full_features)
    return str(prediction[0])
