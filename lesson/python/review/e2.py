import random
code = ''

for i in range(4):
    x = random.randint(0,1)
    if x == 0:
        code += str(random.randint(0,9))
    else:
        code += chr(random.randint(65,90))

print(code)
