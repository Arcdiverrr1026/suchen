import tensorflow as tf
from tensorflow.keras import layers, models, datasets
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint  # 【新增】导入Keras内置的回调函数模块
import matplotlib.pyplot as plt


# 加载MNIST数据集
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()
# 数据预处理
train_images = train_images.reshape((60000, 784)).astype('float32') / 255.0
test_images = test_images.reshape((10000, 784)).astype('float32') / 255.0
train_images = (train_images - 0.5) / 0.5
test_images = (test_images - 0.5) / 0.5
print(f"   训练集: {train_images.shape}, 测试集: {test_images.shape}")

def create_bp_model():
    """创建BP神经网络模型"""
    model = models.Sequential([
        layers.Input(shape=(784,)),#去除keras警告
        layers.Dense(128, activation='relu', input_shape=(784,)),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    return model
model = create_bp_model()
model.summary()

# 配置模型训练参数:
# - optimizer: Adam优化器，自适应学习率
# - loss: 稀疏分类交叉熵，适合整数标签
# - metrics: 监控准确率指标
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 【新增】创建回调函数列表
# 回调1：学习率动态调整（ReduceLROnPlateau）
# 当验证损失连续patience个epoch不下降时，将学习率乘以factor
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',   # 监控验证损失
    factor=0.5,           # 学习率衰减因子，新学习率 = 旧学习率 * 0.5
    patience=2,           # 容忍2个epoch无改善后触发
    min_lr=1e-6,          # 学习率下限，防止过小
    verbose=1             # 打印学习率调整信息
)

# 回调2：早停机制（EarlyStopping）
# 当验证损失连续patience个epoch不改善时，自动停止训练，防止过拟合
early_stopping = EarlyStopping(
    monitor='val_loss',       # 监控验证损失
    patience=3,               # 容忍3个epoch无改善后停止
    min_delta=0.001,          # 最小改善幅度
    restore_best_weights=True,# 恢复最佳模型权重
    verbose=1                 # 打印早停信息
)

# 回调3：模型检查点（ModelCheckpoint）
# 自动保存验证损失最低时的模型版本
model_checkpoint = ModelCheckpoint(
    filepath='best_model.keras',  # 模型保存路径
    monitor='val_loss',           # 监控验证损失
    save_best_only=True,          # 只保存最佳模型
    verbose=1                     # 打印保存信息
)

# 将所有回调函数组合成列表
callbacks_list = [reduce_lr, early_stopping, model_checkpoint]

# 使用fit方法进行训练:
# - epochs: 训练多少个完整周期（从15增加到30，给回调机制更多空间）
# - validation_data: 使用测试集作为验证集
# - verbose: 显示训练进度
# - callbacks: 【新增】传入回调函数列表，实现自动化训练管理
history = model.fit(
    train_images, train_labels,
    epochs=30,
    batch_size=64,
    validation_data=(test_images, test_labels),
    callbacks=callbacks_list,
    verbose=1
)

test_loss, test_accuracy = model.evaluate(test_images, test_labels, verbose=0)
print(f"   测试准确率: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# 设置中文字体
from matplotlib.font_manager import FontProperties

font = FontProperties(
    fname="/Library/Fonts/Arial Unicode.ttf"
)

plt.figure(figsize=(16, 5))

plt.subplot(1, 3, 1)
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('模型损失曲线', fontproperties=font)
plt.xlabel('训练轮次', fontproperties=font)
plt.ylabel('损失值', fontproperties=font)
plt.legend(prop=font)
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(history.history['accuracy'], label='训练准确率')
plt.plot(history.history['val_accuracy'], label='验证准确率')
plt.title('模型准确率曲线', fontproperties=font)
plt.xlabel('训练轮次', fontproperties=font)
plt.ylabel('准确率', fontproperties=font)
plt.legend(prop=font)
plt.grid(True)

# 【新增】绘制学习率变化曲线（从history中获取lr记录）
plt.subplot(1, 3, 3)
if 'lr' in history.history:
    plt.plot(history.history['lr'], 'g-o')
else:
    # 如果history中没有lr记录，手动模拟计算
    lr_values = []
    current_lr = 0.001  # Adam默认学习率
    for i in range(len(history.history['val_loss'])):
        lr_values.append(current_lr)
        # 模拟ReduceLROnPlateau的逻辑
        if i >= 2 and history.history['val_loss'][i] >= history.history['val_loss'][i-2]:
            current_lr *= 0.5
    plt.plot(lr_values, 'g-o')
plt.title('学习率变化曲线', fontproperties=font)
plt.xlabel('训练轮次', fontproperties=font)
plt.ylabel('学习率', fontproperties=font)
plt.grid(True)

plt.tight_layout()
plt.savefig('training_results.png', dpi=300)
plt.show()
