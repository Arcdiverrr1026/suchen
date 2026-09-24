"""Simple version: binary tree operations."""

from collections import deque


class Node:
    def __init__(self, value: str) -> None:
        self.value = value
        self.left = None
        self.right = None


def build_tree(sequence: str) -> Node | None:
    global index

    if index >= len(sequence):
        return None

    value = sequence[index]
    index += 1

    if value == "#":
        return None

    node = Node(value)
    node.left = build_tree(sequence)
    node.right = build_tree(sequence)
    return node


def preorder(root: Node | None) -> list[str]:
    if root is None:
        return []
    return [root.value] + preorder(root.left) + preorder(root.right)


def inorder(root: Node | None) -> list[str]:
    if root is None:
        return []
    return inorder(root.left) + [root.value] + inorder(root.right)


def postorder(root: Node | None) -> list[str]:
    if root is None:
        return []
    return postorder(root.left) + postorder(root.right) + [root.value]


def level_order(root: Node | None) -> list[str]:
    if root is None:
        return []

    answer = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        answer.append(node.value)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return answer


def height(root: Node | None) -> int:
    if root is None:
        return 0
    return max(height(root.left), height(root.right)) + 1


def count_degree(root: Node | None, counts: list[int]) -> None:
    if root is None:
        return

    degree = 0
    if root.left:
        degree += 1
    if root.right:
        degree += 1

    counts[degree] += 1
    count_degree(root.left, counts)
    count_degree(root.right, counts)


sequence = input().strip()
index = 0
tree = build_tree(sequence)
counts = [0, 0, 0]
count_degree(tree, counts)

print("preorder:", " ".join(preorder(tree)))
print("inorder:", " ".join(inorder(tree)))
print("postorder:", " ".join(postorder(tree)))
print("level_order:", " ".join(level_order(tree)))
print("height:", height(tree))
print("degree_0:", counts[0])
print("degree_1:", counts[1])
print("degree_2:", counts[2])
