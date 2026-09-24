"""Four mathematical problems.

Problem 1: Sequence sum — a1=100, a2=99, an=|a(n-1)-a(n-2)|, sum of first 100 terms.
Problem 2: Print a diamond pattern (11 lines).
Problem 3: Find all twin prime pairs up to 10000.
Problem 4: Find quadruples of perfect squares using digits 0-9 exactly once.
"""


def sequence_sum(n: int = 100) -> int:
    """Compute sum of first n terms: a1=100, a2=99, an=|a(n-1)-a(n-2)|."""
    a, b = 100, 99
    total = a + b
    for _ in range(3, n + 1):
        a, b = b, abs(b - a)
        total += b
    return total


def print_diamond(size: int = 6) -> None:
    """Print a diamond pattern. size controls the half-width."""
    for i in range(1, 2 * size):
        stars = i if i <= size else 2 * size - i
        spaces_before = size - stars
        print(" " * spaces_before + "*" * stars + " " * (2 * spaces_before) + "*" * stars)


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def twin_primes(limit: int = 10000) -> list[tuple[int, int]]:
    """Find all twin prime pairs (p, p+2) where both are prime and p+2 <= limit."""
    pairs = []
    for p in range(2, limit - 1):
        if _is_prime(p) and _is_prime(p + 2):
            pairs.append((p, p + 2))
    return pairs


def _is_perfect_square(n: int) -> bool:
    if n < 0:
        return False
    root = int(n**0.5)
    return root * root == n


def perfect_square_quadruples() -> list[tuple[int, int, int, int]]:
    """Find one 1-digit, 2-digit, 3-digit, 4-digit perfect square
    that together use each digit 0-9 exactly once."""
    results = []
    # Generate perfect squares by digit count
    sq1 = [i * i for i in range(1, 10) if i * i < 10]           # 1-digit: 1,4,9
    sq2 = [i * i for i in range(4, 10) if 10 <= i * i < 100]    # 2-digit
    sq3 = [i * i for i in range(10, 32) if 100 <= i * i < 1000] # 3-digit
    sq4 = [i * i for i in range(32, 100) if 1000 <= i * i < 10000]  # 4-digit

    for a in sq1:
        da = set(str(a))
        for b in sq2:
            db = set(str(b))
            if da & db:
                continue
            for c in sq3:
                dc = set(str(c))
                if (da | db) & dc:
                    continue
                for d in sq4:
                    dd = set(str(d))
                    all_digits = da | db | dc | dd
                    if len(all_digits) == 10 and all_digits == set("0123456789"):
                        results.append((a, b, c, d))
    return results


def main() -> None:
    # Problem 1
    print("问题1：数列求和")
    print(f"a1=100, a2=99, an=|a(n-1)-a(n-2)|, 前100项和 = {sequence_sum(100)}")
    print()

    # Problem 2
    print("问题2：菱形图案")
    print_diamond()
    print()

    # Problem 3
    print("问题3：孪生素数对（<=10000）")
    pairs = twin_primes()
    for p, q in pairs:
        print(f"({p}, {q})")
    print(f"共 {len(pairs)} 对")
    print()

    # Problem 4
    print("问题4：四个完全平方数（每位数字0-9恰好用一次）")
    quads = perfect_square_quadruples()
    for a, b, c, d in quads:
        print(f"{a}, {b}, {c}, {d}")
    print(f"共 {len(quads)} 组")


if __name__ == "__main__":
    main()
