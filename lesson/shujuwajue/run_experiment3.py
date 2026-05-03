from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path("/Users/arcdiverrr/python program/lesson hw/suchen/lesson/shujuwajue")
DATA_ROOT = Path("/Users/arcdiverrr/Downloads/20260428-数据挖掘实验课 /实验内容/data")
OUTPUT_ROOT = PROJECT_ROOT / "outputs"

CONSUMPTION_FILE = DATA_ROOT / "consumption_data.xls"
MENU_ORDERS_FILE = DATA_ROOT / "menu_orders.xls"


@dataclass
class ClusterArtifacts:
    clustered_data: pd.DataFrame
    centers_original: pd.DataFrame
    centers_standardized: pd.DataFrame
    cluster_counts: pd.DataFrame
    plot_path: Path


@dataclass
class AssociationArtifacts:
    transactions: list[list[str]]
    one_hot_matrix: pd.DataFrame
    frequent_itemsets: pd.DataFrame
    rules: pd.DataFrame
    selected_rules: pd.DataFrame


def ensure_output_dir() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def run_clustering() -> ClusterArtifacts:
    df = pd.read_excel(CONSUMPTION_FILE, sheet_name="Sheet1")
    features = ["R", "F", "M"]

    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[features])

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=20)
    df["cluster"] = kmeans.fit_predict(scaled)

    tsne = TSNE(
        n_components=2,
        perplexity=30,
        max_iter=1000,
        init="pca",
        learning_rate="auto",
        random_state=42,
    )
    embedding = tsne.fit_transform(scaled)
    df["tsne_1"] = embedding[:, 0]
    df["tsne_2"] = embedding[:, 1]

    centers_original = pd.DataFrame(
        scaler.inverse_transform(kmeans.cluster_centers_),
        columns=features,
    ).round(2)
    centers_original.index.name = "cluster"
    centers_original = centers_original.reset_index()

    centers_standardized = pd.DataFrame(
        kmeans.cluster_centers_,
        columns=features,
    ).round(4)
    centers_standardized.index.name = "cluster"
    centers_standardized = centers_standardized.reset_index()

    cluster_counts = (
        df["cluster"]
        .value_counts()
        .sort_index()
        .rename_axis("cluster")
        .reset_index(name="count")
    )

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(
        df["tsne_1"],
        df["tsne_2"],
        c=df["cluster"],
        cmap="tab10",
        s=24,
        alpha=0.85,
    )
    plt.title("K-Means Clusters Visualized by t-SNE")
    plt.xlabel("t-SNE 1")
    plt.ylabel("t-SNE 2")
    plt.legend(*scatter.legend_elements(), title="Cluster")
    plt.tight_layout()
    plot_path = OUTPUT_ROOT / "kmeans_tsne.png"
    plt.savefig(plot_path, dpi=200)
    plt.close()

    clustered_data = df[["ID", "R", "F", "M", "cluster", "tsne_1", "tsne_2"]]
    return ClusterArtifacts(
        clustered_data=clustered_data,
        centers_original=centers_original,
        centers_standardized=centers_standardized,
        cluster_counts=cluster_counts,
        plot_path=plot_path,
    )


def load_transactions() -> list[list[str]]:
    raw = pd.read_excel(MENU_ORDERS_FILE, header=None)
    transactions: list[list[str]] = []
    for _, row in raw.iterrows():
        items = [str(value).strip() for value in row.dropna() if str(value).strip()]
        if items:
            transactions.append(items)
    return transactions


def build_one_hot_matrix(transactions: list[list[str]]) -> pd.DataFrame:
    items = sorted({item for transaction in transactions for item in transaction})
    rows = []
    for transaction in transactions:
        transaction_set = set(transaction)
        rows.append({item: int(item in transaction_set) for item in items})
    return pd.DataFrame(rows)


