from collections import deque

# Problem 1: English palindrome
s = input("请输入一个字符串：")
stack = []
queue = deque()
for ch in s:
    if ch.isalpha():
        stack.append(ch.lower())
        queue.append(ch.lower())

is_pal = True
while stack:
    if stack.pop() != queue.popleft():
        is_pal = False
        break

print(f"\"{s}\" {'是' if is_pal else '不是'}回文")

# Problem 2: Card game
a = deque(map(int, input("请输入A的牌（空格分隔）：").split()))
b = deque(map(int, input("请输入B的牌（空格分隔）：").split()))
table = []
turn = 0

for _ in range(10000):
    if turn == 0:
        if not a:
            print("赢家是: B")
            break
        card = a.popleft()
    else:
        if not b:
            print("赢家是: A")
            break
        card = b.popleft()

    match_idx = -1
    for i in range(len(table) - 1, -1, -1):
        if table[i] == card:
            match_idx = i
            break

    if match_idx >= 0:
        taken = table[match_idx:] + [card]
        table = table[:match_idx]
        if turn == 0:
            a.extend(taken)
        else:
            b.extend(taken)
    else:
        table.append(card)

    turn = 1 - turn
