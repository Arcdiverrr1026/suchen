"""
任务3：随机森林分类（基于乳腺癌数据集）
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
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
import seaborn as sns

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载乳腺癌数据集"""
    print("=" * 60)
    print("步骤1：加载乳腺癌数据集")
    print("=" * 60)

    # 加载数据集
    cancer = load_breast_cancer()
    X = cancer.data
    y = cancer.target

    # 查看数据集基本信息
    print(f"\n数据集基本信息：")
    print(f"  样本数量: {X.shape[0]}")
    print(f"  特征数量: {X.shape[1]}")
    print(f"  类别数量: {len(cancer.target_names)}")
    print(f"  类别名称: {cancer.target_names}")

    # 查看标签分布
    print(f"\n标签分布情况：")
    unique, counts = np.unique(y, return_counts=True)
    for label, count in zip(unique, counts):
        print(f"  {cancer.target_names[label]}: {count} 个样本 ({count/len(y)*100:.1f}%)")

    return X, y, cancer

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

def build_and_train_models(X_train, y_train, n_estimators=100, max_depth=5):
    """构建并训练随机森林和单棵决策树模型"""
    print("\n" + "=" * 60)
    print("步骤3：构建并训练模型")
    print("=" * 60)

    # 初始化随机森林模型
    rf_model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=42
    )

    # 初始化单棵决策树模型（用于对比）
    dt_model = DecisionTreeClassifier(
        max_depth=max_depth,
        random_state=42
    )

    print(f"\n随机森林模型参数：")
    print(f"  树数量: {n_estimators}")
    print(f"  最大深度: {max_depth}")
    print(f"  随机种子: 42")

    print(f"\n单棵决策树模型参数：")
    print(f"  最大深度: {max_depth}")
    print(f"  随机种子: 42")

    # 训练模型
    rf_model.fit(X_train, y_train)
    dt_model.fit(X_train, y_train)

    print(f"\n模型训练完成！")

    return rf_model, dt_model

def evaluate_models(rf_model, dt_model, X_test, y_test, cancer):
    """评估模型性能"""
    print("\n" + "=" * 60)
    print("步骤4：模型预测与评估")
    print("=" * 60)

    # 随机森林预测
    rf_pred = rf_model.predict(X_test)
    rf_accuracy = accuracy_score(y_test, rf_pred)
    rf_f1 = f1_score(y_test, rf_pred, average='weighted')

    # 单棵决策树预测
    dt_pred = dt_model.predict(X_test)
    dt_accuracy = accuracy_score(y_test, dt_pred)
    dt_f1 = f1_score(y_test, dt_pred, average='weighted')

    print(f"\n模型评估结果：")
    print(f"\n随机森林：")
    print(f"  准确率 (Accuracy): {rf_accuracy:.4f}")
    print(f"  F1分数 (F1-Score): {rf_f1:.4f}")

    print(f"\n单棵决策树：")
    print(f"  准确率 (Accuracy): {dt_accuracy:.4f}")
    print(f"  F1分数 (F1-Score): {dt_f1:.4f}")

    print(f"\n性能对比：")
    print(f"  准确率提升: {(rf_accuracy - dt_accuracy)*100:.2f}%")
    print(f"  F1分数提升: {(rf_f1 - dt_f1)*100:.2f}%")

    return rf_pred, rf_accuracy, rf_f1, dt_pred, dt_accuracy, dt_f1

