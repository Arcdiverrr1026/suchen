"""Experiment 1: long integer addition with linear lists."""

__all__ = ["add_long_integers"]


def __getattr__(name: str):
    if name == "add_long_integers":
        from .main import add_long_integers

        return add_long_integers
    raise AttributeError(name)
