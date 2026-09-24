import os
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import jieba
from gensim.models import Word2Vec
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

def load_stopwords(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r', encoding='utf-8') as f:
        return set([line.strip() for line in f if line.strip()])

def preprocess_text(text, stopwords):
    # 清洗特殊字符
    import re
    text = re.sub('[^\u4E00-\u9FD5]||[0-9]|\\s|\\t', '', str(text))
    # 分词
    words = jieba.lcut(text)
    # 过滤停用词和空词
    return [w for w in words if w not in stopwords and len(w.strip()) > 0]

def document_vector(words, model, vector_size):
    # 过滤不在词汇表中的词，求均值
    valid_words = [w for w in words if w in model.wv]
    if len(valid_words) == 0:
        return np.zeros(vector_size)
    return np.mean(model.wv[valid_words], axis=0)

def main():
    print("="*50)
    print("正在运行 Word2Vec 词向量 + 机器学习实验 (trainer.py)")
    print("="*50)

    # 1. 加载数据
    train_df = pd.read_csv('./tmp/f1.csv')
    test_df = pd.read_csv('./tmp/f2.csv')

    stopwords = load_stopwords('./data/stopwordsHIT.txt')

    # 2. 分词与清洗
    print("正在对训练集和测试集进行分词...")
    train_df['cutted'] = train_df['评论内容'].apply(lambda x: preprocess_text(x, stopwords))
    test_df['cutted'] = test_df['评论内容'].apply(lambda x: preprocess_text(x, stopwords))

    # 3. 训练 Word2Vec 模型
    vector_size = 100
    print(f"正在使用训练集训练 Word2Vec (维度: {vector_size})...")
    w2v_model = Word2Vec(
        sentences=train_df['cutted'].tolist(),
        vector_size=vector_size,
        window=5,
        min_count=2,
        workers=4,
        epochs=10,
        seed=42
    )

    # 4. 生成文档向量
    print("正在生成文档向量表达...")
    X_train = np.array([document_vector(w, w2v_model, vector_size) for w in train_df['cutted']])
    X_test = np.array([document_vector(w, w2v_model, vector_size) for w in test_df['cutted']])
    y_train = train_df['类别'].values
    y_test = test_df['类别'].values

    # 5. 训练分类器 (Logistic Regression)
    print("正在训练逻辑回归分类器...")
    classifier = LogisticRegression(max_iter=1000, random_state=42)
    classifier.fit(X_train, y_train)

    # 6. 预测与评估
    preds = classifier.predict(X_test)
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
    print("混淆矩阵:")
    print(confusion_matrix(y_test, preds))

if __name__ == '__main__':
    main()
