"""Interactive hands-on lab demonstration for AIML Club OCT workshops."""

from __future__ import annotations

import math
import random


def generate_synthetic_data(num_samples: int = 50) -> list[tuple[float, float]]:
    """Generate linear dataset with slight gaussian noise."""
    data = []
    for _ in range(num_samples):
        x = round(random.uniform(-5.0, 5.0), 3)
        noise = random.gauss(0.0, 0.5)
        y = round(2.5 * x + 1.2 + noise, 3)
        data.append((x, y))
    return data


def compute_loss(data: list[tuple[float, float]], w: float, b: float) -> float:
    """Compute Mean Squared Error (MSE)."""
    if not data:
        return 0.0
    total_error = sum((y - (w * x + b)) ** 2 for x, y in data)
    return total_error / len(data)


def run_lab() -> None:
    """Simulate workshop linear regression gradient descent demonstration."""
    print("Running Workshop Lab Demonstration...")
    data = generate_synthetic_data(100)
    w, b = 0.0, 0.0
    lr = 0.01

    for epoch in range(1, 201):
        # Gradients
        dw = sum(-2 * x * (y - (w * x + b)) for x, y in data) / len(data)
        db = sum(-2 * (y - (w * x + b)) for x, y in data) / len(data)
        w -= lr * dw
        b -= lr * db

        if epoch % 50 == 0:
            loss = compute_loss(data, w, b)
            print(f"Epoch {epoch:3d} | Loss: {loss:.4f} | w: {w:.3f} | b: {b:.3f}")

    print(f"\nFinal Model parameters: w={w:.3f}, b={b:.3f}")


if __name__ == "__main__":
    run_lab()
