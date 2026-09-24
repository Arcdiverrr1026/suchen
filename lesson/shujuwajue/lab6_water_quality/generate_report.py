"""
实验报告生成器
==============
本模块生成包含实验流程和关键代码的分析报告。
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from lab6_water_quality.feature_extraction import ColorMomentExtractor
from lab6_water_quality.model import WaterQualityClassifier


def generate_report(image_dir: str, output_path: str = None):
    """生成实验报告

    Args:
        image_dir: 图像数据目录
        output_path: 报告输出路径
    """
    if output_path is None:
        output_path = Path(__file__).parent / "output" / "实验报告.md"
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(exist_ok=True)
    output_dir = output_path.parent

    # ============================================================
    # 收集实验数据
    # ============================================================
    image_dir = Path(image_dir)
    image_files = sorted(image_dir.glob("*.jpg"))

    # 统计数据
    categories = {}
    for img_path in image_files:
        cat = int(img_path.stem.split('_')[0])
        categories[cat] = categories.get(cat, 0) + 1

    # 提取特征
    extractor = ColorMomentExtractor(image_size=(256, 256))
    features, labels = extractor.extract_features_from_directory(str(image_dir))
    features_scaled = extractor.fit_transform(features)

    # 训练模型
    classifier = WaterQualityClassifier(
        feature_names=ColorMomentExtractor.get_feature_names(),
        max_depth=5
    )
    X_train, X_test, y_train, y_test = classifier.split_data(features_scaled, labels, test_size=0.2)
    train_result = classifier.train(X_train, y_train)
    eval_result = classifier.evaluate(X_test, y_test)

    # 获取特征重要性
    importance = classifier.get_feature_importance()
    sorted_importance = sorted(importance.items(), key=lambda x: x[1], reverse=True)

    # ============================================================
    # 输出表格到 CSV 文件
    # ============================================================

    # 1. 数据集分布表
    total = sum(categories.values())
    dist_data = []
    for cat in sorted(categories.keys()):
        count = categories[cat]
        desc = WaterQualityClassifier.WATER_QUALITY_LABELS[cat]
        pct = count / total * 100
        dist_data.append({
            "水质等级": cat,
            "描述": desc,
            "样本数量": count,
            "占比(%)": round(pct, 1)
        })
    pd.DataFrame(dist_data).to_csv(output_dir / "数据集分布.csv", index=False, encoding="utf-8-sig")

    # 2. 分类报告表
    report_data = eval_result['classification_report']
    cls_data = []
    for i in range(1, 6):
        key = str(i)
        if key in report_data:
            r = report_data[key]
            label = WaterQualityClassifier.WATER_QUALITY_LABELS[i]
            cls_data.append({
                "类别": label,
                "精确率": round(r['precision'], 4),
                "召回率": round(r['recall'], 4),
                "F1分数": round(r['f1-score'], 4),
                "支持数": int(r['support'])
            })
    pd.DataFrame(cls_data).to_csv(output_dir / "分类报告.csv", index=False, encoding="utf-8-sig")

    # 3. 混淆矩阵表
    cm = eval_result['confusion_matrix']
    class_names = [WaterQualityClassifier.WATER_QUALITY_LABELS[i] for i in range(1, 6)]
    cm_df = pd.DataFrame(cm, index=[f"真实:{c}" for c in class_names],
                          columns=[f"预测:{c}" for c in class_names])
    cm_df.to_csv(output_dir / "混淆矩阵.csv", encoding="utf-8-sig")

    # 4. 特征重要性表
    imp_data = []
    for rank, (feat, imp) in enumerate(sorted_importance, 1):
        if imp > 0:
            imp_data.append({"排名": rank, "特征": feat, "重要性": round(imp, 4)})
    pd.DataFrame(imp_data).to_csv(output_dir / "特征重要性.csv", index=False, encoding="utf-8-sig")

    print(f"表格已输出至: {output_dir}")
    print("  - 数据集分布.csv")
    print("  - 分类报告.csv")
    print("  - 混淆矩阵.csv")
    print("  - 特征重要性.csv")

    # ============================================================
    # 生成报告内容
    # ============================================================
    report = f"""# 基于水色图像的水质评价实验报告

