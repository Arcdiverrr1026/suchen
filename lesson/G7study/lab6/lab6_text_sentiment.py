"""
机器学习实验6 - 文本情感分类
外卖评论情感分类：使用Word2Vec + 分类模型
"""

import os
import re
import warnings
import numpy as np
import pandas as pd
import jieba

# 确保工作目录为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False


# ===================== 1. 读取数据集 =====================
print("=" * 60)
print("1. 读取waimai_10k.csv文本情感分类数据集")
print("=" * 60)
df = pd.read_csv('waimai_10k.csv', encoding='utf-8-sig')
print(df.head())
print(f"\n数据集形状: {df.shape}")
print(f"标签分布:\n{df['label'].value_counts()}")


# ===================== 2. 文本预处理 =====================
print("\n" + "=" * 60)
print("2. 对评论文本进行预处理（中文分词与清理）")
print("=" * 60)

def clean_text(text):
    """清理文本：去除标点、数字、特殊字符，进行中文分词"""
    text = str(text)
    # 去除URL
    text = re.sub(r'http\S+', '', text)
    # 去除标点符号和特殊字符，保留中文、英文
    text = re.sub(r'[^一-龥a-zA-Z]', ' ', text)
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    # 使用jieba分词
    words = jieba.lcut(text)
    # 去除停用词和单字词
    stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人',
                 '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
                 '你', '会', '着', '没有', '看', '好', '自己', '这'}
    words = [w for w in words if len(w) > 1 and w not in stopwords]
    return ' '.join(words)

df['clean_text'] = df['text'].apply(clean_text)
print(df[['text', 'clean_text']].head())


# ===================== 3. 划分训练集和测试集 =====================
print("\n" + "=" * 60)
print("3. 划分训练集和测试集")
print("=" * 60)

X = df['clean_text']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"训练集形状: {X_train.shape}, 标签形状: {y_train.shape}")
print(f"测试集形状: {X_test.shape}, 标签形状: {y_test.shape}")


# ===================== 4. Word2Vec词向量训练 =====================
print("\n" + "=" * 60)
print("4. 使用Word2Vec训练词向量")
print("=" * 60)

# 将文本转为词列表
train_sentences = [text.split() for text in X_train]

# 训练Word2Vec模型
w2v_model = Word2Vec(
    sentences=train_sentences,
    vector_size=100,
    window=5,
    min_count=2,
    workers=4,
    epochs=20,
    seed=42
)

# 输出词表前20个词
vocab = list(w2v_model.wv.index_to_key)
print(f"词表大小: {len(vocab)}")
print(f"词表前20个词: {vocab[:20]}")


# ===================== 5. 文本转向量（句向量） =====================
print("\n" + "=" * 60)
print("5. 将评论文本转换为固定维度的句向量")
print("=" * 60)

def text_to_vector(text, model, vector_size=100):
    """将文本转换为句向量（所有词向量的平均值）"""
    words = text.split()
    word_vectors = []
    for word in words:
        if word in model.wv:
            word_vectors.append(model.wv[word])
    if word_vectors:
        return np.mean(word_vectors, axis=0)
    else:
        return np.zeros(vector_size)

X_train_vec = np.array([text_to_vector(text, w2v_model) for text in X_train])
X_test_vec = np.array([text_to_vector(text, w2v_model) for text in X_test])

print(f"训练集句向量形状: {X_train_vec.shape}")
print(f"测试集句向量形状: {X_test_vec.shape}")


# ===================== 6 & 7. 构建模型并使用GridSearchCV调参 =====================
print("\n" + "=" * 60)
print("6 & 7. 构建模型并使用GridSearchCV搜索最优超参数")
print("=" * 60)

# 逻辑回归
lr_params = {
    'C': [0.01, 0.1, 1, 10],
    'max_iter': [500, 1000]
}
lr_grid = GridSearchCV(
    LogisticRegression(random_state=42),
    lr_params, cv=5, scoring='accuracy', n_jobs=-1
)
lr_grid.fit(X_train_vec, y_train)
print(f"\n逻辑回归最优参数: {lr_grid.best_params_}")
print(f"逻辑回归最优交叉验证准确率: {lr_grid.best_score_:.4f}")

