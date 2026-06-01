"""Shared helpers for lab 5 experiments."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

if not os.environ.get("MPLCONFIGDIR"):
    os.environ["MPLCONFIGDIR"] = str(
        Path(tempfile.gettempdir()) / "suchen_lab5_matplotlib"
    )
if not os.environ.get("LOKY_MAX_CPU_COUNT"):
    os.environ["LOKY_MAX_CPU_COUNT"] = "1"

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)


LAB_DIR = Path(__file__).resolve().parent
RANDOM_STATE = 42
TEST_SIZE = 0.2


def configure_matplotlib() -> None:
    """Configure matplotlib for Chinese labels and saved images."""
    plt.rcParams["font.sans-serif"] = [
        "SimHei",
        "Arial Unicode MS",
        "Heiti TC",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["savefig.dpi"] = 300


def task_output_dir(task_file: str | Path) -> Path:
    """Return the directory used by the current task script."""
    out_dir = Path(task_file).resolve().parent
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def print_section(title: str) -> None:
    line = "=" * 72
    print(f"\n{line}\n{title}\n{line}")


def print_dataset_summary(
    name: str,
    X: np.ndarray,
    y: np.ndarray | None = None,
    feature_names: list[str] | np.ndarray | None = None,
    target_names: list[str] | np.ndarray | None = None,
) -> None:
    print_section(f"数据集加载：{name}")
    print(f"样本数量: {X.shape[0]}")
    print(f"特征维度: {X.shape[1]}")

    if feature_names is not None:
        print("特征名称:")
        for index, feature_name in enumerate(feature_names, start=1):
            print(f"  {index:02d}. {feature_name}")

    if y is not None:
        print("类别分布:")
        labels, counts = np.unique(y, return_counts=True)
        for label, count in zip(labels, counts):
            label_text = (
                str(target_names[label])
                if target_names is not None and int(label) < len(target_names)
                else str(label)
            )
            ratio = count / len(y) * 100
            print(f"  {label_text}: {count} ({ratio:.2f}%)")

    if feature_names is not None:
        df = pd.DataFrame(X, columns=feature_names)
        print("\n特征统计摘要:")
        print(df.describe().round(3).to_string())


def evaluate_classifier(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray,
    target_names: list[str] | np.ndarray,
    average: str = "weighted",
) -> dict[str, Any]:
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average=average)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(
        y_test,
        y_pred,
        target_names=list(target_names),
        output_dict=True,
        zero_division=0,
    )

    print("模型评估结果:")
    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  F1-score ({average}): {f1:.4f}")
    print("混淆矩阵:")
    print(cm)
    print("\n分类报告:")
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=list(target_names),
            zero_division=0,
        )
    )

    return {
        "y_pred": y_pred,
        "accuracy": accuracy,
        "f1": f1,
        "confusion_matrix": cm,
        "classification_report": report,
    }


def plot_confusion_matrix(
    conf_matrix: np.ndarray,
    labels: list[str] | np.ndarray,
    title: str,
    output_path: str | Path,
) -> None:
    configure_matplotlib()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    image = ax.imshow(conf_matrix, cmap="Blues")
    ax.figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    ax.set(
        xticks=np.arange(len(labels)),
        yticks=np.arange(len(labels)),
        xticklabels=labels,
        yticklabels=labels,
        xlabel="预测标签",
        ylabel="真实标签",
        title=title,
    )

    threshold = conf_matrix.max() / 2 if conf_matrix.size else 0
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            color = "white" if conf_matrix[i, j] > threshold else "black"
            ax.text(
                j,
                i,
                int(conf_matrix[i, j]),
                ha="center",
                va="center",
                color=color,
                fontsize=11,
                fontweight="bold",
            )

    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def plot_2d_decision_boundary(
    model: Any,
    X_2d: np.ndarray,
    y: np.ndarray,
    feature_names: list[str] | np.ndarray,
    target_names: list[str] | np.ndarray,
    title: str,
    output_path: str | Path,
    support_vectors: np.ndarray | None = None,
) -> None:
    configure_matplotlib()
    x_min, x_max = X_2d[:, 0].min() - 0.6, X_2d[:, 0].max() + 0.6
    y_min, y_max = X_2d[:, 1].min() - 0.6, X_2d[:, 1].max() + 0.6
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 500),
        np.linspace(y_min, y_max, 500),
    )
    grid = np.c_[xx.ravel(), yy.ravel()]
    zz = model.predict(grid).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.contourf(xx, yy, zz, alpha=0.25, cmap="Set2")

    for class_id, class_name in enumerate(target_names):
        mask = y == class_id
        ax.scatter(
            X_2d[mask, 0],
            X_2d[mask, 1],
            label=str(class_name),
            edgecolor="white",
            linewidth=0.7,
            s=48,
        )

    if support_vectors is not None and len(support_vectors) > 0:
        ax.scatter(
            support_vectors[:, 0],
            support_vectors[:, 1],
            s=130,
            facecolors="none",
            edgecolors="black",
            linewidths=1.3,
            label="支持向量",
        )

    ax.set_xlabel(str(feature_names[0]))
    ax.set_ylabel(str(feature_names[1]))
    ax.set_title(title, fontweight="bold")
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def plot_metric_bars(
    values: dict[str, float],
    title: str,
    ylabel: str,
    output_path: str | Path,
    ylim: tuple[float, float] | None = None,
) -> None:
    configure_matplotlib()
    fig, ax = plt.subplots(figsize=(7.5, 5))
    names = list(values.keys())
    scores = [values[name] for name in names]
    bars = ax.bar(names, scores, color=["#4C78A8", "#F58518", "#54A24B", "#E45756"])
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel(ylabel)
    if ylim is not None:
        ax.set_ylim(*ylim)
    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{score:.4f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def save_json(data: dict[str, Any], output_path: str | Path) -> None:
    with Path(output_path).open("w", encoding="utf-8") as file:
        json.dump(_to_builtin(data), file, ensure_ascii=False, indent=2)
    print(f"结果已保存: {output_path}")


def _to_builtin(value: Any) -> Any:
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, dict):
        return {str(key): _to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_builtin(item) for item in value]
    return value
