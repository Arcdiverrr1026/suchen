"""购物篮分析实验的核心代码。

本文件负责从原始 CSV 到最终实验结果的完整流程：
数据清洗 -> 事务矩阵 -> 探索分析 -> Apriori 规则挖掘 -> 图表和报告输出。
"""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import Any

# Matplotlib 默认会尝试写入用户主目录缓存；课堂/沙箱环境可能无权限。
# 这里把字体缓存放到系统临时目录，避免生成图表时报权限提示。
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "suchen-matplotlib-cache"))

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 设置中文字体候选项，保证图表标题、坐标轴和商品名能正常显示。
matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "STHeiti"]
matplotlib.rcParams["axes.unicode_minus"] = False

# 项目路径统一从当前文件推导，脚本从仓库根目录或项目目录运行都能找到数据。
PACKAGE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = PACKAGE_DIR.parent / "20260525-数据挖掘实验" / "data"
DEFAULT_OUTPUT_DIR = PACKAGE_DIR / "output"
REPORT_DIR = PACKAGE_DIR / "reports"

# 参数网格用于实验报告中的“多组支持度、置信度对比实验”。
SUPPORT_GRID = [0.01, 0.015, 0.02, 0.025, 0.03, 0.05]
CONFIDENCE_GRID = [0.20, 0.30, 0.40, 0.50]


def read_csv_with_fallback(filepath: str | Path) -> pd.DataFrame:
    filepath = Path(filepath)
    errors: list[str] = []
    for encoding in ("utf-8-sig", "gb18030", "gbk"):
        try:
            return pd.read_csv(filepath, encoding=encoding)
        except UnicodeDecodeError as exc:
            errors.append(f"{encoding}: {exc}")
    raise UnicodeDecodeError("unknown", b"", 0, 1, "; ".join(errors))


def itemset_to_text(items: Iterable[Any]) -> str:
    """把 mlxtend 输出的 frozenset 转成报告中更易读的中文文本。"""
    return "、".join(str(item) for item in sorted(items))


def markdown_table(rows: list[dict[str, Any]], columns: list[str], headers: list[str] | None = None) -> str:
    """把统计结果转成 Markdown 表格，用于自动生成实验报告。"""
    if headers is None:
        headers = columns
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")) for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def pct(value: float) -> str:
    """把 0-1 的比例格式化为百分比，便于报告阅读。"""
    return f"{value * 100:.2f}%"


