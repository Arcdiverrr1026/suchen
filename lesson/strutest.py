def computer(a):
    c = 0
    for x in range(1,a+1):
        b = 1 / x**2
        c += b
    return c


def get_last_three_digits(base, n):
    result = pow(base, n, 1000)
    return f"{result:03d}"

x = 2
n = 1231
print(get_last_three_digits(x, n))

