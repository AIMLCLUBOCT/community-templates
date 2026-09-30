import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from metrics import calculate_classification_metrics, calculate_regression_metrics
from reporter import EvaluationReporter


def test_classification_metrics():
    y_true = [1, 0, 1, 1, 0, 1]
    y_pred = [1, 0, 1, 0, 0, 1]
    res = calculate_classification_metrics(y_true, y_pred)
    assert res["accuracy"] == round(5 / 6, 4)
    assert res["tp"] == 3
    assert res["fp"] == 0
    assert res["fn"] == 1

def test_regression_metrics():
    y_true = [3.0, -0.5, 2.0, 7.0]
    y_pred = [2.5, 0.0, 2.0, 8.0]
    res = calculate_regression_metrics(y_true, y_pred)
    assert res["mae"] == 0.5
    assert res["mse"] == 0.375

def test_reporter():
    metrics = {"accuracy": 0.95, "f1_score": 0.94}
    md = EvaluationReporter.to_markdown_table(metrics)
    assert "| `accuracy` | **0.95** |" in md