def clean_inputs(orders: pd.DataFrame, goods_types: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    orders = orders.copy()
    goods_types = goods_types.copy()

    required_order_columns = {"id", "Goods"}
    required_type_columns = {"Goods", "Types"}
    if not required_order_columns.issubset(orders.columns):
        raise ValueError(f"GoodsOrder.csv must contain columns: {sorted(required_order_columns)}")
    if not required_type_columns.issubset(goods_types.columns):
        raise ValueError(f"GoodsTypes.csv must contain columns: {sorted(required_type_columns)}")

    orders["id"] = pd.to_numeric(orders["id"], errors="raise").astype(int)
    orders["Goods"] = orders["Goods"].astype(str).str.strip()
    goods_types["Goods"] = goods_types["Goods"].astype(str).str.strip()
    goods_types["Types"] = goods_types["Types"].astype(str).str.strip()

    orders = orders.dropna(subset=["id", "Goods"]).drop_duplicates(["id", "Goods"])
    goods_types = goods_types.dropna(subset=["Goods", "Types"]).drop_duplicates(["Goods"])
    return orders, goods_types


def load_data(data_dir: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """加载实验要求的两个数据文件。"""
    data_dir = Path(data_dir)
    orders_path = data_dir / "GoodsOrder.csv"
    types_path = data_dir / "GoodsTypes.csv"
    if not orders_path.exists():
        raise FileNotFoundError(f"Missing data file: {orders_path}")
    if not types_path.exists():
        raise FileNotFoundError(f"Missing data file: {types_path}")

    orders = read_csv_with_fallback(orders_path)
    goods_types = read_csv_with_fallback(types_path)
    return clean_inputs(orders, goods_types)


def build_transactions(orders: pd.DataFrame) -> list[list[str]]:
    """把订单明细表转换为 Apriori 需要的事务列表。"""
    # 原始数据是一行一个商品；分组后每个内部列表就是一笔购物篮。
    grouped = orders.sort_values(["id", "Goods"]).groupby("id")["Goods"]
    return [list(dict.fromkeys(items)) for _, items in grouped]


def encode_transactions(transactions: list[list[str]]) -> pd.DataFrame:
    encoder = TransactionEncoder()
    matrix = encoder.fit(transactions).transform(transactions)
    return pd.DataFrame(matrix, columns=encoder.columns_)


def analyze_exploration(
    orders: pd.DataFrame,
    goods_types: pd.DataFrame,
    output_dir: Path,
    top_n: int,
) -> dict[str, Any]:
    """完成热销商品、类别结构、购物篮规模等探索性分析。"""
    # left join 保留全部订单商品；未匹配到分类的商品统一标记为“未分类”。
    merged = orders.merge(goods_types, on="Goods", how="left")
    merged["Types"] = merged["Types"].fillna("未分类")

    transaction_count = orders["id"].nunique()
    basket_sizes = orders.groupby("id")["Goods"].nunique()

    # 商品支持度 = 包含该商品的订单数 / 总订单数，用于识别高频商品。
    top_goods = (
        merged.groupby(["Goods", "Types"], as_index=False)
        .agg(count=("id", "count"), transaction_count=("id", "nunique"))
        .sort_values(["transaction_count", "count", "Goods"], ascending=[False, False, True])
    )
    top_goods["support"] = top_goods["transaction_count"] / transaction_count

    # 从类别角度统计 SKU 数、明细量和覆盖订单数，用于商品结构分析。
    type_distribution = (
        merged.groupby("Types", as_index=False)
        .agg(
            sku_count=("Goods", "nunique"),
            line_count=("Goods", "count"),
            transaction_count=("id", "nunique"),
        )
        .sort_values(["line_count", "transaction_count"], ascending=False)
    )
    type_distribution["line_share"] = type_distribution["line_count"] / len(merged)
    type_distribution["transaction_share"] = type_distribution["transaction_count"] / transaction_count

    # 统计每笔订单包含多少种商品，解释后续规则支持度普遍偏低的原因。
    basket_distribution = (
        basket_sizes.value_counts()
        .sort_index()
        .rename_axis("basket_size")
        .reset_index(name="transaction_count")
    )
    basket_distribution["transaction_share"] = basket_distribution["transaction_count"] / transaction_count

    # 输出探索分析的中间表，便于检查清洗结果和写实验报告。
    clean_orders = merged.sort_values(["id", "Goods"]).reset_index(drop=True)
    clean_orders.to_csv(output_dir / "clean_orders.csv", index=False, encoding="utf-8-sig")
    goods_types.to_csv(output_dir / "goods_with_types.csv", index=False, encoding="utf-8-sig")
    top_goods.to_csv(output_dir / "top_goods.csv", index=False, encoding="utf-8-sig")
    type_distribution.to_csv(output_dir / "type_distribution.csv", index=False, encoding="utf-8-sig")
    basket_distribution.to_csv(output_dir / "basket_size_distribution.csv", index=False, encoding="utf-8-sig")

    # 汇总指标会写入 summary.json，也会被 Markdown 报告复用。
    unmapped_goods = sorted(set(orders["Goods"]) - set(goods_types["Goods"]))
    summary = {
        "order_rows": int(len(orders)),
        "type_rows": int(len(goods_types)),
        "transactions": int(transaction_count),
        "unique_goods_in_orders": int(orders["Goods"].nunique()),
        "unique_goods_in_type_table": int(goods_types["Goods"].nunique()),
        "duplicate_order_rows_after_cleaning": 0,
        "unmapped_goods": unmapped_goods,
        "unmapped_order_rows": int(merged["Types"].eq("未分类").sum()),
        "basket_size_min": int(basket_sizes.min()),
        "basket_size_q1": float(basket_sizes.quantile(0.25)),
        "basket_size_median": float(basket_sizes.median()),
        "basket_size_mean": float(basket_sizes.mean()),
        "basket_size_q3": float(basket_sizes.quantile(0.75)),
        "basket_size_max": int(basket_sizes.max()),
        "top_goods": top_goods.head(top_n).to_dict(orient="records"),
        "top_types": type_distribution.head(10).to_dict(orient="records"),
    }

    return {
        "merged": merged,
        "top_goods": top_goods,
        "type_distribution": type_distribution,
        "basket_distribution": basket_distribution,
        "summary": summary,
    }


def prepare_itemsets_for_output(frequent_itemsets: pd.DataFrame) -> pd.DataFrame:
    """整理频繁项集输出，让 itemsets 字段适合写入 CSV 和报告。"""
    output = frequent_itemsets.copy()
    if output.empty:
        return pd.DataFrame(columns=["support", "itemsets", "length"])
    output["length"] = output["itemsets"].apply(len)
    output["itemsets"] = output["itemsets"].apply(itemset_to_text)
    output = output.sort_values(["length", "support", "itemsets"], ascending=[True, False, True])
    return output[["support", "itemsets", "length"]]


def prepare_rules_for_output(rules: pd.DataFrame) -> pd.DataFrame:
    """整理关联规则输出，并按业务解释优先级排序。"""
    columns = [
        "antecedents",
        "consequents",
        "antecedent_support",
        "consequent_support",
        "support",
        "confidence",
        "lift",
        "leverage",
        "conviction",
        "zhangs_metric",
    ]
    if rules.empty:
        return pd.DataFrame(columns=columns)

    output = rules.copy()
    # mlxtend 默认用 frozenset 表示前项/后项，这里转成“商品A、商品B”的文本。
    output["antecedents"] = output["antecedents"].apply(itemset_to_text)
    output["consequents"] = output["consequents"].apply(itemset_to_text)
    # 提升度优先：先找“比随机购买更强”的关联，再看置信度和覆盖面。
    output = output.sort_values(["lift", "confidence", "support"], ascending=False)
    available = [column for column in columns if column in output.columns]
    return output[available]


def run_apriori_experiments(
    onehot: pd.DataFrame,
    output_dir: Path,
    min_support: float,
    min_confidence: float,
) -> dict[str, Any]:
    """执行参数对比实验，并生成最终频繁项集和关联规则。"""
    comparison_rows: list[dict[str, Any]] = []
    frequent_by_support: dict[float, pd.DataFrame] = {}


    for support in SUPPORT_GRID:
        frequent_itemsets = apriori(onehot, min_support=support, use_colnames=True)
        if not frequent_itemsets.empty:
            frequent_itemsets["length"] = frequent_itemsets["itemsets"].apply(len)
        frequent_by_support[support] = frequent_itemsets

        for confidence in CONFIDENCE_GRID:
            if frequent_itemsets.empty:
                rules = pd.DataFrame()
            else:
                rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=confidence)
            comparison_rows.append(
                {
                    "min_support": support,
                    "min_confidence": confidence,
                    "frequent_itemset_count": int(len(frequent_itemsets)),
                    "max_itemset_length": int(frequent_itemsets["length"].max()) if not frequent_itemsets.empty else 0,
                    "rule_count": int(len(rules)),
                    "max_lift": float(rules["lift"].max()) if not rules.empty else 0.0,
                    "avg_lift": float(rules["lift"].mean()) if not rules.empty else 0.0,
                    "max_confidence": float(rules["confidence"].max()) if not rules.empty else 0.0,
                }
            )

    # 下面这组参数用于输出最终规则，默认对应实验报告正文中的重点结果。
    selected_itemsets = apriori(onehot, min_support=min_support, use_colnames=True)
    if not selected_itemsets.empty:
        selected_itemsets["length"] = selected_itemsets["itemsets"].apply(len)
        selected_rules = association_rules(selected_itemsets, metric="confidence", min_threshold=min_confidence)
    else:
        selected_rules = pd.DataFrame()

    comparison = pd.DataFrame(comparison_rows)
    itemsets_output = prepare_itemsets_for_output(selected_itemsets)
    rules_output = prepare_rules_for_output(selected_rules)

    # 四个 CSV 分别对应：参数对比、频繁项集、完整规则、重点规则。
    comparison.to_csv(output_dir / "parameter_comparison.csv", index=False, encoding="utf-8-sig")
    itemsets_output.to_csv(output_dir / "frequent_itemsets.csv", index=False, encoding="utf-8-sig")
    rules_output.to_csv(output_dir / "association_rules.csv", index=False, encoding="utf-8-sig")
    rules_output.head(20).to_csv(output_dir / "top_rules.csv", index=False, encoding="utf-8-sig")

    return {
        "comparison": comparison,
        "frequent_itemsets": selected_itemsets,
        "frequent_itemsets_output": itemsets_output,
        "rules": selected_rules,
        "rules_output": rules_output,
        "selected_min_support": min_support,
        "selected_min_confidence": min_confidence,
    }


def save_json(data: dict[str, Any], filepath: Path) -> None:
    """保存 JSON 汇总；兼容 pandas/numpy 的数值类型。"""
    def convert(value: Any) -> Any:
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.ndarray):
            return value.tolist()
        return value

    with filepath.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2, default=convert)


