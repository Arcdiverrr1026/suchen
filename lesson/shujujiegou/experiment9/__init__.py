"""Experiment 9: linked list linear list."""

__all__ = ["LinkedList"]


def __getattr__(name: str):
    if name == "LinkedList":
        from .main import LinkedList

        return LinkedList
    raise AttributeError(name)
