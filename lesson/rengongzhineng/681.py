import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import copy  # 【新增】用于深拷贝模型参数，实现模型检查点功能

# 数据预处理：将图像转换为张量并标准化
transform = transforms.Compose([
    transforms.ToTensor(),  # 将图像转为Tensor格式
    transforms.Normalize((0.5,), (0.5,))  # 标准化到[-1,1]范围
])

# 加载训练集和测试集
train_data = datasets.MNIST('./data', train=True, download=True, transform=transform)
test_data = datasets.MNIST('./data', train=False, download=True, transform=transform)

# 创建数据加载器，方便批量读取数据
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64, shuffle=False)


class EarlyStopping:
    def __init__(self, patience=3, min_delta=0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
        self.early_stop = False

    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            print(f'  [早停] 验证损失未改善，已连续 {self.counter}/{self.patience} 个epoch')
            if self.counter >= self.patience:
                self.early_stop = True
                print('  [早停] 触发早停机制，停止训练！')
        else:
            self.best_loss = val_loss
            self.counter = 0

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        # 网络结构：784(输入) -> 128(隐藏层) -> 64(隐藏层) -> 10(输出)
        self.fc1 = nn.Linear(28 * 28, 128) #第一层：输入784像素，输出128个神经元
        self.fc2 = nn.Linear(128, 64)  #第二层：128输入，64输出
        self.fc3 = nn.Linear(64, 10)  #第三层：64输入，10输出（10个数字）
        self.relu = nn.ReLU()  #激活函数，让网络能够学习非线性关系

    def forward(self, x):
        # 前向传播过程：输入 -> 第一层 -> 激活 -> 第二层 -> 激活 -> 输出层
        x = x.view(-1, 28 * 28)  # 将图片展平成一维向量（28x28=784）
        x = self.relu(self.fc1(x))  # 第一层 + 激活函数
        x = self.relu(self.fc2(x))  # 第二层 + 激活函数
        x = self.fc3(x)  # 输出层（不需要激活函数）
        return x
# 创建模型实例
model = SimpleNet()

criterion = nn.CrossEntropyLoss()  # 损失函数：用于计算预测值与真实值的差异
optimizer = optim.Adam(model.parameters(), lr=0.001)  # 优化器：用于更新网络参数

# 【新增】创建回调函数实例
# 1. 学习率调度器：当验证损失连续patience个epoch不下降时，将学习率乘以factor
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode='min',
    factor=0.5,
    patience=2
)
# 2. 早停实例
early_stopping = EarlyStopping(patience=3, min_delta=0.001)
# 3. 模型检查点相关变量
best_val_loss = float('inf')
best_model_state = None

# 记录训练过程中的损失和准确率c
losses = []
accuracies = []
val_losses = []  # 【新增】记录验证损失，用于早停和学习率调度

# 【修改】训练轮次从10增加到20，给回调机制更多发挥作用的空间
for epoch in range(20):
    total_loss = 0
    correct = 0
    total = 0
    # 遍历所有训练数据
    for images, labels in train_loader:
        # 清零梯度（重要：防止梯度累积）
        optimizer.zero_grad()
        # 前向传播：输入图像得到预测结果
        outputs = model(images)
        # 计算损失：预测结果与真实标签的差异
        loss = criterion(outputs, labels)
        # 反向传播：计算梯度
        loss.backward()

        # 更新参数：根据梯度调整网络权重
        optimizer.step()

        # 统计训练结果
        total_loss += loss.item()
        _, predicted = torch.max(outputs.data, 1)  # 获取预测结果
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    # 计算每个epoch的平均损失和准确率
    avg_loss = total_loss / len(train_loader)
    accuracy = 100 * correct / total
    losses.append(avg_loss)
    accuracies.append(accuracy)

    # 【新增】每个epoch结束后在验证集上评估，用于回调函数判断
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    avg_val_loss = val_loss / len(test_loader)
    val_losses.append(avg_val_loss)
    model.train()

    # 【新增】调用回调函数
    # 回调1：学习率动态调整 - 根据验证损失自动调整学习率
    old_lr = optimizer.param_groups[0]['lr']
    scheduler.step(avg_val_loss)
    new_lr = optimizer.param_groups[0]['lr']
    if new_lr != old_lr:
        print(f'  [学习率调整] {old_lr:.6f} -> {new_lr:.6f}')

    # 回调2：模型检查点 - 保存验证损失最低时的模型
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        best_model_state = copy.deepcopy(model.state_dict())
        print(f'  [模型检查点] 保存最佳模型 (验证损失: {best_val_loss:.4f})')

    # 回调3：早停判断 - 检查是否需要提前停止
    early_stopping(avg_val_loss)

    # 【修改】打印信息增加验证损失和学习率
    current_lr = optimizer.param_groups[0]['lr']
    print(f'Epoch {epoch + 1}/20, Loss: {avg_loss:.4f}, Acc: {accuracy:.2f}%, Val Loss: {avg_val_loss:.4f}, LR: {current_lr:.6f}')

    # 如果触发早停，跳出训练循环
    if early_stopping.early_stop:
        break

# 【新增】加载最佳模型参数进行最终测试
if best_model_state is not None:
    model.load_state_dict(best_model_state)
    print(f'\n已加载最佳模型 (最佳验证损失: {best_val_loss:.4f})')

model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
test_accuracy = 100 * correct / total
print(f'测试集准确率: {test_accuracy:.2f}%')

plt.figure(figsize=(16, 4))
# 绘制损失曲线
plt.subplot(1, 3, 1)
plt.plot(losses, 'b-o', label='训练损失')
plt.plot(val_losses, 'r-o', label='验证损失')  # 【新增】绘制验证损失曲线
plt.title('Training & Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
# 绘制准确率曲线
plt.subplot(1, 3, 2)
plt.plot(accuracies, 'r-o')
plt.title('Training Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.grid(True)

# 【新增】绘制学习率变化曲线
lr_history = []
# 需要重新模拟学习率变化过程来记录
optimizer_lr = optim.Adam(model.parameters(), lr=0.001)
scheduler_lr = optim.lr_scheduler.ReduceLROnPlateau(optimizer_lr, mode='min', factor=0.5, patience=2)
for vl in val_losses:
    lr_history.append(optimizer_lr.param_groups[0]['lr'])
    scheduler_lr.step(vl)

plt.subplot(1, 3, 3)
plt.plot(lr_history, 'g-o')
plt.title('Learning Rate Schedule')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.grid(True)

plt.tight_layout()
plt.savefig('training_results.png')
plt.show()
