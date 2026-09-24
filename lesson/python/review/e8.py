import numpy as np
import matplotlib.pyplot as plt
import PIL
import jieba.analyse
import re
import wordcloud

with open(r'教育.txt',encoding = 'utf-8') as f:
    text1 = f.readlines()
txt = re.sub('[,.、""'']','',str(text1))

keywords = jieba.analyse.extract_tags(txt,topK=30,withWeight=True,allowPOS=())
print('关键词：',keywords)
keyDict = {}
for item in keywords:
    keyDict[item[0]] = item[1]

imagel = PIL.Image.open(r'map.jpg')
MASK = np.array(imagel)

WC = wordcloud.WordCloud(font_path='simei.ttf',
                         mask = MASK,
                         height = 400,width = 400,
                         background_color='white',repeat=False,mode='RGBA')

cloud = WC.generate_from_frequencies(keyDict)
WC.to_file('dang.png')
plt.imshow(cloud)
plt.axis("off")
plt.show()
