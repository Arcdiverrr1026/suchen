# 01
## 定义基类Person
class Person:
# 02
##构造方法，初始化姓名、年龄
    def __init__(self,name,age):
        self.name = name
        self.age = age
# 05
## introduce方法，返回自己的姓名和年龄信息 "大家好，我叫xx，今年xx岁”
    def introduce(self):\
# 06
        print("大家好，我叫{name}，今年{age}".format(name=self.name,age=self.age))
# 08
## 定义子类Student
class Student(Person):
# 09
## 定义构造方法
    def __init__(self,name,age,id,profession):
# 10
## 调用父类的构造函数初始化共有属性
        super().__init__(name,age)
# 12
## 添加子类特有的属性学号和专业
        self.id = id
        self.profession = profession
# 15
## 重写父类的 introduce方法，返回字符串 "大家好，我是学生xx，学号xx，专业是xx。"
    def introduce(self):
        print("大家好，我是学生{name}， 学号{id}，专业是{profession}".format(name=self.name,id=self.id,profession=self.profession))
# 18
## 增加子类特有的方法study(self, subject)： 返回字符串"xx正在学习subject 。"
    def study(self,subject):
# 19
        print("{name}正在学习{subject}。".format(name=self.name,subject=subject))
# 21
## 定义子类Teacher，继承自Person
class Teacher(Person):
# 22
## 构造方法
    def __init__(self,name,age,id,department):
# 23
## 调用父类的构造函数初始化共有属性
        super().__init__(name,age)
# 24
## 初始化工号、部门和课程列表
        self.id = id
        self.department = department
        self.course = []
# 28
##增加子类特有的方法 add_course(self, course):将课程course添加到课程列表，并输出"xx老师开始教授xx课程。"
    def add_course(self,course):
        self.course.append(course)
        print("{name}老师开始教授{course}课程".format(name=self.name,course=self.course))
# 31
##增加方法teach()
    def teach(self):
# 32
##  如该教师授课课程不为空，
        if not self.course:
            print("{name}教师目前没有安排课程".format(name=self.name,course=self.course))
# 33
##  选取课程列表中的最后一门课程输出”xx老师目前正在教授xx课程”
        else:
            print("{name}老师目前正在教授{course}课程".format(name=self.name,course=self.course))
# 38
## 创建Person对象，"张三", 30
p1 = Person("张三",30)
# 39
## 输出张三自我介绍的信息
p1.introduce()
# 41
## 创建Student对象："李四", 20, "2023001", "计算机科学"
s1 = Student("李四",20,"2023001","计算机科学")
# 42
## 调用重写的introduce方法，输出李四的自我介绍信息
s1.introduce()
# 43
## 调用学生类的study方法，输出学习Python课程的信息
s1.study("Python")
# 45
##创建Teacher对象，"王教授", 45, "T1001", "计算机学院"
t1 = Teacher("王教授",45,"T1001","计算机学院")
# 46
## 调用重写的introduce方法，输出王教授的自我介绍信息
t1.introduce()
# 47
## 调用add_course()方法，让王教授增加一门Python编程的课程
t1.add_course("Python")
# 48
## 输出王教授正在教授的课程信息
t1.teach()