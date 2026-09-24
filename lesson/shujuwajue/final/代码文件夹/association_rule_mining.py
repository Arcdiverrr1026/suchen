#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基于电商购物篮数据的协同关联规则挖掘实验
"""

import os
import argparse
import warnings
import textwrap
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def load_data(filepath):
    """加载 Excel 或 CSV 格式的交易数据"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在：{filepath}")
    
    if filepath.lower().endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        excel_file = pd.ExcelFile(filepath)
        sheet_name = "Online Retail" if "Online Retail" in excel_file.sheet_names else 0
        df = excel_file.parse(sheet_name)
        
    if df.empty:
        raise ValueError("数据源为空")
        
    required_cols = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"缺少必要列：{missing_cols}")
    return df


def clean_data(df):
    """数据清洗：过滤缺失值、退货单和异常数值"""
    df = df.copy()
    df = df.dropna(subset=['CustomerID', 'Description'])
    
    df['InvoiceNo'] = df['InvoiceNo'].astype(str).str.strip()
    df['StockCode'] = df['StockCode'].astype(str).str.strip()
    
    df = df[~df['InvoiceNo'].str.startswith(('C', 'c'), na=False)]
    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]
    
    print(f"数据清洗完成：保留有效记录 {len(df):,} 条")
    return df


def filter_low_frequency(df, threshold=10):
    """过滤购买频次低于阈值的商品"""
    counts = df['StockCode'].value_counts()
    valid_stock_codes = counts[counts >= threshold].index
    filtered_df = df[df['StockCode'].isin(valid_stock_codes)].copy()
    print(f"低频商品过滤完成：商品种类从 {len(counts)} 缩减至 {len(valid_stock_codes)}")
    return filtered_df


def categorize_products(df):
    """根据描述将商品划分为五大主要品类"""
    df = df.copy()
    if df.empty:
        df['Category'] = pd.Series(dtype=str)
        return df
        
    def get_category(desc):
        if not isinstance(desc, str):
            return 'Other'
        desc_upper = desc.upper()
        
        # 1. 食品与饮料
        if any(k in desc_upper for k in ['SWEET', 'CHOCOLATE', 'DRINK', 'FOOD', 'SOUP', 'JUICE', 'CANDY', 'COCOA', 'BISCUIT']):
            return 'Food & Beverages'
        # 2. 厨房与餐饮用品
        if any(k in desc_upper for k in ['MUG', 'CUP', 'PLATE', 'BOWL', 'JAR', 'BOTTLE', 'TIN', 'TEATIME', 'CUTLERY', 'SPOON', 'FORK', 'GLASS', 'JUG', 'PAN', 'KITCHEN', 'COFFEE', 'TEA', 'DISH', 'TRAY', 'BAKING', 'CAKE', 'TEAPOT']):
            return 'Kitchenware & Tableware'
        # 3. 家具与家居装饰
        if any(k in desc_upper for k in ['FURNITURE', 'CHAIR', 'TABLE', 'LIGHT', 'CANDLE', 'CLOCK', 'HANGER', 'HOLDER', 'WALL', 'FRAME', 'MIRROR', 'DOORMAT', 'SHELF', 'STAND', 'CABINET', 'CUSHION', 'RUG', 'HEART', 'SIGN', 'HOOK', 'DRAWER', 'PLANT', 'FLOWER', 'POT', 'VASE']):
            return 'Furniture & Home Decor'
        # 4. 礼品、玩具与派对用品
        if any(k in desc_upper for k in ['TOY', 'DOLL', 'GAME', 'PARTY', 'BALLOON', 'BUNTING', 'GIFT', 'WRAP', 'CARD', 'BAG', 'BOX', 'CHRISTMAS', 'PENCIL', 'PEN', 'STICKERS', 'ERASER', 'RIBBON', 'TICKET', 'STICKER']):
            return 'Gifts, Toys & Party'
        return 'Other'

    df['Category'] = df['Description'].apply(get_category)
    return df


