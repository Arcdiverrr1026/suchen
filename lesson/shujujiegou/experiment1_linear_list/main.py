"""Long integer addition.

Run:
    python -m lesson.shujujiegou.experiment1_linear_list.main

Input two integers, one per line. The implementation stores digits in lists and
does not convert the whole value to Python's int.
"""


def _split_sign(number: str) -> tuple[int, str]:
    number = number.strip()
    if not number:
        raise ValueError("empty integer")

    sign = 1
    if number[0] in "+-":
        sign = -1 if number[0] == "-" else 1
        number = number[1:]

    if not number or not number.isdigit():
        raise ValueError("integer can contain only digits and one leading sign")

    number = number.lstrip("0") or "0"
    if number == "0":
        sign = 1
    return sign, number


def _compare_abs(left: str, right: str) -> int:
    if len(left) != len(right):
        return 1 if len(left) > len(right) else -1
    if left == right:
        return 0
    return 1 if left > right else -1


def _add_abs(left: str, right: str) -> str:
    left_digits = [ord(ch) - ord("0") for ch in reversed(left)]
    right_digits = [ord(ch) - ord("0") for ch in reversed(right)]
    result: list[str] = []
    carry = 0

    for index in range(max(len(left_digits), len(right_digits))):
        total = carry
        if index < len(left_digits):
            total += left_digits[index]
        if index < len(right_digits):
            total += right_digits[index]
        result.append(str(total % 10))
        carry = total // 10

    if carry:
        result.append(str(carry))
    return "".join(reversed(result))


def _subtract_abs(larger: str, smaller: str) -> str:
    larger_digits = [ord(ch) - ord("0") for ch in reversed(larger)]
    smaller_digits = [ord(ch) - ord("0") for ch in reversed(smaller)]
    result: list[str] = []
    borrow = 0

    for index, digit in enumerate(larger_digits):
        value = digit - borrow
        if index < len(smaller_digits):
            value -= smaller_digits[index]
        if value < 0:
            value += 10
            borrow = 1
        else:
            borrow = 0
        result.append(str(value))

    return ("".join(reversed(result)).lstrip("0")) or "0"


def add_long_integers(left: str, right: str) -> str:
    """Return left + right using digit lists instead of big integer arithmetic."""
    left_sign, left_abs = _split_sign(left)
    right_sign, right_abs = _split_sign(right)

    if left_sign == right_sign:
        total = _add_abs(left_abs, right_abs)
        return total if left_sign > 0 or total == "0" else f"-{total}"

    comparison = _compare_abs(left_abs, right_abs)
    if comparison == 0:
        return "0"
    if comparison > 0:
        difference = _subtract_abs(left_abs, right_abs)
        return difference if left_sign > 0 else f"-{difference}"

    difference = _subtract_abs(right_abs, left_abs)
    return difference if right_sign > 0 else f"-{difference}"


def main() -> None:
    left = input().strip()
    right = input().strip()
    print(add_long_integers(left, right))


if __name__ == "__main__":
    main()
