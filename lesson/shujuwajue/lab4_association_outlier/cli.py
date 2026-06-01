from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import run_experiment

PACKAGE_DIR = Path(__file__).resolve().parent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lab4-association-outlier",
        description="Run association analysis and K-Means outlier detection.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=PACKAGE_DIR / "data",
        help="Directory containing menu_orders.xls and consumption_data.xls.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PACKAGE_DIR / "output",
        help="Directory where generated CSV, JSON, and image files are written.",
    )
    parser.add_argument("--min-support", type=float, default=0.3)
    parser.add_argument("--min-confidence", type=float, default=0.6)
    parser.add_argument("--clusters", type=int, default=3)
    parser.add_argument("--outlier-threshold", type=float, default=2.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_experiment(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        n_clusters=args.clusters,
        outlier_threshold=args.outlier_threshold,
    )
