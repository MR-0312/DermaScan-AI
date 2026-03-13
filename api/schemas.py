"""Pydantic schemas for API."""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float
    confidence_level: str
    tier: str
    severity: str
    emoji: str
    tagline: str
    action: str
    urgency_message: str
    description: str
    care_advice: List[str]
    risk_factors: List[str]
    hospital_search_query: str
    hospital_type: str
    differential_diagnosis: List[Dict]
    cancer_alert: bool
    cancer_warning: Optional[str] = None
    all_probabilities: Dict[str, float]
    disclaimer: str
    maps_url: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_name: str
    version: str