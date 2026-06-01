import ast

salary = {}

# 读取文件数据
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        data = ast.literal_eval(line.strip())

        sid = data["sid"]

        # 按 key 的递增顺序获取工资，排除 sid
        months = sorted([key for key in data.keys() if key != "sid"])
        wages = [data[month] for month in months]

        # 计算平均工资，取整数
        avg = int(sum(wages) / len(wages))

        # 将月工资和平均工资加入列表
        salary[sid] = wages + [avg]

# 按 key 递增顺序输出
salary = dict(sorted(salary.items()))

print(salary)