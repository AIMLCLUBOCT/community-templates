# 📏 Model Evaluation & Reporting Template

A lightweight metrics calculation and performance reporting harness for AIML Club machine learning projects.

---

## 🚀 Features

- **Classification Metrics**: Accuracy, Precision, Recall, F1 Score, and Confusion Matrix values.
- **Regression Metrics**: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE).
- **Automated Exporters**: Formatted Markdown tables for research READMEs and GitHub PR descriptions, or JSON for automated benchmarks.

---

## 💻 Quick Usage

```python
from metrics import calculate_classification_metrics
from reporter import EvaluationReporter

y_true = [1, 0, 1, 1, 0, 1]
y_pred = [1, 0, 1, 0, 0, 1]

metrics = calculate_classification_metrics(y_true, y_pred)
print(EvaluationReporter.to_markdown_table(metrics))
```
