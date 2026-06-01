from __future__ import annotations

import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "STHeiti"]
matplotlib.rcParams["axes.unicode_minus"] = False

PACKAGE_DIR = Path(__file__).resolve().parent


def load_menu_orders(filepath: str | Path) -> list[list[object]]:
    """Load menu order rows as transaction lists."""
    df = pd.read_excel(filepath, header=None)
    transactions = []
    for _, row in df.iterrows():
        transaction = [item for item in row if pd.notna(item)]
        transactions.append(transaction)
    return transactions


def association_analysis(
    transactions: list[list[object]],
    output_dir: str | Path,
    min_support: float = 0.3,
    min_confidence: float = 0.6,
):
    """Mine frequent itemsets and association rules with Apriori."""
    output_dir = Path(output_dir)

    print("=" * 60)
    print("第一部分：关联分析（Apriori 算法）")
    print("=" * 60)

    print("\n[1] 数据预处理：转换为 0-1 矩阵")
    te = TransactionEncoder()
    te_array = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_array, columns=te.columns_)
    print(f"转换后的 0-1 矩阵（共 {len(df_encoded)} 条事务，{len(te.columns_)} 个菜品）：")
    print(df_encoded.astype(int))

    df_encoded.astype(int).to_csv(output_dir / "menu_transactions_onehot.csv", index=False)

    print(f"\n[2] 挖掘频繁项集（最小支持度 = {min_support}）")
    frequent_itemsets = apriori(df_encoded, min_support=min_support, use_colnames=True)
    frequent_itemsets["length"] = frequent_itemsets["itemsets"].apply(len)
    print(frequent_itemsets)

    frequent_itemsets_out = frequent_itemsets.copy()
    frequent_itemsets_out["itemsets"] = frequent_itemsets_out["itemsets"].apply(lambda x: ", ".join(x))
    frequent_itemsets_out.to_csv(output_dir / "frequent_itemsets.csv", index=False)

    print(f"\n[3] 生成关联规则（最小置信度 = {min_confidence}）")
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules = rules[["antecedents", "consequents", "support", "confidence", "lift"]]
    rules = rules.sort_values("lift", ascending=False)

    rules_display = rules.copy()
    rules_display["antecedents"] = rules_display["antecedents"].apply(lambda x: ", ".join(x))
    rules_display["consequents"] = rules_display["consequents"].apply(lambda x: ", ".join(x))
    print(rules_display.to_string(index=False))

    rules_display.to_csv(output_dir / "association_rules.csv", index=False)

    print("\n[4] 关联规则解读与业务价值分析")
    print("-" * 60)
    for _, row in rules.iterrows():
        ant = ", ".join(row["antecedents"])
        con = ", ".join(row["consequents"])
        print(f"规则：{ant} → {con}")
        print(f"  支持度 = {row['support']:.3f}，置信度 = {row['confidence']:.3f}，提升度 = {row['lift']:.3f}")
        if row["lift"] > 1:
            print(f"  → 正相关：购买 {ant} 的顾客倾向于同时购买 {con}")
        elif row["lift"] < 1:
            print(f"  → 负相关：购买 {ant} 的顾客不太倾向于同时购买 {con}")
        else:
            print(f"  → 独立：{ant} 和 {con} 之间没有关联")
        print()

    return df_encoded, frequent_itemsets, rules


