"""任务2：高斯核 SVM 分类（乳腺癌数据集）。"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lesson.G7study.lab5.common import (  # noqa: E402
    RANDOM_STATE,
    TEST_SIZE,
    configure_matplotlib,
    evaluate_classifier,
    plot_confusion_matrix,
    plot_metric_bars,
    print_dataset_summary,
    print_section,
    save_json,
    task_output_dir,
)

import matplotlib.pyplot as plt  # noqa: E402


def load_data() -> tuple[np.ndarray, np.ndarray, object]:
    cancer = load_breast_cancer()
    X = cancer.data
    y = cancer.target
    print_dataset_summary(
        "乳腺癌二分类数据集 Breast Cancer Wisconsin",
        X,
        y,
        cancer.feature_names,
        cancer.target_names,
    )
    return X, y, cancer


def split_data(
    X: np.ndarray,
    y: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print_section("数据划分：训练集 80% / 测试集 20%")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    print(f"训练集: {X_train.shape[0]} 条")
    print(f"测试集: {X_test.shape[0]} 条")
    return X_train, X_test, y_train, y_test


def build_model(kernel: str = "rbf", C: float = 1.0, gamma: str | float = "scale") -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "svm",
                SVC(
                    kernel=kernel,
                    C=C,
                    gamma=gamma,
                    random_state=RANDOM_STATE,
                ),
            ),
        ]
    )


def parameter_comparison(
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    output_dir: Path,
) -> pd.DataFrame:
    print_section("参数对比实验：C 与 gamma")
    c_values = [0.1, 1.0, 10.0, 100.0]
    gamma_values: list[str | float] = ["scale", 0.001, 0.01, 0.1]
    rows: list[dict[str, float | str]] = []

    for C in c_values:
        for gamma in gamma_values:
            model = build_model(kernel="rbf", C=C, gamma=gamma)
            model.fit(X_train, y_train)
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)
            rows.append(
                {
                    "C": C,
                    "gamma": str(gamma),
                    "train_accuracy": float(np.mean(train_pred == y_train)),
                    "test_accuracy": float(np.mean(test_pred == y_test)),
                    "test_f1_weighted": float(
                        f1_score(y_test, test_pred, average="weighted")
                    ),
                }
            )

    comparison = pd.DataFrame(rows)
    comparison.to_csv(
        output_dir / "task2_rbf_svm_parameter_comparison.csv",
        index=False,
        encoding="utf-8-sig",
    )
    print(comparison.round(4).to_string(index=False))

    plot_parameter_comparison(comparison, output_dir)
    return comparison


def plot_parameter_comparison(comparison: pd.DataFrame, output_dir: Path) -> None:
    configure_matplotlib()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for gamma, group in comparison.groupby("gamma", sort=False):
        group = group.sort_values("C")
        axes[0].plot(
            group["C"],
            group["test_accuracy"],
            marker="o",
            linewidth=2,
            label=f"gamma={gamma}",
        )
        axes[1].plot(
            group["C"],
            group["train_accuracy"] - group["test_accuracy"],
            marker="o",
            linewidth=2,
            label=f"gamma={gamma}",
        )

    axes[0].set_xscale("log")
    axes[0].set_ylim(0.85, 1.01)
    axes[0].set_xlabel("C（对数坐标）")
    axes[0].set_ylabel("测试集准确率")
    axes[0].set_title("RBF SVM 参数对准确率的影响", fontweight="bold")
    axes[0].legend()

    axes[1].set_xscale("log")
    axes[1].axhline(0, color="black", linewidth=0.8)
    axes[1].set_xlabel("C（对数坐标）")
    axes[1].set_ylabel("训练-测试准确率差值")
    axes[1].set_title("过拟合趋势观察", fontweight="bold")
    axes[1].legend()

    fig.tight_layout()
    output_path = output_dir / "task2_rbf_svm_parameter_comparison.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def run_experiment() -> dict[str, float]:
    print_section("任务2：高斯核 SVM 分类（乳腺癌数据集）")
    output_dir = task_output_dir(__file__)

    X, y, cancer = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    print_section("模型构建与训练：SVC(kernel='rbf')")
    rbf_model = build_model(kernel="rbf", C=1.0, gamma="scale")
    rbf_model.fit(X_train, y_train)
    print("模型参数:")
    print("  kernel = rbf")
    print("  C = 1.0")
    print("  gamma = scale")
    print("  特征处理 = StandardScaler")

    print_section("模型预测与评估")
    rbf_result = evaluate_classifier(rbf_model, X_test, y_test, cancer.target_names)
    plot_confusion_matrix(
        rbf_result["confusion_matrix"],
        cancer.target_names,
        f"RBF SVM 混淆矩阵 (Accuracy={rbf_result['accuracy']:.4f})",
        output_dir / "task2_rbf_svm_confusion_matrix.png",
    )

    print_section("与线性核 SVM 对比")
    linear_model = build_model(kernel="linear", C=1.0, gamma="scale")
    linear_model.fit(X_train, y_train)
    linear_result = evaluate_classifier(
        linear_model,
        X_test,
        y_test,
        cancer.target_names,
    )
    plot_metric_bars(
        {
            "Linear SVM": linear_result["accuracy"],
            "RBF SVM": rbf_result["accuracy"],
        },
        "乳腺癌分类：线性核与 RBF 核准确率对比",
        "Accuracy",
        output_dir / "task2_kernel_accuracy_comparison.png",
        ylim=(0.9, 1.0),
    )

    comparison = parameter_comparison(X_train, X_test, y_train, y_test, output_dir)
    best_row = comparison.sort_values("test_accuracy", ascending=False).iloc[0]
    save_json(
        {
            "task": "rbf_svm_breast_cancer",
            "rbf_accuracy": rbf_result["accuracy"],
            "rbf_f1_weighted": rbf_result["f1"],
            "linear_accuracy": linear_result["accuracy"],
            "linear_f1_weighted": linear_result["f1"],
            "best_parameter_row": best_row.to_dict(),
            "confusion_matrix": rbf_result["confusion_matrix"],
            "classification_report": rbf_result["classification_report"],
        },
        output_dir / "task2_rbf_svm_metrics.json",
    )

    print_section("实验小结")
    print(f"RBF 核 SVM 在测试集上的准确率为 {rbf_result['accuracy']:.4f}。")
    print(
        "C 增大通常会增强模型对训练集的拟合能力；gamma 过大时，模型更容易产生过拟合。"
    )
    return {"accuracy": rbf_result["accuracy"], "f1": rbf_result["f1"]}


if __name__ == "__main__":
    run_experiment()
