"""Generate experiment report .docx files for experiments 6-15."""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXPERIMENTS = {
    6: {
        "title": "顺序存储线性表",
        "problem": (
            "实现一个顺序存储的线性表，能够进行插入和删除操作。\n"
            "程序交互式运行：提示用户是否要对线性表进行插入和删除（Y/N），"
            "如果选择Y，则进一步选择插入（1）还是删除（2）。\n"
            "对于插入操作，输入插入位置和元素；对于删除操作，输入删除位置。\n"
            "每次操作成功后输出线性表内容，格式为 (a,b,c)；操作失败则输出错误提示。\n\n"
            "执行示例：\n"
            "插入8到位置1 -> (8)\n"
            "插入2到位置1 -> (2,8)\n"
            "插入5到位置4 -> 插入位置有误\n"
            "插入5到位置3 -> (2,8,5)\n"
            "删除位置3 -> (2,8)\n"
            "删除位置7 -> 删除位置有误\n"
            "删除位置1 -> (8)"
        ),
        "code_file": "experiment6/main.py",
        "summary": (
            "通过本次实验，我掌握了顺序存储线性表的基本操作实现方法。"
            "使用Python列表作为底层存储结构，实现了线性表的插入和删除操作，"
            "理解了顺序存储结构中元素位置的管理以及边界条件的处理。"
            "通过交互式的测试过程，加深了对线性表操作时间复杂度的理解。"
        ),
    },
    7: {
        "title": "数学问题",
        "problem": (
            "本实验包含四个数学编程问题：\n\n"
            "问题1：数列求和。给定 a1=100, a2=99, an=|a(n-1)-a(n-2)| (n>=3)，"
            "求前100项的和。\n\n"
            "问题2：打印菱形图案，共11行。\n\n"
            "问题3：找出10000以内的所有孪生素数对（两个素数p和p+2都为素数）。\n\n"
            "问题4：找出一个1位数、一个2位数、一个3位数和一个4位数，"
            "它们都是完全平方数，且四个数恰好使用了数字0-9各一次。"
        ),
        "code_file": "experiment7/main.py",
        "summary": (
            "通过本次实验，我练习了多种数学问题的编程求解方法。"
            "在数列求和问题中运用了迭代思想，在菱形图案中掌握了循环控制，"
            "在孪生素数问题中实现了素数判断算法，在完全平方数问题中使用了"
            "组合搜索和数字集合判重。这些练习提高了我的算法设计和编程能力。"
        ),
    },
    8: {
        "title": "数列与近似值问题",
        "problem": (
            "本实验包含四个问题：\n\n"
            "问题1：计算e的幂次序列前10项（e^1, e^2, ..., e^10）。\n\n"
            "问题2：计算阶乘倒数之和 1/1! + 1/2! + 1/3! + ... + 1/n!，"
            "该值趋近于 e-1。\n\n"
            "问题3：嵌套数列 1,1,2,1,2,3,1,2,3,4,...，给定位置求该位置的值。\n\n"
            "问题4：给定30天的降雨量数据（0表示无雨），"
            "求最长连续有雨天数和最长连续无雨天数。"
        ),
        "code_file": "experiment8/main.py",
        "summary": (
            "通过本次实验，我学习了数列计算和近似值求解的编程方法。"
            "在阶乘倒数求和中理解了级数收敛的概念，在嵌套数列中掌握了"
            "分组定位的算法思想，在降雨量分析中练习了滑动窗口式的连续统计。"
            "这些练习加深了我对数学建模和数组处理的理解。"
        ),
    },
    9: {
        "title": "链表实现线性表",
        "problem": (
            "使用带头节点的单链表实现线性表，维护一个length变量记录表长。\n"
            "程序交互式运行：提示用户是否要对线性表进行插入和删除（Y/N），"
            "如果选择Y，则进一步选择插入（1）还是删除（2）。\n"
            "对于插入操作，输入插入位置和元素；对于删除操作，输入删除位置。\n"
            "每次操作成功后输出线性表内容，格式为 (a,b,c)；操作失败则输出错误提示。\n\n"
            "与实验6的区别在于：本实验使用链式存储结构而非顺序存储，"
            "重点理解链表的节点链接操作和动态内存管理。"
        ),
        "code_file": "experiment9/main.py",
        "summary": (
            "通过本次实验，我掌握了使用单链表实现线性表的方法。"
            "通过定义节点类和链表类，实现了带头节点链表的插入和删除操作，"
            "理解了链式存储结构与顺序存储结构的区别。"
            "链表的插入删除不需要移动元素，只需修改指针，"
            "但需要从头遍历定位位置，加深了我对不同存储结构优缺点的认识。"
        ),
    },
    10: {
        "title": "多项式求导",
        "problem": (
            "实现一元多项式的求导运算。\n"
            "多项式 Pn(x) = c1*x^e1 + c2*x^e2 + ... + cm*x^em，"
            "其中 ci 为实系数，0 <= e1 < e2 < ... < em = n 为非负整数指数。\n"
            "输入多项式和输出结果均使用带头节点的单链表存储，"
            "每个节点包含三个域：coef（系数）、expn（指数）、next（指针）。\n"
            "需要处理结果为0的特殊情况。"
        ),
        "code_file": "experiment10/main.py",
        "summary": (
            "通过本次实验，我学习了使用链表存储多项式并实现求导运算的方法。"
            "每个链表节点包含系数和指数两个数据域，通过遍历链表对每一项"
            "应用求导公式 (c*x^e)' = c*e*x^(e-1)。"
            "实验中还处理了常数项求导为0的边界情况，"
            "加深了我对链表应用和数学建模的理解。"
        ),
    },
    11: {
        "title": "表达式求值",
        "problem": (
            "本实验包含两个表达式求值问题：\n\n"
            "问题1：后缀表达式求值。操作数为0-9的单个数字，"
            "运算符包括 +、-、*、/，表达式保证正确且无除零。\n\n"
            "问题2：中缀表达式求值。操作数和运算符同上，"
            "允许使用圆括号。关键要求：不能先将整个中缀表达式转换为后缀再求值，"
            "必须在转换的同时进行求值（在线求值）。"
        ),
        "code_file": "experiment11/main.py",
        "summary": (
            "通过本次实验，我掌握了栈在表达式求值中的应用。"
            "后缀表达式求值使用一个操作数栈，遇到运算符弹出两个操作数计算。"
            "中缀表达式求值使用Dijkstra的双栈算法（操作数栈和运算符栈），"
            "实现了在线转换和求值。这些练习加深了我对栈结构和表达式处理的理解。"
        ),
    },
    12: {
        "title": "数组问题",
        "problem": (
            "本实验包含两个数组相关问题：\n\n"
            "问题1：输入20个整数，找出最接近平均值和最远离平均值的整数。\n\n"
            "问题2：数字重排。输入一个非负整数，将其各位数字重新排列，"
            "找出比原数大的最小整数（下一个排列）和比原数小的最大整数（上一个排列）。"
            "如果不存在这样的排列，输出提示信息。"
        ),
        "code_file": "experiment12/main.py",
        "summary": (
            "通过本次实验，我练习了数组处理和排列算法。"
            "在求平均值问题中，通过一次遍历同时记录最近和最远元素；"
            "在数字重排问题中，实现了下一个排列和上一个排列的算法，"
            "理解了字典序排列的生成方法。这些练习提高了我的数组操作和算法设计能力。"
        ),
    },
    13: {
        "title": "栈和队列应用",
        "problem": (
            "本实验包含两个使用栈和队列的问题：\n\n"
            "问题1：英文回文判断。忽略非字母字符，不区分大小写，"
            "判断字符串是否为回文。必须使用栈和队列实现。\n"
            "示例：'Rise to vote, sir.' 是回文。\n\n"
            "问题2：纸牌游戏。A、B两人各持n张牌（队列），"
            "轮流将手中第一张牌打出到桌面（栈），"
            "如果打出的牌与桌面上某张牌相同，则将从该牌到打出牌之间的所有牌"
            "（含打出的牌）全部取回放到手牌末尾。"
            "当一方手牌为空时另一方获胜。必须使用栈和队列实现。"
        ),
        "code_file": "experiment13/main.py",
        "summary": (
            "通过本次实验，我学习了栈和队列在实际问题中的综合应用。"
            "回文判断利用栈的后进先出和队列的先进先出特性进行字符比较；"
            "纸牌游戏用队列管理手牌、栈管理桌面牌，模拟了游戏的完整过程。"
            "这两个练习让我深刻理解了栈和队列的特性和适用场景。"
        ),
    },
    14: {
        "title": "数组旋转",
        "problem": (
            "给定一个长度为n的一维整数数组，将前k个元素移到数组末尾，"
            "将后n-k个元素移到数组前面。\n"
            "关键约束：不能引入新的数组，必须在原数组上原地操作。\n\n"
            "示例：数组 [1,2,3,4,5]，k=2，旋转后为 [3,4,5,1,2]。\n\n"
            "解法：使用三次翻转法（reverse法），时间复杂度O(n)，空间复杂度O(1)。"
        ),
        "code_file": "experiment14/main.py",
        "summary": (
            "通过本次实验，我学习了数组原地旋转的算法。"
            "使用三次翻转法实现：先分别翻转前k个元素和后n-k个元素，"
            "再整体翻转，即可完成旋转。该算法时间复杂度为O(n)，"
            "空间复杂度为O(1)，不需要额外数组。"
            "这个练习让我理解了巧妙的算法设计如何在空间受限时解决问题。"
        ),
    },
    15: {
        "title": "二叉树的实现",
        "problem": (
            "使用二叉链表（每个节点有两个孩子指针）实现二叉树。\n"
            "通过扩展先序序列（空节点用'#'表示）构造二叉树。\n"
            "分别输出交换前后的先序、中序、后序和层序遍历序列。\n\n"
            "示例输入：ABD##E##CF###\n"
            "构造的二叉树结构：\n"
            "        A\n"
            "       / \\\n"
            "      B   C\n"
            "     / \\ /\n"
            "    D  E F\n\n"
            "交换所有左右子树后，输出新的四种遍历序列。"
        ),
        "code_file": "experiment15/main.py",
        "summary": (
            "通过本次实验，我掌握了二叉树的基本操作实现。"
            "通过扩展先序序列递归构建二叉树，实现了先序、中序、后序和层序"
            "四种遍历方式，并通过递归交换所有节点的左右子树。"
            "这些练习加深了我对二叉树递归结构和遍历算法的理解，"
            "也提高了运用队列实现层序遍历的能力。"
        ),
    },
}


