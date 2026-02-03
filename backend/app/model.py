import os
import numpy as np
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "wheat_leaf_disease_model_bgg15.h5")

print("Loading model from:", MODEL_PATH)

# ✅ ORDER MUST MATCH TRAINING CLASS INDICES
CLASS_NAMES = [
    "Crown Root Rot",
    "Healthy",
    "Leaf Rust",
    "Loose Smut"
]

TREATMENTS = {
    "Healthy": "No disease detected. Maintain proper irrigation and nutrition.",
    "Leaf Rust": "Apply fungicide and remove infected leaves.",
    "Crown Root Rot": "Improve soil drainage and use disease-resistant varieties.",
    "Loose Smut": "Use certified seeds and seed treatment fungicides."
}

model = load_model(MODEL_PATH)

def predict_disease(image_array):
    preds = model.predict(image_array)
    preds = np.squeeze(preds)

    idx = int(np.argmax(preds))
    confidence = float(np.max(preds)) * 100

    # ✅ CONFIDENCE THRESHOLD
    if confidence < 70:
        disease = "Healthy"
        treatment = TREATMENTS["Healthy"]
        return disease, round(confidence, 2), treatment

    disease = CLASS_NAMES[idx]
    treatment = TREATMENTS[disease]

    return disease, round(confidence, 2), treatment
