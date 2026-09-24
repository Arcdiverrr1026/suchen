# Problem 1: nearest and farthest from average
nums = list(map(int, input("请输入20个整数（空格分隔）：").split()))
avg = sum(nums) / len(nums)
nearest = farthest = nums[0]
for n in nums[1:]:
    if abs(n - avg) < abs(nearest - avg):
        nearest = n
    if abs(n - avg) > abs(farthest - avg):
        farthest = n
print(f"平均值={avg:.2f}, 最近={nearest}, 最远={farthest}")

# Problem 2: digit rearrangement
num = input("请输入一个非负整数：").strip()
digits = list(num)
n = len(digits)

# Next permutation
i = n - 2
while i >= 0 and digits[i] >= digits[i+1]:
    i -= 1
if i >= 0:
    j = n - 1
    while digits[j] <= digits[i]:
        j -= 1
    digits[i], digits[j] = digits[j], digits[i]
    digits[i+1:] = reversed(digits[i+1:])
    print(f"比{num}大的最小重排 = {''.join(digits)}")
else:
    print(f"不存在比{num}大的重排")

# Previous permutation
digits = list(num)
i = n - 2
while i >= 0 and digits[i] <= digits[i+1]:
    i -= 1
if i >= 0:
    j = n - 1
    while digits[j] >= digits[i]:
        j -= 1
    digits[i], digits[j] = digits[j], digits[i]
    digits[i+1:] = reversed(digits[i+1:])
    result = ''.join(digits)
    if len(result) == n:
        print(f"比{num}小的最大重排 = {result}")
    else:
        print(f"不存在比{num}小的重排")
else:
    print(f"不存在比{num}小的重排")
