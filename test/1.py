class employee:
    def __init__(self,name,id):
        self.name = name
        self.id = id

    def print_info(self):
        print(self.name)
        print(self.id)

    def calucalate_salary(self):
        pass

class fulltimeemployee(employee):
    def __init__(self,name,id,monthly_salary):
        super().__init__(name,id)
        self.monthly_salary = monthly_salary

    def calulate_salary(self):
        print(self.monthly_salary*12)

class parttimeemployee(employee):
    def __init__(self,name,id,daily_salary,work_days):
        super().__init__(name, id)
        self.daily_salary = daily_salary
        self.work_days = work_days

    def calulate_salary(self):
        print(self.daily_salary * self.work_days)

m1 = fulltimeemployee("a",1,11)
m2 = parttimeemployee("b",12,1,10)
m1.print_info()
m2.print_info()
m1.calulate_salary()
m2.calulate_salary()