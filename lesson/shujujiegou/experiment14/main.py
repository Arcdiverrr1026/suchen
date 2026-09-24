"""In-place array rotation.

Move the first k elements to the end, and the last (n-k) elements to the front.
No extra array is introduced — uses the three-reverse algorithm.
"""


def rotate_array(arr: list[int], k: int) -> None:
    """Rotate array arr left by k positions in-place.

    Uses the three-reverse algorithm: O(n) time, O(1) extra space.
    """
    n = len(arr)
    if n == 0:
        return
    k = k % n  # handle k > n
    if k == 0:
        return

    _reverse(arr, 0, k - 1)
    _reverse(arr, k, n - 1)
    _reverse(arr, 0, n - 1)


def _reverse(arr: list[int], left: int, right: int) -> None:
    """Reverse arr[left..right] in-place."""
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1


def main() -> None:
    print("数组旋转（不使用额外数组）")

    parts = input("请输入数组元素（空格分隔）：").split()
    arr = [int(x) for x in parts]
    k = int(input("请输入旋转位置k："))

    print(f"原数组: {arr}")
    rotate_array(arr, k)
    print(f"旋转后: {arr}")


if __name__ == "__main__":
    main()
