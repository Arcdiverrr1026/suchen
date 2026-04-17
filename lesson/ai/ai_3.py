import pandas as pd
import numpy as np

# 餐饮数据路径（注意根据你的实际目录修改路径）
catering_sale = r'D:\python lanqiao\ai-data\catering_fish_congee.xls'

# 读取数据，指定列名为 'date' 和 'sale'
data = pd.read_excel(catering_sale, names=['date', 'sale'])

# 定义分箱边界和标签
bins = [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
labels = ['[0, 500)', '[500, 1000)', '[1000, 1500)', '[1500, 2000)',
          '[2000, 2500)', '[2500, 3000)', '[3000, 3500)', '[3500, 4000)']

# 使用 pd.cut 进行数据分层
data['sale分层'] = pd.cut(data.sale, bins, labels=labels)

# 分组统计数量
aggResult = data.groupby('sale分层').agg(sale=('sale', 'count'))

# 计算百分比
pAggResult = round(aggResult / aggResult.sum(), 2) * 100

import matplotlib.pyplot as plt

# 设置图框大小
plt.figure(figsize=(10, 6))

# 绘制频率直方图（柱状图）
pAggResult['sale'].plot(kind='bar', width=0.8, fontsize=10)

# 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.title('季度销售额频率分布直方图', fontsize=20)
plt.show()