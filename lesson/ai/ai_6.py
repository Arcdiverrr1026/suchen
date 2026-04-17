import pandas as pd

# 1. 定义文件路径（请根据你的实际情况修改路径）
sales_data = r'D:\python lanqiao\ai-data\sales_data.csv'  # 超市日营收数据

# 2. 读取数据，指定"日期"列为索引列，使用 gbk 编码以防中文乱码
data = pd.read_csv(sales_data, index_col='日期', encoding='gbk')

# 3. 过滤异常数据：保留销售额在 15000 到 50000 之间的记录
data = data[(data['销售额/元'] > 15000) & (data['销售额/元'] < 50000)]

# 4. 获取基本统计量（count, mean, std, min, 25%, 50%, 75%, max）
statistics = data.describe()  # 保存基本统计量

# 5. 计算并添加额外的统计量
statistics.loc['range'] = statistics.loc['max'] - statistics.loc['min']  # 极差
statistics.loc['var'] = statistics.loc['std'] / statistics.loc['mean']    # 变异系数
statistics.loc['dis'] = statistics.loc['75%'] - statistics.loc['25%']    # 四分位数间距

# 6. 打印最终的统计结果
print(statistics)