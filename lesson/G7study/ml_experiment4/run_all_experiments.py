"""
运行所有实验
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_all_experiments():
    """运行所有四个实验"""
    print("=" * 80)
    print("机器学习实验4：决策树与集成学习模型构建与评估")
    print("=" * 80)

    # 导入并运行任务1
    print("\n" + "=" * 80)
    print("开始运行任务1：分类决策树（基于鸢尾花数据集）")
    print("=" * 80)
    try:
        from task1_classification_tree.experiment import run_experiment as run_task1
        run_task1()
    except Exception as e:
        print(f"任务1运行出错: {e}")

    # 导入并运行任务2
    print("\n" + "=" * 80)
    print("开始运行任务2：回归决策树（基于房价数据集）")
    print("=" * 80)
    try:
        from task2_regression_tree.experiment import run_experiment as run_task2
        run_task2()
    except Exception as e:
        print(f"任务2运行出错: {e}")

    # 导入并运行任务3
    print("\n" + "=" * 80)
    print("开始运行任务3：随机森林分类（基于乳腺癌数据集）")
    print("=" * 80)
    try:
        from task3_random_forest.experiment import run_experiment as run_task3
        run_task3()
    except Exception as e:
        print(f"任务3运行出错: {e}")

    # 导入并运行任务4
    print("\n" + "=" * 80)
    print("开始运行任务4：AdaBoost分类（基于乳腺癌数据集）")
    print("=" * 80)
    try:
        from task4_adaboost.experiment import run_experiment as run_task4
        run_task4()
    except Exception as e:
        print(f"任务4运行出错: {e}")

    print("\n" + "=" * 80)
    print("所有实验运行完成！")
    print("=" * 80)
    print("\n请查看各任务目录中的图表和分析报告。")

if __name__ == "__main__":
    run_all_experiments()
