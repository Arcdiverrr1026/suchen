class TermNode:
    def __init__(self, coef=0.0, expn=0, next=None):
        self.coef = coef
        self.expn = expn
        self.next = next

head = TermNode()

n = int(input("请输入多项式项数："))
for i in range(n):
    parts = input(f"请输入第{i+1}项的系数和指数（空格分隔）：").split()
    coef, expn = float(parts[0]), int(parts[1])
    if coef == 0:
        continue
    prev = head
    curr = prev.next
    while curr and curr.expn < expn:
        prev = curr
        curr = curr.next
    if curr and curr.expn == expn:
        curr.coef += coef
        if curr.coef == 0:
            prev.next = curr.next
    else:
        prev.next = TermNode(coef, expn, curr)

# Compute derivative
deriv_head = TermNode()
node = head.next
while node:
    if node.expn > 0:
        prev = deriv_head
        curr = prev.next
        new_expn = node.expn - 1
        new_coef = node.coef * node.expn
        while curr and curr.expn < new_expn:
            prev = curr
            curr = curr.next
        prev.next = TermNode(new_coef, new_expn, curr)
    node = node.next

# Display
terms = []
node = deriv_head.next
if not node:
    print("P'(x) = 0")
else:
    while node:
        if node.expn == 0:
            terms.append(f"{node.coef:g}")
        elif node.expn == 1:
            terms.append(f"{node.coef:g}x")
        else:
            terms.append(f"{node.coef:g}x^{node.expn}")
        node = node.next
    result = " + ".join(terms).replace(" + -", " - ")
    print(f"P'(x) = {result}")
