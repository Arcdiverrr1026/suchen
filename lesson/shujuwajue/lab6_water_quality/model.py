"""
决策树分类模型模块
==================
本模块实现基于决策树的水质分类模型，包括：
- 模型训练与预测
- 模型评估（混淆矩阵、准确率等）
- 决策树可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    accuracy_score
)
from typing import Tuple, Dict, Any, Optional
import seaborn as sns


class WaterQualityClassifier:
    """水质分类器

    基于决策树算法的水质分类模型。

    Attributes:
        model: 决策树分类模型
        feature_names: 特征名称列表
        class_names: 类别名称列表
    """

    # 水质等级描述
    WATER_QUALITY_LABELS = {
        1: "Ⅰ类（优质）",
        2: "Ⅱ类（良好）",
        3: "Ⅲ类（轻度污染）",
        4: "Ⅳ类（中度污染）",
        5: "Ⅴ类（重度污染）"
    }

    def __init__(
        self,
        feature_names: Optional[list] = None,
        max_depth: Optional[int] = None,
        random_state: int = 42
    ):
        """初始化分类器

        Args:
            feature_names: 特征名称列表
            max_depth: 决策树最大深度
            random_state: 随机种子
        """
        self.feature_names = feature_names or [f"feature_{i}" for i in range(9)]
        self.class_names = [self.WATER_QUALITY_LABELS[i] for i in range(1, 6)]

        # 初始化决策树分类器
        self.model = DecisionTreeClassifier(
            max_depth=max_depth,
            random_state=random_state,
            criterion='gini'  # 使用基尼不纯度作为分裂标准
        )

        # 存储训练结果
        self.train_result = {}

    def split_data(
        self,
        X: np.ndarray,
        y: np.ndarray,
        test_size: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """划分训练集和测试集

        Args:
            X: 特征矩阵
            y: 标签数组
            test_size: 测试集比例

        Returns:
            (X_train, X_test, y_train, y_test)
        """
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=42,
            stratify=y  # 分层抽样，保持类别比例
        )

        return X_train, X_test, y_train, y_test

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> Dict[str, Any]:
        """训练模型

        Args:
            X_train: 训练特征矩阵
            y_train: 训练标签数组

        Returns:
            训练结果字典
        """
        # 训练模型
        self.model.fit(X_train, y_train)

        # 计算训练集准确率
        train_pred = self.model.predict(X_train)
        train_accuracy = accuracy_score(y_train, train_pred)

        self.train_result = {
            'train_accuracy': train_accuracy,
            'n_samples': len(y_train),
            'n_features': X_train.shape[1],
            'tree_depth': self.model.get_depth(),
            'n_leaves': self.model.get_n_leaves()
        }

        return self.train_result

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """评估模型

        Args:
            X_test: 测试特征矩阵
            y_test: 测试标签数组

        Returns:
            评估结果字典
        """
        # 预测
        y_pred = self.model.predict(X_test)

        # 计算评估指标
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        return {
            'accuracy': accuracy,
            'confusion_matrix': cm,
            'classification_report': report,
            'y_pred': y_pred,
            'y_true': y_test
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测新样本

        Args:
            X: 特征矩阵

        Returns:
            预测结果数组
        """
        return self.model.predict(X)

    def plot_confusion_matrix(
        self,
        confusion_mat: np.ndarray,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """绘制混淆矩阵热力图

        Args:
            confusion_mat: 混淆矩阵
            save_path: 图像保存路径（可选）

        Returns:
            matplotlib Figure对象
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        # 使用seaborn绘制热力图
        sns.heatmap(
            confusion_mat,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=self.class_names,
            yticklabels=self.class_names,
            ax=ax
        )

        ax.set_xlabel('预测标签', fontsize=12)
        ax.set_ylabel('真实标签', fontsize=12)
        ax.set_title('水质分类混淆矩阵', fontsize=14, fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def plot_decision_tree(
        self,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (20, 12)
    ) -> plt.Figure:
        """可视化决策树

        Args:
            save_path: 图像保存路径（可选）
            figsize: 图像尺寸

        Returns:
            matplotlib Figure对象
        """
        fig, ax = plt.subplots(figsize=figsize)

        plot_tree(
            self.model,
            feature_names=self.feature_names,
            class_names=self.class_names,
            filled=True,
            rounded=True,
            ax=ax,
            fontsize=8
        )

        ax.set_title('决策树可视化', fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def get_tree_rules(self) -> str:
        """获取决策树规则文本

        Returns:
            决策树规则的文本描述
        """
        return export_text(
            self.model,
            feature_names=self.feature_names,
            show_weights=True
        )

    def get_feature_importance(self) -> Dict[str, float]:
        """获取特征重要性

        Returns:
            特征名称到重要性的映射字典
        """
        importance = self.model.feature_importances_
        return dict(zip(self.feature_names, importance))

    def summary(self) -> str:
        """生成模型摘要

        Returns:
            模型摘要文本
        """
        lines = [
            "=" * 50,
            "决策树分类模型摘要",
            "=" * 50,
            f"树深度: {self.model.get_depth()}",
            f"叶子节点数: {self.model.get_n_leaves()}",
            f"特征数量: {len(self.feature_names)}",
            "",
            "特征重要性排序:",
            "-" * 30,
        ]

        # 按重要性排序
        importance = self.get_feature_importance()
        sorted_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)

        for feat, imp in sorted_features:
            if imp > 0:
                lines.append(f"  {feat}: {imp:.4f}")

        return "\n".join(lines)
