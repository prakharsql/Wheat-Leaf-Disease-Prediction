from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

from app.utils import preprocess_image
from app.model import predict_disease

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------
app = FastAPI(
    title="Wheat Leaf Disease Prediction API",
    version="1.0.0"
)

# -------------------------------------------------
# CORS Configuration
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Static Files & Templates
# -------------------------------------------------
# NOTE: Run uvicorn from `backend/` directory
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------
# Home Route → UI
# -------------------------------------------------
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# -------------------------------------------------
# Prediction API (CRASH-PROOF)
# -------------------------------------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read & preprocess image
        image = Image.open(file.file).convert("RGB")
        processed_image = preprocess_image(image)

        # Predict
        disease, confidence, treatment = predict_disease(processed_image)

        return {
            "disease": disease,
            "confidence": confidence,
            "treatment": treatment
        }

    except Exception as e:
        # Fallback response (never crash frontend)
        return {
            "disease": "Prediction Error",
            "confidence": 0,
            "treatment": "Unable to process this image. Please try another image."
        }