def add_header_table(doc: Document) -> None:
    """Add the standard header table to the document."""
    table = doc.add_table(rows=4, cols=6, style="Table Grid")

    # Row 0: 院系, 年级专业
    table.cell(0, 0).text = "院、系"
    table.cell(0, 1).text = "计算科学与人工智能"
    table.cell(0, 2).text = "年级专业"
    table.cell(0, 3).text = "25计算机(Z)1"
    table.cell(0, 4).text = "姓名"
    table.cell(0, 5).text = "吴诗宇"

    # Row 1: 课程名称, 成绩
    table.cell(1, 0).text = "课程名称"
    table.cell(1, 1).text = "数据结构"
    table.cell(1, 2).text = "成绩"
    table.cell(1, 3).text = ""
    table.cell(1, 4).text = "指导教师"
    table.cell(1, 5).text = "唐自立"

    # Row 2: 学号
    table.cell(2, 0).text = "学号"
    table.cell(2, 1).text = "2506249007"
    table.cell(2, 2).text = "实验日期"
    table.cell(2, 3).text = ""
    table.cell(2, 4).text = "同组实验者"
    table.cell(2, 5).text = "无"

    # Row 3: placeholder (empty)
    for i in range(6):
        table.cell(3, i).text = ""

    # Merge cells for label+value pairs in row 3
    table.cell(3, 0).merge(table.cell(3, 5))

    # Set font size for all cells
    for row in table.rows:
        for cell in row.cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10.5)
                    run.font.name = "宋体"
                    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


