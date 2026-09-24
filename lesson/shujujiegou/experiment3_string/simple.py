"""Simple version: KMP pattern matching."""


def get_next(pattern: str) -> list[int]:
    next_array = [0] * len(pattern)
    j = 0

    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = next_array[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        next_array[i] = j

    return next_array


n = int(input().strip())
p = input().strip()
m = int(input().strip())
s = input().strip()

next_array = get_next(p)
j = 0
answer = []

for i in range(m):
    while j > 0 and s[i] != p[j]:
        j = next_array[j - 1]
    if s[i] == p[j]:
        j += 1
    if j == n:
        answer.append(i - n + 2)
        j = next_array[j - 1]

print(" ".join(map(str, answer)))
