# Problem 1: postfix
def eval_postfix(expr):
    stack = []
    for ch in expr:
        if ch.isdigit():
            stack.append(float(ch))
        elif ch in "+-*/":
            b, a = stack.pop(), stack.pop()
            if ch == "+": stack.append(a + b)
            elif ch == "-": stack.append(a - b)
            elif ch == "*": stack.append(a * b)
            elif ch == "/": stack.append(a / b)
    return stack[0]

print("问题1：后缀表达式求值")
postfix = input("请输入后缀表达式：").strip()
print(f"结果 = {eval_postfix(postfix):g}")

# Problem 2: infix (online evaluation)
def eval_infix(expr):
    values = []
    ops = []
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}

    def apply():
        op = ops.pop()
        b, a = values.pop(), values.pop()
        if op == "+": values.append(a + b)
        elif op == "-": values.append(a - b)
        elif op == "*": values.append(a * b)
        elif op == "/": values.append(a / b)

    for ch in expr:
        if ch == " ":
            continue
        if ch.isdigit():
            values.append(float(ch))
        elif ch == "(":
            ops.append(ch)
        elif ch == ")":
            while ops[-1] != "(":
                apply()
            ops.pop()
        elif ch in "+-*/":
            while ops and ops[-1] != "(" and prec.get(ops[-1], 0) >= prec.get(ch, 0):
                apply()
            ops.append(ch)

    while ops:
        apply()
    return values[0]

print("\n问题2：中缀表达式求值")
infix = input("请输入中缀表达式：").strip()
print(f"结果 = {eval_infix(infix):g}")