def export_mapping(df, filepath):
    """导出商品映射关系字典为 CSV 文件"""
    if df.empty or 'StockCode' not in df.columns or 'Description' not in df.columns:
        pd.DataFrame(columns=['StockCode', 'Description', 'Category']).to_csv(filepath, index=False)
        return
        
    freq_df = df.groupby(['StockCode', 'Description'], dropna=False).size().reset_index(name='frequency')
    freq_df['desc_len'] = freq_df['Description'].astype(str).str.len()
    freq_df = freq_df.sort_values(by=['StockCode', 'frequency', 'desc_len'], ascending=[True, False, False])
    resolved = freq_df.drop_duplicates(subset=['StockCode'], keep='first').copy()
    
    if 'Category' in df.columns:
        cat_map = df[['StockCode', 'Description', 'Category']].drop_duplicates(subset=['StockCode', 'Description'])
        resolved = resolved.merge(cat_map, on=['StockCode', 'Description'], how='left')
    else:
        resolved = categorize_products(resolved)
        
    output_df = resolved[['StockCode', 'Description', 'Category']]
    output_df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"商品分类映射表已导出：{filepath}")


def binarize_matrix(df):
    """将事务集转化为二值化稀疏矩阵"""
    if df.empty:
        return pd.DataFrame()
    temp = df[['InvoiceNo', 'StockCode']].dropna()
    matrix = temp.groupby(['InvoiceNo', 'StockCode']).size().unstack(fill_value=0)
    matrix = (matrix > 0).astype(int)
    print(f"二值化矩阵构建成功：订单数 {matrix.shape[0]}, 商品种类数 {matrix.shape[1]}")
    return matrix


