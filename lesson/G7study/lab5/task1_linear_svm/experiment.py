"""任务1：线性核 SVM 分类（鸢尾花数据集）。"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
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
    evaluate_classifier,
    plot_2d_decision_boundary,
    plot_confusion_matrix,
    print_dataset_summary,
    print_section,
    save_json,
    task_output_dir,
)


def load_data() -> tuple[np.ndarray, np.ndarray, object]:
    iris = load_iris()
    X = iris.data
    y = iris.target
    print_dataset_summary(
        "鸢尾花数据集 Iris",
        X,
        y,
        iris.feature_names,
        iris.target_names,
    )
    return X, y, iris


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


def build_model(C: float = 1.0) -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "svm",
                SVC(kernel="linear", C=C, random_state=RANDOM_STATE),
            ),
        ]
    )


def visualize_decision_boundary(
    X: np.ndarray,
    y: np.ndarray,
    iris: object,
    output_dir: Path,
) -> None:
    print_section("二维特征决策边界可视化")
    feature_indices = [2, 3]
    X_2d = X[:, feature_indices]
    feature_names = [iris.feature_names[index] for index in feature_indices]

    visual_model = build_model(C=1.0)
    visual_model.fit(X_2d, y)

    scaler = visual_model.named_steps["scaler"]
    svm = visual_model.named_steps["svm"]
    support_vectors = scaler.inverse_transform(svm.support_vectors_)

    plot_2d_decision_boundary(
        visual_model,
        X_2d,
        y,
        feature_names,
        iris.target_names,
        "线性核 SVM 决策边界（花瓣长度 / 花瓣宽度）",
        output_dir / "task1_linear_svm_decision_boundary.png",
        support_vectors=support_vectors,
    )


def run_experiment() -> dict[str, float]:
    print_section("任务1：线性核 SVM 分类（鸢尾花数据集）")
    output_dir = task_output_dir(__file__)

    X, y, iris = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)

    print_section("模型构建与训练：SVC(kernel='linear')")
    model = build_model(C=1.0)
    model.fit(X_train, y_train)
    print("模型参数:")
    print("  kernel = linear")
    print("  C = 1.0")
    print("  特征处理 = StandardScaler")

    print_section("模型预测与评估")
    result = evaluate_classifier(model, X_test, y_test, iris.target_names)
    plot_confusion_matrix(
        result["confusion_matrix"],
        iris.target_names,
        f"线性核 SVM 混淆矩阵 (Accuracy={result['accuracy']:.4f})",
        output_dir / "task1_linear_svm_confusion_matrix.png",
    )
    visualize_decision_boundary(X, y, iris, output_dir)

    predictions = pd.DataFrame(
        {
            "真实标签": y_test,
            "预测标签": result["y_pred"],
            "真实类别": [iris.target_names[index] for index in y_test],
            "预测类别": [iris.target_names[index] for index in result["y_pred"]],
        }
    )
    predictions.to_csv(
        output_dir / "task1_linear_svm_predictions.csv",
        index=False,
        encoding="utf-8-sig",
    )
    save_json(
        {
            "task": "linear_svm_iris",
            "accuracy": result["accuracy"],
            "f1_weighted": result["f1"],
            "confusion_matrix": result["confusion_matrix"],
            "classification_report": result["classification_report"],
        },
        output_dir / "task1_linear_svm_metrics.json",
    )

    print_section("实验小结")
    print(f"线性核 SVM 在测试集上的准确率为 {result['accuracy']:.4f}。")
    print("花瓣长度与花瓣宽度能够较清晰地区分鸢尾花类别，支持向量位于类别边界附近。")
    return {"accuracy": result["accuracy"], "f1": result["f1"]}


if __name__ == "__main__":
    run_experiment()
