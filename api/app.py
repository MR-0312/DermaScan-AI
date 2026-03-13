"""
=================================================================
DERMASCAN-AI — FastAPI Application
=================================================================
"""

import io
import time
import numpy as np
from PIL import Image
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.inference.predictor import SkinPredictor
from src.response.response_engine import ResponseEngine
from src.response.hospital_finder import HospitalFinder
from api.schemas import HealthResponse

# ── Global objects ──
predictor = None
response_engine = None
hospital_finder = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global predictor, response_engine, hospital_finder
    
    print("🚀 Starting DermaScan-AI...")
    
    predictor = SkinPredictor(
        model_path="checkpoints/best_model.pth",
        class_config_path="configs/class_config.json",
        device="cpu",
    )
    
    response_engine = ResponseEngine(
        class_config_path="configs/class_config.json",
        response_templates_path="configs/response_templates.json",
    )
    
    hospital_finder = HospitalFinder()
    
    print("✅ DermaScan-AI ready!")
    yield
    print("🛑 Shutting down...")


app = FastAPI(
    title="🔬 DermaScan-AI",
    description="AI-powered skin disease detection with clinical guidance",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def convert_numpy(obj):
    """Convert numpy types to Python native for JSON serialization."""
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        model_loaded=predictor is not None,
        model_name="EfficientNet-B3",
        version="1.0.0",
    )


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    city: str = Query("Delhi", description="City in India"),
    state: str = Query("Delhi", description="State in India"),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(400, "Only JPG/PNG images supported")
    
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 10MB)")
    
    try:
        image = Image.open(io.BytesIO(contents)).convert('RGB')
    except Exception:
        raise HTTPException(400, "Invalid image file")
    
    start = time.time()
    prediction = predictor.predict(image)
    inference_time = time.time() - start
    
    response = response_engine.generate_response(
        predicted_class=prediction['predicted_class'],
        confidence=prediction['confidence'],
        all_probabilities=prediction['all_probabilities'],
    )
    
    hospital_result = hospital_finder.search(
        query=response['hospital_search_query'],
        city=city,
        state=state,
    )
    response['maps_url'] = hospital_result['maps_url']
    response['maps_embed_url'] = hospital_result['embed_url']
    response['hospital_location'] = hospital_result['location']
    response['inference_time'] = round(inference_time, 3)
    response['emergency_numbers'] = hospital_finder.get_emergency_numbers()
    
    return convert_numpy(response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)