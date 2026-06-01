import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# 1. 读取全文
with open("智改数转.txt", "r", encoding="utf-8") as f:
    text = f.read()

# 2. 去除全文标点符号，只保留中文、英文和数字
text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)

# 3. 将未能识别的新名词、专有名词加入分词词典
jieba.add_word("智改数转")
jieba.add_word("工业互联网")
jieba.add_word("数字化转型")
jieba.add_word("智能制造")

# 4. 中文分词
words = jieba.lcut(text)

# 5. 设置停用词
stopwords = {"的", "很", "我们", "非常"}

# 6. 去除停用词和长度为1的词
words = [word for word in words if word not in stopwords and len(word) > 1]

# 7. 将分词结果拼接成字符串
word_text = " ".join(words)

# 8. 生成词云图，最大显示词数为50
wc = WordCloud(
    font_path="simhei.ttf",
    background_color="white",
    max_words=50,
    width=800,
    height=600
).generate(word_text)

# 9. 显示词云图
plt.imshow(wc)
plt.axis("off")
plt.show()