from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PredictionItem(BaseModel):
    id: Optional[str] = Field(None, description="Optional identifier for input record")
    features: List[float] = Field(..., description="Numerical feature vector for model input")

class PredictionRequest(BaseModel):
    inputs: List[PredictionItem] = Field(..., description="Batch of input instances")
    model_version: Optional[str] = Field("latest", description="Target model version")

class PredictionOutput(BaseModel):
    id: Optional[str] = None
    prediction: float
    probability: Optional[float] = None

class PredictionResponse(BaseModel):
    predictions: List[PredictionOutput]
    model_version: str
    latency_ms: float
    processed_at: str

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool
    version: str
    uptime_seconds: float
