"""Four sequence and approximation problems.

Problem 1: Compute first 10 terms of e-based sequence.
Problem 2: Factorial-based approximation sum.
Problem 3: Nested sequence lookup.
Problem 4: Rainfall analysis — max consecutive rainy/non-rainy days.
"""

import math


def exponential_sequence(n: int = 10) -> list[float]:
    """Compute first n terms: a1 = e, a2 = e^2, ..., an = e^n.

    Approximation using Taylor series for e^x at x=1:
    e = sum_{k=0..inf} 1/k!
    """
    e = math.e
    return [e**i for i in range(1, n + 1)]


def factorial_approximation(n: int = 20) -> float:
    """Compute 1/1! + 1/2! + 1/3! + ... + 1/n!.

    This converges to e - 1 as n -> infinity.
    """
    total = 0.0
    fact = 1
    for i in range(1, n + 1):
        fact *= i
        total += 1.0 / fact
    return total


def nested_sequence_value(pos: int) -> int:
    """Find value at position pos in sequence: 1,1,2,1,2,3,1,2,3,4,...

    The sequence is formed by concatenating groups: (1), (1,2), (1,2,3), ...
    Group k has k elements. Find which group pos falls into.
    """
    remaining = pos
    k = 1
    while remaining > k:
        remaining -= k
        k += 1
    return remaining


def rainfall_analysis(data: list[int]) -> tuple[int, int]:
    """Given 30 days of rainfall data (0=no rain, >0=rain),
    return (max_consecutive_rainy, max_consecutive_non_rainy)."""
    max_rain = 0
    max_dry = 0
    cur_rain = 0
    cur_dry = 0

    for val in data:
        if val > 0:
            cur_rain += 1
            max_rain = max(max_rain, cur_rain)
            cur_dry = 0
        else:
            cur_dry += 1
            max_dry = max(max_dry, cur_dry)
            cur_rain = 0

    return max_rain, max_dry


def main() -> None:
    # Problem 1
    print("问题1：e的幂次序列（前10项）")
    terms = exponential_sequence(10)
    for i, t in enumerate(terms, 1):
        print(f"  a{i} = e^{i} = {t:.6f}")
    print()

    # Problem 2
    print("问题2：阶乘倒数求和")
    print(f"  1/1! + 1/2! + ... + 1/20! = {factorial_approximation(20):.10f}")
    print(f"  (e - 1 = {math.e - 1:.10f})")
    print()

    # Problem 3
    print("问题3：嵌套数列查找")
    test_positions = [1, 3, 6, 10, 15, 20]
    for p in test_positions:
        print(f"  第{p}项 = {nested_sequence_value(p)}")
    print()

    # Problem 4
    print("问题4：降雨量分析")
    # Sample 30-day rainfall data (mm, 0 means no rain)
    data = [5, 3, 0, 0, 8, 12, 0, 0, 0, 7, 2, 0, 15, 20, 10, 0, 0, 0, 0, 3, 1, 0, 6, 9, 0, 0, 11, 0, 0, 4]
    print(f"  30天降雨数据: {data}")
    max_rain, max_dry = rainfall_analysis(data)
    print(f"  最长连续有雨天数: {max_rain}")
    print(f"  最长连续无雨天数: {max_dry}")


if __name__ == "__main__":
    main()
