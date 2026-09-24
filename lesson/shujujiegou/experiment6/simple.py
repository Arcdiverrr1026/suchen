lst = []

while True:
    choice = input("是否要对线性表进行插入和删除？（Y/N）").strip().upper()
    if choice != "Y":
        break

    op = input("进行插入还是删除？（1--插入，2--删除）").strip()
    if op == "1":
        parts = input("请输入插入位置和元素（空格分隔）：").split()
        pos, elem = int(parts[0]), int(parts[1])
        if pos < 1 or pos > len(lst) + 1:
            print("插入位置有误")
        else:
            lst.insert(pos - 1, elem)
            print("(" + ",".join(str(x) for x in lst) + ")")
    elif op == "2":
        pos = int(input("请输入删除位置："))
        if pos < 1 or pos > len(lst):
            print("删除位置有误")
        else:
            lst.pop(pos - 1)
            print("(" + ",".join(str(x) for x in lst) + ")")
