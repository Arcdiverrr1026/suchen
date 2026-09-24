import os
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score, f1_score

# 基础路径配置（使用相对路径）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
TMP_DIR = os.path.join(BASE_DIR, 'tmp')

def load_words_set(file_name):
    """通用词表加载函数"""
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        print(f"警告：未找到词表文件 {path}，将返回空集合。")
        return set()
    with open(path, 'r', encoding='utf-8') as f:
        return set([line.strip() for line in f if line.strip()])

def load_negation_csv(file_name):
    """加载否定词表"""
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        return set()
    df_not = pd.read_csv(path, header=None)
    return set(df_not[0].astype(str).str.strip().tolist())

def extract_lexicon_features(words_list, pos_words, neg_words, not_words):
    """结合否定词的情感词典特征提取"""
    pos_count = 0
    neg_count = 0
    neg_flag = False  # 否定词翻转标志

    for word in words_list:
        if word in not_words:
            neg_flag = not neg_flag
            continue
        if word in pos_words:
            if neg_flag:
                neg_count += 1
            else:
                pos_count += 1
            neg_flag = False  # 重置标志
        elif word in neg_words:
            if neg_flag:
                pos_count += 1
            else:
                neg_count += 1
            neg_flag = False

    return pos_count, neg_count

def run_experiment(stoplist_file, pos_file, neg_file, not_file):
    """运行单次对比实验"""
    print(f"\n" + "="*50)
    print(f"正在运行实验配置:\n停用词:{stoplist_file}\n正向词:{pos_file}\n负向词:{neg_file}\n否定词:{not_file}")
    print("="*50)

    # 1. 加载本次实验所需的词表
    stopwords = load_words_set(stoplist_file)
    pos_words = load_words_set(pos_file)
    neg_words = load_words_set(neg_file)
    not_words = load_negation_csv(not_file)

    # 2. 读取原始数据并清洗分词
    df = pd.read_csv(os.path.join(DATA_DIR, 'Comments.csv'))
    df = df.dropna(subset=['评论内容', '类别'])

    # 分词并过滤停用词
    df['cutted'] = df['评论内容'].apply(lambda x: [w for w in jieba.lcut(str(x)) if w not in stopwords and len(w.strip()) > 0])

    # 3. 提取词典法特征
    lexicon_res = df['cutted'].apply(lambda x: extract_lexicon_features(x, pos_words, neg_words, not_words))
    df['pos_score'] = [r[0] for r in lexicon_res]
    df['neg_score'] = [r[1] for r in lexicon_res]

    # 4. 文本向量化 (使用 TF-IDF 增强表现)
    df['text_str'] = df['cutted'].apply(lambda x: ' '.join(x))
    tfidf = TfidfVectorizer(max_features=2000)
    X_tfidf = tfidf.fit_transform(df['text_str']).toarray()

    # 5. 特征融合：拼接文本矩阵与词典得分特征
    X_combined = np.hstack((X_tfidf, df[['pos_score', 'neg_score']].values))
    y = df['类别'].values

    # 6. 划分数据集与建模评估
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=1)

    # 转换为正数以便朴素贝叶斯处理
    X_train = np.abs(X_train)
    X_test = np.abs(X_test)

    model = MultinomialNB().fit(X_train, y_train)
    preds = model.predict(X_test)

    evaluate_accuracy = accuracy_score(y_test, preds)
    print('准确率为: %.2f%%' % (evaluate_accuracy * 100.0))
    evaluate_p = precision_score(y_test, preds, average='micro')
    print('精确率为: %.2f%%' % (evaluate_p * 100.0))
    evaluate_recall = recall_score(y_test, preds, average='micro')
    print('召回率为: %.2f%%' % (evaluate_recall * 100.0))
    evaluate_f1 = f1_score(y_test, preds, average='micro')
    print('F1 值为: %.2f%%' % (evaluate_f1 * 100.0))
    print("\n分类效果报告:")
    print(classification_report(y_test, preds))

if __name__ == '__main__':
    # 基础配置实验（教材自带/基础词表）
    run_experiment(
        stoplist_file='stopwordsHIT.txt',
        pos_file='正面评价词语（中文）.txt',
        neg_file='负面评价词语（中文）.txt',
        not_file='not.csv'
    )

    # 对比配置实验（使用你新搜集的词表，在此处替换文件名即可）
    run_experiment(
        stoplist_file='stopwords_custom.txt',      # 切换为你搜集的更广的停用词表
        pos_file='pos_custom.txt',
        neg_file='neg_custom.txt',
        not_file='not_custom.csv'
    )