def run_association_analysis() -> AssociationArtifacts:
    transactions = load_transactions()
    one_hot = build_one_hot_matrix(transactions)

    frequent_itemsets = apriori(one_hot.astype(bool), min_support=0.2, use_colnames=True)
    frequent_itemsets = frequent_itemsets.sort_values(
        by=["support", "itemsets"],
        ascending=[False, True],
    ).reset_index(drop=True)
    frequent_itemsets["itemset_size"] = frequent_itemsets["itemsets"].apply(len)
    frequent_itemsets["itemsets"] = frequent_itemsets["itemsets"].apply(
        lambda values: ", ".join(sorted(values))
    )

    rules = association_rules(
        apriori(one_hot.astype(bool), min_support=0.2, use_colnames=True),
        metric="confidence",
        min_threshold=0.6,
    )
    rules = rules.sort_values(
        by=["lift", "confidence", "support"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    display_rules = rules.copy()
    display_rules["antecedents"] = display_rules["antecedents"].apply(
        lambda values: ", ".join(sorted(values))
    )
    display_rules["consequents"] = display_rules["consequents"].apply(
        lambda values: ", ".join(sorted(values))
    )
    display_rules = display_rules[
        [
            "antecedents",
            "consequents",
            "support",
            "confidence",
            "lift",
            "leverage",
            "conviction",
        ]
    ].round(4)

    selected_rules = display_rules[
        (display_rules["lift"] > 1) & (display_rules["confidence"] >= 0.6)
    ].reset_index(drop=True)

    return AssociationArtifacts(
        transactions=transactions,
        one_hot_matrix=one_hot,
        frequent_itemsets=frequent_itemsets,
        rules=display_rules,
        selected_rules=selected_rules,
    )


def describe_clusters(centers: pd.DataFrame) -> dict[int, str]:
    descriptions: dict[int, str] = {}
    ordered = centers.set_index("cluster")
    high_frequency_cluster = int(ordered["F"].idxmax())
    inactive_cluster = int(ordered["R"].idxmax())
    for cluster, row in ordered.iterrows():
        cluster = int(cluster)
        if cluster == high_frequency_cluster:
            descriptions[int(cluster)] = "high-value frequent customers"
        elif cluster == inactive_cluster:
            descriptions[int(cluster)] = "inactive customers requiring reactivation"
        else:
            descriptions[int(cluster)] = "price-sensitive or low-value active customers"
    return descriptions


def save_outputs(cluster_artifacts: ClusterArtifacts, assoc_artifacts: AssociationArtifacts) -> None:
    cluster_artifacts.clustered_data.to_csv(OUTPUT_ROOT / "clustered_consumption_data.csv", index=False)
    cluster_artifacts.centers_original.to_csv(OUTPUT_ROOT / "cluster_centers_original_scale.csv", index=False)
    cluster_artifacts.centers_standardized.to_csv(OUTPUT_ROOT / "cluster_centers_standardized.csv", index=False)
    cluster_artifacts.cluster_counts.to_csv(OUTPUT_ROOT / "cluster_counts.csv", index=False)

    pd.DataFrame(
        {
            "transaction_id": list(range(1, len(assoc_artifacts.transactions) + 1)),
            "items": [" | ".join(items) for items in assoc_artifacts.transactions],
        }
    ).to_csv(OUTPUT_ROOT / "menu_transactions.csv", index=False)

    assoc_artifacts.one_hot_matrix.to_csv(OUTPUT_ROOT / "menu_transactions_onehot.csv", index=False)
    assoc_artifacts.frequent_itemsets.to_csv(OUTPUT_ROOT / "frequent_itemsets.csv", index=False)
    assoc_artifacts.rules.to_csv(OUTPUT_ROOT / "association_rules.csv", index=False)
    assoc_artifacts.selected_rules.to_csv(OUTPUT_ROOT / "selected_rules.csv", index=False)

'''
def write_markdown(cluster_artifacts: ClusterArtifacts, assoc_artifacts: AssociationArtifacts) -> None:
    cluster_descriptions = describe_clusters(cluster_artifacts.centers_original)
    centers_table = dataframe_to_markdown(cluster_artifacts.centers_original)
    counts_table = dataframe_to_markdown(cluster_artifacts.cluster_counts)
    itemsets_table = dataframe_to_markdown(assoc_artifacts.frequent_itemsets.head(10))

    if assoc_artifacts.selected_rules.empty:
        rules_table = "No rules met the business screening condition."
    else:
        rules_table = dataframe_to_markdown(assoc_artifacts.selected_rules)

    markdown = f"""# 实验3流程与结果

## 1. 实验目标
- 对消费数据进行标准化处理，并使用 K-Means 聚为 3 类。
- 输出聚类中心、类别数量，并使用 t-SNE 对聚类结果进行二维可视化。
- 将菜品订单数据整理为 0-1 事务矩阵，使用 Apriori 挖掘频繁项集与关联规则。
- 从结果中筛选具有业务价值的菜品搭配规则。

## 2. 项目结构
```text
shujuwajue/
├── .venv
├── outputs/
│   ├── association_rules.csv
│   ├── cluster_centers_original_scale.csv
│   ├── cluster_centers_standardized.csv
│   ├── cluster_counts.csv
│   ├── clustered_consumption_data.csv
│   ├── frequent_itemsets.csv
│   ├── kmeans_tsne.png
│   ├── menu_transactions.csv
│   ├── menu_transactions_onehot.csv
│   └── selected_rules.csv
├── run_experiment3.py
└── 实验流程.md
```

## 3. 环境准备
1. 创建项目目录：`/Users/arcdiverrr/python program/lesson hw/suchen/lesson/shujuwajue`
2. 创建虚拟环境：`python3 -m venv .venv`
3. 安装依赖：
   `./.venv/bin/python -m pip install pandas numpy scikit-learn mlxtend xlrd matplotlib openpyxl`

## 4. 数据说明
### 4.1 消费聚类数据
- 文件：`consumption_data.xls`
- 有效工作表：`Sheet1`
- 字段：`ID, R, F, M`
- 样本数：{len(cluster_artifacts.clustered_data)}

### 4.2 菜品订单数据
- 文件：`menu_orders.xls`
- 订单数：{len(assoc_artifacts.transactions)}
- 菜品集合：{", ".join(sorted(assoc_artifacts.one_hot_matrix.columns.tolist()))}
- 清洗规则：逐行读取订单，去除空单元格，每一行视为一笔事务。

## 5. 聚类分析流程
1. 读取 `R、F、M` 三个特征。
2. 使用 `StandardScaler` 做标准化，避免不同量纲影响聚类结果。
3. 使用 `KMeans(n_clusters=3, random_state=42, n_init=20)` 完成聚类。
4. 统计每一类的数量和聚类中心。
5. 使用 `t-SNE` 将标准化后的 3 维特征降到 2 维，生成聚类可视化图。

### 5.1 聚类中心（原始量纲）
{centers_table}

### 5.2 各类别样本数量
{counts_table}

### 5.3 聚类结果解释
{chr(10).join(f"- Cluster {cluster}: {desc}" for cluster, desc in cluster_descriptions.items())}

### 5.4 可视化结果
- 图像文件：`outputs/kmeans_tsne.png`

## 6. 关联规则分析流程
1. 读取 `menu_orders.xls`，按行提取事务中的菜品项。
2. 将事务数据转换为 0-1 矩阵。
3. 设置 `min_support=0.2`，挖掘频繁项集。
4. 设置 `min_confidence=0.6`，生成关联规则。
5. 结合 `lift > 1` 和较高置信度筛选更有业务价值的规则。

### 6.1 前 10 个频繁项集
{itemsets_table}

### 6.2 筛选后的业务规则
{rules_table}

## 7. 业务结论
- 高频消费客户和高消费客户可作为重点维护对象，适合会员运营与精准营销。
- `R` 值高的用户说明最近消费间隔长，属于沉默客户，适合通过优惠券或召回活动刺激回流。
- 菜品规则中若某个前件对后件的置信度高且 `lift > 1`，说明组合购买倾向强，适合做套餐、推荐位或满减组合。
- 当前订单样本量较小，仅 {len(assoc_artifacts.transactions)} 笔事务，因此规则更适合作为课堂实验结果，不宜直接用于真实经营决策。

## 8. 运行方法
```bash
cd '/Users/arcdiverrr/python program/lesson hw/suchen/lesson/shujuwajue'
./.venv/bin/python run_experiment3.py
```

## 9. 输出文件说明
- `clustered_consumption_data.csv`：每位用户的聚类标签与 t-SNE 坐标
- `cluster_centers_original_scale.csv`：原始量纲下的聚类中心
- `cluster_counts.csv`：每类数量
- `kmeans_tsne.png`：聚类可视化图
- `menu_transactions_onehot.csv`：订单 0-1 事务矩阵
- `frequent_itemsets.csv`：频繁项集
- `association_rules.csv`：全部关联规则
- `selected_rules.csv`：筛选后的推荐规则
"""

    (PROJECT_ROOT / "实验流程.md").write_text(markdown, encoding="utf-8")


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    columns = [str(column) for column in df.columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for _, row in df.iterrows():
        values = [str(row[column]) for column in df.columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_summary_json(cluster_artifacts: ClusterArtifacts, assoc_artifacts: AssociationArtifacts) -> None:
    selected_rules = assoc_artifacts.selected_rules.replace([math.inf, -math.inf], None)
    summary = {
        "cluster_counts": cluster_artifacts.cluster_counts.to_dict(orient="records"),
        "cluster_centers_original": cluster_artifacts.centers_original.to_dict(orient="records"),
        "selected_rules": selected_rules.to_dict(orient="records"),
    }
    (OUTPUT_ROOT / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
'''

def main() -> None:
    ensure_output_dir()
    cluster_artifacts = run_clustering()
    assoc_artifacts = run_association_analysis()
    save_outputs(cluster_artifacts, assoc_artifacts)
    #write_markdown(cluster_artifacts, assoc_artifacts)
    #write_summary_json(cluster_artifacts, assoc_artifacts)
    print("Experiment 3 analysis completed.")
    print(f"Outputs saved to: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
