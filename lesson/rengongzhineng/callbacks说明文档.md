# 回调函数（Callbacks）系统 — 代码修改说明

## 一、什么是回调函数？

回调函数是在模型训练过程中**自动触发**的机制，用于在特定时机执行特定操作。它不需要手动干预，能够：
- **自动调整学习率**：当模型陷入局部最优时降低学习率
- **自动停止训练**：当模型开始过拟合时及时停止
- **自动保存模型**：保存训练过程中表现最好的模型版本

---

## 二、681.py 修改说明（PyTorch 版本）

### 2.1 新增导入模块
```python
import copy  # 用于深拷贝模型参数，实现模型检查点功能
```
**说明**：PyTorch 中模型参数是引用类型，需要使用 `copy.deepcopy()` 深拷贝才能独立保存最佳模型状态。

### 2.2 新增 EarlyStopping 类（约第24-50行）
```python
class EarlyStopping:
    """早停机制：当验证损失连续多个epoch不再改善时，自动停止训练"""
    def __init__(self, patience=3, min_delta=0.001):
        ...
    def __call__(self, val_loss):
        ...
```
**说明**：PyTorch 没有内置的回调系统，需要手动实现 `EarlyStopping` 类。
- `patience=3`：容忍连续3个epoch验证损失不改善
- `min_delta=0.001`：损失改善幅度小于0.001视为没有改善
- 每次epoch结束后调用 `early_stopping(val_loss)` 判断是否停止

### 2.3 新增回调函数实例化（约第74-86行）
```python
# 1. 学习率调度器
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, mode='min', factor=0.5, patience=2
)
# 2. 早停实例
early_stopping = EarlyStopping(patience=3, min_delta=0.001)
# 3. 模型检查点变量
best_val_loss = float('inf')
best_model_state = None
```
**说明**：
- `ReduceLROnPlateau`：PyTorch 内置的学习率调度器，监控验证损失，连续2个epoch不改善则学习率乘以0.5
- `EarlyStopping`：自定义的早停类，连续3个epoch不改善则触发早停
- 模型检查点通过变量 `best_model_state` 保存最佳参数

### 2.4 修改训练循环（约第90-140行）
**主要修改**：
1. 训练轮次从 `10` 增加到 `20`，给回调机制更多发挥作用的空间
2. 每个epoch结束后在验证集上计算验证损失
3. 调用三个回调函数：
   - `scheduler.step(avg_val_loss)` — 学习率动态调整
   - 模型检查点保存 — 验证损失降低时保存模型
   - `early_stopping(avg_val_loss)` — 早停判断
4. 如果触发早停，使用 `break` 跳出训练循环

### 2.5 新增加载最佳模型（约第150行）
```python
if best_model_state is not None:
    model.load_state_dict(best_model_state)
```
**说明**：训练结束后，加载验证损失最低时的模型参数进行测试，而不是使用最后一个epoch的参数。

### 2.6 修改绘图部分
- 原有：训练损失曲线、准确率曲线（2个子图）
- 修改为：训练+验证损失曲线、准确率曲线、学习率变化曲线（3个子图）

---

## 三、682.py 修改说明（TensorFlow/Keras 版本）

### 3.1 新增导入模块（第3行）
```python
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
```
**说明**：Keras 提供了丰富的内置回调函数，直接导入即可使用，无需手动实现。

### 3.2 新增回调函数列表（约第40-70行）
```python
# 回调1：学习率动态调整
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss', factor=0.5, patience=2, min_lr=1e-6, verbose=1
)

# 回调2：早停机制
early_stopping = EarlyStopping(
    monitor='val_loss', patience=3, min_delta=0.001,
    restore_best_weights=True, verbose=1
)

# 回调3：模型检查点
model_checkpoint = ModelCheckpoint(
    filepath='best_model.keras', monitor='val_loss',
    save_best_only=True, verbose=1
)

callbacks_list = [reduce_lr, early_stopping, model_checkpoint]
```

**三个回调函数详解**：

| 回调函数 | 作用 | 关键参数 |
|---------|------|---------|
| `ReduceLROnPlateau` | 动态调整学习率 | `factor=0.5`：学习率减半；`patience=2`：2个epoch无改善触发 |
| `EarlyStopping` | 早停防止过拟合 | `patience=3`：3个epoch无改善停止；`restore_best_weights=True`：恢复最佳权重 |
| `ModelCheckpoint` | 保存最佳模型 | `save_best_only=True`：只保存最佳模型到 `best_model.keras` |

### 3.3 修改 model.fit() 调用（约第75-85行）
```python
history = model.fit(
    ...
    epochs=30,                    # 【修改】从15增加到30
    callbacks=callbacks_list,     # 【新增】传入回调函数列表
    ...
)
```
**说明**：
- `epochs=30`：增加训练轮次，因为早停机制会自动在合适的时机停止
- `callbacks=callbacks_list`：将三个回调函数传入 `fit()` 方法

### 3.4 新增学习率变化曲线
在原有2个子图基础上，新增第3个子图显示学习率随训练的变化情况。

---

## 四、PyTorch 与 Keras 回调机制对比

| 特性 | PyTorch（681.py） | Keras（682.py） |
|------|-------------------|-----------------|
| 学习率调度 | `optim.lr_scheduler.ReduceLROnPlateau` | `tf.keras.callbacks.ReduceLROnPlateau` |
| 早停机制 | 需要手动实现 `EarlyStopping` 类 | 内置 `tf.keras.callbacks.EarlyStopping` |
| 模型检查点 | 需要手动 `copy.deepcopy()` 保存参数 | 内置 `tf.keras.callbacks.ModelCheckpoint` |
| 使用方式 | 在训练循环中手动调用 | 传入 `fit()` 的 `callbacks` 参数 |

---

## 五、回调函数的工作流程

```
Epoch 1 开始 → 训练 → 验证 → 回调函数检查
                              ├── 学习率是否需要调整？
                              ├── 是否保存为最佳模型？
                              └── 是否触发早停？
Epoch 2 开始 → 训练 → 验证 → 回调函数检查
...
（直到训练完成或触发早停）
```

---

## 六、运行结果预期

运行修改后的代码，你应该能看到类似输出：
```
Epoch 1/20, Loss: 0.3521, Acc: 89.52%, Val Loss: 0.1523, LR: 0.001000
  [模型检查点] 保存最佳模型 (验证损失: 0.1523)
Epoch 2/20, Loss: 0.1234, Acc: 96.21%, Val Loss: 0.1087, LR: 0.001000
  [模型检查点] 保存最佳模型 (验证损失: 0.1087)
...
Epoch 8/20, Loss: 0.0456, Acc: 98.52%, Val Loss: 0.0892, LR: 0.001000
  [早停] 验证损失未改善，已连续 1/3 个epoch
Epoch 9/20, Loss: 0.0412, Acc: 98.67%, Val Loss: 0.0895, LR: 0.001000
  [早停] 验证损失未改善，已连续 2/3 个epoch
Epoch 10/20, Loss: 0.0398, Acc: 98.71%, Val Loss: 0.0891, LR: 0.000500
  [学习率调整] 0.001000 -> 0.000500
...
  [早停] 触发早停机制，停止训练！
已加载最佳模型 (最佳验证损失: 0.0891)
测试集准确率: 98.45%
```

---

## 七、总结

通过添加回调函数系统，模型训练实现了：
1. **学习率动态调整**：自动在训练停滞时降低学习率，帮助模型跳出局部最优
2. **早停机制**：智能判断何时停止训练，避免过拟合，节省训练时间
3. **模型检查点**：自动保存最佳模型版本，确保使用最优参数进行测试
