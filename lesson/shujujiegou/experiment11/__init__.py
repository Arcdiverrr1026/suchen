"""Experiment 11: expression evaluation."""

__all__ = ["eval_postfix", "eval_infix"]


def __getattr__(name: str):
    from . import main
    obj = getattr(main, name, None)
    if obj is not None:
        return obj
    raise AttributeError(name)
