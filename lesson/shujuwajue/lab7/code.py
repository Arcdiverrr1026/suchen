#1.数据探索
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyecharts.charts import Pie
from pyecharts import options as opts

# 设置matplotlib中文显示 (优先注册本地 data 文件夹下的 simhei.ttf 字体)
import os
from matplotlib import font_manager
font_path = './data/simhei.ttf'
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.sans-serif'] = ['SimHei']
else:
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # macOS 备用字体
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取基础数据
df = pd.read_csv('./data/Comments.csv')
print("数据前五行：")
print(df.head())

# 2. 绘制不同情感类型评论的数量分布饼图 (pyecharts 富文本)
phone = ['中性评论', '正面评论', '负面评论']
num = df['类别'].value_counts()  # 类别列计数

def pie_rich_label() -> Pie:
    c = (
        Pie()
        .add(
            "",
            list(zip(phone, num)),
            label_opts=opts.LabelOpts(
                position="outside",
                formatter='{b|{b}: } {per|{d}%}',  # b表示评论类别, d表示占比
                background_color='#eee',
                border_color='#aaa',
                border_width=1,
                border_radius=4,
                rich={  # 调用富文本标签进行个性化设置
                    'b': {'fontSize': 16, 'lineHeight': 33},
                    'per': {
                        'color': '#eee',
                        'backgroundColor': '#334455',
                        'padding': [2, 4],
                        'borderRadius': 2,
                    },
                },
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title='不同情感类型评论的数量分布'))
        .render('./tmp/Pie_basic.html')  # 渲染并输出HTML文件
    )
    return c

pie_rich_label()

# 3. 按月份分组统计评论量变化并绘制折线图
df['评论时间'] = df['评论时间'].astype(str)  # 转换为字符串类型
time_target = ['2']
# 时间列异常值过滤，只保留包含 '2'（即2020、2021年）的有效行
index_target = df['评论时间'].apply(lambda x: sum([1 for i in x if i in time_target]) > 0)
df = df.loc[index_target, :]

df['评论时间'] = pd.to_datetime(df['评论时间'])  # 转换为时间类型
temp = df[['评论时间', '评论内容']]  # 提取时间评论表
x = temp.groupby('评论时间')['评论内容'].count()  # 按天统计评论量
y = x.reset_index()  # 重置索引

month = []  # 用于保存截取的年月 (YYYY-MM)
for i in range(len(y)):
    j = str(y.iloc[i, 0])[0:7]
    month.append(j)
y['评论时间'] = month

y = y.groupby('评论时间')['评论内容'].sum()  # 按月份合并求总评论数
y = y.reset_index()

# 开始绘制折线图
plt.figure(figsize=(12, 7))  # 创建画布
plt.xticks(range(16), y['评论时间'])  # 设置x轴刻度标签
plt.xticks(size='small', rotation=75, fontsize=13)  # 标签逆时针旋转75度
plt.title('每月评论量统计图')
plt.xlabel('日期')
plt.ylabel('评论量')
plt.plot(y['评论时间'], y['评论内容'], c='black')  # 绘制黑色折线
plt.savefig('./tmp/monthly_comments.png')
plt.close()

# 4. 提取获赞数排名前10的评论并绘制柱形图
df1 = df.copy()
df1 = df1.replace(to_replace='-', value=np.nan)  # 特殊字符替换为空值
df1 = df1.dropna(how='any')  # 去除缺失值
df1['点赞数'] = pd.to_numeric(df1['点赞数']).round(0).astype(int)
df1.sort_values(by="点赞数", axis=0, ascending=False, inplace=True)  # 按点赞数降序排列
print("获赞数前五行：")
print(df1.head())

labels = ['第1名', '第2名', '第3名', '第4名', '第5名', '第6名', '第7名', '第8名', '第9名', '第10名']
y1 = df1['点赞数'][:10]

plt.figure(figsize=(10, 6))
plt.xlabel('评论获赞数排名')
plt.ylabel('评论获赞数')
plt.title('评论获赞数排名前10的柱形图')
plt.xticks(range(10), labels)
plt.bar(range(10), y1, width=0.5)  # 绘制柱形图
plt.savefig('./tmp/top10_likes.png')
plt.close()

