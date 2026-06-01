from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 1. 加载数据集
iris = load_iris()
X, y = iris.data, iris.target

# 2. 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# 一、原始默认参数模型
# =========================
model_default = DecisionTreeClassifier(random_state=42)
model_default.fit(X_train, y_train)
y_pred_default = model_default.predict(X_test)

accuracy_default = accuracy_score(y_test, y_pred_default)
print(f"默认参数模型准确率: {accuracy_default:.2f}")


# =========================
# 二、单个参数调优：max_depth
# =========================
max_depth_values = [2, 3, 4, 5, None]
depth_scores = []

for depth in max_depth_values:
    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    depth_scores.append(acc)
    print(f"max_depth={depth}, 准确率={acc:.2f}")

plt.figure(figsize=(8, 5))
plt.plot([str(d) for d in max_depth_values], depth_scores, marker='o')
plt.xlabel("max_depth")
plt.ylabel("Accuracy")
plt.title("不同 max_depth 对准确率的影响")
plt.grid(True)
plt.show()


# =========================
# 三、单个参数调优：criterion
# =========================
criterion_values = ["gini", "entropy"]
criterion_scores = []

for criterion in criterion_values:
    model = DecisionTreeClassifier(
        criterion=criterion,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    criterion_scores.append(acc)
    print(f"criterion={criterion}, 准确率={acc:.2f}")

plt.figure(figsize=(6, 5))
plt.bar(criterion_values, criterion_scores)
plt.xlabel("criterion")
plt.ylabel("Accuracy")
plt.title("不同 criterion 对准确率的影响")
plt.ylim(0, 1.1)
plt.show()


# =========================
# 四、单个参数调优：min_samples_split
# =========================
min_samples_split_values = [2, 3, 4, 5, 10]
split_scores = []

for split in min_samples_split_values:
    model = DecisionTreeClassifier(
        min_samples_split=split,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    split_scores.append(acc)
    print(f"min_samples_split={split}, 准确率={acc:.2f}")

plt.figure(figsize=(8, 5))
plt.plot(min_samples_split_values, split_scores, marker='o')
plt.xlabel("min_samples_split")
plt.ylabel("Accuracy")
plt.title("不同 min_samples_split 对准确率的影响")
plt.grid(True)
plt.show()


# =========================
# 五、单个参数调优：min_samples_leaf
# =========================
min_samples_leaf_values = [1, 2, 3, 4, 5]
leaf_scores = []

for leaf in min_samples_leaf_values:
    model = DecisionTreeClassifier(
        min_samples_leaf=leaf,
        random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    leaf_scores.append(acc)
    print(f"min_samples_leaf={leaf}, 准确率={acc:.2f}")

plt.figure(figsize=(8, 5))
plt.plot(min_samples_leaf_values, leaf_scores, marker='o')
plt.xlabel("min_samples_leaf")
plt.ylabel("Accuracy")
plt.title("不同 min_samples_leaf 对准确率的影响")
plt.grid(True)
plt.show()


# =========================
# 六、组合参数调优
# =========================
results = []

for criterion in ["gini", "entropy"]:
    for depth in [2, 3, 4, 5, None]:
        for split in [2, 3, 4, 5]:
            for leaf in [1, 2, 3]:
                model = DecisionTreeClassifier(
                    criterion=criterion,
                    max_depth=depth,
                    min_samples_split=split,
                    min_samples_leaf=leaf,
                    random_state=42
                )
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                acc = accuracy_score(y_test, y_pred)

                results.append({
                    "criterion": criterion,
                    "max_depth": depth,
                    "min_samples_split": split,
                    "min_samples_leaf": leaf,
                    "accuracy": acc
                })

# 转换为 DataFrame，方便查看
results_df = pd.DataFrame(results)

# 按准确率从高到低排序
results_df = results_df.sort_values(by="accuracy", ascending=False)

print("\n参数组合调优结果：")
print(results_df)

print("\n最优参数组合：")
best_params = results_df.iloc[0]
print(best_params)


import pandas as pd

# =========================
# 七、使用最优参数重新训练模型
# =========================

best_params = results_df.iloc[0]

# 处理 max_depth
# DataFrame 中的 None 可能会变成 NaN，因此这里要手动转换回来
best_max_depth = best_params["max_depth"]

if pd.isna(best_max_depth):
    best_max_depth = None
else:
    best_max_depth = int(best_max_depth)

best_model = DecisionTreeClassifier(
    criterion=best_params["criterion"],
    max_depth=best_max_depth,
    min_samples_split=int(best_params["min_samples_split"]),
    min_samples_leaf=int(best_params["min_samples_leaf"]),
    random_state=42
)

best_model.fit(X_train, y_train)
y_pred_best = best_model.predict(X_test)

best_accuracy = accuracy_score(y_test, y_pred_best)
print(f"\n最优模型准确率: {best_accuracy:.2f}")

print("\n最优参数组合：")
print(f"criterion: {best_params['criterion']}")
print(f"max_depth: {best_max_depth}")
print(f"min_samples_split: {int(best_params['min_samples_split'])}")
print(f"min_samples_leaf: {int(best_params['min_samples_leaf'])}")
print(f"accuracy: {best_params['accuracy']:.2f}")


# =========================
# 八、可视化最优决策树
# =========================
plt.figure(figsize=(12, 8))
plot_tree(
    best_model,
    feature_names=iris.feature_names,
    class_names=iris.target_names,
    filled=True
)
plt.title("最优参数下的决策树")
plt.show()