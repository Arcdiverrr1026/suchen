# 机器学习实验5：SVM 与聚类模型构建与评估

本目录包含实验 5 的完整 Python 代码，覆盖实验文档中的四个任务：

1. 线性核 SVM 分类：鸢尾花数据集
2. 高斯核 RBF SVM 分类：乳腺癌数据集
3. K-Means 聚类：鸢尾花数据集
4. DBSCAN 密度聚类：鸢尾花数据集

## 目录结构

```text
lab5/
├── common.py
├── run_experiments.py
├── task1_linear_svm/
│   └── experiment.py
├── task2_rbf_svm/
│   └── experiment.py
├── task3_kmeans/
│   └── experiment.py
└── task4_dbscan/
    └── experiment.py
```

## 运行方法

在项目根目录运行全部实验：

```bash
python lesson/G7study/lab5/run_experiments.py
```

只运行某个任务：

```bash
python lesson/G7study/lab5/run_experiments.py --task task1
python lesson/G7study/lab5/run_experiments.py --task task2
python lesson/G7study/lab5/run_experiments.py --task task3
python lesson/G7study/lab5/run_experiments.py --task task4
```

也可以进入单个任务目录直接运行：

```bash
python lesson/G7study/lab5/task1_linear_svm/experiment.py
```

## 输出文件

每个任务会在自己的目录下保存实验结果：

- PNG 图表：混淆矩阵、决策边界、聚类结果、参数对比图等
- CSV 文件：预测结果、聚类分配、参数对比结果
- JSON 文件：主要评估指标汇总
- Markdown 分析报告：`EXPERIMENT_RESULTS_ANALYSIS.md` 和各任务目录下的 `analysis_report.md`
- 实验原理补充：`EXPERIMENT_PRINCIPLE.md`

## 依赖

代码使用项目已有依赖：

- numpy
- pandas
- matplotlib
- scikit-learn
