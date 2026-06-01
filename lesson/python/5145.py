import tkinter as tk
import random

# 随机生成 1024 以内的数字
number = random.randint(1, 1024)
count = 0

def guess():
    global count
    count += 1

    try:
        n = int(entry.get())
    except:
        label.config(text="请输入整数！")
        return

    if n > number:
        label.config(text="大了！请输入更小的数字。")
    elif n < number:
        label.config(text="小了！请输入更大的数字。")
    else:
        label.config(text="猜对了！尝试次数：" + str(count))

def close():
    root.destroy()

# 创建窗口
root = tk.Tk()
root.title("猜数字游戏")
root.geometry("500x150")

# 提示标签
label = tk.Label(root, text="请输入1到1024之间的任意整数：", font=("宋体", 12))
label.pack(pady=20)

# 输入框和按钮区域
frame = tk.Frame(root)
frame.pack()

entry = tk.Entry(frame, width=30)
entry.pack(side=tk.LEFT)

btn_guess = tk.Button(frame, text="猜", command=guess)
btn_guess.pack(side=tk.LEFT, padx=5)

btn_close = tk.Button(frame, text="关闭", command=close)
btn_close.pack(side=tk.LEFT)

root.mainloop()