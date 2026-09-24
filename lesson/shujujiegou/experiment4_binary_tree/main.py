"""Binary tree implemented with linked nodes.

Input format for the command line program:
    preorder sequence where '#' means an empty child.

Example:
    ABD##E##CF###
"""

from collections import deque
from dataclasses import dataclass
from typing import Iterator


@dataclass
class TreeNode:
    value: str
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class BinaryTree:
    def __init__(self, root: TreeNode | None = None) -> None:
        self.root = root

    @classmethod
    def from_preorder(cls, sequence: str, empty: str = "#") -> "BinaryTree":
        items = iter(ch for ch in sequence.strip() if not ch.isspace())

        def build(iterator: Iterator[str]) -> TreeNode | None:
            try:
                value = next(iterator)
            except StopIteration:
                raise ValueError("incomplete preorder sequence") from None
            if value == empty:
                return None
            return TreeNode(value, build(iterator), build(iterator))

        root = build(items)
        try:
            next(items)
        except StopIteration:
            return cls(root)
        raise ValueError("extra data after a complete binary tree")

    def preorder(self) -> list[str]:
        result: list[str] = []

        def visit(node: TreeNode | None) -> None:
            if node is None:
                return
            result.append(node.value)
            visit(node.left)
            visit(node.right)

        visit(self.root)
        return result

    def inorder(self) -> list[str]:
        result: list[str] = []

        def visit(node: TreeNode | None) -> None:
            if node is None:
                return
            visit(node.left)
            result.append(node.value)
            visit(node.right)

        visit(self.root)
        return result

    def postorder(self) -> list[str]:
        result: list[str] = []

        def visit(node: TreeNode | None) -> None:
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            result.append(node.value)

        visit(self.root)
        return result

    def level_order(self) -> list[str]:
        if self.root is None:
            return []

        result: list[str] = []
        queue: deque[TreeNode] = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return result

    def height(self) -> int:
        def count(node: TreeNode | None) -> int:
            if node is None:
                return 0
            return max(count(node.left), count(node.right)) + 1

        return count(self.root)

    def degree_counts(self) -> dict[int, int]:
        counts = {0: 0, 1: 0, 2: 0}

        def visit(node: TreeNode | None) -> None:
            if node is None:
                return
            degree = int(node.left is not None) + int(node.right is not None)
            counts[degree] += 1
            visit(node.left)
            visit(node.right)

        visit(self.root)
        return counts


def _join(values: list[str]) -> str:
    return " ".join(values)


def main() -> None:
    sequence = input().strip()
    tree = BinaryTree.from_preorder(sequence)
    counts = tree.degree_counts()

    print(f"preorder: {_join(tree.preorder())}")
    print(f"inorder: {_join(tree.inorder())}")
    print(f"postorder: {_join(tree.postorder())}")
    print(f"level_order: {_join(tree.level_order())}")
    print(f"height: {tree.height()}")
    print(f"degree_0: {counts[0]}")
    print(f"degree_1: {counts[1]}")
    print(f"degree_2: {counts[2]}")


if __name__ == "__main__":
    main()