**实验日期**: 2026年6月9日
**课程名称**: 数据挖掘
**实验名称**: 基于水色图像的水质评价

---

## 一、实验目的

1. 掌握基于图像颜色特征（颜色矩）提取与分析的基本原理与实现流程
2. 掌握水样图像预处理、特征标准化与决策树分类模型构建的完整数据挖掘方法
3. 能够根据模型评价指标解读水质分类效果，并形成对水产养殖场景的应用思考

## 二、实验环境

- **Python版本**: 3.12+
- **主要库**: scikit-learn, numpy, matplotlib, Pillow, pandas
- **数据集**: 水样图像数据集（共{len(image_files)}张图像）

## 三、实验步骤与代码

### 3.1 数据探索与分析

首先，我们对数据集进行探索性分析，了解数据分布情况。

```python
import numpy as np
from pathlib import Path

# 加载图像数据
image_dir = Path("{image_dir}")
image_files = sorted(image_dir.glob("*.jpg"))

# 统计各类别数量
categories = {{}}
for img_path in image_files:
    cat = int(img_path.stem.split('_')[0])
    categories[cat] = categories.get(cat, 0) + 1

print("数据集分布：")
for cat, count in sorted(categories.items()):
    print(f"  水质等级 {{cat}}: {{count}} 张图像")
```

**数据集统计结果**:

| 水质等级 | 描述 | 样本数量 | 占比 |
|---------|------|---------|------|
"""

    for cat in sorted(categories.keys()):
        count = categories[cat]
        desc = WaterQualityClassifier.WATER_QUALITY_LABELS[cat]
        pct = count / total * 100
        report += f"| {cat} | {desc} | {count} | {pct:.1f}% |\n"

    report += f"""
**总样本数**: {total}

**分析**: 数据分布存在明显的不均衡性，Ⅲ类（轻度污染）样本最多，占{categories.get(3, 0)/total*100:.1f}%，而Ⅴ类（重度污染）样本最少，仅{categories.get(5, 0)/total*100:.1f}%。这种不均衡可能影响模型对少数类的识别能力。

### 3.2 图像预处理与颜色矩特征提取

**颜色矩原理**:

颜色矩是一种有效的颜色特征描述方法，通过计算颜色分布的矩来表征图像的颜色特征：
- **一阶矩（均值）**: 反映颜色的平均强度
- **二阶矩（标准差）**: 反映颜色的分布范围
- **三阶矩（偏度）**: 反映颜色分布的对称性

对RGB三个通道分别计算这三个矩，共得到9个特征。

```python
import numpy as np
from PIL import Image

def extract_color_moments(img_array):
    \"\"\"
    提取颜色矩特征
    对RGB三个通道分别计算一阶矩（均值）、二阶矩（标准差）、三阶矩（偏度）
    \"\"\"
    features = []

    # 对每个颜色通道计算颜色矩
    for channel in range(3):  # R, G, B
        channel_data = img_array[:, :, channel].flatten()

        # 一阶矩：均值 - 反映颜色的平均强度
        mean = np.mean(channel_data)

        # 二阶矩：标准差 - 反映颜色的分布范围
        std = np.std(channel_data)

        # 三阶矩：偏度 - 反映颜色分布的对称性
        # 偏度 = E[(X-μ)³] / σ³
        if std > 0:
            skewness = np.mean(((channel_data - mean) / std) ** 3)
        else:
            skewness = 0.0

        features.extend([mean, std, skewness])

    return np.array(features)

def load_and_preprocess(image_path, target_size=(256, 256)):
    \"\"\"加载并预处理图像\"\"\"
    # 加载图像并转换为RGB模式
    img = Image.open(image_path).convert('RGB')
    # 缩放到统一尺寸
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    # 转换为numpy数组
    return np.array(img, dtype=np.float64)
```

