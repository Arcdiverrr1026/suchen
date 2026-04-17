import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ================== 1. 参数初始化与数据导入 ==================
inputfile = r'D:\qqflie\20260414-数据挖掘实验课\实验内容\data\sales_data.xls'
data = pd.read_excel(inputfile, index_col='序号')

# ================== 2. 数据预处理 ==================
# 放弃会报错的布尔索引，使用最安全的字典映射替换
mapping_dict = {
    '好': 1, '是': 1, '高': 1,
    '坏': 0, '否': 0, '低': 0
}
data = data.replace(mapping_dict)

x = data.iloc[:, :3].astype(int)
y = data.iloc[:, 3].astype(int)

# ================== 3. 构建神经网络模型 ==================
model = Sequential()
model.add(Dense(input_dim=3, units=5))
model.add(Activation('relu'))

# 修复上一版中潜在的维度冲突报错，这里直接指定输出 units 即可
model.add(Dense(units=1))
model.add(Activation('sigmoid'))

# ================== 4. 编译与训练模型 ==================
model.compile(loss='binary_crossentropy', optimizer='adam')
model.fit(x, y, epochs=1000, batch_size=10, verbose=1)  # 训练模型

# ================== 5. 模型预测 ==================
yp = (model.predict(x) > 0.5).astype(int).reshape(len(y))

# ================== 6. 结果可视化 (彻底告别 cm_plot) ==================
# 设置中文字体，防止图表显示方块乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 计算并直接绘制混淆矩阵
cm = confusion_matrix(y, yp)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['类别 0', '类别 1'])
disp.plot(cmap=plt.cm.Blues)
plt.title('混淆矩阵可视化')
plt.show()  # 弹出图表