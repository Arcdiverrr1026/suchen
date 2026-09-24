"""Find all occurrences of a pattern in a string with KMP."""


def build_next(pattern: str) -> list[int]:
    prefix = [0] * len(pattern)
    matched = 0

    for index in range(1, len(pattern)):
        while matched > 0 and pattern[index] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        prefix[index] = matched

    return prefix


def kmp_search(text: str, pattern: str) -> list[int]:
    """Return 1-based starting positions of pattern in text."""
    if not pattern:
        return []

    prefix = build_next(pattern)
    result: list[int] = []
    matched = 0

    for index, char in enumerate(text):
        while matched > 0 and char != pattern[matched]:
            matched = prefix[matched - 1]
        if char == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            result.append(index - len(pattern) + 2)
            matched = prefix[matched - 1]

    return result


def main() -> None:
    pattern_length = int(input().strip())
    pattern = input().strip()
    text_length = int(input().strip())
    text = input().strip()

    if len(pattern) != pattern_length:
        raise ValueError("pattern length does not match N")
    if len(text) != text_length:
        raise ValueError("text length does not match M")

    print(" ".join(map(str, kmp_search(text, pattern))))


if __name__ == "__main__":
    main()
