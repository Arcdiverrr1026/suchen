import jieba
import jieba.analyse
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

try:
    with open('苏东坡传.txt', 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("错误：请确保'苏东坡传.txt'文件与脚本在同一目录下。")
    content = ""

if content:
    clean_content = re.sub(r'[^\u4e00-\u9fa5]+', '', content)
    seg_list = jieba.lcut(clean_content)
    print(f"--- 分词完成，总词数：{len(seg_list)} ---\n")
    print("--- 前20个关键词及其权重 ---")
    keywords = jieba.analyse.extract_tags(content, topK=20, withWeight=True)
    for word, weight in keywords:
        print(f"关键词: {word:<10} | 权重: {weight:.4f}")
    keyword_dict = {word: weight for word, weight in keywords}
    wc = WordCloud(
        font_path='/System/Library/Fonts/STHeiti Light.ttc',
        background_color='white',
        width=1000,
        height=800,
        max_words=100,
        colormap='viridis',  # 颜色方案
        margin=2
    ).generate_from_frequencies(keyword_dict)

    wc.to_file('苏东坡.png')
    print("\n--- 词云图已保存为 '苏东坡.png' ---")

    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.show()