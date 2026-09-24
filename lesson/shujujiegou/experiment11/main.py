"""Expression evaluation using stacks.

Problem 1: Postfix expression evaluation.
Problem 2: Infix expression evaluation (online conversion + evaluation).
"""

_OPERATORS = set("+-*/")
_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def eval_postfix(expr: str) -> float:
    """Evaluate a postfix expression. Operands are single digits 0-9."""
    stack: list[float] = []
    for ch in expr:
        if ch.isdigit():
            stack.append(float(ch))
        elif ch in _OPERATORS:
            b = stack.pop()
            a = stack.pop()
            if ch == "+":
                stack.append(a + b)
            elif ch == "-":
                stack.append(a - b)
            elif ch == "*":
                stack.append(a * b)
            elif ch == "/":
                stack.append(a / b)
    return stack[0]


def _apply_op(op: str, b: float, a: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return a / b


def eval_infix(expr: str) -> float:
    """Evaluate an infix expression using online conversion (no full postfix generation).

    Uses Dijkstra's two-stack algorithm with operator stack and value stack.
    Operands are single digits 0-9, parentheses allowed.
    """
    values: list[float] = []
    ops: list[str] = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch == " ":
            i += 1
            continue
        if ch.isdigit():
            values.append(float(ch))
        elif ch == "(":
            ops.append(ch)
        elif ch == ")":
            while ops and ops[-1] != "(":
                op = ops.pop()
                b = values.pop()
                a = values.pop()
                values.append(_apply_op(op, b, a))
            ops.pop()  # remove "("
        elif ch in _OPERATORS:
            while (ops and ops[-1] != "(" and
                   _PRECEDENCE.get(ops[-1], 0) >= _PRECEDENCE.get(ch, 0)):
                op = ops.pop()
                b = values.pop()
                a = values.pop()
                values.append(_apply_op(op, b, a))
            ops.append(ch)
        i += 1

    while ops:
        op = ops.pop()
        b = values.pop()
        a = values.pop()
        values.append(_apply_op(op, b, a))

    return values[0]


def main() -> None:
    # Problem 1
    print("问题1：后缀表达式求值")
    postfix = input("请输入后缀表达式（如 34+5*）：").strip()
    print(f"结果 = {eval_postfix(postfix):g}")
    print()

    # Problem 2
    print("问题2：中缀表达式求值")
    infix = input("请输入中缀表达式（如 3+4*5）：").strip()
    print(f"结果 = {eval_infix(infix):g}")


if __name__ == "__main__":
    main()