def create_report(exp_num: int, exp_info: dict) -> None:
    """Create a single experiment report document."""
    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "宋体"
    font.size = Pt(12)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("苏州城市学院实验报告")
    run.bold = True
    run.font.size = Pt(16)
    run.font.name = "宋体"
    run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Header table
    add_header_table(doc)

    # Section 1: Experiment title
    doc.add_paragraph()
    heading1 = doc.add_paragraph()
    run1 = heading1.add_run(f"一. 实验题目：{exp_info['title']}")
    run1.bold = True
    run1.font.size = Pt(12)
    run1.font.name = "宋体"
    run1._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Section 2: Problem description
    heading2 = doc.add_paragraph()
    run2 = heading2.add_run("二. 问题描述")
    run2.bold = True
    run2.font.size = Pt(12)
    run2.font.name = "宋体"
    run2._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    for line in exp_info["problem"].split("\n"):
        p = doc.add_paragraph(line)
        for run in p.runs:
            run.font.size = Pt(10.5)
            run.font.name = "宋体"
            run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Section 3: Program and results
    heading3 = doc.add_paragraph()
    run3 = heading3.add_run("三. 程序和执行结果（执行结果用截图）")
    run3.bold = True
    run3.font.size = Pt(12)
    run3.font.name = "宋体"
    run3._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    prog_label = doc.add_paragraph()
    run_label = prog_label.add_run("程序：")
    run_label.bold = True
    run_label.font.size = Pt(10.5)
    run_label.font.name = "宋体"
    run_label._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Read and insert code
    code_path = os.path.join(BASE_DIR, exp_info["code_file"])
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()

    code_para = doc.add_paragraph()
    code_run = code_para.add_run(code)
    code_run.font.size = Pt(9)
    code_run.font.name = "Courier New"

    result_label = doc.add_paragraph()
    run_rlabel = result_label.add_run("执行结果：")
    run_rlabel.bold = True
    run_rlabel.font.size = Pt(10.5)
    run_rlabel.font.name = "宋体"
    run_rlabel._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Placeholder for screenshot
    result_hint = doc.add_paragraph("（此处粘贴运行截图）")
    for run in result_hint.runs:
        run.font.size = Pt(10.5)
        run.font.name = "宋体"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Section 4: Summary
    heading4 = doc.add_paragraph()
    run4 = heading4.add_run("四. 实验总结")
    run4.bold = True
    run4.font.size = Pt(12)
    run4.font.name = "宋体"
    run4._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    summary_para = doc.add_paragraph(exp_info["summary"])
    for run in summary_para.runs:
        run.font.size = Pt(10.5)
        run.font.name = "宋体"
        run._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Footer
    doc.add_paragraph()
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_f = footer.add_run("教务处制")
    run_f.font.size = Pt(10.5)
    run_f.font.name = "宋体"
    run_f._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")

    # Save
    filename = f"2506249007吴诗宇实验{exp_num}.docx"
    filepath = os.path.join(BASE_DIR, filename)
    doc.save(filepath)
    print(f"Created: {filename}")


def main() -> None:
    for exp_num, exp_info in EXPERIMENTS.items():
        create_report(exp_num, exp_info)
    print("All reports generated.")


if __name__ == "__main__":
    main()
