"""Simple version: evaluate an infix expression with two stacks."""


def apply_operator(numbers: list[float], operators: list[str]) -> None:
    b = numbers.pop()
    a = numbers.pop()
    op = operators.pop()

    if op == "+":
        numbers.append(a + b)
    elif op == "-":
        numbers.append(a - b)
    elif op == "*":
        numbers.append(a * b)
    elif op == "/":
        numbers.append(a / b)


priority = {"+": 1, "-": 1, "*": 2, "/": 2}
expression = input().strip()
numbers: list[float] = []
operators: list[str] = []
i = 0

while i < len(expression) and expression[i] != "#":
    ch = expression[i]

    if ch == " ":
        i += 1
    elif ch.isdigit() or ch == ".":
        j = i
        while j < len(expression) and (expression[j].isdigit() or expression[j] == "."):
            j += 1
        numbers.append(float(expression[i:j]))
        i = j
    elif ch == "(":
        operators.append(ch)
        i += 1
    elif ch == ")":
        while operators[-1] != "(":
            apply_operator(numbers, operators)
        operators.pop()
        i += 1
    else:
        while (
            operators
            and operators[-1] != "("
            and priority[operators[-1]] >= priority[ch]
        ):
            apply_operator(numbers, operators)
        operators.append(ch)
        i += 1

while operators:
    apply_operator(numbers, operators)

answer = numbers[0]
if answer == int(answer):
    print(int(answer))
else:
    print(answer)
