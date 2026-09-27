"""Load testing and latency benchmarking script for inference endpoint."""
import time
import statistics
import concurrent.futures
from typing import List, Dict, Any
import requests

ENDPOINT = "http://localhost:8000/predict"
CONCURRENT_USERS = 10
TOTAL_REQUESTS = 100

SAMPLE_PAYLOAD = {
    "inputs": [
        {"id": f"sample_{i}", "features": [0.5, -0.2, 1.3, -0.9, 0.44]}
        for i in range(4)
    ],
    "model_version": "1.0.0"
}

def send_request(session: requests.Session) -> float:
    t0 = time.perf_counter()
    resp = session.post(ENDPOINT, json=SAMPLE_PAYLOAD, timeout=5.0)
    latency_ms = (time.perf_counter() - t0) * 1000.0
    if resp.status_code != 200:
        raise RuntimeError(f"Request failed with status {resp.status_code}")
    return latency_ms

def run_benchmark():
    print(f"Starting benchmark: {TOTAL_REQUESTS} requests across {CONCURRENT_USERS} concurrent workers...")
    latencies: List[float] = []

    with requests.Session() as session:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_USERS) as executor:
            futures = [executor.submit(send_request, session) for _ in range(TOTAL_REQUESTS)]
            for fut in concurrent.futures.as_completed(futures):
                try:
                    latencies.append(fut.result())
                except Exception as e:
                    print(f"Error during request: {e}")

    if not latencies:
        print("No requests completed successfully.")
        return

    latencies.sort()
    avg = statistics.mean(latencies)
    p50 = statistics.median(latencies)
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print("=== Benchmark Results ===")
    print(f"Total Completed: {len(latencies)}/{TOTAL_REQUESTS}")
    print(f"Mean Latency:    {avg:.2f} ms")
    print(f"p50 Latency:     {p50:.2f} ms")
    print(f"p95 Latency:     {p95:.2f} ms")
    print(f"p99 Latency:     {p99:.2f} ms")

if __name__ == "__main__":
    run_benchmark()
