# 🚀 ML Model Inference Container Template

Production-grade template for packaging machine learning models into containerized, low-latency REST APIs using **FastAPI**, **Uvicorn**, and **Docker**.

---

## 📋 Features

- **⚡ Fast & Async**: Built with FastAPI for sub-millisecond route dispatching and asynchronous worker pools.
- **🛡️ Schema Validation**: Strict input/output validation with Pydantic v2.
- **🐳 Multi-Stage Docker Build**: Minimal attack surface with non-root security context (`appuser`) and slim base image.
- **📊 Prometheus Observability**: Built-in `/metrics` endpoint with request counters and latency histograms.
- **🩺 Health Checks**: Built-in `/health` endpoint compatible with Kubernetes liveness/readiness probes and Docker healthchecks.
- **🧪 Automated Tests**: Unit tests with `pytest` and `httpx`.
- **📈 Benchmarking**: Multi-threaded load testing script for p50/p95/p99 latency measurements.

---

## 🏗️ Architecture

```
Client Request
      │
      ▼
┌────────────── Docker Container :8000 ──────────────┐
│                                                    │
│  FastAPI (Uvicorn Workers)                         │
│  ├── /health   -> HealthCheck Probe                │
│  ├── /metrics  -> Prometheus Metrics Exporter      │
│  └── /predict  -> Pydantic Parser                  │
│                        │                           │
│                 ModelEngine (Inference)            │
│                        │                           │
│                 Latency & Metric Observer          │
└────────────────────────────────────────────────────┘
```

---

## 🚀 Quickstart

### Local Development

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

## 🐳 Docker Deployment

### Build Container
```bash
docker build -t aimlclub/inference-service:latest .
```

### Run Container
```bash
docker run -d --name ml-inference -p 8000:8000 aimlclub/inference-service:latest
```

### Run with Docker Compose
```bash
docker-compose up -d
```

---

## 📡 API Reference

### Health Check
```bash
curl -X GET http://localhost:8000/health
```

### Model Inference
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": [
      {"id": "doc_1", "features": [1.5, -0.4, 0.99, -1.2]},
      {"id": "doc_2", "features": [-0.8, 1.2, -0.5, 0.3]}
    ],
    "model_version": "1.0.0"
  }'
```

### Prometheus Metrics
```bash
curl -X GET http://localhost:8000/metrics
```

---

## 🧪 Testing & Benchmarking

Run unit tests:
```bash
pytest tests/ -v
```

Run load test benchmark:
```bash
python benchmarks/load_test.py
```
