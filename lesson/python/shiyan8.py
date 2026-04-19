n, k = map(int, input().split())
a = []
b = []
for i in range(1,n+1):
    if i % k != 0:
        a.append(i)
    else:
        b.append(i)
ans_a = sum(a) / len(a)
ans_b = sum(b) / len(b)
print(f"{ans_b:.1f} {ans_a:.1f}")
