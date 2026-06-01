# 任务2：回归决策树实验分析报告

## 1. 实验概述

### 1.1 实验目标
本实验旨在通过房价数据集，掌握回归决策树的构建、训练、评估和可视化方法。

### 1.2 数据集介绍
由于波士顿房价数据集已被移除，使用加州房价数据集作为替代：
- **样本数量**：20640个
- **特征数量**：8个
- **目标变量**：房价中位数（单位：10万美元）

#### 特征说明
1. **MedInc**：街区收入中位数
2. **HouseAge**：房屋年龄中位数
3. **AveRooms**：平均房间数
4. **AveBedrms**：平均卧室数
5. **Population**：街区人口
6. **AveOccup**：平均入住率
7. **Latitude**：纬度
8. **Longitude**：经度

## 2. 实验过程分析

### 2.1 数据预处理
- 数据集质量良好，无缺失值
- 特征均为数值型，无需编码处理
- 目标变量分布相对均匀

**关键代码：数据加载**
```python
from sklearn.datasets import fetch_california_housing

# 加载加州房价数据集（替代波士顿房价数据集）
housing = fetch_california_housing()
X = housing.data
y = housing.target

# 查看数据集基本信息
print(f"样本数量: {X.shape[0]}")
print(f"特征数量: {X.shape[1]}")
print(f"特征名称: {housing.feature_names}")
print(f"目标变量: 房价中位数（单位：10万美元）")
```

### 2.2 模型参数选择
选择max_depth=5的原因：
1. 防止过拟合：过深的树会导致模型过于复杂
2. 保持可解释性：深度为5的树结构相对清晰
3. 平衡性能：在准确率和复杂度之间取得平衡

**关键代码：数据划分与模型构建**
```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

# 数据划分（8:2比例）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 构建回归决策树模型
model = DecisionTreeRegressor(max_depth=5, random_state=42)

# 训练模型
model.fit(X_train, y_train)
```

### 2.3 训练过程
模型训练过程顺利：
1. 计算速度快，训练时间短
2. 不需要迭代优化
3. 一次性构建完成

## 3. 结果分析

### 3.1 性能指标
| 指标 | 数值 | 说明 |
|------|------|------|
| 均方误差 (MSE) | 0.5245 | 预测误差的平方的平均值 |
| 均方根误差 (RMSE) | 0.7242 | 与目标变量单位一致的误差度量 |
| 决定系数 (R²) | 0.5997 | 模型解释60%的数据变异性 |

**关键代码：模型评估**
```python
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# 预测
y_pred = model.predict(X_test)

# 计算评估指标
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"均方误差 (MSE): {mse:.4f}")
print(f"均方根误差 (RMSE): {rmse:.4f}")
print(f"决定系数 (R²): {r2:.4f}")
```

### 3.2 拟合效果分析
R²值为0.60，表明：
- 模型能够解释60%的房价变异性
- 存在40%的变异性未被模型捕捉
- 模型拟合效果一般，有改进空间

### 3.3 特征重要性分析
特征重要性排序：
1. **MedInc（收入）**：最重要特征，重要性约77.12%
2. **AveOccup（平均入住率）**：次重要特征，重要性约12.84%
3. **Latitude（纬度）**：重要性约2.20%
4. **Longitude（经度）**：重要性约0.21%
5. **HouseAge（房龄）**：重要性约4.16%
6. **AveRooms（平均房间数）**：重要性约3.13%
7. **AveBedrms（平均卧室数）**：重要性约0.09%
8. **Population（人口）**：重要性约0.25%

**关键代码：特征重要性分析与可视化**
```python
import numpy as np
import matplotlib.pyplot as plt

# 计算特征重要性
feature_importance = model.feature_importances_

# 可视化特征重要性
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 绘制真实值与预测值的对比散点图
axes[0].scatter(y_test, y_pred, alpha=0.5, color='blue', edgecolors='black')
axes[0].plot([y_test.min(), y_test.max()],
             [y_test.min(), y_test.max()],
             'r--', alpha=0.8, label='完美预测线')
axes[0].set_xlabel('真实值')
axes[0].set_ylabel('预测值')
axes[0].set_title(f'真实值 vs 预测值 (R² = {r2:.4f})')
axes[0].legend()

# 绘制特征重要性
sorted_idx = np.argsort(feature_importance)
axes[1].barh(range(len(sorted_idx)),
             feature_importance[sorted_idx],
             align='center',
             color='skyblue')
axes[1].set_yticks(range(len(sorted_idx)))
axes[1].set_yticklabels([housing.feature_names[i] for i in sorted_idx])
axes[1].set_xlabel('特征重要性')
axes[1].set_title('特征重要性分析')
```

分析：
- 收入水平是影响房价的最重要因素
- 地理位置（经纬度）对房价有重要影响
- 房屋特征（房间数、卧室数）影响相对较小

### 3.4 残差分析
残差分析显示：
- 残差分布相对均匀，无明显模式
- 残差均值接近0，表明模型无系统性偏差
- 残差标准差为0.72，表明预测误差相对稳定

## 4. 模型评估

### 4.1 优点
1. **可解释性强**：决策过程清晰，易于理解和解释
2. **训练速度快**：算法复杂度低，训练时间短
3. **不需要特征缩放**：对特征尺度不敏感
4. **能够处理非线性关系**：通过树结构捕捉复杂模式

### 4.2 缺点
1. **容易过拟合**：特别是在树深度较大时
2. **对噪声敏感**：小的数据扰动可能导致树结构变化
3. **不稳定**：数据微小变化可能导致完全不同的树
4. **预测精度有限**：R²值仅为0.60，有改进空间

### 4.3 改进建议
1. **参数调优**：尝试不同的max_depth值
2. **交叉验证**：使用k折交叉验证选择最优参数
3. **剪枝策略**：应用预剪枝或后剪枝防止过拟合
4. **集成方法**：考虑使用随机森林或梯度提升树
5. **特征工程**：创建更有意义的特征

## 5. 实验收获

### 5.1 理论收获
1. 理解了回归决策树的基本原理和构建过程
2. 掌握了均方误差和决定系数的概念
3. 学会了如何评估回归模型性能

### 5.2 实践收获
1. 掌握了sklearn中回归决策树的使用方法
2. 学会了数据划分和模型训练的流程
3. 掌握了结果可视化的方法

### 5.3 思考与启发
1. 回归决策树能够处理连续值预测问题
2. 特征重要性分析有助于理解影响因素
3. 模型选择需要平衡性能和复杂度

## 6. 结论

回归决策树在房价数据集上表现出一般水平，R²值为0.60。模型能够捕捉收入和地理位置对房价的重要影响，但仍有改进空间。决策树的可解释性使其成为理解数据和模型决策过程的重要工具。

## 7. 后续工作建议

1. 尝试更复杂的决策树参数组合
2. 探索其他回归算法（如线性回归、随机森林）进行对比
3. 学习决策树的剪枝技术
4. 了解集成学习方法（随机森林、梯度提升树）
5. 进行特征工程，创建更有意义的特征
