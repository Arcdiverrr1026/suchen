# 快速开始指南

## 环境要求

- Python 3.7+
- 依赖包：scikit-learn, numpy, pandas, matplotlib, seaborn

## 安装依赖

```bash
cd ml_experiment4
pip install -r requirements.txt
```

或者使用uv（推荐）：
```bash
cd ml_experiment4
uv pip install -r requirements.txt
```

## 运行实验

### 方法1：运行所有实验
```bash
python run_experiments.py
```
然后选择"5"运行所有实验。

### 方法2：运行单个实验
```bash
# 任务1：分类决策树
cd task1_classification_tree
python experiment.py

# 任务2：回归决策树
cd task2_regression_tree
python experiment.py

# 任务3：随机森林分类
cd task3_random_forest
python experiment.py

# 任务4：AdaBoost分类
cd task4_adaboost
python experiment.py
```

### 方法3：使用uv运行
```bash
uv run python run_experiments.py
```

## 实验结果

运行完成后，每个任务目录中会生成以下文件：

### 任务1：分类决策树
- `task1_results.png`：决策树结构图和特征重要性图
- `task1_confusion_matrix.png`：混淆矩阵热力图

### 任务2：回归决策树
- `task2_results.png`：真实值vs预测值散点图和特征重要性图
- `task2_residuals.png`：残差分析图

### 任务3：随机森林分类
- `task3_results.png`：特征重要性图和模型性能对比图

### 任务4：AdaBoost分类
- `task4_results.png`：三种模型性能对比图

## 文档说明

每个任务目录包含：
- `experiment.py`：实验代码
- `experiment_process.md`：实验流程文档
- `analysis_report.md`：分析报告（包含关键代码）

主目录包含：
- `README.md`：详细说明文档
- `experiment_results_summary.md`：实验结果汇总（包含关键代码）
- `QUICKSTART.md`：本快速开始指南

## 实验结果概览

| 任务 | 模型 | 数据集 | 主要指标 |
|------|------|--------|----------|
| 1 | 分类决策树 | 鸢尾花 | 准确率: 100% |
| 2 | 回归决策树 | 加州房价 | R²: 59.97% |
| 3 | 随机森林 | 乳腺癌 | 准确率: 96.49% |
| 4 | AdaBoost | 乳腺癌 | 准确率: 97.37% |

## 关键发现

1. **决策树可解释性强**：决策过程清晰，易于理解
2. **集成学习提升性能**：随机森林和AdaBoost通常优于单棵决策树
3. **特征重要性分析**：有助于理解数据特征对结果的影响
4. **参数调优重要**：最大深度、学习率等参数对模型性能有重要影响

## 常见问题

### Q: 如何查看生成的图表？
A: 图表保存在各任务目录中，格式为PNG，可以用图片查看器打开。

### Q: 如何修改模型参数？
A: 编辑各任务目录中的`experiment.py`文件，修改对应的参数值。

### Q: 如何添加新的数据集？
A: 修改`experiment.py`中的数据加载部分，使用sklearn的其他数据集或自定义数据集。

### Q: 实验结果与文档不一致？
A: 实验结果可能因随机种子和参数设置而有所不同，这是正常现象。

## 联系方式

如有问题，请参考：
- scikit-learn官方文档：https://scikit-learn.org/
- 实验报告中的分析和建议