def outlier_detection(
    filepath: str | Path,
    output_dir: str | Path,
    n_clusters: int = 3,
    outlier_threshold: float = 2.0,
):
    """Detect outliers with K-Means distances on RFM features."""
    output_dir = Path(output_dir)

    print("\n" + "=" * 60)
    print("第二部分：离群点检测（K-Means 聚类）")
    print("=" * 60)

    print("\n[1] 加载消费数据")
    df = pd.read_excel(filepath)
    print(f"数据集大小：{df.shape[0]} 行 × {df.shape[1]} 列")
    print(f"字段：{', '.join(df.columns)}")
    print("\n数据前 5 行：")
    print(df.head())

    print("\n[2] 数据标准化处理")
    features = ["R", "F", "M"]
    x = df[features].values
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)
    df_scaled = pd.DataFrame(x_scaled, columns=features)
    print("标准化后的数据统计：")
    print(df_scaled.describe().round(3))

    print(f"\n[3] K-Means 聚类（K = {n_clusters}）")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(x_scaled)
    print("聚类中心（标准化空间）：")
    centers_df = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    print(centers_df.round(3))

    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    centers_original_df = pd.DataFrame(centers_original, columns=features)
    print("\n聚类中心（原始尺度）：")
    print(centers_original_df.round(2))

    print("\n各簇样本数量：")
    cluster_counts = df["Cluster"].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  簇 {cluster_id}: {count} 个样本 ({count / len(df) * 100:.1f}%)")

    print("\n[4] 计算各样本到所属聚类中心的相对距离")
    distances = []
    for i in range(len(x_scaled)):
        cluster_id = int(df.iloc[i]["Cluster"])
        center = kmeans.cluster_centers_[cluster_id]
        dist = np.sqrt(np.sum((x_scaled[i] - center) ** 2))
        distances.append(dist)
    df["Distance"] = distances

    print("距离统计：")
    print(f"  平均距离: {df['Distance'].mean():.4f}")
    print(f"  标准差: {df['Distance'].std():.4f}")
    print(f"  最大距离: {df['Distance'].max():.4f}")

    print(f"\n[5] 离群点检测（阈值 = 均值 + {outlier_threshold} × 标准差）")
    threshold = df["Distance"].mean() + outlier_threshold * df["Distance"].std()
    df["Is_Outlier"] = df["Distance"] > threshold
    outlier_count = df["Is_Outlier"].sum()
    print(f"阈值: {threshold:.4f}")
    print(f"检测到 {outlier_count} 个离群点 ({outlier_count / len(df) * 100:.1f}%)")

    print("\n[6] 离群点特征分析")
    outliers = df[df["Is_Outlier"]]
    normal = df[~df["Is_Outlier"]]
    print("离群点统计：")
    print(f"  R（最近消费）: 均值={outliers['R'].mean():.2f} (正常={normal['R'].mean():.2f})")
    print(f"  F（消费频率）: 均值={outliers['F'].mean():.2f} (正常={normal['F'].mean():.2f})")
    print(f"  M（消费金额）: 均值={outliers['M'].mean():.2f} (正常={normal['M'].mean():.2f})")

    print("\n离群点的业务含义：")
    for _, row in outliers.head(5).iterrows():
        print(f"  ID={int(row['ID'])}: R={row['R']}, F={row['F']}, M={row['M']:.2f}, 距离={row['Distance']:.4f}")

    print("\n[7] 生成可视化图表")
    visualize_clusters(df, features, threshold, output_dir)

    df.to_csv(output_dir / "clustered_consumption_data.csv", index=False)
    centers_original_df.to_csv(output_dir / "cluster_centers_original_scale.csv", index=False)
    centers_df.to_csv(output_dir / "cluster_centers_standardized.csv", index=False)
    cluster_counts.to_csv(output_dir / "cluster_counts.csv", header=["count"])

    summary = {
        "n_samples": len(df),
        "n_clusters": n_clusters,
        "outlier_threshold_multiplier": outlier_threshold,
        "outlier_threshold_value": float(threshold),
        "n_outliers": int(outlier_count),
        "outlier_percentage": float(outlier_count / len(df) * 100),
        "cluster_sizes": cluster_counts.to_dict(),
        "cluster_centers_original": centers_original_df.round(2).to_dict(orient="records"),
    }
    with (output_dir / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return df, kmeans, scaler


def visualize_clusters(df: pd.DataFrame, features: list[str], threshold: float, output_dir: str | Path) -> None:
    """Visualize cluster assignments and detected outliers."""
    output_dir = Path(output_dir)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    ax1 = axes[0, 0]
    colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336"]
    for cluster_id in sorted(df["Cluster"].unique()):
        mask = df["Cluster"] == cluster_id
        ax1.scatter(
            df.loc[mask, "R"],
            df.loc[mask, "M"],
            c=colors[cluster_id % len(colors)],
            label=f"簇 {cluster_id}",
            alpha=0.6,
            s=30,
        )
    outliers = df[df["Is_Outlier"]]
    ax1.scatter(outliers["R"], outliers["M"], c="red", marker="x", s=100, linewidths=2, label="离群点", zorder=5)
    ax1.set_xlabel("R (最近消费天数)")
    ax1.set_ylabel("M (消费金额)")
    ax1.set_title("聚类结果 (R vs M)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = axes[0, 1]
    for cluster_id in sorted(df["Cluster"].unique()):
        mask = df["Cluster"] == cluster_id
        ax2.scatter(
            df.loc[mask, "F"],
            df.loc[mask, "M"],
            c=colors[cluster_id % len(colors)],
            label=f"簇 {cluster_id}",
            alpha=0.6,
            s=30,
        )
    ax2.scatter(outliers["F"], outliers["M"], c="red", marker="x", s=100, linewidths=2, label="离群点", zorder=5)
    ax2.set_xlabel("F (消费频率)")
    ax2.set_ylabel("M (消费金额)")
    ax2.set_title("聚类结果 (F vs M)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = axes[1, 0]
    ax3.hist(df["Distance"], bins=50, color="steelblue", edgecolor="white", alpha=0.7)
    ax3.axvline(threshold, color="red", linestyle="--", linewidth=2, label=f"阈值={threshold:.2f}")
    ax3.set_xlabel("到聚类中心的距离")
    ax3.set_ylabel("样本数量")
    ax3.set_title("距离分布与离群点阈值")
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    axes[1, 1].remove()
    ax4 = fig.add_subplot(2, 2, 4, projection="3d")
    for cluster_id in sorted(df["Cluster"].unique()):
        mask = df["Cluster"] == cluster_id
        ax4.scatter(
            df.loc[mask, "R"],
            df.loc[mask, "F"],
            df.loc[mask, "M"],
            c=colors[cluster_id % len(colors)],
            label=f"簇 {cluster_id}",
            alpha=0.6,
            s=30,
        )
    ax4.scatter(outliers["R"], outliers["F"], outliers["M"], c="red", marker="x", s=100, linewidths=2, label="离群点", zorder=5)
    ax4.set_xlabel("R")
    ax4.set_ylabel("F")
    ax4.set_zlabel("M")
    ax4.set_title("3D 聚类可视化")
    ax4.legend()

    plt.tight_layout()
    plt.savefig(output_dir / "kmeans_tsne.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"图表已保存至 {output_dir / 'kmeans_tsne.png'}")


def run_experiment(
    data_dir: str | Path | None = None,
    output_dir: str | Path | None = None,
    min_support: float = 0.3,
    min_confidence: float = 0.6,
    n_clusters: int = 3,
    outlier_threshold: float = 2.0,
) -> None:
    """Run the complete lab workflow."""
    data_dir = Path(data_dir) if data_dir is not None else PACKAGE_DIR / "data"
    output_dir = Path(output_dir) if output_dir is not None else PACKAGE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "★" * 60)
    print("数据挖掘实验4：关联分析与离群点检测")
    print("★" * 60)

    transactions = load_menu_orders(data_dir / "menu_orders.xls")
    print(f"\n菜品订单数据：共 {len(transactions)} 条事务")
    for i, transaction in enumerate(transactions[:5]):
        print(f"  事务 {i + 1}: {transaction}")
    print("  ...")

    association_analysis(
        transactions,
        output_dir=output_dir,
        min_support=min_support,
        min_confidence=min_confidence,
    )

    outlier_detection(
        data_dir / "consumption_data.xls",
        output_dir=output_dir,
        n_clusters=n_clusters,
        outlier_threshold=outlier_threshold,
    )

    print("\n" + "★" * 60)
    print(f"实验完成！所有结果已保存至 {output_dir}/ 目录")
    print("★" * 60)