**提取的特征列表**:

| 序号 | 特征名称 | 说明 |
|-----|---------|------|
"""

    feature_names = ColorMomentExtractor.get_feature_names()
    for i, name in enumerate(feature_names):
        channel, moment = name.split('_')
        moment_desc = {'均值': '颜色平均强度', '标准差': '颜色分布范围', '偏度': '颜色分布对称性'}[moment]
        report += f"| {i+1} | {name} | {channel}通道{moment_desc} |\n"

    report += f"""
**特征提取结果**:
- 特征矩阵形状: {features.shape}
- 共提取{features.shape[0]}个样本，每个样本{features.shape[1]}个特征

### 3.3 特征标准化

为了消除不同特征之间的量纲差异，对特征进行标准化处理（Z-score标准化）：

```python
from sklearn.preprocessing import StandardScaler

# 初始化标准化器
scaler = StandardScaler()

# 拟合并转换特征
features_scaled = scaler.fit_transform(features)

# 标准化后特征均值为0，标准差为1
print(f"标准化后均值范围: [{{features_scaled.mean(axis=0).min():.4f}}, "
      f"{{features_scaled.mean(axis=0).max():.4f}}]")
print(f"标准化后标准差范围: [{{features_scaled.std(axis=0).min():.4f}}, "
      f"{{features_scaled.std(axis=0).max():.4f}}]")
```

**标准化前后对比**:

| 统计量 | 标准化前 | 标准化后 |
|-------|---------|---------|
| 均值范围 | [{features.mean(axis=0).min():.2f}, {features.mean(axis=0).max():.2f}] | [{features_scaled.mean(axis=0).min():.4f}, {features_scaled.mean(axis=0).max():.4f}] |
| 标准差范围 | [{features.std(axis=0).min():.2f}, {features.std(axis=0).max():.2f}] | [{features_scaled.std(axis=0).min():.4f}, {features_scaled.std(axis=0).max():.4f}] |

### 3.4 数据集划分

将数据集按80:20的比例划分为训练集和测试集，使用分层抽样保持类别比例：

```python
from sklearn.model_selection import train_test_split

# 划分数据集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(
    features_scaled, labels,
    test_size=0.2,
    random_state=42,
    stratify=y  # 分层抽样，保持类别比例
)

print(f"训练集大小: {{len(y_train)}}")
print(f"测试集大小: {{len(y_test)}}")
```

**数据集划分结果**:
- 训练集: {len(y_train)}个样本
- 测试集: {len(y_test)}个样本

### 3.5 决策树模型训练

使用决策树算法构建水质分类模型：

```python
from sklearn.tree import DecisionTreeClassifier

# 初始化决策树分类器
model = DecisionTreeClassifier(
    max_depth=5,      # 限制树深度防止过拟合
    random_state=42,  # 随机种子
    criterion='gini'  # 使用基尼不纯度作为分裂标准
)

# 训练模型
model.fit(X_train, y_train)

# 计算训练集准确率
train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, train_pred)
print(f"训练集准确率: {{train_accuracy:.4f}}")
```

**训练结果**:
- 训练集准确率: {train_result['train_accuracy']:.4f}
- 决策树深度: {train_result['tree_depth']}
- 叶子节点数: {train_result['n_leaves']}

### 3.6 模型评估

使用混淆矩阵和分类报告评估模型性能：

```python
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

# 预测测试集
y_pred = model.predict(X_test)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"测试集准确率: {{accuracy:.4f}}")

# 混淆矩阵
cm = confusion_matrix(y_test, y_pred)
print("混淆矩阵:")
print(cm)

# 分类报告
report = classification_report(y_test, y_pred)
print("分类报告:")
print(report)
```

**模型评估结果**:

#### 测试集准确率: {eval_result['accuracy']:.4f}

#### 分类报告

