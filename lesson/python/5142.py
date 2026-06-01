import jieba
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# 1. 读取文件内容
with open("苏东坡传.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. 去除全文标点符号，只保留中文、英文和数字
text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)

# 3. 中文分词
words = jieba.lcut(text)
word_text = " ".join(words)

# 4. 使用 TF-IDF 关键词提取算法，提取前20个关键词及权重
keywords = jieba.analyse.extract_tags(
    text,
    topK=20,
    withWeight=True
)

# 5. 输出前20个关键词及对应权重
for word, weight in keywords:
    print(word, weight)

# 6. 将关键词和权重转换为词云需要的字典格式
word_freq = dict(keywords)

# 7. 生成词云图
wc = WordCloud(
    font_path="simhei.ttf",
    background_color="white",
    width=800,
    height=600,
    max_words=20
).generate_from_frequencies(word_freq)

# 8. 显示词云图
plt.imshow(wc)
plt.axis("off")
plt.show()

# 9. 保存图片为“苏东坡.png”
wc.to_file("苏东坡.png")