#2.文本预处理
import jieba
import re
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# 1. 评论数据去重
df = pd.read_csv('./data/Comments.csv')
df_drop = df.drop_duplicates('评论内容', keep='first')  # 保留重复数据的首条
print("去重前样本量：", df.shape)
print("去重后样本量：", df_drop.shape)

# 2. 特殊字符与干扰词清洗
df_clean = df_drop.copy()
# 过滤非中文字符、数字、部分特定的高频停用词（如天问一号、胖5等）
df_clean['评论内容'] = df_clean['评论内容'].astype('str').apply(
    lambda x: re.sub('[^\u4E00-\u9FD5]||[0-9]|\\s|\\t|天问一号|天问1号|天问|胖5|时分', '', x)
)
print("清洗后前5条文本：")
print(df_clean.head(5))

# 3. 使用 jieba 进行中文分词
def chinese_word_cut(mytext):
    return jieba.lcut(mytext)  # 精确分词模式

df_clean['cutted_content'] = df_clean['评论内容'].apply(chinese_word_cut)
print("分词后结果前5条：")
print(df_clean['cutted_content'].head(5))

# 4. 加载自定义停用词表并过滤
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file, 'r', encoding='UTF-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list

stop_words_file = './data/stopwordsHIT.txt'
stopwords = get_custom_stopwords(stop_words_file)
# 过滤分词列表中的停用词
df_clean['cutted_content'] = df_clean.cutted_content.apply(lambda x: [i for i in x if i not in stopwords])

# 保存预处理后的中间结果
df_clean.to_excel('./tmp/data_clean.xlsx', index=False)

# 5. 全局词频统计与词云图绘制
def words_count():
    word_dict = {}
    for index, item in df_clean.iterrows():
        for i in item.cutted_content:
            if i not in word_dict:
                word_dict[i] = 1
            else:
                word_dict[i] += 1
    return word_dict

words_count()  # 执行全局词频统计

def wordcloud_plot(mask_picture='./data/p1.jpg'):
    plt.figure(figsize=(16, 8), dpi=1080)
    image = Image.open(mask_picture)
    graph = np.array(image)
    wc = WordCloud(
        background_color='White',
        mask=graph,
        max_words=1000,
        stopwords=STOPWORDS,
        font_path='./data/simhei.ttf',  # 指定中文字体
        random_state=30
    )
    wc.generate_from_frequencies(words_count())
    plt.imshow(wc)
    plt.axis("off")  # 关闭坐标轴
    plt.savefig('./tmp/wordcloud_global.png')
    plt.close()

wordcloud_plot()

# 6. 分别统计不同情感分类(-1, 0, 1)的词频并绘制对比词云图
def words_counte(labels=0):
    word_dict = {}
    # 筛选指定情感标签的数据进行词频统计
    for index, item in df_clean[df_clean['类别'] == labels].iterrows():
        for i in item.cutted_content:
            if i not in word_dict:
                word_dict[i] = 1
            else:
                word_dict[i] += 1
    return word_dict

def wordcloud_plote(mask_picture='./data/p1.jpg'):
    p1 = plt.figure(figsize=(16, 8), dpi=1080)
    image = Image.open(mask_picture)
    graph = np.array(image)
    wc = WordCloud(
        background_color='White',
        mask=graph,
        max_words=2000,
        stopwords=STOPWORDS,
        font_path='./data/simhei.ttf',
        random_state=30
    )
    # 循环在一张画布上绘制消极(-1)、中性(0)、积极(1)的词云
    for i in [-1, 0, 1]:
        p1.add_subplot(1, 3, i + 2)  # 子图位置分别为1, 2, 3
        wc.generate_from_frequencies(words_counte(i))
        plt.imshow(wc)
        plt.axis('off')
    plt.savefig('./tmp/wordcloud_sentiment.png')
    plt.close()

wordcloud_plote()

#3.贝叶斯模型与评价
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

