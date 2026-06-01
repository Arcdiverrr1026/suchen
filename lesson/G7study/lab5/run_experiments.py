#!/usr/bin/env python3
"""机器学习实验5：SVM 与聚类模型构建与评估。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lesson.G7study.lab5.common import print_section  # noqa: E402
from lesson.G7study.lab5.task1_linear_svm.experiment import (  # noqa: E402
    run_experiment as run_task1,
)
from lesson.G7study.lab5.task2_rbf_svm.experiment import (  # noqa: E402
    run_experiment as run_task2,
)
from lesson.G7study.lab5.task3_kmeans.experiment import (  # noqa: E402
    run_experiment as run_task3,
)
from lesson.G7study.lab5.task4_dbscan.experiment import (  # noqa: E402
    run_experiment as run_task4,
)


TASKS = {
    "task1": ("任务1：线性核 SVM 分类（鸢尾花数据集）", run_task1),
    "task2": ("任务2：高斯核 SVM 分类（乳腺癌数据集）", run_task2),
    "task3": ("任务3：K-Means 聚类（鸢尾花数据集）", run_task3),
    "task4": ("任务4：DBSCAN 密度聚类（鸢尾花数据集）", run_task4),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="运行机器学习实验5。")
    parser.add_argument(
        "--task",
        choices=["all", *TASKS.keys()],
        default="all",
        help="选择要运行的任务，默认运行全部任务。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print_section("机器学习实验5：使用 SVM 与聚类模型构建与评估")

    selected_tasks = TASKS.items() if args.task == "all" else [(args.task, TASKS[args.task])]
    summary: dict[str, dict[str, float]] = {}

    for key, (title, runner) in selected_tasks:
        print_section(f"开始运行：{title}")
        summary[key] = runner()

    print_section("实验运行完成")
    for key, metrics in summary.items():
        metric_text = ", ".join(f"{name}={value:.4f}" for name, value in metrics.items())
        print(f"{key}: {metric_text}")
    print("图表、CSV 与 JSON 结果已保存到各任务目录。")


if __name__ == "__main__":
    main()
