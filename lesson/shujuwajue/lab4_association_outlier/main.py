"""Compatibility entry point for running the lab package as a script."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__:
    from .cli import main
else:
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from lesson.shujuwajue.lab4_association_outlier.cli import main


if __name__ == "__main__":
    main()
