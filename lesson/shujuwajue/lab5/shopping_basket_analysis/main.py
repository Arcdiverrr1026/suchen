"""Compatibility entry point for direct script execution."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__:
    from .cli import main
else:
    # 允许直接执行本文件：
    # ./.venv/bin/python lesson/shujuwajue/lab5/shopping_basket_analysis/main.py
    sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
    from lesson.shujuwajue.lab5.shopping_basket_analysis.cli import main


if __name__ == "__main__":
    main()
