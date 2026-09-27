"""Model evaluation metrics calculation engine."""
import math
from typing import List, Dict, Any, Union

def calculate_classification_metrics(
    y_true: List[int], y_pred: List[int]
) -> Dict[str, float]:
    """Calculate accuracy, precision, recall, and f1 score."""
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must be non-empty lists of the same length.")

    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    tn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 0)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    total = len(y_true)
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn
    }

def calculate_regression_metrics(
    y_true: List[float], y_pred: List[float]
) -> Dict[str, float]:
    """Calculate MAE, MSE, and RMSE."""
    if len(y_true) != len(y_pred) or not y_true:
        raise ValueError("y_true and y_pred must be non-empty lists of the same length.")

    n = len(y_true)
    mae = sum(abs(yt - yp) for yt, yp in zip(y_true, y_pred)) / n
    mse = sum((yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)) / n
    rmse = math.sqrt(mse)

    return {
        "mae": round(mae, 4),
        "mse": round(mse, 4),
        "rmse": round(rmse, 4)
    }
