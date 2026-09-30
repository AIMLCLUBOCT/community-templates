import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from app.model import ModelEngine
from app.schemas import HealthResponse, PredictionOutput, PredictionRequest, PredictionResponse

START_TIME = time.time()
REQUEST_COUNT = Counter("inference_requests_total", "Total inference requests", ["endpoint", "status"])
REQUEST_LATENCY = Histogram("inference_latency_seconds", "Inference latency in seconds", ["endpoint"])

model_engine: ModelEngine = ModelEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_engine
    if model_engine is None or not model_engine.is_loaded:
        model_engine = ModelEngine()
    yield

app = FastAPI(
    title="ML Model Inference Service",
    description="High-performance containerized ML inference service template for AIML Club.",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time-Ms"] = f"{duration * 1000:.2f}"
    return response

@app.get("/health", response_model=HealthResponse)
def health():
    if model_engine is None or not model_engine.is_loaded:
        raise HTTPException(status_code=503, detail="Model engine not ready")
    return HealthResponse(
        status="healthy",
        model_loaded=model_engine.is_loaded,
        version=model_engine.version,
        uptime_seconds=round(time.time() - START_TIME, 2)
    )

@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest):
    if model_engine is None or not model_engine.is_loaded:
        REQUEST_COUNT.labels(endpoint="predict", status="error").inc()
        raise HTTPException(status_code=503, detail="Model is not ready")

    start_time = time.perf_counter()
    raw_vectors = [item.features for item in payload.inputs]

    try:
        raw_outputs = model_engine.predict(raw_vectors)
    except Exception as exc:
        REQUEST_COUNT.labels(endpoint="predict", status="error").inc()
        raise HTTPException(status_code=500, detail=str(exc))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    REQUEST_COUNT.labels(endpoint="predict", status="success").inc()
    REQUEST_LATENCY.labels(endpoint="predict").observe(elapsed_ms / 1000.0)

    outputs = [
        PredictionOutput(
            id=item.id,
            prediction=pred,
            probability=prob
        )
        for item, (pred, prob) in zip(payload.inputs, raw_outputs, strict=False)
    ]

    return PredictionResponse(
        predictions=outputs,
        model_version=model_engine.version,
        latency_ms=round(elapsed_ms, 3),
        processed_at=datetime.now(timezone.utc).isoformat()
    )

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