def mine_rules(binary_df, min_support=0.01, min_confidence=0.5):
    """使用 Apriori 算法计算强关联规则"""
    columns = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
    if binary_df.empty:
        return pd.DataFrame(columns=columns), 0
        
    from mlxtend.frequent_patterns import apriori, association_rules
    df_bool = binary_df.astype(bool)
    
    frequent_itemsets = apriori(df_bool, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame(columns=columns), 0
        
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    if rules.empty:
        return pd.DataFrame(columns=columns), len(frequent_itemsets)
        
    rules = rules[rules['lift'] > 1.0].sort_values(by='lift', ascending=False)
    rules = rules[columns].reset_index(drop=True)
    print(f"频繁项集挖掘完成：频繁项集数 {len(frequent_itemsets)}，强关联规则数 {len(rules)}")
    return rules, len(frequent_itemsets)


def generate_plots(df, rules, plot_dir):
    """生成各类关联规则挖掘的可视化图表"""
    os.makedirs(plot_dir, exist_ok=True)
    
    # 1. Top 20 高频商品购买频次柱状图
    plt.figure(figsize=(12, 7))
    if not df.empty and 'Description' in df.columns:
        top_20 = df['Description'].value_counts().head(20)
        colors = sns.color_palette('viridis', n_colors=20)
        plt.barh(range(len(top_20)), top_20.values, color=colors)
        plt.yticks(range(len(top_20)), top_20.index, fontsize=9)
        plt.gca().invert_yaxis()
        for i, val in enumerate(top_20.values):
            plt.text(val + 10, i, f'{val:,}', va='center', fontsize=8)
        plt.title('Top 20 高频商品购买频次柱状图', fontsize=14, fontweight='bold')
        plt.xlabel('购买频次', fontsize=11)
        plt.ylabel('商品描述', fontsize=11)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'top_products.png'), dpi=150)
    plt.close()
    
    # 2. 商品大类分布饼图
    plt.figure(figsize=(9, 9))
    if not df.empty and 'Category' in df.columns:
        cat_counts = df['Category'].value_counts()
        colors = sns.color_palette('pastel', n_colors=len(cat_counts))
        explode = [0.03 if cat != 'Other' else 0 for cat in cat_counts.index]
        wedges, texts, autotexts = plt.pie(
            cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%',
            startangle=140, colors=colors, explode=explode, pctdistance=0.85,
            textprops={'fontsize': 10}
        )
        for autotext in autotexts:
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        plt.title('商品大类分布饼图', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'categories_pie.png'), dpi=150)
    plt.close()
    
    # 3. 商品购买频次长尾效应分布图
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    if not df.empty and 'StockCode' in df.columns:
        counts = df['StockCode'].value_counts().values
        ranks = np.arange(1, len(counts) + 1)
        
        ax1.plot(ranks, counts, color='#2196F3', linewidth=1.5, alpha=0.8)
        ax1.fill_between(ranks, counts, alpha=0.15, color='#2196F3')
        ax1.set_title('商品频次分布（线性坐标）', fontsize=12, fontweight='bold')
        ax1.set_xlabel('商品排名', fontsize=10)
        ax1.set_ylabel('购买频次', fontsize=10)
        ax1.grid(True, linestyle='--', alpha=0.3)
        
        top_10_pct = int(len(counts) * 0.1)
        top_10_sales = counts[:top_10_pct].sum()
        total_sales = counts.sum()
        ax1.axvline(x=top_10_pct, color='red', linestyle='--', alpha=0.7,
                    label=f'前10%商品贡献 {top_10_sales/total_sales*100:.1f}% 销量')
        ax1.legend(fontsize=9)
        
        ax2.plot(ranks, counts, 'o', color='#FF5722', markersize=2, alpha=0.6)
        ax2.set_yscale('log')
        ax2.set_title('商品频次分布（对数坐标 - 长尾效应）', fontsize=12, fontweight='bold')
        ax2.set_xlabel('商品排名', fontsize=10)
        ax2.set_ylabel('购买频次（对数尺度）', fontsize=10)
        ax2.grid(True, linestyle='--', alpha=0.3)
        
    fig.suptitle('商品购买频次长尾效应分析', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'long_tail_distribution.png'), dpi=150, bbox_inches='tight')
    plt.close()
    
    # 4. 关联规则 Support vs Confidence 散点图
    plt.figure(figsize=(10, 7))
    if rules is not None and not rules.empty:
        min_lift = rules['lift'].min()
        max_lift = rules['lift'].max()
        sizes = 50 if pd.isna(min_lift) or pd.isna(max_lift) or min_lift == max_lift else 50 + 250 * (rules['lift'] - min_lift) / (max_lift - min_lift)
        sc = plt.scatter(
            rules['support'], rules['confidence'], c=rules['lift'], s=sizes,
            cmap='plasma', alpha=0.65, edgecolors='white', linewidth=0.5
        )
        plt.colorbar(sc, label='提升度 (Lift)')
        plt.title('关联规则散点图：支持度 vs 置信度', fontsize=14, fontweight='bold')
        plt.xlabel('支持度 (Support)', fontsize=11)
        plt.ylabel('置信度 (Confidence)', fontsize=11)
        plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'association_rules_scatter.png'), dpi=150)
    plt.close()
    
    # 5. Top 10 强关联规则网络拓扑图
    plt.figure(figsize=(12, 12))
    if rules is not None and not rules.empty:
        top_rules = rules.head(10)
        mapping_dict = {}
        if df is not None and not df.empty:
            df_temp = df.dropna(subset=['StockCode', 'Description'])
            for _, row in df_temp.drop_duplicates(subset=['StockCode']).iterrows():
                mapping_dict[str(row['StockCode']).strip()] = str(row['Description']).strip()
                
        def get_wrapped_label(items):
            if isinstance(items, str):
                items = [items]
            descs = [mapping_dict.get(str(x).strip(), str(x)) for x in items]
            return textwrap.fill(", ".join(descs), width=18)
            
        G = nx.DiGraph()
        for _, row in top_rules.iterrows():
            ant_label = get_wrapped_label(row['antecedents'])
            con_label = get_wrapped_label(row['consequents'])
            G.add_edge(ant_label, con_label, weight=row['lift'], confidence=row['confidence'], lift=row['lift'])
            
        pos = nx.spring_layout(G, k=2.5, seed=42)
        edges = G.edges()
        weights = [G[u][v]['weight'] for u, v in edges]
        if weights:
            max_w, min_w = max(weights), min(weights)
            span = max_w - min_w
            widths = [1.5 + 3.5 * (w - min_w) / (span if span > 0 else 1) for w in weights]
        else:
            widths = []
            
        node_colors = []
        for node in G.nodes():
            in_deg = G.in_degree(node)
            out_deg = G.out_degree(node)
            if in_deg == 0:
                node_colors.append('#FFD1B3')
            elif out_deg == 0:
                node_colors.append('#B3E5FC')
            else:
                node_colors.append('#C3B1E1')
                
        nx.draw_networkx_nodes(G, pos, node_size=4000, node_color=node_colors, alpha=0.9, edgecolors='#666', linewidths=1.5)
        nx.draw_networkx_edges(G, pos, width=widths, edge_color='#888', arrows=True, arrowstyle='->', arrowsize=18, node_size=4000, connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
        
        edge_labels = {(u, v): f"C:{d['confidence']:.2f}\nL:{d['lift']:.1f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
        
        plt.title('Top 10 强关联规则网络拓扑图', fontsize=14, fontweight='bold')
        plt.axis('off')
        
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FFD1B3', edgecolor='#666', label='前件 (Antecedent)'),
            Patch(facecolor='#B3E5FC', edgecolor='#666', label='后件 (Consequent)'),
            Patch(facecolor='#C3B1E1', edgecolor='#666', label='双向关联'),
        ]
        plt.legend(handles=legend_elements, loc='lower right', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'rules_network.png'), dpi=150)
    plt.close()
    print("数据可视化图表生成成功。")
    print()


