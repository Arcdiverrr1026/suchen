import tkinter as tk
import random

poems = [
    ["春晓", "唐·孟浩然", ["春眠不觉晓", "处处闻啼鸟", "夜来风雨声", "花落知多少"]],
    ["静夜思", "唐·李白", ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"]],
    ["望洞庭", "唐·刘禹锡", ["湖光秋月两相和", "潭面无风镜未磨", "遥望洞庭山水翠", "白银盘里一青螺"]],
    ["登鹳雀楼", "唐·王之涣", ["白日依山尽", "黄河入海流", "欲穷千里目", "更上一层楼"]],
    ["悯农", "唐·李绅", ["锄禾日当午", "汗滴禾下土", "谁知盘中餐", "粒粒皆辛苦"]]
]

right_count = 0
wrong_count = 0
current_answer = ""
answered = False


def next_question():
    global current_answer, answered

    answered = False
    entry.delete(0, tk.END)

    poem = random.choice(poems)
    title = poem[0]
    author = poem[1]
    lines = poem[2]

    index = random.randint(0, len(lines) - 1)
    current_answer = lines[index]

    show_lines = lines[:]
    show_lines[index] = "____________"

    poem_text = title + "\n" + author + "\n\n" + "\n".join(show_lines)

    poem_label.config(text=poem_text, fg="blue")
    result_label.config(text="---- 请补充空缺的诗句： ----", fg="red")


def submit_answer(event=None):
    global right_count, wrong_count, answered

    if current_answer == "":
        result_label.config(text="请先点击“下一题”开始答题！", fg="red")
        return

    if answered:
        result_label.config(text="本题已经提交过，请点击“下一题”。", fg="red")
        return

    user_answer = entry.get().strip().replace(" ", "")

    if user_answer == current_answer:
        right_count += 1
        result_label.config(text="恭喜你，答对了！", fg="green")
    else:
        wrong_count += 1
        result_label.config(text="回答错误！正确答案是：" + current_answer, fg="red")

    answered = True


def end_game():
    global current_answer, answered

    current_answer = ""
    answered = False
    entry.delete(0, tk.END)

    poem_label.config(
        text="本次答题结束\n\n您一共答对{}题，答错{}题！".format(right_count, wrong_count),
        fg="blue"
    )

    result_label.config(text="继续练习请点击“下一题”。", fg="red")


root = tk.Tk()
root.title("中华古诗词练习")
root.geometry("620x600")
root.resizable(False, False)

poem_label = tk.Label(
    root,
    text="点击“下一题”开始练习",
    font=("楷体", 24, "bold"),
    fg="blue",
    justify="center"
)
poem_label.pack(pady=40)

result_label = tk.Label(
    root,
    text="---- 请补充空缺的诗句： ----",
    font=("宋体", 16, "bold"),
    fg="red"
)
result_label.pack(pady=15)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

submit_btn = tk.Button(
    button_frame,
    text="提交",
    width=10,
    height=2,
    command=submit_answer
)
submit_btn.grid(row=0, column=0, padx=10)

next_btn = tk.Button(
    button_frame,
    text="下一题",
    width=10,
    height=2,
    command=next_question
)
next_btn.grid(row=0, column=1, padx=10)

end_btn = tk.Button(
    button_frame,
    text="结束答题",
    width=10,
    height=2,
    command=end_game
)
end_btn.grid(row=0, column=2, padx=10)

entry = tk.Entry(
    root,
    width=35,
    font=("宋体", 22)
)
entry.pack(pady=20)
entry.bind("<Return>", submit_answer)

root.mainloop()