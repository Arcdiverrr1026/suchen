"""Simple version: long integer addition for non-negative integers."""


def add(a: str, b: str) -> str:
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    answer = []

    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1

        answer.append(str(total % 10))
        carry = total // 10

    return "".join(reversed(answer))

a = input().strip()
b = input().strip()
print(add(a, b))
