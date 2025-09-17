from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from transformers import pipeline
from PIL import Image
import base64
from io import BytesIO
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Leaf Disease Detection API")

# Load Hugging Face model
classifier = pipeline("image-classification", model="linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification")

# ----------- Schemas -----------

# For base64 request
class Base64ImageRequest(BaseModel):
    image_base64: str

# Response schema
class PredictionResponse(BaseModel):
    label: str
    confidence: float
    all_probs: dict

# ----------- Endpoints -----------

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict/upload", response_model=PredictionResponse)
async def predict_upload(file: UploadFile = File(...)):
    """Predict from an uploaded image file"""
    img = Image.open(file.file).convert("RGB")
    results = classifier(img)

    # Take top-1 prediction
    top_result = results[0]
    return PredictionResponse(
        label=top_result["label"],
        confidence=float(top_result["score"]),
        all_probs={r["label"]: float(r["score"]) for r in results}
    )

@app.post("/predict/base64", response_model=PredictionResponse)
async def predict_base64(req: Base64ImageRequest):
    """Predict from a base64-encoded image"""
    img_data = base64.b64decode(req.image_base64)
    img = Image.open(BytesIO(img_data)).convert("RGB")
    results = classifier(img)

    top_result = results[0]
    return PredictionResponse(
        label=top_result["label"],
        confidence=float(top_result["score"]),
        all_probs={r["label"]: float(r["score"]) for r in results}
    )


