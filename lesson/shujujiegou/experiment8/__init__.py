"""Experiment 8: sequence and approximation problems."""

__all__ = ["exponential_sequence", "factorial_approximation", "nested_sequence_value", "rainfall_analysis"]


def __getattr__(name: str):
    from . import main
    obj = getattr(main, name, None)
    if obj is not None:
        return obj
    raise AttributeError(name)
