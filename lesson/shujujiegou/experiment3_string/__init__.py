"""Experiment 3: KMP pattern matching."""

__all__ = ["kmp_search"]


def __getattr__(name: str):
    if name == "kmp_search":
        from .main import kmp_search

        return kmp_search
    raise AttributeError(name)
