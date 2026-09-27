# 🛠️ Code Quality & Formatting Guide

This guide describes how to set up automated linting and formatting for repositories within **AIML Club**.

---

## 🎯 Overview

We enforce modern, lightweight Python tooling across all templates:
- **[Ruff](https://github.com/astral-sh/ruff)**: Ultra-fast Python linter and code formatter.
- **[Black](https://github.com/psf/black)**: Uncompromising Python code formatter.
- **[Pre-commit](https://pre-commit.com/)**: Git hooks framework that verifies code quality before commits are made.

---

## 🚀 Setup Instructions

1. Install `pre-commit`:
   ```bash
   pip install pre-commit ruff black
   ```

2. Install the Git hooks:
   ```bash
   pre-commit install
   ```

3. (Optional) Run against all files manually:
   ```bash
   pre-commit run --all-files
   ```

---

## ⚙️ Configuration

The configurations are defined centrally in `pyproject.toml` and `.pre-commit-config.yaml`.
- Line length: **100 characters**
- Python target: **3.10+**
- Trailing whitespace and missing end-of-file newlines are automatically corrected on commit.
