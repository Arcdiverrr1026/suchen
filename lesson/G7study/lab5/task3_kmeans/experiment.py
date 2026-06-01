"""任务3：K-Means 聚类（鸢尾花数据集）。"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score, calinski_harabasz_score, silhouette_score
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[4]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lesson.G7study.lab5.common import (  # noqa: E402
    RANDOM_STATE,
    configure_matplotlib,
    print_dataset_summary,
    print_section,
    save_json,
    task_output_dir,
)

import matplotlib.pyplot as plt  # noqa: E402


def load_data() -> tuple[np.ndarray, np.ndarray, object]:
    iris = load_iris()
    X = iris.data
    y = iris.target
    print_dataset_summary(
        "鸢尾花数据集 Iris（聚类训练不使用标签）",
        X,
        y,
        iris.feature_names,
        iris.target_names,
    )
    return X, y, iris


def evaluate_k_values(
    X_scaled: np.ndarray,
    true_labels: np.ndarray,
    output_dir: Path,
) -> tuple[pd.DataFrame, dict[int, KMeans], dict[int, np.ndarray]]:
    print_section("K-Means 聚类训练与评估：K=2, 3, 4")
    rows: list[dict[str, float | int]] = []
    models: dict[int, KMeans] = {}
    labels_by_k: dict[int, np.ndarray] = {}

    for k in [2, 3, 4]:
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10)
        labels = model.fit_predict(X_scaled)
        silhouette = silhouette_score(X_scaled, labels)
        ch_score = calinski_harabasz_score(X_scaled, labels)
        ari = adjusted_rand_score(true_labels, labels)
        rows.append(
            {
                "K": k,
                "silhouette_score": silhouette,
                "calinski_harabasz_score": ch_score,
                "adjusted_rand_index_vs_true_label": ari,
            }
        )
        models[k] = model
        labels_by_k[k] = labels
        print(
            f"K={k}: 轮廓系数={silhouette:.4f}, "
            f"Calinski-Harabasz={ch_score:.2f}, ARI={ari:.4f}"
        )

    metrics = pd.DataFrame(rows)
    metrics.to_csv(
        output_dir / "task3_kmeans_metrics.csv",
        index=False,
        encoding="utf-8-sig",
    )
    return metrics, models, labels_by_k


def plot_metrics(metrics: pd.DataFrame, output_dir: Path) -> None:
    configure_matplotlib()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(
        metrics["K"],
        metrics["silhouette_score"],
        marker="o",
        linewidth=2,
        color="#4C78A8",
    )
    axes[0].set_xticks(metrics["K"])
    axes[0].set_xlabel("K")
    axes[0].set_ylabel("轮廓系数")
    axes[0].set_title("不同 K 值的轮廓系数", fontweight="bold")

    axes[1].plot(
        metrics["K"],
        metrics["calinski_harabasz_score"],
        marker="o",
        linewidth=2,
        color="#F58518",
    )
    axes[1].set_xticks(metrics["K"])
    axes[1].set_xlabel("K")
    axes[1].set_ylabel("Calinski-Harabasz 指数")
    axes[1].set_title("不同 K 值的 CH 指数", fontweight="bold")

    fig.tight_layout()
    output_path = output_dir / "task3_kmeans_metric_comparison.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def plot_cluster_results(
    X: np.ndarray,
    X_scaled: np.ndarray,
    y_true: np.ndarray,
    iris: object,
    scaler: StandardScaler,
    models: dict[int, KMeans],
    labels_by_k: dict[int, np.ndarray],
    output_dir: Path,
) -> None:
    configure_matplotlib()
    feature_indices = [2, 3]
    feature_names = [iris.feature_names[index] for index in feature_indices]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    for ax, k in zip(axes, [2, 3, 4]):
        labels = labels_by_k[k]
        scatter = ax.scatter(
            X[:, feature_indices[0]],
            X[:, feature_indices[1]],
            c=labels,
            cmap="Set2",
            s=48,
            edgecolor="white",
            linewidth=0.6,
        )
        centers_raw = scaler.inverse_transform(models[k].cluster_centers_)
        ax.scatter(
            centers_raw[:, feature_indices[0]],
            centers_raw[:, feature_indices[1]],
            c="black",
            marker="*",
            s=220,
            label="簇中心",
        )
        ax.set_title(f"K={k} 聚类结果", fontweight="bold")
        ax.set_xlabel(feature_names[0])
        ax.set_ylabel(feature_names[1])
        cluster_legend = ax.legend(*scatter.legend_elements(), title="簇", loc="lower right")
        ax.add_artist(cluster_legend)
        ax.legend(loc="upper left")

    fig.tight_layout()
    output_path = output_dir / "task3_kmeans_cluster_results.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")

    fig2, ax2 = plt.subplots(figsize=(7, 5.5))
    for class_id, class_name in enumerate(iris.target_names):
        mask = y_true == class_id
        ax2.scatter(
            X[mask, feature_indices[0]],
            X[mask, feature_indices[1]],
            label=class_name,
            s=48,
            edgecolor="white",
            linewidth=0.6,
        )
    ax2.set_xlabel(feature_names[0])
    ax2.set_ylabel(feature_names[1])
    ax2.set_title("鸢尾花真实类别分布（仅用于结果对比）", fontweight="bold")
    ax2.legend()
    fig2.tight_layout()
    output_path = output_dir / "task3_iris_true_labels.png"
    fig2.savefig(output_path, bbox_inches="tight")
    plt.close(fig2)
    print(f"图表已保存: {output_path}")

    cluster_assignments = pd.DataFrame(
        {
            "true_label": y_true,
            "true_class": [iris.target_names[index] for index in y_true],
            "cluster_K2": labels_by_k[2],
            "cluster_K3": labels_by_k[3],
            "cluster_K4": labels_by_k[4],
        }
    )
    cluster_assignments.to_csv(
        output_dir / "task3_kmeans_cluster_assignments.csv",
        index=False,
        encoding="utf-8-sig",
    )


def run_experiment() -> dict[str, float]:
    print_section("任务3：K-Means 聚类（鸢尾花数据集）")
    output_dir = task_output_dir(__file__)

    X, y_true, iris = load_data()

    print_section("数据预处理：StandardScaler 标准化")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("标准化后各特征均值约为 0，标准差约为 1。")

    metrics, models, labels_by_k = evaluate_k_values(X_scaled, y_true, output_dir)
    plot_metrics(metrics, output_dir)
    plot_cluster_results(
        X,
        X_scaled,
        y_true,
        iris,
        scaler,
        models,
        labels_by_k,
        output_dir,
    )

    best_row = metrics.sort_values("silhouette_score", ascending=False).iloc[0]
    save_json(
        {
            "task": "kmeans_iris",
            "best_k_by_silhouette": int(best_row["K"]),
            "best_silhouette_score": float(best_row["silhouette_score"]),
            "metrics": metrics.to_dict(orient="records"),
        },
        output_dir / "task3_kmeans_summary.json",
    )

    print_section("实验小结")
    print(
        f"按轮廓系数判断，本次最优 K 为 {int(best_row['K'])}，"
        f"轮廓系数为 {best_row['silhouette_score']:.4f}。"
    )
    print("K-Means 对近似球形簇较有效，但对簇形状和初始 K 值较敏感。")
    return {
        "best_k": float(best_row["K"]),
        "best_silhouette": float(best_row["silhouette_score"]),
    }


if __name__ == "__main__":
    run_experiment()
