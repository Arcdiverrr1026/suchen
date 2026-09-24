class Node:
    def __init__(self, data=0, next=None):
        self.data = data
        self.next = next

head = Node()  # head sentinel
length = 0

def display():
    elems = []
    node = head.next
    while node:
        elems.append(str(node.data))
        node = node.next
    print("(" + ",".join(elems) + ")")

while True:
    choice = input("是否要对线性表进行插入和删除？（Y/N）").strip().upper()
    if choice != "Y":
        break

    op = input("进行插入还是删除？（1--插入，2--删除）").strip()
    if op == "1":
        parts = input("请输入插入位置和元素（空格分隔）：").split()
        pos, elem = int(parts[0]), int(parts[1])
        if pos < 1 or pos > length + 1:
            print("插入位置有误")
        else:
            prev = head
            for _ in range(pos - 1):
                prev = prev.next
            new_node = Node(elem, prev.next)
            prev.next = new_node
            length += 1
            display()
    elif op == "2":
        pos = int(input("请输入删除位置："))
        if pos < 1 or pos > length:
            print("删除位置有误")
        else:
            prev = head
            for _ in range(pos - 1):
                prev = prev.next
            prev.next = prev.next.next
            length -= 1
            display()