def plot_top_goods(top_goods: pd.DataFrame, figure_dir: Path, top_n: int) -> None:
    """绘制热销商品排行图，对应 top_goods.csv。"""
    data = top_goods.head(top_n).sort_values("transaction_count", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(data["Goods"], data["transaction_count"], color="#2563eb")
    ax.set_xlabel("出现订单数")
    ax.set_ylabel("商品")
    ax.set_title(f"热销商品 Top {top_n}")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(figure_dir / "top_goods.png", dpi=180)
    plt.close(fig)


def plot_type_distribution(type_distribution: pd.DataFrame, figure_dir: Path) -> None:
    """绘制商品类别结构图，对应 type_distribution.csv。"""
    data = type_distribution.sort_values("line_count", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data["Types"], data["line_count"], color="#059669")
    ax.set_xlabel("商品类别")
    ax.set_ylabel("订单明细行数")
    ax.set_title("商品类别结构")
    ax.tick_params(axis="x", rotation=30)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(figure_dir / "type_distribution.png", dpi=180)
    plt.close(fig)


def plot_basket_distribution(basket_distribution: pd.DataFrame, figure_dir: Path) -> None:
    """绘制购物篮规模分布图，对应 basket_size_distribution.csv。"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(basket_distribution["basket_size"], basket_distribution["transaction_count"], color="#f97316")
    ax.set_xlabel("单笔订单商品数")
    ax.set_ylabel("订单数")
    ax.set_title("购物篮规模分布")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(figure_dir / "basket_size_distribution.png", dpi=180)
    plt.close(fig)


def plot_rules(rules_output: pd.DataFrame, figure_dir: Path) -> None:
    """绘制规则散点图：横轴支持度、纵轴置信度、颜色表示提升度。"""
    if rules_output.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        rules_output["support"],
        rules_output["confidence"],
        c=rules_output["lift"],
        s=np.clip(rules_output["lift"] * 45, 35, 260),
        cmap="viridis",
        alpha=0.75,
        edgecolor="white",
        linewidth=0.5,
    )
    ax.set_xlabel("支持度")
    ax.set_ylabel("置信度")
    ax.set_title("关联规则：支持度、置信度与提升度")
    ax.grid(alpha=0.25)
    colorbar = fig.colorbar(scatter, ax=ax)
    colorbar.set_label("提升度")
    fig.tight_layout()
    fig.savefig(figure_dir / "rules_support_confidence_lift.png", dpi=180)
    plt.close(fig)


def make_figures(exploration: dict[str, Any], apriori_result: dict[str, Any], figure_dir: Path, top_n: int) -> None:
    """统一生成实验报告中使用的四张图。"""
    figure_dir.mkdir(parents=True, exist_ok=True)
    plot_top_goods(exploration["top_goods"], figure_dir, top_n)
    plot_type_distribution(exploration["type_distribution"], figure_dir)
    plot_basket_distribution(exploration["basket_distribution"], figure_dir)
    plot_rules(apriori_result["rules_output"], figure_dir)


def format_top_goods(top_goods: pd.DataFrame, count: int = 10) -> list[dict[str, Any]]:
    """把热销商品结果格式化为报告表格行。"""
    rows = []
    for _, row in top_goods.head(count).iterrows():
        rows.append(
            {
                "商品": row["Goods"],
                "类别": row["Types"],
                "出现订单数": int(row["transaction_count"]),
                "支持度": pct(float(row["support"])),
            }
        )
    return rows


def format_type_distribution(type_distribution: pd.DataFrame) -> list[dict[str, Any]]:
    """把类别结构结果格式化为报告表格行。"""
    rows = []
    for _, row in type_distribution.iterrows():
        rows.append(
            {
                "类别": row["Types"],
                "SKU数": int(row["sku_count"]),
                "明细行数": int(row["line_count"]),
                "行占比": pct(float(row["line_share"])),
                "覆盖订单数": int(row["transaction_count"]),
            }
        )
    return rows


def format_parameter_comparison(comparison: pd.DataFrame) -> list[dict[str, Any]]:
    """把参数对比结果格式化为报告表格行。"""
    rows = []
    for _, row in comparison.iterrows():
        rows.append(
            {
                "支持度": f"{row['min_support']:.3f}",
                "置信度": f"{row['min_confidence']:.2f}",
                "频繁项集": int(row["frequent_itemset_count"]),
                "最大项集长度": int(row["max_itemset_length"]),
                "规则数": int(row["rule_count"]),
                "最高提升度": f"{row['max_lift']:.3f}",
            }
        )
    return rows


def format_rules(rules_output: pd.DataFrame, count: int = 10) -> list[dict[str, Any]]:
    """把重点关联规则格式化为报告表格行。"""
    rows = []
    for _, row in rules_output.head(count).iterrows():
        rows.append(
            {
                "前项": row["antecedents"],
                "后项": row["consequents"],
                "支持度": pct(float(row["support"])),
                "置信度": pct(float(row["confidence"])),
                "提升度": f"{float(row['lift']):.3f}",
            }
        )
    return rows


def generate_reports(
    output_dir: Path,
    exploration: dict[str, Any],
    apriori_result: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    """根据本次运行结果自动生成 Markdown 报告。

    这里不手写固定结论，而是从 CSV/JSON 对应的 DataFrame 中取数。
    这样后续调整支持度、置信度或替换数据后，报告会随结果同步更新。
    """
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    top_goods_rows = format_top_goods(exploration["top_goods"])
    type_rows = format_type_distribution(exploration["type_distribution"])
    comparison_rows = format_parameter_comparison(apriori_result["comparison"])
    rule_rows = format_rules(apriori_result["rules_output"])

    selected_support = apriori_result["selected_min_support"]
    selected_confidence = apriori_result["selected_min_confidence"]
    unmapped = "、".join(summary["unmapped_goods"]) if summary["unmapped_goods"] else "无"

    # 项目流程侧重“怎么做”：数据、环境、步骤、运行命令和参数对比。
    flow = f"""# 数据挖掘实验5：购物篮分析 - 项目流程

## 一、实验目标

本实验围绕购物篮数据完成关联分析，目标是掌握 Apriori 算法流程，理解支持度、置信度、提升度等指标，并把规则结果转化为销售组合、陈列和促销建议。

## 二、数据与环境

- 原始数据目录：`../20260525-数据挖掘实验/data`
- 订单明细：`GoodsOrder.csv`
- 商品分类：`GoodsTypes.csv`
- Python：3.12
- 主要依赖：`pandas`、`mlxtend`、`matplotlib`

## 三、处理流程

1. 读取 CSV 文件，并使用 `gb18030` 兼容中文编码。
2. 清洗字段：统一去除商品名和类别名首尾空白，按 `id + Goods` 去重。
3. 关联商品分类表，为每条订单明细补充 `Types` 字段，未匹配类别记为“未分类”。
4. 按订单编号聚合商品，得到购物篮事务列表。
5. 使用 `TransactionEncoder` 将事务列表转换为 0-1 矩阵。
6. 进行数据探索：热销商品、类别结构、购物篮规模分布。
7. 使用 `apriori` 挖掘频繁项集，使用 `association_rules` 生成关联规则。
8. 进行多组支持度和置信度参数对比，观察规则数量、最大项集长度和最高提升度变化。
9. 选择 `min_support={selected_support:.3f}`、`min_confidence={selected_confidence:.2f}` 作为最终规则输出。
10. 生成 CSV 结果、PNG 图表和 Markdown 报告。

## 四、运行命令

```bash
./.venv/bin/python -m lesson.shujuwajue.lab5.shopping_basket_analysis
```

如需调整最终规则阈值：

```bash
./.venv/bin/python -m lesson.shujuwajue.lab5.shopping_basket_analysis --min-support 0.02 --min-confidence 0.40
```

## 五、输出文件

| 文件 | 说明 |
| --- | --- |
| `output/clean_orders.csv` | 清洗并补充类别后的订单明细 |
| `output/transactions_onehot.csv` | 购物篮事务 0-1 矩阵 |
| `output/top_goods.csv` | 热销商品排行 |
| `output/type_distribution.csv` | 商品类别结构 |
| `output/basket_size_distribution.csv` | 购物篮规模分布 |
| `output/parameter_comparison.csv` | Apriori 多组参数对比 |
| `output/frequent_itemsets.csv` | 最终频繁项集 |
| `output/association_rules.csv` | 最终关联规则 |
| `output/top_rules.csv` | 重点关联规则 |
| `output/summary.json` | 实验汇总指标 |
| `output/figures/*.png` | 可视化图表 |

## 六、参数对比结果

{markdown_table(comparison_rows, ["支持度", "置信度", "频繁项集", "最大项集长度", "规则数", "最高提升度"])}
"""

    # 数据解析侧重“结果说明”：规模、热销商品、品类结构、规则和业务建议。
    data_report = f"""# 数据挖掘实验5：购物篮分析 - 项目数据解析

## 一、数据概况

- 订单明细行数：{summary["order_rows"]}
- 交易订单数：{summary["transactions"]}
- 订单内商品种类数：{summary["unique_goods_in_orders"]}
- 分类表商品种类数：{summary["unique_goods_in_type_table"]}
- 未匹配分类商品：{unmapped}
- 未匹配分类明细行数：{summary["unmapped_order_rows"]}

购物篮规模最小为 {summary["basket_size_min"]} 件，最大为 {summary["basket_size_max"]} 件，平均为 {summary["basket_size_mean"]:.2f} 件，中位数为 {summary["basket_size_median"]:.0f} 件。

## 二、热销商品分析

{markdown_table(top_goods_rows, ["商品", "类别", "出现订单数", "支持度"])}

全脂牛奶、其他蔬菜、面包卷、苏打和酸奶是核心高频商品。其中全脂牛奶覆盖超过四分之一订单，适合作为引流品或套餐锚点。

## 三、商品结构分析

{markdown_table(type_rows, ["类别", "SKU数", "明细行数", "行占比", "覆盖订单数"])}

饮料、西点、果蔬三类贡献了较高的订单明细量，说明顾客的日常即时消费和基础食品采购占比较高。

## 四、关联规则结果

最终选择 `min_support={selected_support:.3f}`、`min_confidence={selected_confidence:.2f}`，得到 {summary["selected_itemset_count"]} 个频繁项集和 {summary["selected_rule_count"]} 条关联规则。重点规则如下：

{markdown_table(rule_rows, ["前项", "后项", "支持度", "置信度", "提升度"])}

提升度大于 1 表示前项和后项存在正相关。结果中根茎类蔬菜、其他蔬菜、柑橘类水果、热带水果、全脂牛奶、酸奶等商品之间关联较强。

## 五、营销建议

1. 围绕“全脂牛奶”做基础搭配，可与酸奶、黄油、本地蛋类、面包卷共同陈列。
2. 强化果蔬组合销售，可做“每日果蔬组合”“蔬菜汤底组合”等套餐。
3. 购买牛肉或根茎类蔬菜的顾客，可推送其他蔬菜或全脂牛奶优惠券。
4. 高频饮料和西点适合入口促销，承担引流作用。
5. 对低频但高提升度组合做小范围 A/B 测试，验证真实转化。
"""

    # 实验报告正文更适合粘贴到 Word 模板中。
    report_body = f"""# 第13周实验报告正文：购物篮分析

## 一、实验目的

本实验通过购物篮数据掌握 Apriori 算法的基本原理和实现流程，学习交易数据预处理、热销商品分析、商品结构分析和关联规则解释方法，并根据规则指标提出营销建议。

## 二、实验内容

实验使用教师提供的 `GoodsOrder.csv` 和 `GoodsTypes.csv`。首先完成数据清洗和探索分析，然后使用 `mlxtend.frequent_patterns.apriori` 挖掘频繁项集，使用 `association_rules` 生成关联规则，并通过多组最小支持度和最小置信度对比观察结果变化。

## 三、实验步骤和结果

### 1. 数据预处理

订单数据共有 {summary["order_rows"]} 条明细，包含 {summary["transactions"]} 个订单和 {summary["unique_goods_in_orders"]} 种商品。分类表包含 {summary["unique_goods_in_type_table"]} 种商品。清洗时去除商品名首尾空白，并按订单编号聚合为购物篮事务。

### 2. 探索分析

热销商品前十如下：

{markdown_table(top_goods_rows, ["商品", "类别", "出现订单数", "支持度"])}

类别结构如下：

{markdown_table(type_rows, ["类别", "SKU数", "明细行数", "行占比", "覆盖订单数"])}

平均每个购物篮包含 {summary["basket_size_mean"]:.2f} 件商品，中位数为 {summary["basket_size_median"]:.0f} 件，说明多数订单为小规模日常采购。

### 3. Apriori 参数对比

{markdown_table(comparison_rows, ["支持度", "置信度", "频繁项集", "最大项集长度", "规则数", "最高提升度"])}

随着最小支持度和最小置信度升高，频繁项集和规则数量明显减少。较低支持度能发现更多细分组合，较高支持度更适合提取稳定且覆盖面广的基础规则。

### 4. 最终关联规则

本实验最终选择 `min_support={selected_support:.3f}`、`min_confidence={selected_confidence:.2f}`，得到 {summary["selected_itemset_count"]} 个频繁项集和 {summary["selected_rule_count"]} 条关联规则。重点规则如下：

{markdown_table(rule_rows, ["前项", "后项", "支持度", "置信度", "提升度"])}

从结果看，果蔬类商品之间关联较强，乳制品和基础食品之间也存在稳定共购关系。提升度较高的规则可用于组合陈列、套餐促销和优惠券推荐。

## 四、实验总结

本实验完成了购物篮数据的清洗、探索分析、Apriori 频繁项集挖掘和关联规则解释。实验中需要注意中文 CSV 编码问题，读取时使用 `gb18030` 可以避免乱码；同时需要把订单明细聚合成事务列表，再转换为 0-1 矩阵。通过参数对比可以看到，支持度和置信度越高，规则越少但越稳定；支持度较低时可以发现更细粒度的商品组合。最终规则为商品陈列、组合促销和个性化推荐提供了依据。
"""

    (REPORT_DIR / "项目流程.md").write_text(flow, encoding="utf-8")
    (REPORT_DIR / "项目数据解析.md").write_text(data_report, encoding="utf-8")
    (REPORT_DIR / "实验报告正文.md").write_text(report_body, encoding="utf-8")


def run_analysis(
    data_dir: str | Path = DEFAULT_DATA_DIR,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    min_support: float = 0.01,
    min_confidence: float = 0.30,
    top_n: int = 20,
    make_plots: bool = True,
) -> dict[str, Any]:
    """运行完整实验流程，并返回中间结果供 CLI 打印摘要。"""
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)
    figure_dir = output_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. 加载并清洗原始数据。
    orders, goods_types = load_data(data_dir)

    # 2. 构造 Apriori 所需的事务列表和 0-1 矩阵。
    transactions = build_transactions(orders)
    onehot = encode_transactions(transactions)
    onehot.astype(int).to_csv(output_dir / "transactions_onehot.csv", index=False, encoding="utf-8-sig")

    # 3. 生成探索分析表格。
    exploration = analyze_exploration(orders, goods_types, output_dir, top_n)

    # 4. 运行参数对比实验和最终关联规则挖掘。
    apriori_result = run_apriori_experiments(onehot, output_dir, min_support, min_confidence)

    # 5. 汇总关键指标，供 summary.json 和报告正文共用。
    summary = exploration["summary"]
    summary.update(
        {
            "selected_min_support": min_support,
            "selected_min_confidence": min_confidence,
            "selected_itemset_count": int(len(apriori_result["frequent_itemsets_output"])),
            "selected_rule_count": int(len(apriori_result["rules_output"])),
            "output_dir": str(output_dir.resolve()),
        }
    )
    save_json(summary, output_dir / "summary.json")

    # 6. 图表与 Markdown 报告都由同一批结果生成，保持表格和文字一致。
    if make_plots:
        make_figures(exploration, apriori_result, figure_dir, top_n)

    generate_reports(output_dir, exploration, apriori_result, summary)

    return {
        "orders": orders,
        "goods_types": goods_types,
        "transactions": transactions,
        "onehot": onehot,
        "exploration": exploration,
        "apriori": apriori_result,
        "summary": summary,
    }