def main():
    parser = argparse.ArgumentParser(description="基于电商购物篮数据的协同关联规则挖掘实验")
    parser.add_argument("--input", type=str, default="Online Retail.xlsx", help="输入数据文件路径")
    parser.add_argument("--min-support", type=float, default=0.01, help="最小支持度阈值")
    parser.add_argument("--min-confidence", type=float, default=0.5, help="最小置信度阈值")
    parser.add_argument("--low-freq-threshold", type=int, default=10, help="低频商品过滤阈值")
    parser.add_argument("--output-rules", type=str, default="association_rules.csv", help="关联规则输出路径")
    parser.add_argument("--output-mapping", type=str, default="category_mapping.csv", help="商品映射表输出路径")
    parser.add_argument("--output-plot-dir", type=str, default="plots", help="图表输出目录")
    parser.add_argument("--no-plots", action="store_true", help="禁止生成可视化图表")
    args = parser.parse_args()
    
    if args.min_support < 0.0 or args.min_support > 1.0:
        parser.error("min-support 必须在 0.0 到 1.0 之间")
    if args.min_confidence < 0.0 or args.min_confidence > 1.0:
        parser.error("min-confidence 必须在 0.0 到 1.0 之间")
        
    print("正在加载数据...")
    df = load_data(args.input)
    
    print("正在清洗数据...")
    df_clean = clean_data(df)
    
    print("正在过滤低频商品...")
    df_filtered = filter_low_frequency(df_clean, threshold=args.low_freq_threshold)
    
    print("正在建立商品类别映射...")
    df_cat = categorize_products(df_filtered)
    
    print("正在导出商品大类映射表...")
    export_mapping(df_cat, args.output_mapping)
    
    print("正在构建订单二值化事务矩阵...")
    binary_df = binarize_matrix(df_filtered)
    
    print("正在运行 Apriori 关联规则挖掘...")
    rules, freq_count = mine_rules(binary_df, args.min_support, args.min_confidence)
    
    print("正在导出强关联规则结果...")
    export_rules = rules.copy()
    if not export_rules.empty:
        export_rules['antecedents'] = export_rules['antecedents'].apply(lambda x: ", ".join(sorted([str(item) for item in x])) if isinstance(x, (frozenset, set, list, tuple)) else str(x))
        export_rules['consequents'] = export_rules['consequents'].apply(lambda x: ", ".join(sorted([str(item) for item in x])) if isinstance(x, (frozenset, set, list, tuple)) else str(x))
    export_rules.to_csv(args.output_rules, index=False, encoding='utf-8-sig')
    print(f"关联规则已成功保存至 {args.output_rules}")
    print()
    
    if not args.no_plots:
        print("正在生成可视化图表...")
        generate_plots(df_cat, rules, args.output_plot_dir)
        
    print("所有实验步骤均已成功运行完毕。")


if __name__ == "__main__":
    main()
