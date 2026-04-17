import numpy as np

# 1. 输出numpy的版本
print("1. NumPy 版本:", np.__version__)

# 2. 创建数组10到50，并输出第5个元素之后的所有元素
arr = np.arange(10, 51)
print("\n2. 创建的数组:\n", arr)
print("第5个元素之后的所有元素:\n", arr[5:])

# 3. 矩阵生成：5阶单位矩阵A 和 5阶随机方阵B
A = np.eye(5)
B = np.random.randn(5, 5)

print("\n3. 5阶单位矩阵 A:\n", A)
print("5阶随机方阵 B:\n", B)

# 4. 输出矩阵的形状shape
print("\n4. 矩阵A的形状:", A.shape)
print("矩阵B的形状:", B.shape)

# 5. 使用切片输出B的2-4列 (即索引为 1, 2, 3 的列)
print("\n5. B的第2-4列:\n", B[:, 1:4])

# 6. 输出B中最后一列元素 > 0 的所有行
print("\n6. B中最后一列元素 > 0 的所有行:\n", B[B[:, -1] > 0])

# 7. 对矩阵A进行与常数的加、减、乘法
c = 3
print("\n7. A + 3:\n", A + c)
print("A - 3:\n", A - c)
print("A * 3:\n", A * c)

# 8. 对矩阵A进行与B的加、减、乘法
print("\n8. A + B:\n", A + B)
print("A - B:\n", A - B)
print("A * B (逐元素相乘):\n", A * B)
print("A @ B (矩阵点乘):\n", A @ B)

# 9. 求矩阵B的统计特征
print("\n9. 矩阵B的统计数据:")
print("① 每一行的和:", np.sum(B, axis=1))
print("① 每一列的和:", np.sum(B, axis=0))

print("② 每一行的最大值:", np.max(B, axis=1))
print("② 每一列的最小值:", np.min(B, axis=0))

print("③ 每一行的标准差:", np.std(B, axis=1))
print("③ 每一列的方差:", np.var(B, axis=0))

# 10. 创建5阶方阵C并进行拼接
C = np.ones((5, 5))
concat_0 = np.concatenate((B, C), axis=0)
concat_1 = np.concatenate((B, C), axis=1)
print("\n10. 第0维拼接后形状:", concat_0.shape)
print("第1维拼接后形状:", concat_1.shape)

# 11. 矩阵B的排序
sort_0 = np.sort(B, axis=0)
sort_1 = np.sort(B, axis=1)
print("\n11. B按第0轴排序:\n", sort_0)
print("B按第1轴排序:\n", sort_1)

# 12. 获取B每一行最大元素的索引
max_indices = np.argmax(B, axis=1)
print("\n12. B每一行最大元素的索引:", max_indices)