# 外部引入前面定义的停用词获取函数
def get_custom_stopwords(stop_words_file):
    with open(stop_words_file, 'r', encoding='UTF-8') as f:
        stopwords = f.read()
    return stopwords.split('\n')

# 1. 读取清洗后的文本数据
df_clean = pd.read_excel('./tmp/data_clean.xlsx')
df_clean = df_clean.iloc[:, [3, 4, 5, 8, 9]]  # 只提取关键特征及标签列 (点赞数, 评论内容, 评论时间, 类别, cutted_content)
df_clean = df_clean.dropna(how='any')

# 2. 将列表形式的词语拼接为用空格分隔的字符串
def join_words(words):
    # 兼容处理: 如果读取出来已经是str则直接返回，否则join
    if isinstance(words, str):
        return words
    return ' '.join(words)

df_clean['cutted_content'] = df_clean['cutted_content'].apply(join_words)

# 拆分特征(X)与标签(y)
x = df_clean[['评论时间', '点赞数', 'cutted_content']]
y = df_clean['类别']

# 3. 文本特征工程：构建词频矩阵
# 方法一：默认配置（未添加停用词和边界过滤）
vect_1 = CountVectorizer(analyzer='char', token_pattern=r'(?u)\b\w+\b')
term_matrix_1 = pd.DataFrame(vect_1.fit_transform(x.cutted_content).toarray(), columns=vect_1.get_feature_names_out())

# 方法二：高级配置（剔除平凡词与独特词，引入停用词限制）
max_df = 0.8  # 剔除在80%以上文档出现的超高频词
min_df = 5    # 剔除出现少于5次的超低频词
stop_words_file = './data/stopwordsHIT.txt'
stopwords = get_custom_stopwords(stop_words_file)

vect_2 = CountVectorizer(max_df=max_df, min_df=min_df, token_pattern=r'(?u)\b\w+\b', analyzer='char', stop_words=stopwords)
term_matrix_2 = pd.DataFrame(vect_2.fit_transform(x.cutted_content).toarray(), columns=vect_2.get_feature_names_out())
print("最终特征词矩阵形状：", term_matrix_2.shape)

# 4. 划分训练集与测试集（按 4:1 比例）
x_train, x_test, y_train, y_test = train_test_split(term_matrix_2, y, random_state=1, test_size=0.2)
print('训练集特征形状: ', x_train.shape)
print('测试集特征形状: ', x_test.shape)

# 5. 构建多项式朴素贝叶斯模型并进行训练预测
model_nb = MultinomialNB().fit(x_train, y_train)
res_nb = model_nb.predict(x_test)

# 6. 基础模型效果评价
print('混淆矩阵如下:\n', confusion_matrix(y_test, res_nb))
print('\n分类效果报告：\n', classification_report(y_test, res_nb))

evaluate_accuracy = accuracy_score(y_test, res_nb)
print('准确率为: %.2f%%' % (evaluate_accuracy * 100.0))
evaluate_p = precision_score(y_test, res_nb, average='micro')
print('精确率为: %.2f%%' % (evaluate_p * 100.0))
evaluate_recall = recall_score(y_test, res_nb, average='micro')
print('召回率为: %.2f%%' % (evaluate_recall * 100.0))
evaluate_f1 = f1_score(y_test, res_nb, average='micro')
print('F1 值为: %.2f%%' % (evaluate_f1 * 100.0))

#4.模型优化
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score

# 1. 结构化特征抽取与清洗（评论时间与点赞数）
df = pd.read_csv('./data/Comments.csv')
df['评论时间'] = df['评论时间'].astype(str)
time_target = ['2']
index_target = df['评论时间'].apply(lambda x: sum([1 for i in x if i in time_target]) > 0)
df = df.loc[index_target, :]

df['评论时间'] = pd.to_datetime(df['评论时间'])
temp = df[['评论时间', '评论内容']]

re_time = []  # 用于保存截取的年月日长度 (YYYY-MM-DD)
for i in range(len(temp)):
    j = str(temp.iloc[i, 0])[0:10]
    re_time.append(j)
