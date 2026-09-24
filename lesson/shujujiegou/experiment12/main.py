"""Two array-based problems.

Problem 1: Find the integer nearest to and farthest from the average of 20 integers.
Problem 2: Digit rearrangement — find next larger and previous smaller permutations.
"""


def nearest_and_farthest(nums: list[int]) -> tuple[int, int]:
    """Return (nearest_to_avg, farthest_from_avg) among the given integers."""
    avg = sum(nums) / len(nums)
    nearest = nums[0]
    farthest = nums[0]
    min_diff = abs(nums[0] - avg)
    max_diff = abs(nums[0] - avg)

    for n in nums[1:]:
        diff = abs(n - avg)
        if diff < min_diff:
            min_diff = diff
            nearest = n
        if diff > max_diff:
            max_diff = diff
            farthest = n

    return nearest, farthest


def digit_rearrange(num: int) -> tuple[int | None, int | None]:
    """Given a non-negative integer, find:
    - The smallest integer larger than num using the same digits (next permutation).
    - The largest integer smaller than num using the same digits (previous permutation).
    Returns (next_larger, prev_smaller), either may be None if not possible.
    """
    digits = list(str(num))
    n = len(digits)

    # Next permutation (smallest larger)
    next_larger = _next_permutation(digits[:])
    # Previous permutation (largest smaller)
    prev_smaller = _prev_permutation(digits[:])

    return next_larger, prev_smaller


def _next_permutation(digits: list[str]) -> int | None:
    """Find the next lexicographic permutation. Return as int or None."""
    n = len(digits)
    # Find rightmost digit smaller than its successor
    i = n - 2
    while i >= 0 and digits[i] >= digits[i + 1]:
        i -= 1
    if i < 0:
        return None

    # Find rightmost digit greater than digits[i]
    j = n - 1
    while digits[j] <= digits[i]:
        j -= 1

    digits[i], digits[j] = digits[j], digits[i]
    # Reverse the suffix
    digits[i + 1:] = reversed(digits[i + 1:])
    return int("".join(digits))


def _prev_permutation(digits: list[str]) -> int | None:
    """Find the previous lexicographic permutation. Return as int or None."""
    n = len(digits)
    # Find rightmost digit greater than its successor
    i = n - 2
    while i >= 0 and digits[i] <= digits[i + 1]:
        i -= 1
    if i < 0:
        return None

    # Find rightmost digit smaller than digits[i]
    j = n - 1
    while digits[j] >= digits[i]:
        j -= 1

    digits[i], digits[j] = digits[j], digits[i]
    # Reverse the suffix
    digits[i + 1:] = reversed(digits[i + 1:])

    result = int("".join(digits))
    # Check no leading zero (unless it's a single digit)
    if len(str(result)) < len(digits):
        return None
    return result


def main() -> None:
    # Problem 1
    print("问题1：距离平均值最近和最远的数")
    print("请输入20个整数（空格分隔）：")
    nums = list(map(int, input().split()))
    if len(nums) != 20:
        print("错误：需要恰好20个整数")
        return
    avg = sum(nums) / len(nums)
    near, far = nearest_and_farthest(nums)
    print(f"平均值 = {avg:.2f}")
    print(f"最接近平均值的数 = {near}")
    print(f"最远离平均值的数 = {far}")
    print()

    # Problem 2
    print("问题2：数字重排")
    num = int(input("请输入一个非负整数："))
    next_larger, prev_smaller = digit_rearrange(num)
    if next_larger is not None:
        print(f"比{num}大的最小重排 = {next_larger}")
    else:
        print(f"不存在比{num}大的重排")
    if prev_smaller is not None:
        print(f"比{num}小的最大重排 = {prev_smaller}")
    else:
        print(f"不存在比{num}小的重排")


if __name__ == "__main__":
    main()
