"""Experiment 15: binary tree."""

__all__ = ["BinaryTree"]


def __getattr__(name: str):
    if name == "BinaryTree":
        from .main import BinaryTree

        return BinaryTree
    raise AttributeError(name)
