# -*- coding: utf-8 -*-
"""
==============================================================================
 文本分析 + 机器学习
------------------------------------------------------------------------------
 练习场景：电影短评情感分析
   - 任务：判断一条中文电影短评是「好评(1)」还是「差评(0)」（二分类）

 覆盖的知识点：
   1) jieba 中文分词与语料构建
   2) 文本表征：Word2Vec 词向量 + 求平均得句向量（含 Doc2Vec 对照方案）
   3) t-SNE 降维
   4) KMeans 无监督聚类 + matplotlib 散点图可视化
   5) 三种【有监督】分类算法对比训练：
        - 逻辑回归 LogisticRegression
        - K 近邻 KNN（KNeighborsClassifier）
        - 决策树 DecisionTree（DecisionTreeClassifier）
   6) 模型评估：准确率 + 精确率/召回率/F1 + classification_report
   7) 工程规范：先划分再训练向量（避免数据泄露）、类别不平衡下的正确评估

 运行前请先安装依赖：
   pip install jieba gensim scikit-learn matplotlib numpy
==============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import jieba


from gensim.models import Word2Vec
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, f1_score


# 让 matplotlib 正常显示中文（如本机无此字体可改成自己系统里的中文字体）
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

RANDOM_STATE = 42  # 固定随机种子，保证结果可复现


# ============================================================================
# 0. 准备数据
#    这里内置一份很小的示例数据，便于直接跑通流程。
# ============================================================================
def load_sample_data():
    """返回 (text_list, label_list)。1=好评，0=差评。"""
    text_list = [
        "剧情紧凑，演员演技在线，看得很过瘾，强烈推荐！",
        "画面太美了，配乐也好听，二刷依旧感动。",
        "节奏明快，笑点密集，全程没有尿点，超出预期。",
        "故事温暖治愈，结尾的反转非常惊喜，值得一看。",
        "特效炸裂，世界观宏大，是今年最棒的科幻片。",
        "演员选得很合适，台词自然，整体质量很高。",
        "剧情拖沓冗长，看了一半就想退场，浪费时间。",
        "演技尴尬，台词僵硬，剧情漏洞百出，非常失望。",
        "完全看不懂在讲什么，逻辑混乱，劝退。",
        "特效廉价，配音出戏，这钱花得太不值了。",
        "故事老套，毫无新意，结局还烂尾，差评。",
        "节奏拖沓，人物单薄，看完只想睡觉。",
    ]
    label_list = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    return text_list, label_list

    # 读取真实 CSV 的示例
    # import pandas as pd
    # df = pd.read_csv("movie_reviews.csv")
    # return df["review"].tolist(), df["label"].tolist()


# ============================================================================
# 1. 中文分词与语料构建
#    要点：用 jieba.lcut 分词，把「每条评论的词列表」收集成语料库（词列表的列表）。
# ============================================================================
def build_corpus(text_list):
    """把原始文本列表转成分词后的语料库：[[词, 词, ...], [...], ...]"""
    corpus = []
    for raw_text in text_list:
        word_list = jieba.lcut(raw_text.strip())  # 分词 + 去掉首尾空白
        corpus.append(word_list)                  # 注意：放进去的是词列表，不是原字符串
    return corpus


# ============================================================================
# 2. 文本表征
# ============================================================================
# ---- 方案 A：Word2Vec 词向量 + 求平均得到句向量 ----------------------------
VECTOR_SIZE = 100  # 词向量 / 文档向量维度


def train_word2vec(train_corpus):
    """仅用【训练集】语料训练 Word2Vec（避免数据泄露）。"""
    model = Word2Vec(
        train_corpus,
        vector_size=VECTOR_SIZE,
        window=5,
        min_count=1,
    )
    return model


def sentence_vector(model, words):
    """一条评论的句向量 = 该评论中所有「在词表内」的词向量的平均。"""
    valid_words = [w for w in words if w in model.wv]  # 过滤未登录词
    if not valid_words:
        return np.zeros(VECTOR_SIZE)                   # 没有有效词时返回零向量兜底
    return np.mean(model.wv[valid_words], axis=0)      # 按列求平均


def corpus_to_matrix_w2v(model, corpus):
    """把整个语料转成特征矩阵 X，形状 = (样本数, VECTOR_SIZE)。"""
    return np.array([sentence_vector(model, words) for words in corpus])


# ---- 方案 B：Doc2Vec（作为对照，可选）-------------------------------------
def train_doc2vec(corpus):
    """直接学习「整条评论」的文档向量，用 model.dv[i] 取出。"""
    tagged = [TaggedDocument(words=words, tags=[i]) for i, words in enumerate(corpus)]
    model = Doc2Vec(
        tagged,
        vector_size=VECTOR_SIZE,
        window=3,
        min_count=1,
        epochs=100,
    )
    X = np.array([model.dv[i] for i in range(len(corpus))])
    return X


# ============================================================================
# 3. t-SNE 降维 + KMeans 聚类 + 可视化
#    要点：高维向量降到 2 维 -> KMeans 聚类 -> 散点图按簇着色。
# ============================================================================
def visualize_clusters(X, n_clusters=2, title="t-SNE + KMeans 聚类可视化"):
    # 3.1 降维到 2 维（注意：t-SNE 样本数需 > perplexity，小数据集要调小 perplexity）
    perplexity = min(30, max(2, len(X) - 1))
    tsne = TSNE(n_components=2, random_state=RANDOM_STATE, perplexity=perplexity)
    X_2d = tsne.fit_transform(X)

    # 3.2 KMeans 聚类（无监督，只用 X，用 fit_predict 直接拿到簇标签）
    kmeans = KMeans(n_clusters=n_clusters, random_state=RANDOM_STATE, n_init=10)
    cluster_labels = kmeans.fit_predict(X)

    # 3.3 画散点图：X_2d 的第 0 列作横坐标、第 1 列作纵坐标，按簇着色
    plt.figure(figsize=(8, 6))
    plt.scatter(X_2d[:, 0], X_2d[:, 1], c=cluster_labels, cmap="viridis")
    plt.title(title)
    plt.xlabel("维度 1")
    plt.ylabel("维度 2")
    plt.colorbar(label="簇编号")
    plt.tight_layout()
    plt.show()
    return cluster_labels


# ============================================================================
# 4 + 5. 三种有监督分类算法对比训练与评估
#    工程规范（重点）：
#      先划分训练/测试集 -> 只用训练集训练词向量与模型 -> 再变换测试集。
#      若先用全部文本训练向量再划分，测试集信息会泄露，评估结果会偏乐观。
# ============================================================================
def report_model(name, y_true, y_pred):
    """打印单个模型的评估结果，并返回 (准确率, 宏平均F1) 供汇总。"""
    acc = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    print("\n" + "-" * 60)
    print("【{}】测试集准确率：{:.4f}　宏平均 F1：{:.4f}".format(name, acc, macro_f1))
    print(classification_report(
        y_true, y_pred,
        target_names=["差评(0)", "好评(1)"],
        zero_division=0,
    ))
    return acc, macro_f1


def compare_models(text_list, label_list, test_size=0.2):
    """在同一份训练/测试划分上，对比 逻辑回归 / KNN / 决策树 三种有监督分类算法。"""
    y = np.array(label_list)

    # 4.1 先在「原始文本」层面划分，杜绝数据泄露
    text_train, text_test, y_train, y_test = train_test_split(
        text_list, y, test_size=test_size,
        random_state=RANDOM_STATE, stratify=y,  # stratify 保持正负样本比例
    )

    # 4.2 Word2Vec 只在训练集上训练，再分别变换训练集与测试集
    train_corpus = build_corpus(text_train)
    test_corpus = build_corpus(text_test)
    w2v = train_word2vec(train_corpus)
    X_train = corpus_to_matrix_w2v(w2v, train_corpus)
    X_test = corpus_to_matrix_w2v(w2v, test_corpus)

    results = {}

    # —— 算法 1：逻辑回归 ——
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    results["逻辑回归"] = report_model("逻辑回归", y_test, y_pred_lr)

    # —— 算法 2：KNN ——
    # n_neighbors 不能大于训练样本数；数据少时取小一点（如 3）
    n_neighbors = min(3, len(X_train))
    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_train, y_train)
    y_pred_knn = knn.predict(X_test)
    results["KNN"] = report_model("KNN（k={}）".format(n_neighbors), y_test, y_pred_knn)

    # —— 算法 3：决策树 ——
    dt = DecisionTreeClassifier(random_state=RANDOM_STATE)
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)
    results["决策树"] = report_model("决策树", y_test, y_pred_dt)

    # —— 汇总对比 ——
    print("\n" + "=" * 60)
    print("三种算法效果汇总：")
    print("{:<14}{:>10}{:>12}".format("算法", "准确率", "宏平均F1"))
    for name, (acc, mf1) in results.items():
        print("{:<14}{:>10.4f}{:>12.4f}".format(name, acc, mf1))

    return results


# ============================================================================
# 主流程
# ============================================================================
def main():
    text_list, label_list = load_sample_data()

    # —— 演示 1：无监督聚类 + 可视化（用全部数据做探索性分析是允许的）——
    corpus_all = build_corpus(text_list)
    w2v_all = train_word2vec(corpus_all)
    X_all = corpus_to_matrix_w2v(w2v_all, corpus_all)
    visualize_clusters(X_all, n_clusters=2,
                       title="电影短评 · Word2Vec + t-SNE + KMeans")

    # —— 演示 2：三种算法对比训练（严格先划分、再训练向量，避免数据泄露）——
    print("=" * 60)
    compare_models(text_list, label_list, test_size=0.2)


if __name__ == "__main__":
    main()


