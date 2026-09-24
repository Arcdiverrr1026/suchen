import random

def getData():
    stuDict = {
        '230101': '张三',
        '230102': '韦小宝',
        '230103': '王二',
        '230104': '黄药师',
        '230105': '李四',
        '230106': '丁春秋',
        '230107': '段誉',
        '230108': '苗人凤',
        '230109': '虚竹',
        '230110': '程灵素',
        '230111': '阿朱',
        '230112': '王重阳',
        '230113': '郭靖',
        '230114': '段王爷',
        '230115': '萧峰',
        '230116': '欧阳锋',
        '230117': '黄蓉',
        '230118': '洪七公'
    }

    return stuDict

def rollcall(students:dict) -> tuple:
    tmpls = list(students.items())
    randomItem = random.choice(tmpls)
    return randomItem

stulist = getData()
for i in range(1,11):
    choiceStudent = rollcall(stulist)
    print('第{0}次点名：学号{1}姓名{2}'.format(i,choiceStudent[0],choiceStudent[1]))
