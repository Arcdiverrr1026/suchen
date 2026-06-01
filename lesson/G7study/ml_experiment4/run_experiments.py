#!/usr/bin/env python3
"""
机器学习实验4：决策树与集成学习模型构建与评估
运行所有实验的主程序
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """主函数：运行所有实验"""
    print("=" * 80)
    print("机器学习实验4：决策树与集成学习模型构建与评估")
    print("=" * 80)

    print("\n请选择要运行的实验：")
    print("1. 任务1：分类决策树（鸢尾花数据集）")
    print("2. 任务2：回归决策树（加州房价数据集）")
    print("3. 任务3：随机森林分类（乳腺癌数据集）")
    print("4. 任务4：AdaBoost分类（乳腺癌数据集）")
    print("5. 运行所有实验")
    print("0. 退出")

    while True:
        try:
            choice = input("\n请输入选项 (0-5): ").strip()

            if choice == '0':
                print("退出程序。")
                break
            elif choice == '1':
                run_task1()
            elif choice == '2':
                run_task2()
            elif choice == '3':
                run_task3()
            elif choice == '4':
                run_task4()
            elif choice == '5':
                run_all_tasks()
            else:
                print("无效选项，请输入0-5之间的数字。")
        except KeyboardInterrupt:
            print("\n\n程序被用户中断。")
            break
        except Exception as e:
            print(f"发生错误: {e}")

def run_task1():
    """运行任务1：分类决策树"""
    print("\n" + "=" * 80)
    print("开始运行任务1：分类决策树（基于鸢尾花数据集）")
    print("=" * 80)
    try:
        from task1_classification_tree.experiment import run_experiment
        run_experiment()
    except Exception as e:
        print(f"任务1运行出错: {e}")

def run_task2():
    """运行任务2：回归决策树"""
    print("\n" + "=" * 80)
    print("开始运行任务2：回归决策树（基于房价数据集）")
    print("=" * 80)
    try:
        from task2_regression_tree.experiment import run_experiment
        run_experiment()
    except Exception as e:
        print(f"任务2运行出错: {e}")

def run_task3():
    """运行任务3：随机森林分类"""
    print("\n" + "=" * 80)
    print("开始运行任务3：随机森林分类（基于乳腺癌数据集）")
    print("=" * 80)
    try:
        from task3_random_forest.experiment import run_experiment
        run_experiment()
    except Exception as e:
        print(f"任务3运行出错: {e}")

def run_task4():
    """运行任务4：AdaBoost分类"""
    print("\n" + "=" * 80)
    print("开始运行任务4：AdaBoost分类（基于乳腺癌数据集）")
    print("=" * 80)
    try:
        from task4_adaboost.experiment import run_experiment
        run_experiment()
    except Exception as e:
        print(f"任务4运行出错: {e}")

def run_all_tasks():
    """运行所有任务"""
    print("\n" + "=" * 80)
    print("开始运行所有实验")
    print("=" * 80)

    run_task1()
    run_task2()
    run_task3()
    run_task4()

    print("\n" + "=" * 80)
    print("所有实验运行完成！")
    print("=" * 80)
    print("\n请查看各任务目录中的图表和分析报告。")
    print("\n生成的文件：")
    print("  - task1_classification_tree/: 任务1的实验结果")
    print("  - task2_regression_tree/: 任务2的实验结果")
    print("  - task3_random_forest/: 任务3的实验结果")
    print("  - task4_adaboost/: 任务4的实验结果")

if __name__ == "__main__":
    main()
