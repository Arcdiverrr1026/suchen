"""Evaluate an infix expression ending with '#'.

Supported operators: +, -, *, / and parentheses. Operands are real numbers.
The evaluator uses two stacks, one for operands and one for operators.
"""

from collections.abc import Iterable


PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def _tokens(expression: str) -> Iterable[str]:
    index = 0
    previous = "operator"

    while index < len(expression):
        char = expression[index]
        if char.isspace():
            index += 1
            continue
        if char == "#":
            return

        unary = (
            char in "+-"
            and previous in {"operator", "left_paren"}
            and index + 1 < len(expression)
            and (expression[index + 1].isdigit() or expression[index + 1] == ".")
        )
        if char.isdigit() or char == "." or unary:
            start = index
            if unary:
                index += 1
            dot_count = 0
            while index < len(expression) and (
                expression[index].isdigit() or expression[index] == "."
            ):
                if expression[index] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("invalid number")
                index += 1
            token = expression[start:index]
            float(token)
            previous = "number"
            yield token
            continue

        if char in PRECEDENCE:
            previous = "operator"
            index += 1
            yield char
            continue
        if char == "(":
            previous = "left_paren"
            index += 1
            yield char
            continue
        if char == ")":
            previous = "number"
            index += 1
            yield char
            continue

        raise ValueError(f"unsupported character: {char}")


def _calculate(left: float, right: float, operator: str) -> float:
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero")
        return left / right
    raise ValueError(f"unsupported operator: {operator}")


def _apply_top_operator(numbers: list[float], operators: list[str]) -> None:
    if len(numbers) < 2:
        raise ValueError("missing operand")
    operator = operators.pop()
    right = numbers.pop()
    left = numbers.pop()
    numbers.append(_calculate(left, right, operator))


def evaluate_infix(expression: str) -> float:
    """Evaluate an infix expression that may end with '#'."""
    numbers: list[float] = []
    operators: list[str] = []

    for token in _tokens(expression):
        if token in PRECEDENCE:
            while (
                operators
                and operators[-1] in PRECEDENCE
                and PRECEDENCE[operators[-1]] >= PRECEDENCE[token]
            ):
                _apply_top_operator(numbers, operators)
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                _apply_top_operator(numbers, operators)
            if not operators:
                raise ValueError("unmatched right parenthesis")
            operators.pop()
        else:
            numbers.append(float(token))

    while operators:
        if operators[-1] == "(":
            raise ValueError("unmatched left parenthesis")
        _apply_top_operator(numbers, operators)

    if len(numbers) != 1:
        raise ValueError("invalid expression")
    return numbers[0]


def format_result(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.12g}"


def main() -> None:
    expression = input().strip()
    print(format_result(evaluate_infix(expression)))


if __name__ == "__main__":
    main()
