import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

plt.rcParams['font.sans-serif'] = ['SimHei']

# 1. & 2. 数据集加载
cancer = load_breast_cancer()
X = cancer.data
# sklearn默认乳腺癌数据集中0是恶性，1是良性。
y = 1 - cancer.target

print("乳腺癌数据集标签分布 (0=良性, 1=恶性):")
print(pd.Series(y).value_counts())

# 3. 数据划分：按8:2比例划分
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 模型构建与训练：
log_reg = LogisticRegression(max_iter=10000)
log_reg.fit(X_train, y_train)

# 5. 模型预测与评估
y_pred = log_reg.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
print("\n分类准确率 (Accuracy):", accuracy)
print("F1分数 (F1 Score):", f1)

# 6. 结果可视化：绘制评估指标柱状图
metrics_names = ['准确率 (Accuracy)', 'F1分数 (F1 Score)']
metrics_values = [accuracy, f1]

plt.figure(figsize=(6, 5))
bars = plt.bar(metrics_names, metrics_values, color=['#87CEEB', '#98FB98'], width=0.5)
plt.ylim(0, 1.1)
plt.ylabel("评估分数")
plt.title("逻辑回归模型评估结果")

# 在柱状图上方标出具体数值
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 4), ha='center', va='bottom')

plt.show()