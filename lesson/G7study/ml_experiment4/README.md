# 机器学习实验4：决策树与集成学习模型构建与评估

## 实验概述

本实验旨在通过四个任务，深入理解决策树和集成学习算法，包括分类决策树、回归决策树、随机森林和AdaBoost。

## 实验任务

### 任务1：分类决策树（基于鸢尾花数据集）
- **目标**：使用决策树进行多分类任务
- **数据集**：鸢尾花数据集（150个样本，4个特征，3个类别）
- **评估指标**：准确率、F1分数、混淆矩阵
- **可视化**：决策树结构图、特征重要性图、混淆矩阵热力图

### 任务2：回归决策树（基于波士顿房价数据集）
- **目标**：使用决策树进行连续值预测
- **数据集**：加州房价数据集（替代波士顿房价数据集）
- **评估指标**：均方误差（MSE）、决定系数（R²）
- **可视化**：真实值vs预测值散点图、特征重要性图、残差分析图

### 任务3：随机森林分类（基于乳腺癌数据集）
- **目标**：使用随机森林进行二分类任务
- **数据集**：乳腺癌数据集（569个样本，30个特征，2个类别）
- **评估指标**：准确率、F1分数
- **可视化**：特征重要性图、模型性能对比图

### 任务4：AdaBoost分类（基于乳腺癌数据集）
- **目标**：使用AdaBoost进行二分类任务
- **数据集**：乳腺癌数据集（与任务3相同）
- **评估指标**：准确率、F1分数
- **可视化**：三种模型性能对比图、性能提升对比图

## 软件包结构

```
ml_experiment4/
├── __init__.py                    # 主包初始化文件
├── README.md                      # 本说明文档
├── task1_classification_tree/     # 任务1：分类决策树
│   ├── experiment.py              # 实验代码
│   ├── experiment_process.md      # 实验流程文档
│   └── analysis_report.md         # 分析报告
├── task2_regression_tree/         # 任务2：回归决策树
│   ├── experiment.py              # 实验代码
│   ├── experiment_process.md      # 实验流程文档
│   └── analysis_report.md         # 分析报告
├── task3_random_forest/           # 任务3：随机森林分类
│   ├── experiment.py              # 实验代码
│   ├── experiment_process.md      # 实验流程文档
│   └── analysis_report.md         # 分析报告
└── task4_adaboost/                # 任务4：AdaBoost分类
    ├── experiment.py              # 实验代码
    ├── experiment_process.md      # 实验流程文档
    └── analysis_report.md         # 分析报告
```

## 使用方法

### 环境要求
- Python 3.7+
- scikit-learn
- numpy
- pandas
- matplotlib
- seaborn

### 安装依赖
```bash
pip install scikit-learn numpy pandas matplotlib seaborn
```

### 运行实验
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

## 实验结果汇总

### 性能对比
| 模型 | 任务 | 准确率/决定系数 | F1分数 |
|------|------|----------------|--------|
| 分类决策树 | 鸢尾花分类 | 96.67% | 96.65% |
| 回归决策树 | 房价预测 | R² = 0.60 | - |
| 随机森林 | 乳腺癌分类 | 96.49% | 96.48% |
| AdaBoost | 乳腺癌分类 | 97.37% | 97.36% |

### 关键发现
1. **决策树可解释性强**：决策过程清晰，易于理解
2. **集成学习提升性能**：随机森林和AdaBoost通常优于单棵决策树
3. **特征重要性分析**：有助于理解数据特征对结果的影响
4. **参数调优重要**：最大深度、学习率等参数对模型性能有重要影响

## 实验总结

### 模型优势
- **决策树**：可解释性强，能够处理非线性关系
- **随机森林**：不容易过拟合，能够评估特征重要性
- **AdaBoost**：自动调整样本权重，关注难分类样本

### 潜在改进方向
1. 尝试不同的参数组合
2. 使用交叉验证选择最优参数
3. 探索其他集成方法（如梯度提升树、XGBoost）
4. 进行特征工程，创建更有意义的特征

## 注意事项

1. 波士顿房价数据集在sklearn 1.2版本后已被移除，实验中使用加州房价数据集作为替代
2. 实验结果可能因随机种子和参数设置而有所不同
3. 可视化图表已保存为PNG格式，可在对应任务目录中查看

## 参考资料

1. scikit-learn官方文档：https://scikit-learn.org/
2. 决策树算法原理：https://en.wikipedia.org/wiki/Decision_tree_learning
3. 随机森林算法原理：https://en.wikipedia.org/wiki/Random_forest
4. AdaBoost算法原理：https://en.wikipedia.org/wiki/AdaBoost
