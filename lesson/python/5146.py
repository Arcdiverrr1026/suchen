import tkinter as tk
import random

# 姓名列表
names = ["张三", "李四", "王五", "赵六", "马艺萌", "刘明", "陈晨", "周杰"]

count = 0
max_count = 30

def animate():
    global count

    # 动画过程中不断随机显示姓名
    name = random.choice(names)
    label.config(text=name)

    count += 1

    if count < max_count:
        # 每隔 80 毫秒换一次名字
        root.after(80, animate)
    else:
        # 最终确定一个姓名
        final_name = random.choice(names)
        label.config(text=final_name)
        button.config(state="normal")

def choose_name():
    global count
    count = 0
    button.config(state="disabled")
    animate()

# 创建窗口
root = tk.Tk()
root.title("点名程序")
root.geometry("500x300")

# 显示姓名的标签
label = tk.Label(
    root,
    text="点击开始点名",
    font=("宋体", 28, "bold"),
    fg="blue"
)
label.pack(pady=80)

# 点名按钮
button = tk.Button(
    root,
    text="点名",
    width=12,
    height=2,
    command=choose_name
)
button.pack()

root.mainloop()