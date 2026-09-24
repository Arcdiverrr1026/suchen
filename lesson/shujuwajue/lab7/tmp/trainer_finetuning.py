import os
import warnings
warnings.filterwarnings('ignore')
import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.optim import AdamW
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

# 设置设备
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")

# 评论数据集类
class CommentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=64):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long)
        }

def train_epoch(model, data_loader, optimizer, device):
    model.train()
    total_loss = 0
    for batch in data_loader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(data_loader)

def evaluate(model, data_loader, device):
    model.eval()
    predictions = []
    real_values = []
    with torch.no_grad():
        for batch in data_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            _, preds = torch.max(outputs.logits, dim=1)

            predictions.extend(preds.cpu().tolist())
            real_values.extend(labels.cpu().tolist())
    return predictions, real_values

def main():
    print("="*50)
    print("正在运行 BERT/RoBERTa 微调实验 (trainer_finetuning.py)")
    print("="*50)

    # 1. 加载数据并映射标签
    train_df = pd.read_csv('./tmp/f1.csv')
    test_df = pd.read_csv('./tmp/f2.csv')

    # 限制样本数量加速微调演示 (训练 1000 条，测试 200 条)
    train_df = train_df.sample(n=min(1000, len(train_df)), random_state=42).reset_index(drop=True)
    test_df = test_df.sample(n=min(200, len(test_df)), random_state=42).reset_index(drop=True)

    # 标签从 (-1, 0, 1) 映射到 (0, 1, 2)
    label_map = {-1: 0, 0: 1, 1: 2}
    train_df['label_mapped'] = train_df['类别'].map(label_map)
    test_df['label_mapped'] = test_df['类别'].map(label_map)

    # 2. 初始化分词器与模型
    model_name = "bert-base-chinese"
    print(f"正在加载预训练模型与分词器: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)
    model.to(device)

    # 3. 创建 DataLoader
    train_dataset = CommentDataset(train_df['评论内容'].values, train_df['label_mapped'].values, tokenizer)
    test_dataset = CommentDataset(test_df['评论内容'].values, test_df['label_mapped'].values, tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16)

    # 4. 设置优化器
    optimizer = AdamW(model.parameters(), lr=2e-5)

    # 5. 微调训练 (运行 2 个 epoch)
    epochs = 2
    print("开始微调训练...")
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader, optimizer, device)
        print(f"Epoch {epoch+1}/{epochs} - 训练 Loss: {train_loss:.4f}")

    # 6. 测试集评估
    predictions, real_values = evaluate(model, test_loader, device)

    # 映射回原始标签 [-1, 0, 1]
    rev_label_map = {0: -1, 1: 0, 2: 1}
    y_test_orig = [rev_label_map[y] for y in real_values]
    preds_orig = [rev_label_map[p] for p in predictions]

    evaluate_accuracy = accuracy_score(y_test_orig, preds_orig)
    print('准确率为: %.2f%%' % (evaluate_accuracy * 100.0))
    evaluate_p = precision_score(y_test_orig, preds_orig, average='micro')
    print('精确率为: %.2f%%' % (evaluate_p * 100.0))
    evaluate_recall = recall_score(y_test_orig, preds_orig, average='micro')
    print('召回率为: %.2f%%' % (evaluate_recall * 100.0))
    evaluate_f1 = f1_score(y_test_orig, preds_orig, average='micro')
    print('F1 值为: %.2f%%' % (evaluate_f1 * 100.0))
    print("\n分类效果报告:")
    print(classification_report(y_test_orig, preds_orig))
    print("混淆矩阵:")
    print(confusion_matrix(y_test_orig, preds_orig))

if __name__ == '__main__':
    main()
