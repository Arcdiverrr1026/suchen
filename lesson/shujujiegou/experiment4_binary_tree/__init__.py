"""Experiment 4: binary tree operations."""

__all__ = ["BinaryTree", "TreeNode"]


def __getattr__(name: str):
    if name in __all__:
        from .main import BinaryTree, TreeNode

        return {"BinaryTree": BinaryTree, "TreeNode": TreeNode}[name]
    raise AttributeError(name)
