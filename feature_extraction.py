import cv2
import numpy as np

def extract_image_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    h, w = binary.shape
    ink_density = np.sum(binary > 0) / (h * w)

    stroke_lengths = [cv2.arcLength(c, False) for c in contours]

    return {
        "max_x_extension1": w,
        "max_y_extension1": h,
        "num_of_pendown1": len(contours),
        "pressure_mean1": ink_density * 100,
        "total_time1": np.sum(stroke_lengths)
    }
