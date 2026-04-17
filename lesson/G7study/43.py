import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 解决matplotlib画图时的中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. & 2. 数据集加载 (替换为从原始数据源读取)
data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep=r"\s+", skiprows=22, header=None)
X = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
y = raw_df.values[1::2, 2]

print("波士顿房价数据集特征数：", X.shape[1])
print("样本总数：", X.shape[0])

# 3. 数据划分：按8:2比例划分训练集和测试集，设置随机种子42
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 模型构建与训练
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
print("\n线性回归模型系数 (w):", lin_reg.coef_)
print("线性回归模型截距 (b):", lin_reg.intercept_)

# 5. 模型预测与评估
y_pred = lin_reg.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("\n均方误差 (MSE):", mse)
print("决定系数 (R2):", r2)

# 6. 结果可视化：真实值与预测值对比散点图
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.6, label='预测值 vs 真实值')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='理想预测线')
plt.xlabel("测试集真实房价")
plt.ylabel("模型预测房价")
plt.title("波士顿房价：线性回归预测效果")
plt.legend()
plt.show()