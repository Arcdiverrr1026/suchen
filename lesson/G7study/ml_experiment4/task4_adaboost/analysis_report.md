# 任务4：AdaBoost分类实验分析报告

## 1. 实验概述

### 1.1 实验目标
本实验旨在通过乳腺癌数据集，掌握AdaBoost的构建、训练、评估和可视化方法，并与随机森林和单棵决策树进行对比。

### 1.2 数据集介绍
沿用任务3中的乳腺癌数据集：
- **样本数量**：569个
- **特征数量**：30个
- **类别数量**：2个（良性、恶性）
- **样本分布**：良性357个（62.7%），恶性212个（37.3%）

## 2. 实验过程分析

### 2.1 数据预处理
- 数据集质量良好，无缺失值
- 特征均为数值型，无需编码处理
- 存在一定的类别不平衡（良性样本较多）

**关键代码：数据加载**
```python
from sklearn.datasets import load_breast_cancer

# 加载乳腺癌数据集（与任务3相同）
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target

# 查看数据集基本信息
print(f"样本数量: {X.shape[0]}")
print(f"特征数量: {X.shape[1]}")
print(f"类别数量: {len(cancer.target_names)}")
print(f"类别名称: {cancer.target_names}")
```

### 2.2 模型参数选择
AdaBoost参数选择：
- **n_estimators=100**：使用100个弱学习器，平衡性能和计算成本
- **learning_rate=1.0**：学习率，控制每个弱学习器的贡献

随机森林参数：
- **n_estimators=100**：与AdaBoost保持一致
- **max_depth=5**：限制树深度，防止过拟合

单棵决策树参数：
- **max_depth=5**：与随机森林保持一致

**关键代码：模型构建与训练**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

# 数据划分（8:2比例，与任务3相同）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 构建AdaBoost模型
ada_model = AdaBoostClassifier(
    n_estimators=100,
    learning_rate=1.0,
    random_state=42
)

# 构建随机森林模型（用于对比）
rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42
)

# 构建单棵决策树模型（用于对比）
dt_model = DecisionTreeClassifier(
    max_depth=5,
    random_state=42
)

# 训练模型
ada_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)
```

### 2.3 训练过程
模型训练过程顺利：
1. AdaBoost需要顺序训练弱学习器
2. 随机森林可以并行训练
3. 单棵决策树训练速度最快

## 3. 结果分析

### 3.1 性能指标
| 模型 | 准确率 | F1分数 |
|------|--------|--------|
| AdaBoost | 97.37% | 97.36% |
| 随机森林 | 96.49% | 96.47% |
| 单棵决策树 | 94.74% | 94.74% |

**关键代码：模型评估**
```python
from sklearn.metrics import accuracy_score, f1_score

# AdaBoost预测
ada_pred = ada_model.predict(X_test)
ada_accuracy = accuracy_score(y_test, ada_pred)
ada_f1 = f1_score(y_test, ada_pred, average='weighted')

# 随机森林预测
rf_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_pred)
rf_f1 = f1_score(y_test, rf_pred, average='weighted')

# 单棵决策树预测
dt_pred = dt_model.predict(X_test)
dt_accuracy = accuracy_score(y_test, dt_pred)
dt_f1 = f1_score(y_test, dt_pred, average='weighted')

print(f"AdaBoost准确率: {ada_accuracy:.4f}")
print(f"AdaBoostF1分数: {ada_f1:.4f}")
print(f"随机森林准确率: {rf_accuracy:.4f}")
print(f"随机森林F1分数: {rf_f1:.4f}")
print(f"单棵决策树准确率: {dt_accuracy:.4f}")
print(f"单棵决策树F1分数: {dt_f1:.4f}")

# 性能对比
print(f"AdaBoost vs 单棵决策树：")
print(f"  准确率提升: {(ada_accuracy - dt_accuracy)*100:.2f}%")
print(f"  F1分数提升: {(ada_f1 - dt_f1)*100:.2f}%")

print(f"AdaBoost vs 随机森林：")
print(f"  准确率差异: {(ada_accuracy - rf_accuracy)*100:.2f}%")
print(f"  F1分数差异: {(ada_f1 - rf_f1)*100:.2f}%")
```

### 3.2 性能对比分析
AdaBoost相对于单棵决策树：
- 准确率提升：2.63%
- F1分数提升：2.63%

AdaBoost相对于随机森林：
- 准确率差异：0.88%
- F1分数差异：0.89%

分析：
- AdaBoost性能略优于随机森林
- 两种集成方法都显著优于单棵决策树
- AdaBoost通过调整样本权重，能够更好地关注难分类样本

### 3.3 集成学习方法对比

**关键代码：结果可视化**
```python
import numpy as np
import matplotlib.pyplot as plt

