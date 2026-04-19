'''
def is_prime(n):
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5)+1, 2):
        if n % i == 0:
            return False
    return True

for n in range(1, 100):
    if is_prime(n):
        print(n,end=" ")
'''

#有一分数序列：2/1，3/2，5/3，8/5，13/8，21/13...求出这个数列的前20项之和

'''
def qiuhe(a,b,cont):
    if cont == 0:
        return 0
    return (a / b)+qiuhe(a + b,a,cont-1)

print(qiuhe(2,1,20))
'''
'''
import random
nums = [random.randint(0,500) for _ in range(100)]

def is_prime(n):
    if n == 1 or n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3,int(n**0.5)+1,2):
        if n % i == 0:
            return False
    return True

ans = [n for n in nums if is_prime(n)]
print(f"共找到{len(ans)}个质数")
for i in range(len(ans)):
    print(f"{ans[i]:>5}",end="\n" if (i + 1) % 5 == 0 else " ")
'''

'''
编程实现：产生一个四位随机验证码，验证码由数字和大写字母组成，每次产生验证码不同。
提示：需要加载random模块，使用 randrange(start,end)函数，最后验证码以字符串输出
'''

'''
import random

def code():
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    code_1 = ""#创建空字符作为容器
    for _ in range(4):
        index = random.randint(0,len(chars))#随机标签，而不是随机值
        code_1 += chars[index]

    return code_1

print(code())
'''
'''
n = int(input())
m = 1
for _ in range(n - 1):
    m = (m + 1)*2
print(m)
'''

'''
1.从键盘输入10个英文单词，输出其中以元音字母开头的单词。
分析：输入一个英文单词，并进行判断，用for循环控制重复执行10次。可以将所有元音字母构成一个字符串，遍历该字符串中的各个字符，并判断单词的首字母。
'''

'''
a_list = input().split()
for i in a_list:
    if i[0] in "aeiouAEIOU":
        print(i)
    else:
        continue
'''
'''
从键盘输入几个数字，用逗号分隔，求这些数字之和。
分析：输入的数字当作一个字符串来处理，首先分离出数字串，再转换成数值，这样就能求和
'''

'''
print(sum(map(int,input().split(","))))
'''

'''
密码安全，让用户设置（输入）一个密码，要求：
（1）不少于6位，必须包含数字、大写字母、小写字母，否则提醒用户安全强度太低，请重新设置；
（2）密码确认：再输一次，如果两次输入不同，提醒用户重新输入！
'''
'''
def checkpassword(password):
    has_digtal = any(a.isdigit() for a in password)
    has_lower = any(a.islower() for a in password)
    has_upper = any(a.isupper() for a in password)

    if len(password) >= 6 and has_digtal and has_lower and has_upper:
        return True
    return False

num = input()
if checkpassword(num):
    print("请再输入一次")
    while True:
        num_2 = input()
        if num == num_2:
            print("设置成功")
            break
        else:
            print("两次密码不一致")
else:
    print("强度太低，请重新设置！")
'''
'''
编写程序判断一个从键盘输入的字符串包含的字母、数字字符和其它字符的个数
分析：遍历字符串，在遍历字符串时，判断该字符是什么类型的字符
'''
def checkpassword(password):
    ditgit,aplha,other = 0,0,0

    for c in password:
        if c.isdigit():
            ditgit += 1
        elif c.isalpha():
            aplha += 1
        else:
            other += 1

    return ditgit,aplha,other

print(*checkpassword(input())) # *解包器




