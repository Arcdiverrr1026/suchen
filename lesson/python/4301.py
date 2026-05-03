#01
## 导入 jieba库
import jieba.analyse
#02
## 用with方式打开文件’npl.txt’
with open('npl.txt','r',encoding='utf-8') as f:
    text = f.read()
#05
##打印原文内容，
print("原文摘要:")
#06
##只显示前100字符
print(text[:101])
#08
print("\nTF-IDF关键词提取:")
#09
# 1. 基于TF-IDF算法的关键词提取
tag = jieba.analyse.extract_tags(text, topK=100, withWeight=True)
#10
##循环输出关键词及其权重
for i,item in enumerate(tag):
    print(f"{item[0]}, {item[1]:.4f}",end='\t')
    if (i+1) % 5 == 0:
        print()
#11
## 权重保留4位小数，输出格式如下：
## 处理: 0.4919
print("\nTextRank关键词提取:")
#14
## 2. 基于TextRank算法的关键词提取
atg = jieba.analyse.textrank(text, topK=20, withWeight=True)
#15
##循环输出关键词及其权重
for i,item in enumerate(atg):
    print(f"{item[0]}, {item[1]:.4f}",end='\t')
    if (i+1) % 5 == 0:
        print()
#15
## 权重保留4位小数，输出格式如下：
## 处理: 0.4919