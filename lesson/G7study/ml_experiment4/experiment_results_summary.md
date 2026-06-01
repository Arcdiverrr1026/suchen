# 机器学习实验4：实验结果汇总

## 实验概述
本实验包含四个任务，分别实现了决策树和集成学习算法，并对模型性能进行了评估和对比。

## 实验结果汇总

### 任务1：分类决策树（鸢尾花数据集）
| 指标 | 数值 |
|------|------|
| 准确率 | 100.00% |
| F1分数 | 100.00% |
| 最重要特征 | 花瓣长度 (93.46%) |

**关键代码：分类决策树**
```python
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# 加载数据
iris = load_iris()
X, y = iris.data, iris.target

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建并训练模型
model = DecisionTreeClassifier(max_depth=3, random_state=42)
model.fit(X_train, y_train)

# 评估模型
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred, average='weighted')
print(f"准确率: {accuracy:.4f}, F1分数: {f1:.4f}")
```

**关键发现**：
- 决策树在鸢尾花数据集上表现完美
- 花瓣长度是最重要特征
- 模型可解释性强

### 任务2：回归决策树（加州房价数据集）
| 指标 | 数值 |
|------|------|
| 均方误差 (MSE) | 0.5245 |
| 均方根误差 (RMSE) | 0.7242 |
| 决定系数 (R²) | 59.97% |
| 最重要特征 | 收入 (77.12%) |

**关键代码：回归决策树**
```python
from sklearn.datasets import fetch_california_housing
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 加载数据
housing = fetch_california_housing()
X, y = housing.data, housing.target

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建并训练模型
model = DecisionTreeRegressor(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 评估模型
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
print(f"MSE: {mse:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
```

**关键发现**：
- 决策树能够处理回归任务
- 收入水平是影响房价的最重要因素
- 模型拟合效果一般，有改进空间

### 任务3：随机森林分类（乳腺癌数据集）
| 指标 | 随机森林 | 单棵决策树 | 提升 |
|------|----------|------------|------|
| 准确率 | 96.49% | 94.74% | +1.75% |
| F1分数 | 96.47% | 94.74% | +1.74% |
| 最重要特征 | 最差面积 (15.47%) | - | - |

**关键代码：随机森林分类**
```python
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# 加载数据
cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建随机森林模型
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

# 构建单棵决策树模型（用于对比）
dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train, y_train)

# 评估模型
rf_pred = rf_model.predict(X_test)
dt_pred = dt_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_pred)
dt_accuracy = accuracy_score(y_test, dt_pred)

print(f"随机森林准确率: {rf_accuracy:.4f}")
print(f"单棵决策树准确率: {dt_accuracy:.4f}")
print(f"准确率提升: {(rf_accuracy - dt_accuracy)*100:.2f}%")
```

**关键发现**：
- 随机森林优于单棵决策树
- 集成学习能够有效提升模型性能
- 最差特征对分类结果影响最大

### 任务4：AdaBoost分类（乳腺癌数据集）
| 指标 | AdaBoost | 随机森林 | 单棵决策树 |
|------|----------|----------|------------|
| 准确率 | 97.37% | 96.49% | 94.74% |
| F1分数 | 97.36% | 96.47% | 94.74% |

**关键代码：AdaBoost分类**
```python
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# 加载数据
cancer = load_breast_cancer()
X, y = cancer.data, cancer.target

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 构建AdaBoost模型
ada_model = AdaBoostClassifier(n_estimators=100, learning_rate=1.0, random_state=42)
ada_model.fit(X_train, y_train)

# 构建随机森林和单棵决策树模型（用于对比）
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
dt_model.fit(X_train, y_train)

# 评估模型
ada_pred = ada_model.predict(X_test)
rf_pred = rf_model.predict(X_test)
dt_pred = dt_model.predict(X_test)

ada_accuracy = accuracy_score(y_test, ada_pred)
rf_accuracy = accuracy_score(y_test, rf_pred)
dt_accuracy = accuracy_score(y_test, dt_pred)

print(f"AdaBoost准确率: {ada_accuracy:.4f}")
print(f"随机森林准确率: {rf_accuracy:.4f}")
print(f"单棵决策树准确率: {dt_accuracy:.4f}")

print(f"AdaBoost vs 单棵决策树：准确率提升 {(ada_accuracy - dt_accuracy)*100:.2f}%")
print(f"AdaBoost vs 随机森林：准确率差异 {(ada_accuracy - rf_accuracy)*100:.2f}%")
```

