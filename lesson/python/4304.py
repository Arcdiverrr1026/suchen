'''
（1）读取文件“给青年的十二封信.txt”内容，去除全文标点符号，进行中文分词；
（2）分析分词结果，将一些未能识别的新名词、专有名词以词典的方式导入到分词库中；
（3）设置停用词：“的”、“很”、“我们”、“非常”等。
（4）用全文分词结果绘制词云图，图中设置最大显示词数为100。
（5）设计程序思路，再转换为代码，并在开发环境中运行、调试代码，验证代码的准确性。
'''

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


with open('给青年的十二封信.txt','r',encoding='utf-8') as f:
    text = f.read()

clean_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '',text)
user_dict = ["朱光潜", "十二封信", "因缘居", "情趣"]
for word in user_dict:
        jieba.add_word(word)
stop_words = {"的", "很", "我们", "非常", "了", "在", "是", "我", "你", "他", "也", "就", "着"}
words_list = jieba.lcut(clean_text)
filtered_words = [word for word in words_list if word not in stop_words and len(word) > 1]
word_space_split = " ".join(filtered_words)
wc = WordCloud(
    font_path='/System/Library/Fonts/STHeiti Light.ttc',
    background_color='white',    # 背景颜色
    max_words=100,               # 最大显示词数
    width=800,
    height=600,
    colormap='viridis'           # 颜色主题
)

    # 生成词云
wc.generate(word_space_split)

    # 7. 运行与展示
plt.figure(figsize=(10, 8))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off') # 隐藏坐标轴
plt.show()

    # 保存图片
wc.to_file("letter_wordcloud.png")
print("词云图已生成并保存为 letter_wordcloud.png")

# 执行程序
# text_analysis_pipeline("给青年的十二封信.txt")
