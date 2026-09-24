"""Experiment 12: array problems."""

__all__ = ["nearest_and_farthest", "digit_rearrange"]


def __getattr__(name: str):
    from . import main
    obj = getattr(main, name, None)
    if obj is not None:
        return obj
    raise AttributeError(name)
