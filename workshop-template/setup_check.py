"""Pre-workshop participant environment verification script."""

from __future__ import annotations

import platform
import sys


def verify_environment() -> bool:
    """Check Python runtime version and print diagnostics."""
    print("=" * 60)
    print(" AIML Club OCT - Workshop Environment Diagnostics")
    print("=" * 60)
    print(f"Python Version:   {platform.python_version()}")
    print(f"Platform:         {platform.platform()}")
    print(f"Executable:       {sys.executable}")
    print("-" * 60)

    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required for this workshop.")
        return False

    print("[OK] Python environment is ready for hands-on exercises!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = verify_environment()
    sys.exit(0 if success else 1)
