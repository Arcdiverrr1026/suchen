# 任务4：AdaBoost分类（基于乳腺癌数据集）

## 实验目的
1. 理解AdaBoost算法的基本原理
2. 掌握AdaBoost的构建和评估方法
3. 学会使用AdaBoost进行分类任务
4. 对比AdaBoost与随机森林的性能差异

## 实验原理

### AdaBoost算法
AdaBoost（Adaptive Boosting）是一种基于Boosting思想的集成学习方法，通过迭代地训练弱学习器并调整样本权重来构建强学习器。

### 核心概念
1. **Boosting**：通过顺序训练多个弱学习器，每个学习器关注前一个学习器的错误
2. **样本权重调整**：增加错误分类样本的权重，减少正确分类样本的权重
3. **弱学习器加权**：根据弱学习器的性能给予不同的权重

### 评估指标
- **准确率（Accuracy）**：正确预测的样本数占总样本数的比例
- **F1分数（F1-Score）**：精确率和召回率的调和平均值

## 实验步骤

### 步骤1：库导入
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
```

### 步骤2：数据集加载
沿用任务3中的乳腺癌数据集：
- 数据集包含569个样本，30个特征
- 类别：良性（0）和恶性（1）
- 确保数据集与随机森林实验一致，保证对比公平性

### 步骤3：数据划分
使用与随机森林实验相同的train_test_split参数：
- 设置随机种子random_state=42保证结果可重复
- 训练集：455个样本，测试集：114个样本
- 确保数据划分结果一致

### 步骤4：模型构建与训练
- 初始化AdaBoost模型（n_estimators=100, learning_rate=1.0）
- 初始化随机森林模型（用于对比）
- 初始化单棵决策树模型（用于对比）
- 使用训练集数据训练三个模型

### 步骤5：模型预测与评估
- 使用训练好的模型对测试集进行预测
- 计算准确率和F1分数
- 对比三种模型的性能

### 步骤6：结果可视化
- 绘制三种模型的准确率和F1分数对比柱状图
- 绘制相对于单棵决策树的性能提升对比图

## 实验结果分析

### 模型性能
| 模型 | 准确率 | F1分数 |
|------|--------|--------|
| AdaBoost | 约97.37% | 约97.36% |
| 随机森林 | 约96.49% | 约96.48% |
| 单棵决策树 | 约94.74% | 约94.72% |

### 性能对比分析
AdaBoost相对于单棵决策树：
- 准确率提升：约2.63%
- F1分数提升：约2.64%

AdaBoost相对于随机森林：
- 准确率差异：约0.88%
- F1分数差异：约0.88%

### 集成学习方法对比
1. **AdaBoost**：通过调整样本权重，关注难分类样本
2. **随机森林**：通过Bagging和随机特征选择，减少方差
3. **单棵决策树**：基准模型，性能相对较低

## 实验总结

### 关键发现
1. 集成学习方法（随机森林和AdaBoost）通常优于单棵决策树
2. AdaBoost和随机森林各有优势，性能相近
3. 集成学习能够有效提升模型性能

### 模型优势
- AdaBoost能够自动调整样本权重
- 随机森林能够并行训练
- 两种方法都能有效提升模型性能

### 潜在改进方向
1. 调整学习率和弱学习器数量参数
2. 使用交叉验证选择最优参数
3. 尝试其他集成方法（如梯度提升树）

## 生成文件
- `task4_results.png`：三种模型性能对比图和性能提升对比图
