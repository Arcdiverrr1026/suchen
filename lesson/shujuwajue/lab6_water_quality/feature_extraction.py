"""
图像颜色特征提取模块
=====================
本模块实现水样图像的颜色矩特征提取，包括：
- 图像预处理（切割）
- 颜色矩计算（一阶矩、二阶矩、三阶矩）
- 特征标准化

颜色矩原理：
- 一阶矩（均值）：反映颜色的平均强度
- 二阶矩（标准差）：反映颜色的分布范围
- 三阶矩（偏度）：反映颜色分布的对称性
"""

import numpy as np
from PIL import Image
from pathlib import Path
from typing import List, Tuple, Optional
from sklearn.preprocessing import StandardScaler


class ColorMomentExtractor:
    """颜色矩特征提取器

    从水样图像中提取颜色矩特征，用于水质分类。

    Attributes:
        image_size: 目标图像尺寸 (width, height)
        scaler: 特征标准化器
    """

    def __init__(self, image_size: Tuple[int, int] = (256, 256)):
        """初始化特征提取器

        Args:
            image_size: 图像缩放目标尺寸
        """
        self.image_size = image_size
        self.scaler = StandardScaler()
        self._is_fitted = False

    def load_and_preprocess(self, image_path: str) -> np.ndarray:
        """加载并预处理图像

        Args:
            image_path: 图像文件路径

        Returns:
            预处理后的图像数组 (H, W, C)
        """
        # 加载图像并转换为RGB模式
        img = Image.open(image_path).convert('RGB')

        # 缩放到统一尺寸
        img = img.resize(self.image_size, Image.Resampling.LANCZOS)

        # 转换为numpy数组
        img_array = np.array(img, dtype=np.float64)

        return img_array

    def extract_color_moments(self, img_array: np.ndarray) -> np.ndarray:
        """提取颜色矩特征

        对RGB三个通道分别计算一阶矩（均值）、二阶矩（标准差）、三阶矩（偏度），
        共得到9个特征。

        Args:
            img_array: 图像数组 (H, W, C)

        Returns:
            颜色矩特征向量，长度为9
        """
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

    def extract_features_from_directory(
        self,
        image_dir: str,
        labels: Optional[List[int]] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """从目录中批量提取特征

        Args:
            image_dir: 图像目录路径
            labels: 图像标签列表（可选，如果为None则从文件名解析）

        Returns:
            (特征矩阵, 标签数组)
        """
        image_dir = Path(image_dir)
        image_files = sorted(image_dir.glob("*.jpg"))

        if not image_files:
            raise ValueError(f"目录 {image_dir} 中没有找到jpg图像文件")

        features_list = []
        labels_list = []

        for i, img_path in enumerate(image_files):
            # 从文件名解析标签（格式：类别_编号.jpg）
            if labels is None:
                label = int(img_path.stem.split('_')[0])
            else:
                label = labels[i]

            # 提取特征
            img_array = self.load_and_preprocess(str(img_path))
            color_moments = self.extract_color_moments(img_array)

            features_list.append(color_moments)
            labels_list.append(label)

        features = np.array(features_list)
        labels = np.array(labels_list)

        return features, labels

    def fit_transform(self, features: np.ndarray) -> np.ndarray:
        """拟合并转换特征（标准化）

        Args:
            features: 原始特征矩阵

        Returns:
            标准化后的特征矩阵
        """
        self._is_fitted = True
        return self.scaler.fit_transform(features)

    def transform(self, features: np.ndarray) -> np.ndarray:
        """转换特征（使用已拟合的标准化器）

        Args:
            features: 原始特征矩阵

        Returns:
            标准化后的特征矩阵
        """
        if not self._is_fitted:
            raise RuntimeError("请先调用 fit_transform 方法拟合标准化器")
        return self.scaler.transform(features)

    @staticmethod
    def get_feature_names() -> List[str]:
        """获取特征名称列表

        Returns:
            特征名称列表
        """
        channels = ['R', 'G', 'B']
        moments = ['均值', '标准差', '偏度']
        return [f"{ch}_{m}" for ch in channels for m in moments]