def visualize_results(rf_model, cancer, rf_accuracy, dt_accuracy, rf_f1, dt_f1):
    """可视化结果"""
    print("\n" + "=" * 60)
    print("步骤5：结果可视化")
    print("=" * 60)

    # 创建图形
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 1. 绘制特征重要性
    feature_importance = rf_model.feature_importances_
    sorted_idx = np.argsort(feature_importance)

    # 只显示前10个最重要的特征
    top_n = 10
    top_idx = sorted_idx[-top_n:]

    axes[0].barh(range(top_n),
                 feature_importance[top_idx],
                 align='center',
                 color='skyblue',
                 edgecolor='black')
    axes[0].set_yticks(range(top_n))
    axes[0].set_yticklabels([cancer.feature_names[i] for i in top_idx])
    axes[0].set_xlabel('特征重要性')
    axes[0].set_title('随机森林特征重要性分析\n(Top 10)', fontsize=14, fontweight='bold')

    # 2. 绘制模型对比柱状图
    models = ['单棵决策树', '随机森林']
    x = np.arange(len(models))
    width = 0.35

    # 准确率对比
    accuracy_scores = [dt_accuracy, rf_accuracy]
    f1_scores = [dt_f1, rf_f1]

    bars1 = axes[1].bar(x - width/2, accuracy_scores, width,
                        label='准确率', color='skyblue', edgecolor='black')
    bars2 = axes[1].bar(x + width/2, f1_scores, width,
                        label='F1分数', color='lightcoral', edgecolor='black')

    axes[1].set_xlabel('模型', fontsize=12)
    axes[1].set_ylabel('分数', fontsize=12)
    axes[1].set_title('模型性能对比', fontsize=14, fontweight='bold')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(models)
    axes[1].legend()
    axes[1].set_ylim(0.9, 1.0)  # 调整y轴范围以突出差异

    # 在柱状图上添加数值标签
    for bar in bars1:
        height = bar.get_height()
        axes[1].annotate(f'{height:.4f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9)

    for bar in bars2:
        height = bar.get_height()
        axes[1].annotate(f'{height:.4f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig('task3_results.png', dpi=300, bbox_inches='tight')
    print(f"\n结果图已保存为 'task3_results.png'")

    # 3. 绘制特征重要性详情
    print(f"\n特征重要性详情 (Top 10)：")
    for i in top_idx:
        print(f"  {cancer.feature_names[i]}: {feature_importance[i]:.4f}")

def run_experiment():
    """运行完整实验"""
    print("\n" + "=" * 80)
    print("任务3：随机森林分类（基于乳腺癌数据集）")
    print("=" * 80)

    # 1. 加载数据
    X, y, cancer = load_data()

    # 2. 划分数据
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 3. 构建并训练模型
    rf_model, dt_model = build_and_train_models(X_train, y_train)

    # 4. 评估模型
    rf_pred, rf_accuracy, rf_f1, dt_pred, dt_accuracy, dt_f1 = evaluate_models(
        rf_model, dt_model, X_test, y_test, cancer
    )

    # 5. 可视化结果
    visualize_results(rf_model, cancer, rf_accuracy, dt_accuracy, rf_f1, dt_f1)

    # 实验总结
    print("\n" + "=" * 60)
    print("实验总结")
    print("=" * 60)
    print(f"\n1. 模型性能：")
    print(f"   - 随机森林准确率: {rf_accuracy:.4f}")
    print(f"   - 随机森林F1分数: {rf_f1:.4f}")
    print(f"   - 单棵决策树准确率: {dt_accuracy:.4f}")
    print(f"   - 单棵决策树F1分数: {dt_f1:.4f}")

    print(f"\n2. 关键发现：")
    print(f"   - 随机森林通常优于单棵决策树")
    print(f"   - 集成学习能够有效提升模型性能")
    print(f"   - 特征重要性分析有助于理解数据")

    print(f"\n3. 模型优势：")
    print(f"   - 能够处理高维数据")
    print(f"   - 不容易过拟合")
    print(f"   - 能够评估特征重要性")

    print(f"\n4. 潜在改进方向：")
    print(f"   - 调整树数量和最大深度参数")
    print(f"   - 使用交叉验证选择最优参数")
    print(f"   - 尝试其他集成方法（如AdaBoost）")

    return rf_model, rf_accuracy, rf_f1

if __name__ == "__main__":
    rf_model, rf_accuracy, rf_f1 = run_experiment()
