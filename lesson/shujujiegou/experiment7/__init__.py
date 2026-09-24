"""Experiment 7: mathematical problems."""

__all__ = ["sequence_sum", "print_diamond", "twin_primes", "perfect_square_quadruples"]


def __getattr__(name: str):
    from . import main
    obj = getattr(main, name, None)
    if obj is not None:
        return obj
    raise AttributeError(name)
