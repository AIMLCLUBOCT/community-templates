from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PredictionItem(BaseModel):
    id: str | None = Field(None, description="Optional identifier for input record")
    features: list[float] = Field(..., description="Numerical feature vector for model input")

class PredictionRequest(BaseModel):
    inputs: list[PredictionItem] = Field(..., description="Batch of input instances")
    model_version: str | None = Field("latest", description="Target model version")

class PredictionOutput(BaseModel):
    id: str | None = None
    prediction: float
    probability: float | None = None

class PredictionResponse(BaseModel):
    predictions: list[PredictionOutput]
    model_version: str
    latency_ms: float
    processed_at: str

class HealthResponse(BaseModel):
    status: str = "healthy"
    model_loaded: bool
    version: str
    uptime_seconds: float
