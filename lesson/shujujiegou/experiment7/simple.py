# Problem 1: sequence sum
a, b = 100, 99
total = a + b
for _ in range(3, 101):
    a, b = b, abs(b - a)
    total += b
print(f"问题1：前100项和 = {total}")
print()

# Problem 2: diamond pattern
for i in range(1, 12):
    stars = i if i <= 6 else 12 - i
    char = '*' if stars % 2 == 1 else '#'
    spaces = 6 - stars
    print(char * stars + " " * (2 * spaces) + char * stars)

# Problem 3: twin primes
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print("问题3：孪生素数对")
count = 0
for p in range(2, 9999):
    if is_prime(p) and is_prime(p + 2):
        print(f"({p}, {p+2})")
        count += 1
print(f"共 {count} 对")
print()

# Problem 4: perfect square quadruples
sq1 = [i*i for i in range(1, 10) if i*i < 10]
sq2 = [i*i for i in range(4, 10) if 10 <= i*i < 100]
sq3 = [i*i for i in range(10, 32) if 100 <= i*i < 1000]
sq4 = [i*i for i in range(32, 100) if 1000 <= i*i < 10000]

print("问题4：四个完全平方数")
for a in sq1:
    for b in sq2:
        if set(str(a)) & set(str(b)):
            continue
        for c in sq3:
            if (set(str(a)) | set(str(b))) & set(str(c)):
                continue
            for d in sq4:
                digits = set(str(a)) | set(str(b)) | set(str(c)) | set(str(d))
                if digits == set("0123456789"):
                    print(f"{a}, {b}, {c}, {d}")
