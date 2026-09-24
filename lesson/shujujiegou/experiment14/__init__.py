"""Experiment 14: array rotation."""

__all__ = ["rotate_array"]


def __getattr__(name: str):
    if name == "rotate_array":
        from .main import rotate_array

        return rotate_array
    raise AttributeError(name)
