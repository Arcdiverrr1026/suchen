"""
基于水色图像的水质评价系统
==============================
本模块实现了基于图像颜色特征（颜色矩）的水质分类评价系统。

主要功能：
1. 图像预处理与切割
2. 颜色矩特征提取
3. 特征标准化
4. 决策树分类模型构建与评估

作者：数据挖掘实验课
日期：2026.6.9
"""

from .feature_extraction import ColorMomentExtractor
from .model import WaterQualityClassifier

__version__ = "1.0.0"
__all__ = ["ColorMomentExtractor", "WaterQualityClassifier"]
