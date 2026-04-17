import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 解决 KMeans 在某些环境下的 RuntimeWarning 问题
os.environ['OMP_NUM_THREADS'] = '1'

# 1. 参数初始化与数据导入
inputfile = r'D:\qqflie\20260414-数据挖掘实验课\实验内容\data\consumption_data.xls'
outputfile = r'D:\qqflie\20260414-数据挖掘实验课\实验内容\data\data.type.xlsx'
k = 3                                       # 聚类的类别
iteration = 500                             # 聚类最大循环次数

# 2. 读取数据
# 假设 Excel 文件中第一列是 'ID'，作为索引
data = pd.read_excel(inputfile, index_col='ID')
# 获取特征名称
features = data.columns.tolist()

# 3. 数据预处理
# 数据标准化（Z-score标准化）
# 计算标准化后的数据
data_zs = 1.0 * (data - data.mean()) / data.std()

# 4. 构建神经网络模型与训练
# 初始化K-Means模型，指定类别数、最大循环次数和 random_state 以保证结果可复现
model = KMeans(n_clusters=k, max_iter=iteration, random_state=1234, n_init='auto')
# 开始聚类，使用标准化后的数据
model.fit(data_zs)

# 5. 结果统计
# 统计各个类别的数目
r1 = pd.Series(model.labels_).value_counts()
# 找出聚类中心
r2 = pd.DataFrame(model.cluster_centers_)
# 横向连接（0是纵向），得到聚类中心对应的类别下的数目
r = pd.concat([r2, r1], axis=1)
# 重命名表头，使用原始特征名称 + '类别数目'
r.columns = features + ['类别数目']
print("聚类中心及类别数目：")
print(r)

# 6. 保存聚类结果
# 详细输出原始数据及其类别，以及标准化后的特征数据
# 将标准化特征数据、原始数据和标签连接
r = pd.concat([data_zs, data, pd.Series(model.labels_, index=data.index)], axis=1)
# 重命名表头，使用标准化特征名称、原始特征名称 + '聚类类别'
r.columns = [f + '_zs' for f in features] + features + ['聚类类别']
# 保存结果
r.to_excel(outputfile)
print(f"\n聚类结果已成功保存至：{outputfile}")

# 7. 绘制各类型特征的概率密度分布图
# 设置绘图风格
sns.set_style("whitegrid")
# 设置中文显示，防止乱码（根据系统环境可能需要调整）
plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows 系统通常使用黑体
plt.rcParams['axes.unicode_minus'] = False

# 准备绘图数据
# 将标准化数据和标签合并
plot_data = data_zs.copy()
plot_data['聚类类别'] = model.labels_

# 创建一个 3 行 1 列的画布，用于分别绘制三个类别
fig, axes = plt.subplots(k, 1, figsize=(10, 15), sharex=True)

# 循环为每个类别绘制概率密度图
for i in range(k):
    # 提取第 i 个类别的数据
    cls_data = plot_data[plot_data['聚类类别'] == i]
    # 在第 i 个子图中，为每个特征（R, F, M）绘制 kdeplot
    # 使用 melt 函数将宽格式数据转换为长格式，方便 seaborn 绘图
    cls_data_melt = cls_data.melt(id_vars='聚类类别', var_name='特征', value_name='标准化值')
    sns.kdeplot(data=cls_data_melt, x='标准化值', hue='特征', fill=True, ax=axes[i], legend=(i==0))
    axes[i].set_title(f'类别 {i} 的特征概率密度分布图')
    axes[i].set_ylabel('密度')

# 设置共同的 x 轴标签
plt.xlabel('标准化值')
plt.tight_layout()
plt.show()