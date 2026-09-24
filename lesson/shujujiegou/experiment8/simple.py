import math

# Problem 1: e-based sequence
print("问题1：e的幂次序列")
for i in range(1, 11):
    print(f"  e^{i} = {math.e**i:.6f}")
print()

# Problem 2: factorial approximation
total = 0.0
fact = 1
for i in range(1, 21):
    fact *= i
    total += 1.0 / fact
print(f"问题2：1/1! + 1/2! + ... + 1/20! = {total:.10f}")
print()

# Problem 3: nested sequence
pos = int(input("问题3：请输入要查找的位置："))
remaining = pos
k = 1
while remaining > k:
    remaining -= k
    k += 1
print(f"  第{pos}项 = {remaining}")
print()

# Problem 4: rainfall analysis
data = [5, 3, 0, 0, 8, 12, 0, 0, 0, 7, 2, 0, 15, 20, 10, 0, 0, 0, 0, 3, 1, 0, 6, 9, 0, 0, 11, 0, 0, 4]
max_rain = max_dry = cur_rain = cur_dry = 0
for v in data:
    if v > 0:
        cur_rain += 1
        max_rain = max(max_rain, cur_rain)
        cur_dry = 0
    else:
        cur_dry += 1
        max_dry = max(max_dry, cur_dry)
        cur_rain = 0
print(f"问题4：最长连续有雨: {max_rain}天, 最长连续无雨: {max_dry}天")
