# 数据挖掘实验4：关联分析与离群点检测

## 项目概述

本项目是数据挖掘课程的实验4，主要包含两个部分：

1. **关联分析**：使用 Apriori 算法挖掘菜品订单数据中的关联规则
2. **离群点检测**：基于 K-Means 聚类算法识别消费数据中的异常客户

## 项目结构

```
lab4_association_outlier/
├── data/                          # 数据文件
│   ├── menu_orders.xls           # 菜品订单数据
│   └── consumption_data.xls      # 消费数据（RFM模型）
├── output/                        # 输出结果
│   ├── menu_transactions_onehot.csv    # 0-1 矩阵
│   ├── frequent_itemsets.csv           # 频繁项集
│   ├── association_rules.csv           # 关联规则
│   ├── clustered_consumption_data.csv  # 聚类结果
│   ├── cluster_centers_*.csv           # 聚类中心
│   ├── cluster_counts.csv              # 簇大小
│   ├── summary.json                    # 汇总统计
│   └── kmeans_tsne.png                 # 可视化图表
├── reports/                       # 实验报告
│   ├── 实验流程.md               # 实验步骤文档
│   └── 实验数据分析报告.md       # 数据分析报告
├── __init__.py                    # Python 包标记
├── __main__.py                    # python -m 入口
├── analysis.py                    # 核心分析逻辑
├── cli.py                         # 命令行入口
├── main.py                        # 兼容入口
└── README.md                      # 项目说明
```

## 环境配置

### 使用 uv（推荐）

```bash
# 安装依赖
uv sync

# 运行程序
uv run python -m lesson.shujuwajue.lab4_association_outlier

# 或者兼容旧入口
uv run python lesson/shujuwajue/lab4_association_outlier/main.py
```

### 使用 pip

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install pandas mlxtend scikit-learn matplotlib openpyxl xlrd

# 运行程序
python main.py
```

## 快速开始

1. 确保数据文件在 `data/` 目录下
2. 运行主程序：`uv run python -m lesson.shujuwajue.lab4_association_outlier`
3. 查看输出结果：`output/` 目录
4. 阅读实验报告：`reports/` 目录

也可以指定数据和输出目录：

```bash
uv run python -m lesson.shujuwajue.lab4_association_outlier --data-dir lesson/shujuwajue/lab4_association_outlier/data --output-dir lesson/shujuwajue/lab4_association_outlier/output
```

## 实验结果摘要

### 关联分析

- **数据规模**：10 条事务，5 种菜品
- **频繁项集**：11 个
- **关联规则**：15 条
- **关键发现**：
  - 菜品 e 与 {a, c} 强正相关（提升度 2.0）
  - 菜品 b 与 {a, c} 弱负相关（提升度 0.89）

### 离群点检测

- **数据规模**：940 条客户记录
- **聚类数量**：3 簇
- **离群点数量**：11 个（1.2%）
- **关键发现**：
  - 离群点主要是"高价值流失客户"
  - R 值和 M 值是区分离群点的关键特征

## 技术栈

- **Python**：3.12
- **包管理**：uv
- **数据处理**：pandas, numpy
- **机器学习**：scikit-learn, mlxtend
- **可视化**：matplotlib

## 实验报告

详细的实验流程和数据分析报告请查看 `reports/` 目录：

- [实验流程.md](reports/实验流程.md)：详细的实验步骤和技术要点
- [实验数据分析报告.md](reports/实验数据分析报告.md)：完整的数据分析结果和业务洞察

## 许可证

本项目仅用于学术学习目的。

---

*完成时间：2026 年 5 月 12 日*
