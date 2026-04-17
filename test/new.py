import sys

sys.set_int_max_str_digits(20000)

count = 0
a = ["1"] * 10000
b = ["1"] * 1000

e = int("".join(a)) - int("".join(b))

for i in range(1,e):
    if "0" in str(i):
        continue

    if "3" in str(i) and "7" in str(i):
        count += 1

print(count)
