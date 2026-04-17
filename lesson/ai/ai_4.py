import pandas as pd
import matplotlib.pyplot as plt

# 餐饮数据路径（注意：运行前请确认文件路径是否正确）
catering_dish_profit = r'D:\python lanqiao\ai-data\catering_dish_profit.xls'  # 餐饮数据
data = pd.read_excel(catering_dish_profit)  # 读取数据

# --- 绘制饼图 ---
x = data['盈利/元']
labels = data['菜品名']

plt.figure(figsize=(8, 6))                # 设置画布大小
plt.pie(x, labels=labels)                 # 绘制饼图
plt.rcParams['font.sans-serif'] = 'SimHei' # 设置中文字体
plt.title('菜品销售量分布（饼图）')        # 设置标题
plt.axis('equal')                         # 保证饼图是正圆
plt.show()

# --- 绘制条形图 ---
x = data['菜品名']
y = data['盈利/元']

plt.figure(figsize=(8, 4))                # 设置画布大小
plt.bar(x, y)                             # 绘制条形图
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.xlabel('菜品')                         # 设置x轴标题
plt.ylabel('销量')                         # 设置y轴标题（注：原图中此处为销量，建议根据实际数据改为盈利）
plt.title('菜品销售量分布（条形图）')       # 设置标题
plt.show()                                # 展示图片