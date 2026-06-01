"""
任务1：分类决策树（基于鸢尾花数据集）
实验流程：
1. 库导入
2. 数据集加载
3. 数据划分
4. 模型构建与训练
5. 模型预测与评估
6. 结果可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载鸢尾花数据集"""
    print("=" * 60)
    print("步骤1：加载鸢尾花数据集")
    print("=" * 60)

    # 加载数据集
    iris = load_iris()
    X = iris.data
    y = iris.target

    # 查看数据集基本信息
    print(f"\n数据集基本信息：")
    print(f"  样本数量: {X.shape[0]}")
    print(f"  特征数量: {X.shape[1]}")
    print(f"  特征名称: {iris.feature_names}")
    print(f"  目标类别: {iris.target_names}")

    # 查看标签分布
    print(f"\n标签分布情况：")
    unique, counts = np.unique(y, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"  {iris.target_names[label]}: {count} 个样本 ({count/len(y)*100:.1f}%)")

    return X, y, iris

def split_data(X, y, test_size=0.2, random_state=42):
    """划分数据集"""
    print("\n" + "=" * 60)
    print("步骤2：划分数据集")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"\n数据划分结果：")
    print(f"  训练集样本数: {X_train.shape[0]}")
    print(f"  测试集样本数: {X_test.shape[0]}")
    print(f"  划分比例: {int((1-test_size)*100)}:{int(test_size*100)}")

    return X_train, X_test, y_train, y_test

def build_and_train_model(X_train, y_train, max_depth=3):
    """构建并训练分类决策树模型"""
    print("\n" + "=" * 60)
    print("步骤3：构建并训练分类决策树模型")
    print("=" * 60)

    # 初始化模型
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    print(f"\n模型参数：")
    print(f"  最大深度: {max_depth}")
    print(f"  随机种子: 42")

    # 训练模型
    model.fit(X_train, y_train)
    print(f"\n模型训练完成！")

    return model

def evaluate_model(model, X_test, y_test, iris):
    """评估模型性能"""
    print("\n" + "=" * 60)
    print("步骤4：模型预测与评估")
    print("=" * 60)

    # 预测
    y_pred = model.predict(X_test)

    # 计算评估指标
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_test, y_pred)

    print(f"\n模型评估结果：")
    print(f"  准确率 (Accuracy): {accuracy:.4f}")
    print(f"  F1分数 (F1-Score): {f1:.4f}")

    print(f"\n混淆矩阵：")
    print(conf_matrix)

    # 分析分类效果
    print(f"\n分类效果分析：")
    for i in range(len(iris.target_names)):
        precision = conf_matrix[i, i] / conf_matrix[:, i].sum() if conf_matrix[:, i].sum() > 0 else 0
        recall = conf_matrix[i, i] / conf_matrix[i, :].sum() if conf_matrix[i, :].sum() > 0 else 0
        print(f"  {iris.target_names[i]}:")
        print(f"    精确率: {precision:.4f}")
        print(f"    召回率: {recall:.4f}")

    return y_pred, accuracy, f1, conf_matrix

def visualize_results(model, X, y, iris, conf_matrix, accuracy):
    """可视化结果"""
    print("\n" + "=" * 60)
    print("步骤5：结果可视化")
    print("=" * 60)

    # 创建图形
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    # 1. 绘制决策树结构
    plt.sca(axes[0])
    plot_tree(model,
              feature_names=iris.feature_names,
              class_names=iris.target_names,
              filled=True,
              rounded=True,
              fontsize=10)
    axes[0].set_title('决策树结构可视化', fontsize=14, fontweight='bold')

    # 2. 绘制特征重要性
    feature_importance = model.feature_importances_
    sorted_idx = np.argsort(feature_importance)

    axes[1].barh(range(len(sorted_idx)),
                 feature_importance[sorted_idx],
                 align='center',
                 color='skyblue',
                 edgecolor='black')
    axes[1].set_yticks(range(len(sorted_idx)))
    axes[1].set_yticklabels([iris.feature_names[i] for i in sorted_idx])
    axes[1].set_xlabel('特征重要性')
    axes[1].set_title('特征重要性分析', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('task1_results.png', dpi=300, bbox_inches='tight')
    print(f"\n决策树结构图和特征重要性图已保存为 'task1_results.png'")

    # 3. 绘制混淆矩阵热力图
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.heatmap(conf_matrix,
                annot=True,
                fmt='d',
                cmap='Blues',
                xticklabels=iris.target_names,
                yticklabels=iris.target_names,
                ax=ax2)
    ax2.set_xlabel('预测标签', fontsize=12)
    ax2.set_ylabel('真实标签', fontsize=12)
    ax2.set_title(f'混淆矩阵 (准确率: {accuracy:.4f})', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('task1_confusion_matrix.png', dpi=300, bbox_inches='tight')
    print(f"混淆矩阵热力图已保存为 'task1_confusion_matrix.png'")

    # 显示特征重要性详情
    print(f"\n特征重要性详情：")
    for i, (name, importance) in enumerate(zip(iris.feature_names, feature_importance)):
        print(f"  {name}: {importance:.4f}")

def run_experiment():
    """运行完整实验"""
    print("\n" + "=" * 80)
    print("任务1：分类决策树（基于鸢尾花数据集）")
    print("=" * 80)

    # 1. 加载数据
    X, y, iris = load_data()

    # 2. 划分数据
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 3. 构建并训练模型
    model = build_and_train_model(X_train, y_train, max_depth=3)

    # 4. 评估模型
    y_pred, accuracy, f1, conf_matrix = evaluate_model(model, X_test, y_test, iris)

    # 5. 可视化结果
    visualize_results(model, X, y, iris, conf_matrix, accuracy)

    # 实验总结
    print("\n" + "=" * 60)
    print("实验总结")
    print("=" * 60)
    print(f"\n1. 模型性能：")
    print(f"   - 准确率: {accuracy:.4f}")
    print(f"   - F1分数: {f1:.4f}")

    print(f"\n2. 关键发现：")
    print(f"   - 决策树能够有效处理多分类问题")
    print(f"   - 特征重要性分析显示不同特征对分类的贡献不同")
    print(f"   - 最大深度参数对模型复杂度和泛化能力有重要影响")

    print(f"\n3. 模型优势：")
    print(f"   - 模型可解释性强，决策过程清晰")
    print(f"   - 能够处理非线性关系")
    print(f"   - 不需要特征缩放")

    print(f"\n4. 潜在改进方向：")
    print(f"   - 尝试不同的max_depth值")
    print(f"   - 使用交叉验证选择最优参数")
    print(f"   - 考虑使用集成方法提升性能")

    return model, accuracy, f1

if __name__ == "__main__":
    model, accuracy, f1 = run_experiment()
