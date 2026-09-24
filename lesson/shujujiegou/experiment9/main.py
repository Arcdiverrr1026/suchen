"""Linked list linear list with insert and delete operations.

Uses a singly linked list with a head node and a length variable.
Interactive prompts for insert/delete operations.
"""

from __future__ import annotations


class _Node:
    __slots__ = ("data", "next")

    def __init__(self, data: int = 0, next_node: _Node | None = None) -> None:
        self.data = data
        self.next = next_node


class LinkedList:
    """Singly linked list with head node and length counter."""

    def __init__(self) -> None:
        self._head = _Node()  # head node (sentinel)
        self._length = 0

    @property
    def length(self) -> int:
        return self._length

    def insert(self, pos: int, elem: int) -> bool:
        """Insert elem at position pos (1-indexed). Return True on success."""
        if pos < 1 or pos > self._length + 1:
            return False

        prev = self._head
        for _ in range(pos - 1):
            prev = prev.next  # type: ignore[union-attr]
        new_node = _Node(elem, prev.next)
        prev.next = new_node
        self._length += 1
        return True

    def delete(self, pos: int) -> tuple[bool, int | None]:
        """Delete element at position pos (1-indexed). Return (success, element)."""
        if pos < 1 or pos > self._length:
            return False, None

        prev = self._head
        for _ in range(pos - 1):
            prev = prev.next  # type: ignore[union-attr]
        elem = prev.next.data  # type: ignore[union-attr]
        prev.next = prev.next.next  # type: ignore[union-attr]
        self._length -= 1
        return True, elem

    def display(self) -> str:
        elems: list[int] = []
        node = self._head.next
        while node is not None:
            elems.append(node.data)
            node = node.next
        return "(" + ",".join(str(x) for x in elems) + ")"


def main() -> None:
    ll = LinkedList()

    while True:
        choice = input("是否要对线性表进行插入和删除？（Y/N）").strip().upper()
        if choice != "Y":
            break

        op = input("进行插入还是删除？（1--插入，2--删除）").strip()
        if op == "1":
            parts = input("请输入插入位置和元素（空格分隔）：").split()
            pos, elem = int(parts[0]), int(parts[1])
            if ll.insert(pos, elem):
                print(ll.display())
            else:
                print("插入位置有误")
        elif op == "2":
            pos = int(input("请输入删除位置："))
            ok, _ = ll.delete(pos)
            if ok:
                print(ll.display())
            else:
                print("删除位置有误")


if __name__ == "__main__":
    main()
