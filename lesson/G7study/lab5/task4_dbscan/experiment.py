"""任务4：DBSCAN 密度聚类（鸢尾花数据集）。"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import adjusted_rand_score, silhouette_score
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
        "鸢尾花数据集 Iris（DBSCAN 聚类训练不使用标签）",
        X,
        y,
        iris.feature_names,
        iris.target_names,
    )
    return X, y, iris


def run_parameter_grid(
    X_scaled: np.ndarray,
    true_labels: np.ndarray,
    output_dir: Path,
) -> pd.DataFrame:
    print_section("DBSCAN 参数对比：eps 与 min_samples")
    eps_values = [0.3, 0.5, 0.6, 0.7, 0.8, 1.0]
    min_samples_values = [3, 5, 8]
    rows: list[dict[str, float | int | None]] = []

    for eps in eps_values:
        for min_samples in min_samples_values:
            model = DBSCAN(eps=eps, min_samples=min_samples)
            labels = model.fit_predict(X_scaled)
            cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
            noise_count = int(np.sum(labels == -1))
            silhouette = _safe_silhouette(X_scaled, labels)
            ari = adjusted_rand_score(true_labels, labels)
            rows.append(
                {
                    "eps": eps,
                    "min_samples": min_samples,
                    "cluster_count": cluster_count,
                    "noise_count": noise_count,
                    "silhouette_score": silhouette,
                    "adjusted_rand_index_vs_true_label": ari,
                }
            )
            silhouette_text = "N/A" if silhouette is None else f"{silhouette:.4f}"
            print(
                f"eps={eps:.1f}, min_samples={min_samples}: "
                f"簇数={cluster_count}, 噪声点={noise_count}, "
                f"轮廓系数={silhouette_text}, ARI={ari:.4f}"
            )

    grid = pd.DataFrame(rows)
    grid.to_csv(
        output_dir / "task4_dbscan_parameter_grid.csv",
        index=False,
        encoding="utf-8-sig",
    )
    return grid


def _safe_silhouette(X_scaled: np.ndarray, labels: np.ndarray) -> float | None:
    non_noise = labels != -1
    usable_labels = labels[non_noise]
    if len(np.unique(usable_labels)) < 2:
        return None
    if np.sum(non_noise) <= len(np.unique(usable_labels)):
        return None
    return float(silhouette_score(X_scaled[non_noise], usable_labels))


def select_best_params(grid: pd.DataFrame) -> tuple[float, int]:
    valid = grid.dropna(subset=["silhouette_score"]).copy()
    if valid.empty:
        return 0.6, 5

    valid["noise_ratio"] = valid["noise_count"] / 150
    valid["score"] = valid["silhouette_score"] - valid["noise_ratio"] * 0.15
    best = valid.sort_values(["score", "cluster_count"], ascending=[False, False]).iloc[0]
    return float(best["eps"]), int(best["min_samples"])


def fit_dbscan(X_scaled: np.ndarray, eps: float, min_samples: int) -> np.ndarray:
    model = DBSCAN(eps=eps, min_samples=min_samples)
    return model.fit_predict(X_scaled)


def summarize_labels(labels: np.ndarray) -> dict[str, int]:
    cluster_count = len(set(labels)) - (1 if -1 in labels else 0)
    noise_count = int(np.sum(labels == -1))
    return {"cluster_count": cluster_count, "noise_count": noise_count}


def plot_dbscan_results(
    X: np.ndarray,
    y_true: np.ndarray,
    dbscan_labels: np.ndarray,
    kmeans_labels: np.ndarray,
    iris: object,
    output_dir: Path,
) -> None:
    configure_matplotlib()
    feature_indices = [2, 3]
    feature_names = [iris.feature_names[index] for index in feature_indices]

    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    _scatter_labels(
        axes[0],
        X,
        dbscan_labels,
        feature_indices,
        feature_names,
        "DBSCAN 聚类结果（-1 为噪声）",
        mark_noise=True,
    )
    _scatter_labels(
        axes[1],
        X,
        kmeans_labels,
        feature_indices,
        feature_names,
        "K-Means 聚类结果（K=3）",
    )

    for class_id, class_name in enumerate(iris.target_names):
        mask = y_true == class_id
        axes[2].scatter(
            X[mask, feature_indices[0]],
            X[mask, feature_indices[1]],
            label=str(class_name),
            s=48,
            edgecolor="white",
            linewidth=0.6,
        )
    axes[2].set_title("真实类别分布（仅用于对比）", fontweight="bold")
    axes[2].set_xlabel(feature_names[0])
    axes[2].set_ylabel(feature_names[1])
    axes[2].legend(loc="best")

    fig.tight_layout()
    output_path = output_dir / "task4_dbscan_vs_kmeans_true_labels.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def _scatter_labels(
    ax: plt.Axes,
    X: np.ndarray,
    labels: np.ndarray,
    feature_indices: list[int],
    feature_names: list[str],
    title: str,
    mark_noise: bool = False,
) -> None:
    unique_labels = sorted(set(labels))
    colors = plt.cm.Set2(np.linspace(0, 1, max(len(unique_labels), 2)))

    for color, label in zip(colors, unique_labels):
        mask = labels == label
        if mark_noise and label == -1:
            ax.scatter(
                X[mask, feature_indices[0]],
                X[mask, feature_indices[1]],
                c="black",
                marker="x",
                s=58,
                label="噪声点",
            )
        else:
            ax.scatter(
                X[mask, feature_indices[0]],
                X[mask, feature_indices[1]],
                color=color,
                edgecolor="white",
                linewidth=0.6,
                s=48,
                label=f"簇 {label}",
            )

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel(feature_names[0])
    ax.set_ylabel(feature_names[1])
    ax.legend(loc="best")


def plot_parameter_grid(grid: pd.DataFrame, output_dir: Path) -> None:
    configure_matplotlib()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    for min_samples, group in grid.groupby("min_samples"):
        group = group.sort_values("eps")
        axes[0].plot(
            group["eps"],
            group["cluster_count"],
            marker="o",
            linewidth=2,
            label=f"min_samples={min_samples}",
        )
        axes[1].plot(
            group["eps"],
            group["noise_count"],
            marker="o",
            linewidth=2,
            label=f"min_samples={min_samples}",
        )

    axes[0].set_xlabel("eps")
    axes[0].set_ylabel("簇数量")
    axes[0].set_title("eps 对簇数量的影响", fontweight="bold")
    axes[0].legend()

    axes[1].set_xlabel("eps")
    axes[1].set_ylabel("噪声点数量")
    axes[1].set_title("eps 对噪声点数量的影响", fontweight="bold")
    axes[1].legend()

    fig.tight_layout()
    output_path = output_dir / "task4_dbscan_parameter_effect.png"
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"图表已保存: {output_path}")


def run_experiment() -> dict[str, float]:
    print_section("任务4：DBSCAN 密度聚类（鸢尾花数据集）")
    output_dir = task_output_dir(__file__)

    X, y_true, iris = load_data()

    print_section("数据预处理：StandardScaler 标准化")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print("标准化完成。")

    grid = run_parameter_grid(X_scaled, y_true, output_dir)
    plot_parameter_grid(grid, output_dir)
    eps, min_samples = select_best_params(grid)

    print_section("最终 DBSCAN 模型")
    dbscan_labels = fit_dbscan(X_scaled, eps=eps, min_samples=min_samples)
    summary = summarize_labels(dbscan_labels)
    silhouette = _safe_silhouette(X_scaled, dbscan_labels)
    ari = adjusted_rand_score(y_true, dbscan_labels)
    print(f"选用参数: eps={eps}, min_samples={min_samples}")
    print(f"生成簇数量: {summary['cluster_count']}")
    print(f"噪声点数量: {summary['noise_count']}")
    print(f"轮廓系数: {'N/A' if silhouette is None else f'{silhouette:.4f}'}")
    print(f"与真实标签对比 ARI: {ari:.4f}")

    kmeans_labels = KMeans(n_clusters=3, random_state=RANDOM_STATE, n_init=10).fit_predict(
        X_scaled
    )
    plot_dbscan_results(X, y_true, dbscan_labels, kmeans_labels, iris, output_dir)

    assignments = pd.DataFrame(
        {
            "true_label": y_true,
            "true_class": [iris.target_names[index] for index in y_true],
            "dbscan_cluster": dbscan_labels,
            "kmeans_cluster_K3": kmeans_labels,
        }
    )
    assignments.to_csv(
        output_dir / "task4_dbscan_cluster_assignments.csv",
        index=False,
        encoding="utf-8-sig",
    )

    save_json(
        {
            "task": "dbscan_iris",
            "eps": eps,
            "min_samples": min_samples,
            "cluster_count": summary["cluster_count"],
            "noise_count": summary["noise_count"],
            "silhouette_score": silhouette,
            "adjusted_rand_index_vs_true_label": ari,
        },
        output_dir / "task4_dbscan_summary.json",
    )

    print_section("实验小结")
    print("DBSCAN 不需要预先指定簇数量，可以识别噪声点。")
    print("在鸢尾花这类较规则的小数据集上，K-Means 往往更稳定；DBSCAN 对 eps 参数更敏感。")
    return {
        "cluster_count": float(summary["cluster_count"]),
        "noise_count": float(summary["noise_count"]),
        "ari": float(ari),
    }


if __name__ == "__main__":
    run_experiment()
