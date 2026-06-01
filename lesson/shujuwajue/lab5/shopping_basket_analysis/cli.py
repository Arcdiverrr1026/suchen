"""Command-line interface for the shopping basket analysis project."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import DEFAULT_DATA_DIR, DEFAULT_OUTPUT_DIR, run_analysis


def build_parser() -> argparse.ArgumentParser:
    """定义命令行参数，便于复现实验或调整 Apriori 阈值。"""
    parser = argparse.ArgumentParser(description="Run shopping basket analysis with Apriori.")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DEFAULT_DATA_DIR,
        help="Directory containing GoodsOrder.csv and GoodsTypes.csv.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory used for generated tables, figures, and reports.",
    )
    parser.add_argument(
        "--min-support",
        type=float,
        default=0.01,
        help="Selected minimum support for the final Apriori result.",
    )
    parser.add_argument(
        "--min-confidence",
        type=float,
        default=0.30,
        help="Selected minimum confidence for the final association rules.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=20,
        help="Number of records shown in top product/rule outputs.",
    )
    parser.add_argument("--skip-plots", action="store_true", help="Skip figure generation.")
    return parser


def main() -> None:
    """命令行入口：运行完整分析，并在终端打印关键摘要。"""
    args = build_parser().parse_args()
    # 具体分析逻辑放在 analysis.py，CLI 只负责接收参数和展示结果。
    result = run_analysis(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        min_support=args.min_support,
        min_confidence=args.min_confidence,
        top_n=args.top_n,
        make_plots=not args.skip_plots,
    )

    summary = result["summary"]
    print("购物篮分析已完成")
    print(f"- 交易数：{summary['transactions']}")
    print(f"- 商品数：{summary['unique_goods_in_orders']}")
    print(f"- 最终频繁项集：{summary['selected_itemset_count']}")
    print(f"- 最终关联规则：{summary['selected_rule_count']}")
    print(f"- 输出目录：{Path(args.output_dir).resolve()}")


if __name__ == "__main__":
    main()