| 类别 | 精确率 | 召回率 | F1分数 | 支持数 |
|-----|-------|-------|-------|-------|
"""

    report_data = eval_result['classification_report']
    for i in range(1, 6):
        key = str(i)
        if key in report_data:
            r = report_data[key]
            label = WaterQualityClassifier.WATER_QUALITY_LABELS[i]
            report += f"| {label} | {r['precision']:.4f} | {r['recall']:.4f} | {r['f1-score']:.4f} | {int(r['support'])} |\n"

    report += f"""
### 3.7 特征重要性分析

分析决策树中各特征的重要性：

```python
# 获取特征重要性
importance = model.feature_importances_
feature_importance = dict(zip(feature_names, importance))

# 按重要性排序
sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

print("特征重要性排序:")
for feat, imp in sorted_features:
    if imp > 0:
        print(f"  {{feat}}: {{imp:.4f}}")
```

**特征重要性排序**:

| 排名 | 特征 | 重要性 |
|-----|------|-------|
"""

    for i, (feat, imp) in enumerate(sorted_importance[:5], 1):
        if imp > 0:
            report += f"| {i} | {feat} | {imp:.4f} |\n"

    report += f"""
**分析**: {sorted_importance[0][0]}是最重要的特征（重要性: {sorted_importance[0][1]:.4f}），说明该特征对水质分类的贡献最大。

## 四、实验结果分析

### 4.1 模型性能总结

- **测试集准确率**: {eval_result['accuracy']:.2%}
- **模型复杂度**: 树深度{train_result['tree_depth']}，叶子节点{train_result['n_leaves']}个

### 4.2 误分类原因分析

1. **数据不均衡问题**: Ⅴ类样本仅{categories.get(5, 0)}个，模型难以充分学习该类别的特征
2. **特征区分度**: 部分水质等级（如Ⅱ类和Ⅲ类）的颜色特征可能较为接近，导致混淆
3. **样本数量**: 总样本数{total}相对较少，可能影响模型的泛化能力

### 4.3 模型优缺点

**优点**:
- 决策树模型可解释性强，易于理解分类规则
- 对特征标准化不敏感
- 训练速度快，适合小规模数据集
- 可以直接可视化决策过程

**缺点**:
- 对于样本不均衡的数据集，可能偏向多数类
- 决策树容易过拟合
- 对于边界样本的分类能力有限

## 五、改进建议

1. **处理数据不均衡**:
   - 使用过采样技术（如SMOTE）增加少数类样本
   - 使用欠采样技术减少多数类样本
   - 调整类别权重

2. **模型优化**:
   - 尝试集成学习方法（随机森林、梯度提升树）
   - 使用交叉验证选择最优超参数
   - 尝试其他分类算法（SVM、KNN）

3. **特征工程**:
   - 增加更多图像特征（纹理特征、形状特征）
   - 尝试深度学习特征提取（CNN）
   - 使用特征选择方法筛选最相关特征

4. **数据增强**:
   - 收集更多样本数据
   - 使用图像增强技术（旋转、翻转、裁剪）

## 六、实验总结

本次实验成功实现了基于水色图像的水质评价系统，主要收获：

1. **掌握了颜色矩特征提取方法**: 通过计算RGB三通道的一阶矩、二阶矩和三阶矩，有效提取了图像的颜色特征
2. **理解了决策树分类原理**: 决策树通过递归地选择最优特征进行分裂，构建分类规则
3. **学会了模型评估方法**: 使用混淆矩阵、准确率、精确率、召回率等指标全面评估模型性能
4. **认识了数据挖掘的完整流程**: 从数据预处理到特征提取，再到模型训练和评估

本次实验为水产养殖场景中的水质监测提供了可行的技术方案，通过分析水样图像的颜色特征，可以快速、无损地评估水质等级。

---

**实验完成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    # 保存报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"实验报告已生成至: {output_path}")
    return output_path


def main():
    """主函数"""
    image_dir = "/Users/lucent/课程报告/数据挖掘/20260609-数据挖掘实验课/data/images"
    generate_report(image_dir)


if __name__ == "__main__":
    main()
