# 数据挖掘实验5：购物篮分析

## 项目概述

本项目根据 `第13周实验报告.doc` 的要求完成购物篮分析实验：

1. 对购物篮交易数据做探索分析，包括热销商品、商品结构和购物篮规模。
2. 使用 `mlxtend.frequent_patterns.apriori` 与 `association_rules` 生成频繁项集和关联规则。
3. 调整最小支持度、最小置信度进行多组对比实验。
4. 根据商品关联结果给出可落地的营销建议。

## 项目结构

```text
shopping_basket_analysis/
├── __init__.py
├── __main__.py
├── analysis.py
├── cli.py
├── main.py
├── requirements.txt
├── output/
│   ├── figures/
│   ├── association_rules.csv
│   ├── basket_size_distribution.csv
│   ├── frequent_itemsets.csv
│   ├── parameter_comparison.csv
│   ├── summary.json
│   ├── top_goods.csv
│   ├── top_rules.csv
│   ├── transactions_onehot.csv
│   └── type_distribution.csv
└── reports/
    ├── 实验报告正文.md
    ├── 关键代码解析.md
    ├── 项目数据解析.md
    └── 项目流程.md
```

原始数据位于同级目录：

```text
../20260525-数据挖掘实验/data/
├── GoodsOrder.csv
└── GoodsTypes.csv
```

## 运行方式

在仓库根目录运行：

```bash
./.venv/bin/python -m lesson.shujuwajue.lab5.shopping_basket_analysis
```

也可以直接运行项目入口：

```bash
./.venv/bin/python lesson/shujuwajue/lab5/shopping_basket_analysis/main.py
```

可选参数：

```bash
./.venv/bin/python -m lesson.shujuwajue.lab5.shopping_basket_analysis \
  --min-support 0.01 \
  --min-confidence 0.30 \
  --top-n 20
```

## 主要输出

- `output/summary.json`：实验汇总指标
- `output/top_goods.csv`：热销商品排行
- `output/type_distribution.csv`：商品类别结构
- `output/parameter_comparison.csv`：Apriori 参数对比实验
- `output/frequent_itemsets.csv`：最终频繁项集
- `output/association_rules.csv`：最终关联规则
- `output/top_rules.csv`：按提升度排序的重点规则
- `output/figures/*.png`：热销商品、类别结构、购物篮规模和规则散点图
- `reports/项目流程.md`：项目流程说明
- `reports/项目数据解析.md`：数据解析与业务建议
- `reports/关键代码解析.md`：核心代码逻辑说明
- `reports/实验报告正文.md`：可粘贴到实验报告的正文内容
