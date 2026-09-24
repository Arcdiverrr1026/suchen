"""Experiment 2: infix expression evaluation with stacks."""

__all__ = ["evaluate_infix"]


def __getattr__(name: str):
    if name == "evaluate_infix":
        from .main import evaluate_infix

        return evaluate_infix
    raise AttributeError(name)