# 创建图形
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 1. 绘制三种模型的准确率对比柱状图
models = ['单棵决策树', '随机森林', 'AdaBoost']
accuracy_scores = [dt_accuracy, rf_accuracy, ada_accuracy]
f1_scores = [dt_f1, rf_f1, ada_f1]

x = np.arange(len(models))
width = 0.35

bars1 = axes[0].bar(x - width/2, accuracy_scores, width,
                    label='准确率', color='skyblue', edgecolor='black')
bars2 = axes[0].bar(x + width/2, f1_scores, width,
                    label='F1分数', color='lightcoral', edgecolor='black')

axes[0].set_xlabel('模型')
axes[0].set_ylabel('分数')
axes[0].set_title('三种模型性能对比')
axes[0].set_xticks(x)
axes[0].set_xticklabels(models)
axes[0].legend()
axes[0].set_ylim(0.9, 1.0)

# 2. 绘制性能提升对比图
# 计算相对于单棵决策树的提升
rf_acc_improvement = (rf_accuracy - dt_accuracy) * 100
rf_f1_improvement = (rf_f1 - dt_f1) * 100
ada_acc_improvement = (ada_accuracy - dt_accuracy) * 100
ada_f1_improvement = (ada_f1 - dt_f1) * 100

improvements = ['准确率提升', 'F1分数提升']
rf_improvements = [rf_acc_improvement, rf_f1_improvement]
ada_improvements = [ada_acc_improvement, ada_f1_improvement]

x2 = np.arange(len(improvements))
width2 = 0.35

bars3 = axes[1].bar(x2 - width2/2, rf_improvements, width2,
                    label='随机森林', color='lightgreen', edgecolor='black')
bars4 = axes[1].bar(x2 + width2/2, ada_improvements, width2,
                    label='AdaBoost', color='lightyellow', edgecolor='black')

axes[1].set_xlabel('指标')
axes[1].set_ylabel('提升百分比 (%)')
axes[1].set_title('相对于单棵决策树的性能提升')
axes[1].set_xticks(x2)
axes[1].set_xticklabels(improvements)
axes[1].legend()
axes[1].axhline(y=0, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('task4_results.png', dpi=300, bbox_inches='tight')
```

#### AdaBoost特点
1. **顺序训练**：每个弱学习器基于前一个的错误进行训练
2. **样本权重调整**：增加错误分类样本的权重
3. **弱学习器加权**：根据性能给予不同权重
4. **关注难分类样本**：能够自动关注难分类样本

#### 随机森林特点
1. **并行训练**：多棵树可以并行构建
2. **Bagging**：通过自助采样法生成多个训练子集
3. **随机特征选择**：在每个节点随机选择特征子集
4. **减少方差**：通过集成减少模型方差

#### 性能对比
- AdaBoost：97.37%准确率
- 随机森林：96.49%准确率
- 差异：0.88%

## 4. 模型评估

### 4.1 AdaBoost优点
1. **性能优越**：通常优于单棵决策树，略优于随机森林
2. **自动调整权重**：能够自动关注难分类样本
3. **不容易过拟合**：通过集成减少方差
4. **能够处理不平衡数据**：通过权重调整处理类别不平衡

### 4.2 AdaBoost缺点
1. **对噪声敏感**：容易受到噪声数据的影响
2. **训练时间较长**：需要顺序训练弱学习器
3. **对异常值敏感**：异常值可能获得过高权重

### 4.3 改进建议
1. **参数调优**：尝试不同的learning_rate和n_estimators值
2. **交叉验证**：使用k折交叉验证选择最优参数
3. **尝试其他Boosting方法**：如梯度提升树（GBDT）、XGBoost
4. **处理噪声数据**：预先处理噪声和异常值

## 5. 实验收获

### 5.1 理论收获
1. 理解了AdaBoost的基本原理和构建过程
2. 掌握了Boosting和样本权重调整的概念
3. 学会了如何对比不同集成学习方法

### 5.2 实践收获
1. 掌握了sklearn中AdaBoost的使用方法
2. 学会了模型对比和性能评估的方法
3. 掌握了结果可视化的方法

### 5.3 思考与启发
1. 集成学习能够有效提升模型性能
2. 不同的集成方法有不同的特点和适用场景
3. 模型选择需要平衡性能和复杂度

## 6. 结论

AdaBoost在乳腺癌数据集上表现出色，准确率达到97.37%，略优于随机森林的96.49%，显著优于单棵决策树的94.74%。AdaBoost通过调整样本权重，能够更好地关注难分类样本，从而提升模型性能。两种集成学习方法都显著优于单棵决策树，验证了集成学习的有效性。

## 7. 后续工作建议

1. 尝试更复杂的AdaBoost参数组合
2. 探索其他Boosting方法（如梯度提升树、XGBoost）进行对比
3. 学习AdaBoost的参数调优技术
4. 了解如何处理噪声和异常值
5. 尝试使用交叉验证评估模型性能
