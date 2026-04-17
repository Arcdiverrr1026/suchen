import pandas as pd
import matplotlib.pyplot as plt
import warnings

# 屏蔽所有无用警告
warnings.filterwarnings("ignore")

# 解决中文显示（Windows 100%可用）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ------------------- 第一张图：快递类型对比 -------------------
data = pd.read_excel(r'D:\python lanqiao\ai-data\Business_volume.xls')

plt.figure(figsize=(8, 4))
plt.plot(data['月份'], data['同城快递量当期值/件'], color='green', label='同城快递量', marker='o')
plt.plot(data['月份'], data['异地快递量当期值/件'], color='red', label='异地快递量', marker='s')
plt.plot(data['月份'], data['国际快递量当期值/件'], color='skyblue', label='国际快递量', marker='x')

plt.legend()
plt.ylabel('快递量/件')
plt.title('各类型快递量对比')
plt.show()

# ------------------- 第二张图：年份对比 -------------------
data = pd.read_excel(r'D:\python lanqiao\ai-data\Business_volume_b.xls')

plt.figure(figsize=(8, 4))
plt.plot(data['月份'], data['2021年'], color='green', label='2021年', marker='o')
plt.plot(data['月份'], data['2022年'], color='red', label='2022年', marker='s')
plt.plot(data['月份'], data['2023年'], color='skyblue', label='2023年', marker='x')

plt.legend()
plt.ylabel('快递量/件')
plt.title('同城快递各年份对比')
plt.show()