import numpy as np
import matplotlib.pyplot as plt
import PIL
import jieba.analyse
import re
import wordcloud

with open(r'教育.txt',encoding = 'utf-8') as f:
    text1 = f.readlines()
txt = re.sub('[,.、""'']','',str(text1))

cutlist = jieba.lcut(txt)
content = ''.join(cutlist)

imagel = PIL.Image.open(r'map.jpg')
MASK = np.array(imagel)
excludeWords = ['的','我们','是','和']

WC= wordcloud.WordCloud(font_path = 'simhei.ttf',
                        max_words = 200,
                        mask = MASK,
                        height = 400,width = 400,
                        stopwords = excludeWords,
                        background_color = 'white',repeat = False,mode = 'RGBA'
                        )

cloud = WC.generate(content)
WC.to_file('党的二十大报告.png')
plt.imshow(cloud)
plt.axis("off")
plt.show()