**关键发现**：
- AdaBoost性能略优于随机森林
- 两种集成方法都显著优于单棵决策树
- AdaBoost通过调整样本权重关注难分类样本

## 性能对比总结

### 分类任务性能对比
| 模型 | 数据集 | 准确率 | F1分数 |
|------|--------|--------|--------|
| 分类决策树 | 鸢尾花 | 100.00% | 100.00% |
| 随机森林 | 乳腺癌 | 96.49% | 96.47% |
| AdaBoost | 乳腺癌 | 97.37% | 97.36% |

### 集成学习效果
在乳腺癌数据集上：
- **单棵决策树**：94.74%准确率
- **随机森林**：96.49%准确率（提升1.75%）
- **AdaBoost**：97.37%准确率（提升2.63%）

## 关键发现总结

### 1. 决策树特性
- **可解释性强**：决策过程清晰，易于理解
- **能够处理非线性关系**：通过树结构捕捉复杂模式
- **不需要特征缩放**：对特征尺度不敏感
- **容易过拟合**：特别是在树深度较大时

### 2. 集成学习优势
- **性能提升**：集成方法通常优于单棵决策树
- **稳定性增强**：通过集成减少方差
- **特征重要性**：能够评估特征重要性

### 3. 随机森林 vs AdaBoost
| 特性 | 随机森林 | AdaBoost |
|------|----------|----------|
| 训练方式 | 并行 | 顺序 |
| 核心思想 | Bagging | Boosting |
| 样本权重 | 均等 | 动态调整 |
| 对噪声敏感度 | 较低 | 较高 |
| 性能 | 略低 | 略高 |

## 模型选择建议

### 选择决策树的场景
1. 需要模型可解释性强
2. 数据量较小
3. 特征数量较少
4. 需要快速训练

### 选择随机森林的场景
1. 需要稳定性能
2. 数据量较大
3. 特征数量较多
4. 需要并行训练

### 选择AdaBoost的场景
1. 需要最高性能
2. 数据质量较好
3. 能够接受较长训练时间
4. 需要关注难分类样本

## 实验收获

### 理论收获
1. 理解决策树的基本原理和构建过程
2. 掌握集成学习的基本思想（Bagging和Boosting）
3. 学会评估分类和回归模型性能

### 实践收获
1. 掌握sklearn中各种模型的使用方法
2. 学会数据划分和模型训练的流程
3. 掌握结果可视化和性能对比的方法

### 思考与启发
1. 集成学习能够有效提升模型性能
2. 特征重要性分析有助于理解数据
3. 模型选择需要平衡性能和复杂度
4. 没有绝对最优的模型，需要根据具体场景选择

## 后续工作建议

1. 尝试更复杂的参数组合
2. 使用交叉验证选择最优参数
3. 探索其他集成方法（如梯度提升树、XGBoost）
4. 进行特征工程，创建更有意义的特征
5. 尝试处理不平衡数据的方法
6. 学习模型解释性技术（如SHAP值）

## 生成文件说明

每个任务目录包含：
- `experiment.py`：实验代码
- `experiment_process.md`：实验流程文档
- `analysis_report.md`：分析报告
- `*.png`：可视化图表

主目录包含：
- `__init__.py`：主包初始化文件
- `README.md`：说明文档
- `requirements.txt`：依赖文件
- `run_all_experiments.py`：运行所有实验的脚本
- `experiment_results_summary.md`：本汇总文档
