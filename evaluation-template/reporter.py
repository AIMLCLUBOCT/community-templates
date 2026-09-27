"""Markdown and JSON report generator for model evaluation."""
import json
from typing import Dict, Any

class EvaluationReporter:
    """Format and export evaluation metrics to Markdown or JSON."""

    @staticmethod
    def to_markdown_table(metrics: Dict[str, Any], title: str = "Model Performance Summary") -> str:
        lines = [
            f"### {title}\n",
            "| Metric | Value |",
            "| :--- | :--- |"
        ]
        for k, v in metrics.items():
            lines.append(f"| `{k}` | **{v}** |")
        return "\n".join(lines) + "\n"

    @staticmethod
    def to_json(metrics: Dict[str, Any]) -> str:
        return json.dumps(metrics, indent=2)
