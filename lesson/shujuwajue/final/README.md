# 电商购物篮关联规则挖掘 - 运行说明

本项目为数据挖掘课程大作业，基于经典的 **Online Retail** 真实数据集，使用 **Apriori 算法**进行频繁项集挖掘与强关联规则分析。

---

## 📁 目录结构

本提交包共包含以下三个文件夹：
1. **`电子版论文/`**：包含课程设计论文的完整正文（Markdown 格式，便于复制及格式转换）。
2. **`代码文件夹/`**：包含核心运行脚本及本说明文件。
   - `association_rule_mining.py`：主运行脚本（包含超详细中文注释）。
   - `README.md`：本运行说明文件。
3. **`中间过程文件夹/`**：存放代码运行中生成的图表和中间数据。
   - `plots/`：5 张可视化分析图表（柱状图、饼图、长尾分布图、散点图、网络拓扑图）。
   - `association_rules.csv`：挖掘出的 323 条强关联规则（按 Lift 降序）。
   - `category_mapping.csv`：商品编码与五大品类的映射表。
   - `binarized_matrix.csv`：二值化处理后的订单-商品矩阵（由于文件较大约 106MB，若超出提交限制，可运行代码重新生成）。

---

## 🛠️ 环境依赖与安装

本项目使用 Python 3.9+ 编写。运行代码前需要安装以下依赖包：

```bash
pip install pandas numpy openpyxl mlxtend matplotlib seaborn
```

### 依赖包说明：
- `pandas` & `openpyxl`：用于高效读取 `.xlsx` 格式的交易数据集并进行数据清洗。
- `mlxtend`：提供高效的 `apriori` 和 `association_rules` 算法支持。
- `matplotlib` & `seaborn`：用于绘制精美的实验图表，支持中文字体显示。

---

## 🚀 代码运行方法

1. 将原始数据集 `Online Retail.xlsx` 放置在与 `association_rule_mining.py` 相同的目录下（或在命令行中指定路径）。
2. 打开终端并执行以下命令运行脚本：

```bash
python association_rule_mining.py --input "Online Retail.xlsx"
```

运行后，脚本会自动执行以下 **10 个步骤**：
1. **加载数据**：读取 54 余万条原始交易数据。
2. **数据清洗**：剔除缺失值、退货单（C开头）、异常值。
3. **低频商品过滤**：保留频次 $\ge 10$ 的 2882 种核心商品。
4. **商品分类映射**：将商品归入家居装饰、厨房餐饮、礼品派对、食品饮料及其他五大品类。
5. **导出映射表**：生成 `category_mapping.csv`。
6. **事务集二值化**：构建 18,507×2,882 的 0/1 稀疏矩阵并导出。
7. **Apriori 挖掘**：基于 `min_support=0.01` 挖掘频繁项集。
8. **关联规则计算**：基于 `min_confidence=0.5` 与 `lift > 1.0` 筛选 323 条强关联规则。
9. **可视化出图**：在指定的输出目录下生成 5 张 PNG 图表。
10. **输出统计报告**：在终端打印中文实验统计报告和 Top 10 强关联规则。
