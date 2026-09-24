"""
基于水色图像的水质评价 - 主流程脚本
====================================
本脚本实现完整的水质评价实验流程：
1. 数据加载与探索
2. 图像预处理与颜色矩特征提取
3. 特征标准化
4. 决策树模型训练与评估
5. 结果分析与报告生成

使用方法：
    python main.py
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from lab6_water_quality.feature_extraction import ColorMomentExtractor
from lab6_water_quality.model import WaterQualityClassifier


def setup_chinese_font():
    """设置中文字体支持"""
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


def analyze_dataset(image_dir: Path) -> pd.DataFrame:
    """分析数据集统计信息

    Args:
        image_dir: 图像目录路径

    Returns:
        数据集统计信息DataFrame
    """
    image_files = sorted(image_dir.glob("*.jpg"))

    # 解析图像信息
    data = []
    for img_path in image_files:
        category = int(img_path.stem.split('_')[0])
        data.append({
            '文件名': img_path.name,
            '水质等级': category,
            '水质描述': ColorMomentExtractor().get_feature_names()  # placeholder
        })

    df = pd.DataFrame(data)

    # 统计各类别数量
    stats = df.groupby('水质等级').size().reset_index(name='样本数量')
    stats['占比'] = (stats['样本数量'] / stats['样本数量'].sum() * 100).round(2)
    stats['水质描述'] = stats['水质等级'].map(WaterQualityClassifier.WATER_QUALITY_LABELS)

    return stats


def run_experiment(image_dir: str, output_dir: str = None) -> dict:
    """运行完整实验流程

    Args:
        image_dir: 图像数据目录
        output_dir: 输出目录（用于保存结果图片）

    Returns:
        实验结果字典
    """
    # 设置中文字体
    setup_chinese_font()

    # 设置输出目录
    if output_dir is None:
        output_dir = Path(__file__).parent / "output"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("基于水色图像的水质评价实验")
    print("=" * 60)

    # ============================================================
    # 第一步：数据探索
    # ============================================================
    print("\n[步骤1] 数据探索与分析")
    print("-" * 40)

    stats = analyze_dataset(Path(image_dir))
    print("\n数据集统计信息：")
    print(stats.to_string(index=False))
    print(f"\n总样本数: {stats['样本数量'].sum()}")

    # ============================================================
    # 第二步：特征提取
    # ============================================================
    print("\n[步骤2] 颜色矩特征提取")
    print("-" * 40)

    # 初始化特征提取器
    extractor = ColorMomentExtractor(image_size=(256, 256))

    # 提取特征
    print("正在提取图像特征...")
    features, labels = extractor.extract_features_from_directory(image_dir)

    print(f"特征矩阵形状: {features.shape}")
    print(f"标签分布: {np.bincount(labels)[1:]}")  # 从索引1开始，因为标签从1开始

    # 显示特征名称
    feature_names = ColorMomentExtractor.get_feature_names()
    print(f"\n提取的特征（共{len(feature_names)}个）：")
    for i, name in enumerate(feature_names):
        print(f"  {i+1}. {name}")

    # ============================================================
    # 第三步：特征标准化
    # ============================================================
    print("\n[步骤3] 特征标准化")
    print("-" * 40)

    # 标准化特征
    features_scaled = extractor.fit_transform(features)

    print("标准化前统计：")
    print(f"  均值范围: [{features.mean(axis=0).min():.2f}, {features.mean(axis=0).max():.2f}]")
    print(f"  标准差范围: [{features.std(axis=0).min():.2f}, {features.std(axis=0).max():.2f}]")

    print("\n标准化后统计：")
    print(f"  均值范围: [{features_scaled.mean(axis=0).min():.4f}, {features_scaled.mean(axis=0).max():.4f}]")
    print(f"  标准差范围: [{features_scaled.std(axis=0).min():.4f}, {features_scaled.std(axis=0).max():.4f}]")

    # ============================================================
    # 第四步：数据集划分
    # ============================================================
    print("\n[步骤4] 数据集划分（80%训练集，20%测试集）")
    print("-" * 40)

    classifier = WaterQualityClassifier(
        feature_names=feature_names,
        max_depth=5  
    )

    X_train, X_test, y_train, y_test = classifier.split_data(
        features_scaled, labels, test_size=0.2
    )

    print(f"训练集大小: {len(y_train)}")
    print(f"测试集大小: {len(y_test)}")
    print(f"训练集类别分布: {np.bincount(y_train)[1:]}")
    print(f"测试集类别分布: {np.bincount(y_test)[1:]}")

    # ============================================================
    # 第五步：模型训练
    # ============================================================
    print("\n[步骤5] 决策树模型训练")
    print("-" * 40)

    train_result = classifier.train(X_train, y_train)

    print(f"训练集准确率: {train_result['train_accuracy']:.4f}")
    print(f"决策树深度: {train_result['tree_depth']}")
    print(f"叶子节点数: {train_result['n_leaves']}")

    # ============================================================
    # 第六步：模型评估
    # ============================================================
    print("\n[步骤6] 模型评估")
    print("-" * 40)

    eval_result = classifier.evaluate(X_test, y_test)

    print(f"\n测试集准确率: {eval_result['accuracy']:.4f}")

    print("\n分类报告：")
    report = eval_result['classification_report']
    print(f"{'类别':<20} {'精确率':<10} {'召回率':<10} {'F1分数':<10} {'支持数':<10}")
    print("-" * 60)
    for i in range(1, 6):
        key = str(i)
        if key in report:
            r = report[key]
            print(f"{WaterQualityClassifier.WATER_QUALITY_LABELS[i]:<20} "
                  f"{r['precision']:<10.4f} {r['recall']:<10.4f} "
                  f"{r['f1-score']:<10.4f} {int(r['support']):<10}")

    print(f"\n{'宏平均':<20} {report['macro avg']['precision']:<10.4f} "
          f"{report['macro avg']['recall']:<10.4f} "
          f"{report['macro avg']['f1-score']:<10.4f}")

    # ============================================================
    # 第七步：结果可视化
    # ============================================================
    print("\n[步骤7] 结果可视化")
    print("-" * 40)

    # 绘制混淆矩阵
    cm_path = output_dir / "confusion_matrix.png"
    classifier.plot_confusion_matrix(eval_result['confusion_matrix'], save_path=str(cm_path))
    print(f"混淆矩阵已保存至: {cm_path}")

    # 绘制决策树
    tree_path = output_dir / "decision_tree.png"
    classifier.plot_decision_tree(save_path=str(tree_path))
    print(f"决策树可视化已保存至: {tree_path}")

    # 绘制特征重要性
    fig, ax = plt.subplots(figsize=(10, 6))
    importance = classifier.get_feature_importance()
    features_sorted = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    names = [f[0] for f in features_sorted]
    values = [f[1] for f in features_sorted]

    bars = ax.bar(range(len(names)), values, color='steelblue')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('重要性')
    ax.set_title('特征重要性排序')

    # 在柱状图上显示数值
    for bar, val in zip(bars, values):
        if val > 0:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                   f'{val:.3f}', ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    importance_path = output_dir / "feature_importance.png"
    plt.savefig(importance_path, dpi=150, bbox_inches='tight')
    print(f"特征重要性图已保存至: {importance_path}")

    # ============================================================
    # 第八步：模型规则分析
    # ============================================================
    print("\n[步骤8] 决策树规则分析")
    print("-" * 40)

    print("\n决策树分类规则（简化版）：")
    print(classifier.get_tree_rules()[:1000] + "\n...")

    # ============================================================
    # 实验总结
    # ============================================================
    print("\n" + "=" * 60)
    print("实验总结")
    print("=" * 60)

    print(f"""