# K近邻
knn_params = {
    'n_neighbors': [3, 5, 7, 9],
    'weights': ['uniform', 'distance']
}
knn_grid = GridSearchCV(
    KNeighborsClassifier(),
    knn_params, cv=5, scoring='accuracy', n_jobs=-1
)
knn_grid.fit(X_train_vec, y_train)
print(f"\nK近邻最优参数: {knn_grid.best_params_}")
print(f"K近邻最优交叉验证准确率: {knn_grid.best_score_:.4f}")

# 决策树
dt_params = {
    'max_depth': [5, 10, 15, 20, None],
    'min_samples_split': [2, 5, 10]
}
dt_grid = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    dt_params, cv=5, scoring='accuracy', n_jobs=-1
)
dt_grid.fit(X_train_vec, y_train)
print(f"\n决策树最优参数: {dt_grid.best_params_}")
print(f"决策树最优交叉验证准确率: {dt_grid.best_score_:.4f}")


# ===================== 8. 测试集评估与可视化 =====================
print("\n" + "=" * 60)
print("8. 在测试集上评估各模型性能")
print("=" * 60)

models = {
    '逻辑回归': lr_grid.best_estimator_,
    'K近邻': knn_grid.best_estimator_,
    '决策树': dt_grid.best_estimator_
}

results = {}
for name, model in models.items():
    y_pred = model.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    results[name] = {
        'accuracy': acc,
        'y_pred': y_pred,
        'report': classification_report(y_test, y_pred, output_dict=True)
    }
    print(f"\n--- {name} ---")
    print(f"准确率: {acc:.4f}")
    print(classification_report(y_test, y_pred, target_names=['负面', '正面']))

# ---------- 模型性能对比柱状图 ----------
fig, ax = plt.subplots(figsize=(8, 5))
model_names = list(results.keys())
accuracies = [results[name]['accuracy'] for name in model_names]
colors = ['#4ECDC4', '#FF6B6B', '#45B7D1']
bars = ax.bar(model_names, accuracies, color=colors, edgecolor='black', linewidth=0.8)
for bar, acc in zip(bars, accuracies):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.005,
            f'{acc:.4f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
ax.set_ylabel('准确率', fontsize=12)
ax.set_title('模型性能对比', fontsize=14)
ax.set_ylim(0, 1.05)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("模型性能对比柱状图已保存: model_comparison.png")

# ---------- 混淆矩阵 ----------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, (name, model) in enumerate(models.items()):
    cm = confusion_matrix(y_test, results[name]['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                xticklabels=['负面', '正面'], yticklabels=['负面', '正面'])
    axes[idx].set_title(f'{name} 混淆矩阵', fontsize=13)
    axes[idx].set_xlabel('预测标签')
    axes[idx].set_ylabel('真实标签')
plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=150, bbox_inches='tight')
plt.show()
print("混淆矩阵已保存: confusion_matrices.png")

# ---------- 学习曲线 ----------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, (name, model) in enumerate(models.items()):
    train_sizes, train_scores, val_scores = learning_curve(
        model, X_train_vec, y_train, cv=5, n_jobs=-1,
        train_sizes=np.linspace(0.1, 1.0, 10), scoring='accuracy'
    )
    train_mean = train_scores.mean(axis=1)
    train_std = train_scores.std(axis=1)
    val_mean = val_scores.mean(axis=1)
    val_std = val_scores.std(axis=1)

    axes[idx].fill_between(train_sizes, train_mean - train_std,
                           train_mean + train_std, alpha=0.1, color='blue')
    axes[idx].fill_between(train_sizes, val_mean - val_std,
                           val_mean + val_std, alpha=0.1, color='orange')
    axes[idx].plot(train_sizes, train_mean, 'o-', color='blue', label='训练集')
    axes[idx].plot(train_sizes, val_mean, 'o-', color='orange', label='验证集')
    axes[idx].set_title(f'{name} 学习曲线', fontsize=13)
    axes[idx].set_xlabel('训练样本数')
    axes[idx].set_ylabel('准确率')
    axes[idx].legend(loc='lower right')
    axes[idx].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('learning_curves.png', dpi=150, bbox_inches='tight')
plt.show()
print("学习曲线已保存: learning_curves.png")

print("\n" + "=" * 60)
print("实验完成！")
print("=" * 60)
