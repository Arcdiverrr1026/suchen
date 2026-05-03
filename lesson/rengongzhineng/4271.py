import heapq
import math
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import rcParams

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'STHeiti']
plt.rcParams['axes.unicode_minus'] = False


class GraphVisualizer:
    def __init__(self):
        self.graph = None
        self.pos = None
        self.node_colors = []

    def create_graph(self):
        """创建图结构并设置节点位置"""
        # 定义图结构（邻接表表示）
        self.graph = {
            'A': [('B', 1), ('C', 4),('E',25)],#新增直达E的线路
            'B': [('A', 1), ('C', 2), ('D', 100)],
            'C': [('A', 4), ('B', 2), ('D', 100)],#原代价为1，现改为100
            'D': [('B', 100), ('C', 100), ('E', 3)],#同步上一步的修改
            'E': [('A',25),('D', 3)]#新增线路
        }
        # 为节点设置固定位置，便于可视化
        self.pos = {
            'A': (0, 2),
            'B': (2, 3),
            'C': (2, 1),
            'D': (4, 2),
            'E': (6, 2)
        }
        return self.graph

    def get_heuristic_values(self, goal):
        """计算并返回启发函数值（使用曼哈顿距离）"""
        heuristic = {}
        for node in self.graph:
            # 使用曼哈顿距离作为启发函数
            #dx = abs(self.pos[node][0] - self.pos[goal][0])
            #dy = abs(self.pos[node][1] - self.pos[goal][1])
            #取消使用哈曼顿函数，将所有节点启发值设为0
            heuristic[node] = 0
        # 确保目标节点的启发值为0
        #heuristic[goal] = 0
        return heuristic

    def visualize_graph(self, title="图结构可视化", highlight_nodes=None, highlight_edges=None):
        """可视化图结构"""
        if highlight_nodes is None:
            highlight_nodes = []
        if highlight_edges is None:
            highlight_edges = []

        # 创建networkx图对象
        G = nx.Graph()
        # 添加节点和边
        for node, neighbors in self.graph.items():
            G.add_node(node)
            for neighbor, cost in neighbors:
                G.add_edge(node, neighbor, weight=cost)

        plt.figure(figsize=(12, 8))
        # 绘制节点
        node_colors = ['lightblue' if node not in highlight_nodes else 'red' for node in G.nodes()]
        node_sizes = [800 if node not in highlight_nodes else 1200 for node in G.nodes()]
        nx.draw_networkx_nodes(G, self.pos,
                               node_color=node_colors,
                               node_size=node_sizes,
                               alpha=0.9)
        # 绘制所有边（灰色）
        nx.draw_networkx_edges(G, self.pos,
                               alpha=0.6,
                               width=1,
                               edge_color='gray')
        # 高亮显示特定边（红色）
        if highlight_edges:
            nx.draw_networkx_edges(G, self.pos,
                                   edgelist=highlight_edges,
                                   width=3,
                                   alpha=0.8,
                                   edge_color='red')
        # 添加节点标签
        nx.draw_networkx_labels(G, self.pos,
                                font_size=14,
                                font_weight='bold')
        # 添加边权重标签
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, self.pos,
                                     edge_labels=edge_labels,
                                     font_size=10)

        plt.title(title, fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def visualize_heuristic(self, heuristic, goal):
        """可视化启发函数值"""
        plt.figure(figsize=(10, 6))
        G = nx.Graph()
        for node, neighbors in self.graph.items():
            G.add_node(node)
            for neighbor, cost in neighbors:
                G.add_edge(node, neighbor, weight=cost)

        nx.draw_networkx_nodes(G, self.pos,
                               node_color='lightgreen',
                               node_size=1000,
                               alpha=0.8)
        nx.draw_networkx_edges(G, self.pos,
                               alpha=0.6,
                               width=2)
        nx.draw_networkx_labels(G, self.pos,
                                font_size=14,
                                font_weight='bold')

        # 添加启发值标签
        heuristic_labels = {node: f"h({node})={heuristic[node]}" for node in G.nodes()}
        label_pos = {k: (v[0], v[1] - 0.3) for k, v in self.pos.items()}
        nx.draw_networkx_labels(G, label_pos,
                                labels=heuristic_labels,
                                font_size=10,
                                font_color='darkred')

        # 添加边权重
        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, self.pos,
                                     edge_labels=edge_labels,
                                     font_size=10)

        plt.title(f"启发函数可视化 (目标节点: {goal})", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


# 初始化及基础数据展示
visualizer = GraphVisualizer()
graph = visualizer.create_graph()
start_node = 'A'
goal_node = 'E'
heuristic = visualizer.get_heuristic_values(goal_node)

print("=== 图结构信息 ===")
print("图结构:", graph)
print("\n=== 启发函数信息 ===")
print("启发函数值:", heuristic)
visualizer.visualize_graph("A*算法 - 图结构展示")
visualizer.visualize_heuristic(heuristic, goal_node)


def visualize_search_process(graph, search_steps, visualizer, final_path=None):
    """可视化搜索过程"""
    if not search_steps:
        return
    # 只显示关键步骤（起始、中间、最后一步）
    key_steps = [search_steps[0]]
    if len(search_steps) > 1:
        key_steps.append(search_steps[len(search_steps) // 2])
    key_steps.append(search_steps[-1])

    for step_info in key_steps:
        step = step_info['step']
        current = step_info['current']
        open_list = step_info['open_list']
        closed_list = step_info['closed_list']

        plt.figure(figsize=(10, 6))
        G = nx.Graph()
        for node, neighbors in graph.items():
            G.add_node(node)
            for neighbor, cost in neighbors:
                G.add_edge(node, neighbor, weight=cost)

        # 确定节点颜色
        node_colors = []
        for node in G.nodes():
            if node == current:
                node_colors.append('red')  # 当前节点
            elif node in closed_list:
                node_colors.append('lightgray')  # 已关闭节点
            elif node in open_list:
                node_colors.append('yellow')  # 开放列表中节点
            else:
                node_colors.append('lightblue')  # 未访问节点

        nx.draw_networkx_nodes(G, visualizer.pos,
                               node_color=node_colors,
                               node_size=800,
                               alpha=0.9)
        nx.draw_networkx_edges(G, visualizer.pos,
                               alpha=0.6,
                               width=2)
        nx.draw_networkx_labels(G, visualizer.pos,
                                font_size=14,
                                font_weight='bold')

        edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, visualizer.pos,
                                     edge_labels=edge_labels,
                                     font_size=10)

        plt.title(f"A*搜索过程 - 步骤 {step}\n当前节点: {current}",
                  fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


# 过程分析打印
print("\n=== 搜索过程分析 ===")
print(f"起始节点: {start_node}")
print(f"目标节点: {goal_node}")
print(f"启发函数: {heuristic}")

