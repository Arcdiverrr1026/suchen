import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer, load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 设置中文字体，防止图表中文显示为方块
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

print("="*40)
print("第一部分：朴素贝叶斯分类实验（乳腺癌数据集）")
print("="*40)

# 1. 数据集加载
cancer_data = load_breast_cancer()
X_cancer = cancer_data.data
y_cancer = cancer_data.target
print(f"乳腺癌数据集形状: 样本数={X_cancer.shape[0]}, 特征数={X_cancer.shape[1]}")
print(f"标签分布: 0(恶性)={np.sum(y_cancer==0)}, 1(良性)={np.sum(y_cancer==1)}")

# 2. 数据划分 (8:2)
X_train_nb, X_test_nb, y_train_nb, y_test_nb = train_test_split(
    X_cancer, y_cancer, test_size=0.2, random_state=42
)

# 3. 模型构建与训练
nb_model = GaussianNB()
nb_model.fit(X_train_nb, y_train_nb)

# 4. 模型预测与评估
y_pred_nb = nb_model.predict(X_test_nb)
acc_nb = accuracy_score(y_test_nb, y_pred_nb)
prec_nb = precision_score(y_test_nb, y_pred_nb)
rec_nb = recall_score(y_test_nb, y_pred_nb)
f1_nb = f1_score(y_test_nb, y_pred_nb)

print(f"朴素贝叶斯评估结果:\n准确率: {acc_nb:.4f}\n精确率: {prec_nb:.4f}\n召回率: {rec_nb:.4f}\nF1分数: {f1_nb:.4f}\n")

# 5. 结果可视化
metrics_names = ['准确率', '精确率', '召回率', 'F1分数']
metrics_values = [acc_nb, prec_nb, rec_nb, f1_nb]

plt.figure(figsize=(8, 5))
plt.bar(metrics_names, metrics_values, color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'])
plt.ylim(0.8, 1.0) # 设置y轴范围使差异更明显
plt.title('朴素贝叶斯模型评估指标 (乳腺癌数据集)')
plt.ylabel('分数')
for i, v in enumerate(metrics_values):
    plt.text(i, v + 0.01, f"{v:.4f}", ha='center', va='bottom')
plt.show()


print("="*40)
print("第二部分：K 近邻（KNN）分类实验（鸢尾花数据集）")
print("="*40)

# 1. 数据集加载
iris_data = load_iris()
X_iris = iris_data.data
y_iris = iris_data.target
print(f"鸢尾花数据集形状: 样本数={X_iris.shape[0]}, 特征数={X_iris.shape[1]}")

# 2. 数据预处理 (标准化)
scaler = StandardScaler()
X_iris_scaled = scaler.fit_transform(X_iris)

# 3. 数据划分 (8:2)
X_train_knn, X_test_knn, y_train_knn, y_test_knn = train_test_split(
    X_iris_scaled, y_iris, test_size=0.2, random_state=42
)

# 4. 模型构建与训练 (默认 K=5)
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_knn, y_train_knn)

# 5. 模型预测与评估
y_pred_knn = knn_model.predict(X_test_knn)
# 由于是多分类，使用 macro 平均计算精确率、召回率和 F1
acc_knn = accuracy_score(y_test_knn, y_pred_knn)
prec_knn = precision_score(y_test_knn, y_pred_knn, average='macro')
rec_knn = recall_score(y_test_knn, y_pred_knn, average='macro')
f1_knn = f1_score(y_test_knn, y_pred_knn, average='macro')

print(f"KNN(K=5)评估结果:\n准确率: {acc_knn:.4f}\n精确率(Macro): {prec_knn:.4f}\n召回率(Macro): {rec_knn:.4f}\nF1分数(Macro): {f1_knn:.4f}\n")

# 6. 结果可视化：绘制 K 值与准确率的关系曲线
k_values = range(1, 20)
accuracies = []
for k in k_values:
    temp_knn = KNeighborsClassifier(n_neighbors=k)
    temp_knn.fit(X_train_knn, y_train_knn)
    accuracies.append(accuracy_score(y_test_knn, temp_knn.predict(X_test_knn)))

plt.figure(figsize=(8, 5))
plt.plot(k_values, accuracies, marker='o', linestyle='-', color='#DD8452')
plt.title('KNN 模型中 K 值与准确率的关系曲线 (鸢尾花数据集)')
plt.xlabel('K 值')
plt.ylabel('测试集准确率')
plt.xticks(k_values)
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
