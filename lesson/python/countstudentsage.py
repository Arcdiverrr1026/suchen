#01
## 导入日期时间模块（datetime, date）
from datetime import datetime, date

#02
## 定义类名Student
class Student:
#03
## 定义构造函数，接收3个参数，学号，姓名，出生日期'YYYY-MM-DD'
    def __init__(self, id, name, birthday):
        self.id = id
        self.name = name
        # 循环校验日期，直到格式正确
        while True:
            try:
                # 转换日期，格式错误会抛出异常
                self.birthday = datetime.strptime(birthday, "%Y-%m-%d")
                break  # 格式正确，退出循环
            except ValueError:
                #09
                ##提醒：出生日期格式不正确，应为 'YYYY-MM-DD'
                print("出生日期格式不正确，应为‘YYYY-MM-DD’")
                # 让用户重新输入正确的日期
                birthday = input("请重新输入正确的出生日期(YYYY-MM-DD)：")

#10
## 定义计算年龄函数calculate_age
    def calculate_age(self):
#11
##   获取当前日期
        today = date.today()
#12
##   计算年龄，为当前年份与出生年份的差
        age = today.year - self.birthday.year
#13
##    如果今年生日还没过
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
#14
##      年龄减1
            age -= 1
#15
##   返回年龄
        return age

#16
## 创建学生对象，学号"2023001", 姓名"张三",出生日期 "2005-03-15"
s1 = Student("2023001", "张三", "2005-03-15")

#17
## 创建学生对象，学号"2023002", 姓名"李四",出生日期 "2004-11-22"
s2 = Student("2023002", "李四", "2004-11-22")

#18
## 计算并打印张三年龄
print(f"{s1.name}的年龄：{s1.calculate_age()}岁")

#19
## 计算并打印李四年龄
print(f"{s2.name}的年龄：{s2.calculate_age()}岁")

#20
## 测试异常情况，进行日期格式异常捕获
print("\n===== 测试异常日期格式 =====")
try:
#21
##创建学生对象，学号"2023001", 姓名"王五",出生日期 "2005/03/15"
    s3 = Student("2023001", "王五", "2005/03/15")
#22
## 捕获异常
except Exception as e:
#23
## 输出异常信息
    print("捕获到异常：", e)
    print()