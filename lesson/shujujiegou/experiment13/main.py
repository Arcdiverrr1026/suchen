"""Stack and queue applications.

Problem 1: English palindrome detection using stack and queue.
Problem 2: Card game simulation using stack and queue.
"""

from collections import deque


def is_english_palindrome(s: str) -> bool:
    """Check if string is an English palindrome using a stack and a queue.

    Ignores non-alphabetic characters; case-insensitive.
    """
    stack: list[str] = []
    queue: deque[str] = deque()

    for ch in s:
        if ch.isalpha():
            lower = ch.lower()
            stack.append(lower)
            queue.append(lower)

    while stack:
        if stack.pop() != queue.popleft():
            return False
    return True


def card_game(a_cards: list[int], b_cards: list[int]) -> str:
    """Simulate the card game. Return 'A' or 'B' as the winner.

    Rules:
    - Each player has a queue of cards.
    - Each turn, the current player plays the first card from their hand onto the table (stack).
    - If the played card matches a card on the table, the player takes all cards from
      the matching card onward (inclusive) and adds them to the back of their hand.
    - When one player runs out of cards, the other wins.
    """
    hand_a: deque[int] = deque(a_cards)
    hand_b: deque[int] = deque(b_cards)
    table: list[int] = []
    turn = 0  # 0 = A's turn, 1 = B's turn

    max_rounds = 10000  # safety limit
    for _ in range(max_rounds):
        if turn == 0:
            if not hand_a:
                return "B"
            card = hand_a.popleft()
        else:
            if not hand_b:
                return "A"
            card = hand_b.popleft()

        # Check if card matches any on the table
        match_idx = -1
        for i in range(len(table) - 1, -1, -1):
            if table[i] == card:
                match_idx = i
                break

        if match_idx >= 0:
            # Take all cards from match_idx onward (inclusive)
            taken = table[match_idx:] + [card]
            table = table[:match_idx]
            if turn == 0:
                hand_a.extend(taken)
            else:
                hand_b.extend(taken)
        else:
            table.append(card)

        turn = 1 - turn

    return "Draw"  # Should not happen in normal play


def main() -> None:
    # Problem 1
    print("问题1：英文回文判断（使用栈和队列）")
    s = input("请输入一个字符串：")
    if is_english_palindrome(s):
        print(f"\"{s}\" 是回文")
    else:
        print(f"\"{s}\" 不是回文")
    print()

    # Problem 2
    print("问题2：纸牌游戏（使用栈和队列）")
    a_cards = list(map(int, input("请输入A的牌（空格分隔）：").split()))
    b_cards = list(map(int, input("请输入B的牌（空格分隔）：").split()))
    winner = card_game(a_cards, b_cards)
    print(f"赢家是: {winner}")


if __name__ == "__main__":
    main()
