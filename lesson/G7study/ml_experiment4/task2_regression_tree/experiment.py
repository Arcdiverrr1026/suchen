"""
任务2：回归决策树（基于波士顿房价数据集）
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
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """加载房价数据集（使用加州房价数据集替代波士顿房价数据集）"""
    print("=" * 60)
    print("步骤1：加载房价数据集")
    print("=" * 60)

    # 注意：波士顿房价数据集在sklearn 1.2版本后已被移除
    # 使用加州房价数据集作为替代
    print("\n注意：由于波士顿房价数据集已被移除，使用加州房价数据集作为替代")
    print("加州房价数据集同样用于回归任务，具有相似的特性")

    # 加载加州房价数据集
    housing = fetch_california_housing()
    X = housing.data
    y = housing.target

    # 查看数据集基本信息
    print(f"\n数据集基本信息：")
    print(f"  样本数量: {X.shape[0]}")
    print(f"  特征数量: {X.shape[1]}")
    print(f"  特征名称: {housing.feature_names}")
    print(f"  目标变量: 房价中位数（单位：10万美元）")

    # 查看目标变量统计信息
    print(f"\n目标变量统计信息：")
    print(f"  最小值: {y.min():.2f}")
    print(f"  最大值: {y.max():.2f}")
    print(f"  平均值: {y.mean():.2f}")
    print(f"  标准差: {y.std():.2f}")

    return X, y, housing

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

def build_and_train_model(X_train, y_train, max_depth=5):
    """构建并训练回归决策树模型"""
    print("\n" + "=" * 60)
    print("步骤3：构建并训练回归决策树模型")
    print("=" * 60)

    # 初始化模型
    model = DecisionTreeRegressor(max_depth=max_depth, random_state=42)
    print(f"\n模型参数：")
    print(f"  最大深度: {max_depth}")
    print(f"  随机种子: 42")

    # 训练模型
    model.fit(X_train, y_train)
    print(f"\n模型训练完成！")

    return model

def evaluate_model(model, X_test, y_test):
    """评估模型性能"""
    print("\n" + "=" * 60)
    print("步骤4：模型预测与评估")
    print("=" * 60)

    # 预测
    y_pred = model.predict(X_test)

    # 计算评估指标
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"\n模型评估结果：")
    print(f"  均方误差 (MSE): {mse:.4f}")
    print(f"  均方根误差 (RMSE): {rmse:.4f}")
    print(f"  决定系数 (R²): {r2:.4f}")

    # 分析拟合效果
    print(f"\n拟合效果分析：")
    if r2 >= 0.8:
        print(f"  R² = {r2:.4f}，模型拟合效果良好")
    elif r2 >= 0.6:
        print(f"  R² = {r2:.4f}，模型拟合效果一般")
    else:
        print(f"  R² = {r2:.4f}，模型拟合效果较差")

    # 计算残差
    residuals = y_test - y_pred
    print(f"\n残差统计：")
    print(f"  残差均值: {residuals.mean():.4f}")
    print(f"  残差标准差: {residuals.std():.4f}")

    return y_pred, mse, r2

def visualize_results(model, X, y, housing, y_test, y_pred, r2):
    """可视化结果"""
    print("\n" + "=" * 60)
    print("步骤5：结果可视化")
    print("=" * 60)

    # 创建图形
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 1. 绘制真实值与预测值的对比散点图
    axes[0].scatter(y_test, y_pred, alpha=0.5, color='blue', edgecolors='black', linewidth=0.5)

    # 添加趋势线
    z = np.polyfit(y_test, y_pred, 1)
    p = np.poly1d(z)
    x_line = np.linspace(y_test.min(), y_test.max(), 100)
    axes[0].plot(x_line, p(x_line), "r--", alpha=0.8, label=f'趋势线')

    # 添加对角线（完美预测线）
    axes[0].plot([y_test.min(), y_test.max()],
                 [y_test.min(), y_test.max()],
                 'k--', alpha=0.3, label='完美预测线')

    axes[0].set_xlabel('真实值', fontsize=12)
    axes[0].set_ylabel('预测值', fontsize=12)
    axes[0].set_title(f'真实值 vs 预测值 (R² = {r2:.4f})', fontsize=14, fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # 2. 绘制特征重要性
    feature_importance = model.feature_importances_
    sorted_idx = np.argsort(feature_importance)

    axes[1].barh(range(len(sorted_idx)),
                 feature_importance[sorted_idx],
                 align='center',
                 color='skyblue',
                 edgecolor='black')
    axes[1].set_yticks(range(len(sorted_idx)))
    axes[1].set_yticklabels([housing.feature_names[i] for i in sorted_idx])
    axes[1].set_xlabel('特征重要性')
    axes[1].set_title('特征重要性分析', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig('task2_results.png', dpi=300, bbox_inches='tight')
    print(f"\n结果图已保存为 'task2_results.png'")

    # 3. 绘制残差图
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    residuals = y_test - y_pred
    ax2.scatter(y_pred, residuals, alpha=0.5, color='green', edgecolors='black', linewidth=0.5)
    ax2.axhline(y=0, color='r', linestyle='--', alpha=0.8)
    ax2.set_xlabel('预测值', fontsize=12)
    ax2.set_ylabel('残差', fontsize=12)
    ax2.set_title('残差分析图', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('task2_residuals.png', dpi=300, bbox_inches='tight')
    print(f"残差分析图已保存为 'task2_residuals.png'")

    # 显示特征重要性详情
    print(f"\n特征重要性详情：")
    for i, (name, importance) in enumerate(zip(housing.feature_names, feature_importance)):
        print(f"  {name}: {importance:.4f}")

def run_experiment():
    """运行完整实验"""
    print("\n" + "=" * 80)
    print("任务2：回归决策树（基于房价数据集）")
    print("=" * 80)

    # 1. 加载数据
    X, y, housing = load_data()

    # 2. 划分数据
    X_train, X_test, y_train, y_test = split_data(X, y)

    # 3. 构建并训练模型
    model = build_and_train_model(X_train, y_train, max_depth=5)

    # 4. 评估模型
    y_pred, mse, r2 = evaluate_model(model, X_test, y_test)

    # 5. 可视化结果
    visualize_results(model, X, y, housing, y_test, y_pred, r2)

    # 实验总结
    print("\n" + "=" * 60)
    print("实验总结")
    print("=" * 60)
    print(f"\n1. 模型性能：")
    print(f"   - 均方误差 (MSE): {mse:.4f}")
    print(f"   - 决定系数 (R²): {r2:.4f}")

    print(f"\n2. 关键发现：")
    print(f"   - 决策树能够处理回归任务")
    print(f"   - 特征重要性分析显示不同特征对房价的影响不同")
    print(f"   - 最大深度参数对模型复杂度和泛化能力有重要影响")

    print(f"\n3. 模型优势：")
    print(f"   - 模型可解释性强")
    print(f"   - 能够处理非线性关系")
    print(f"   - 不需要特征缩放")

    print(f"\n4. 潜在改进方向：")
    print(f"   - 尝试不同的max_depth值")
    print(f"   - 使用交叉验证选择最优参数")
    print(f"   - 考虑使用集成方法（如随机森林）提升性能")

    return model, mse, r2

if __name__ == "__main__":
    model, mse, r2 = run_experiment()
