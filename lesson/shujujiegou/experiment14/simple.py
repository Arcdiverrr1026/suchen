"""Simple version: in-place array rotation using three-reverse."""

arr = list(map(int, input("请输入数组元素（空格分隔）：").split()))
k = int(input("请输入旋转位置k："))
n = len(arr)
k = k % n

# Three-reverse algorithm
arr[:k] = reversed(arr[:k])
arr[k:] = reversed(arr[k:])
arr[:] = reversed(arr)

print(f"旋转后: {arr}")