temp['评论时间'] = re_time
temp_time = temp.iloc[:, 0]

z = []
for i in temp_time:
    i = str(i).split("-", 3)  # 以 '-' 切分出年、月、日
    z.append(i)
z = pd.DataFrame(z)
z.columns = list('年月日')

# 将年、月、日纯数字合并，转化为连续数值型日期格式（如 20200515）
z['日期'] = z['年'].str.cat(z['月']).str.cat(z['日'])
z['点赞数'] = df['点赞数'].values  # 引入原始点赞数
z = z.iloc[:, [3, 4]]  # 只保留 '日期' 和 '点赞数'

# 2. 连续特征清洗与离差标准化 (MinMax)
z = z.replace(to_replace='-', value=np.nan)
z = z.dropna(how='any')
z['点赞数'] = pd.to_numeric(z['点赞数']).round(0).astype(int)

# 点赞数统一执行 +1 处理，消除 0 值的负面量纲干扰
va = []
for i in z['点赞数']:
    i = i + 1
    va.append(i)
va = pd.DataFrame(va, columns=['点赞数'])
z['点赞数'] = va['点赞数']
z = z.dropna(how='any')

# 实施 MinMaxScaler 标准化
min_max_scaler = preprocessing.MinMaxScaler()
z1 = min_max_scaler.fit_transform(z)
z1 = pd.DataFrame(z1)
z1 = z1.rename(columns={0: '日期', 1: '点赞数'})

# 3. 特征大融合（标准化特征 + 文本词频特征）
df_clean = pd.read_excel('./tmp/data_clean.xlsx')
df_clean = df_clean.iloc[:, [8, 9]]  # 提取 '类别' 和 'cutted_content'
z1 = z1.join(df_clean)
z1 = z1.dropna(how='any')

def join_words(words):
    if isinstance(words, str):
        return words
    return ' '.join(words)

z1['cutted_content'] = z1['cutted_content'].apply(join_words)

# 特征标签拆开
x = z1[['日期', '点赞数', 'cutted_content']]
y = z1['类别']

# 4. 重新构建优化后的 TfidfVectorizer 矩阵 (引入 N-gram 与对数缩放 TF-IDF)
from sklearn.feature_extraction.text import TfidfVectorizer
max_df = 0.8
min_df = 5
stop_words_file = './data/stopwordsHIT.txt'

with open(stop_words_file, 'r', encoding='UTF-8') as f:
    stopwords = f.read().split('\n')

# 使用 TfidfVectorizer 替代 CountVectorizer，加入 sublinear_tf 与 ngram_range=(1, 2)
vect = TfidfVectorizer(max_df=max_df, min_df=min_df, token_pattern=r'(?u)\b\w+\b', 
                        analyzer='char', stop_words=stopwords, sublinear_tf=True, ngram_range=(1, 2))
term_matrix_2 = pd.DataFrame(vect.fit_transform(x.cutted_content).toarray(), columns=vect.get_feature_names_out())

# 5. 划分数据集并重新进行多项式朴素贝叶斯训练
x_train, x_test, y_train, y_test = train_test_split(term_matrix_2, y, random_state=1, test_size=0.2)

model_nb = MultinomialNB().fit(x_train, y_train)
res_nb = model_nb.predict(x_test)

# 6. 打印最终模型评估效果报告
print('【优化后模型】混淆矩阵如下:\n', confusion_matrix(y_test, res_nb))
print('\n【优化后模型】分类效果报告：\n', classification_report(y_test, res_nb))

evaluate_accuracy = accuracy_score(y_test, res_nb)
print('准确率为: %.2f%%' % (evaluate_accuracy * 100.0))
evaluate_p = precision_score(y_test, res_nb, average='micro')
print('精确率为: %.2f%%' % (evaluate_p * 100.0))
evaluate_recall = recall_score(y_test, res_nb, average='micro')
print('召回率为: %.2f%%' % (evaluate_recall * 100.0))
evaluate_f1 = f1_score(y_test, res_nb, average='micro')
print('F1 值为: %.2f%%' % (evaluate_f1 * 100.0))
