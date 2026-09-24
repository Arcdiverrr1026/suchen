import pandas as pd
import numpy as np
import os

# 路径设置
data_path = './data/Comments.csv'
f1_path = './tmp/f1.csv'
f2_path = './tmp/f2.csv'
reviews_path = './tmp/reviews.csv'

# 读取数据
df = pd.read_csv(data_path)
print(f"原始数据维度: {df.shape}")

# 去除缺失值
df = df.dropna(subset=['评论内容', '类别'])
print(f"清除空值后维度: {df.shape}")

# 随机打乱并按 8:2 比例划分
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
train_size = int(len(df_shuffled) * 0.8)

train_df = df_shuffled.iloc[:train_size]
test_df = df_shuffled.iloc[train_size:]

# 保存文件
train_df.to_csv(f1_path, index=False, encoding='utf-8-sig')
test_df.to_csv(f2_path, index=False, encoding='utf-8-sig')
test_df.to_csv(reviews_path, index=False, encoding='utf-8-sig')

print(f"训练集 ({f1_path}) 样本数: {train_df.shape[0]}")
print(f"测试集 ({f2_path}) 样本数: {test_df.shape[0]}")
