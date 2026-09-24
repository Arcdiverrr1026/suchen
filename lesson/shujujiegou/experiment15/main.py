"""Binary tree: construction from extended preorder, traversals, subtree swap.

Extended preorder uses '#' to represent empty nodes.
Outputs preorder, inorder, postorder, and level-order traversals before and after swapping.
"""

from __future__ import annotations
from collections import deque


class _Node:
    __slots__ = ("data", "left", "right")

    def __init__(self, data: str = "", left: _Node | None = None, right: _Node | None = None) -> None:
        self.data = data
        self.left = left
        self.right = right


class BinaryTree:
    """Binary tree built from extended preorder sequence."""

    def __init__(self) -> None:
        self._root: _Node | None = None

    @classmethod
    def from_preorder(cls, seq: str) -> BinaryTree:
        """Build tree from extended preorder sequence (e.g. 'ABD##E##CF###').

        '#' represents an empty node.
        """
        tree = cls()
        tree._root, _ = cls._build(seq, 0)
        return tree

    @staticmethod
    def _build(seq: str, index: int) -> tuple[_Node | None, int]:
        if index >= len(seq) or seq[index] == "#":
            return None, index + 1

        node = _Node(seq[index])
        node.left, index = BinaryTree._build(seq, index + 1)
        node.right, index = BinaryTree._build(seq, index)
        return node, index

    def preorder(self) -> list[str]:
        result: list[str] = []
        self._preorder(self._root, result)
        return result

    def _preorder(self, node: _Node | None, result: list[str]) -> None:
        if node is None:
            return
        result.append(node.data)
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def inorder(self) -> list[str]:
        result: list[str] = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: _Node | None, result: list[str]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.data)
        self._inorder(node.right, result)

    def postorder(self) -> list[str]:
        result: list[str] = []
        self._postorder(self._root, result)
        return result

    def _postorder(self, node: _Node | None, result: list[str]) -> None:
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.data)

    def level_order(self) -> list[str]:
        result: list[str] = []
        if self._root is None:
            return result
        queue: deque[_Node] = deque([self._root])
        while queue:
            node = queue.popleft()
            result.append(node.data)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def swap_subtrees(self) -> None:
        """Swap all left and right subtrees recursively."""
        self._swap(self._root)

    def _swap(self, node: _Node | None) -> None:
        if node is None:
            return
        node.left, node.right = node.right, node.left
        self._swap(node.left)
        self._swap(node.right)


def main() -> None:
    seq = input("请输入扩展先序序列（如 ABD##E##CF###）：").strip()
    tree = BinaryTree.from_preorder(seq)

    print("交换前：")
    print(f"  先序: {' '.join(tree.preorder())}")
    print(f"  中序: {' '.join(tree.inorder())}")
    print(f"  后序: {' '.join(tree.postorder())}")
    print(f"  层序: {' '.join(tree.level_order())}")

    tree.swap_subtrees()

    print("交换后：")
    print(f"  先序: {' '.join(tree.preorder())}")
    print(f"  中序: {' '.join(tree.inorder())}")
    print(f"  后序: {' '.join(tree.postorder())}")
    print(f"  层序: {' '.join(tree.level_order())}")


if __name__ == "__main__":
    main()
