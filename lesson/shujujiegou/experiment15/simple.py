"""Simple version: binary tree construction, traversal, and subtree swap."""

from collections import deque

class Node:
    def __init__(self, data=""):
        self.data = data
        self.left = None
        self.right = None

def build(seq, idx):
    if idx >= len(seq) or seq[idx] == "#":
        return None, idx + 1
    node = Node(seq[idx])
    node.left, idx = build(seq, idx + 1)
    node.right, idx = build(seq, idx)
    return node, idx

def preorder(node, r):
    if not node: return
    r.append(node.data)
    preorder(node.left, r)
    preorder(node.right, r)

def inorder(node, r):
    if not node: return
    inorder(node.left, r)
    r.append(node.data)
    inorder(node.right, r)

def postorder(node, r):
    if not node: return
    postorder(node.left, r)
    postorder(node.right, r)
    r.append(node.data)

def level_order(root):
    if not root: return []
    q = deque([root])
    r = []
    while q:
        n = q.popleft()
        r.append(n.data)
        if n.left: q.append(n.left)
        if n.right: q.append(n.right)
    return r

def swap(node):
    if not node: return
    node.left, node.right = node.right, node.left
    swap(node.left)
    swap(node.right)

seq = input("请输入扩展先序序列：").strip()
root, _ = build(seq, 0)

for label in ["交换前", "交换后"]:
    print(f"{label}：")
    r = []; preorder(root, r); print(f"  先序: {' '.join(r)}")
    r = []; inorder(root, r); print(f"  中序: {' '.join(r)}")
    r = []; postorder(root, r); print(f"  后序: {' '.join(r)}")
    print(f"  层序: {' '.join(level_order(root))}")
    if label == "交换前":
        swap(root)