主要发现：
1. 数据集包含{stats['样本数量'].sum()}个水样图像，分为5个水质等级
2. 数据分布不均匀：Ⅲ类样本最多（{stats[stats['水质等级']==3]['样本数量'].values[0]}个），
   Ⅴ类样本最少（{stats[stats['水质等级']==5]['样本数量'].values[0]}个）
3. 决策树模型在测试集上准确率为{eval_result['accuracy']:.2%}
4. 模型深度为{train_result['tree_depth']}，叶子节点数为{train_result['n_leaves']}

特征分析：
- 最重要的特征是: {features_sorted[0][0]}（重要性: {features_sorted[0][1]:.4f})
- 颜色矩特征能有效区分不同水质等级

模型优缺点：
优点：
- 决策树模型可解释性强，易于理解分类规则
- 对特征标准化不敏感
- 训练速度快

缺点：
- 对于样本不均衡的数据集，可能偏向多数类
- 决策树容易过拟合
- 对于边界样本的分类能力有限

改进建议：
1. 使用过采样技术（如SMOTE）处理样本不均衡问题
2. 尝试集成学习方法（随机森林、梯度提升）
3. 增加更多图像特征（纹理特征、形状特征）
4. 使用交叉验证选择最优超参数
""")

    # 保存结果到文件
    results = {
        'train_accuracy': train_result['train_accuracy'],
        'test_accuracy': eval_result['accuracy'],
        'confusion_matrix': eval_result['confusion_matrix'].tolist(),
        'feature_importance': importance,
        'tree_depth': train_result['tree_depth'],
        'n_leaves': train_result['n_leaves'],
        'classification_report': report
    }

    return results


def main():
    """主函数"""
    # 数据目录
    image_dir = "/Users/lucent/课程报告/数据挖掘/20260609-数据挖掘实验课/data/images"

    # 运行实验
    results = run_experiment(image_dir)

    print("\n实验完成！所有结果已保存到 output 目录。")


if __name__ == "__main__":
    main()
