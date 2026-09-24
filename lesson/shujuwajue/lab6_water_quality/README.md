# 基于水色图像的水质评价系统

## 项目概述

本项目实现了基于图像颜色特征（颜色矩）的水质分类评价系统，用于数据挖掘实验课程。

## 项目结构

```
lab6_water_quality/
├── __init__.py              # 包初始化文件
├── feature_extraction.py    # 颜色矩特征提取模块
├── model.py                 # 决策树分类模型模块
├── main.py                  # 主实验流程脚本
├── generate_report.py       # 实验报告生成器
├── README.md                # 项目说明文档
└── output/                  # 输出目录
    ├── confusion_matrix.png # 混淆矩阵可视化
    ├── decision_tree.png    # 决策树可视化
    ├── feature_importance.png # 特征重要性图
    └── 实验报告.md           # 实验报告
```

## 功能模块

### 1. 特征提取模块 (feature_extraction.py)

- **图像预处理**: 加载图像、缩放到统一尺寸
- **颜色矩提取**: 计算RGB三通道的一阶矩（均值）、二阶矩（标准差）、三阶矩（偏度）
- **特征标准化**: 使用Z-score标准化消除量纲差异

### 2. 分类模型模块 (model.py)

- **决策树训练**: 使用基尼不纯度作为分裂标准
- **模型评估**: 混淆矩阵、分类报告、准确率
- **结果可视化**: 混淆矩阵热力图、决策树可视化、特征重要性图

## 使用方法

### 运行完整实验

```bash
cd /Users/lucent/PycharmProjects/suchen
uv run python lesson/shujuwajue/lab6_water_quality/main.py
```

### 生成实验报告

```bash
cd /Users/lucent/PycharmProjects/suchen
uv run python lesson/shujuwajue/lab6_water_quality/generate_report.py
```

## 实验结果

- **数据集**: 203张水样图像，5个水质等级
- **特征**: 9个颜色矩特征（RGB三通道 × 三个矩）
- **模型**: 决策树（深度5，叶子节点19个）
- **测试集准确率**: 53.66%

## 关键发现

1. **最重要的特征**: B_标准差（重要性: 0.2362）
2. **数据不均衡**: Ⅴ类样本仅6个，影响模型识别能力
3. **分类难点**: Ⅳ类和Ⅴ类样本难以正确分类

## 改进建议

1. 使用SMOTE等过采样技术处理数据不均衡
2. 尝试随机森林等集成学习方法
3. 增加纹理特征、形状特征等更多图像特征
4. 收集更多样本数据

## 依赖环境

- Python 3.12+
- scikit-learn
- numpy
- matplotlib
- Pillow
- pandas
- seaborn

## 实验日期

2026年6月9日
