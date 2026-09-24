"""Experiment 10: polynomial derivative."""

__all__ = ["Polynomial"]


def __getattr__(name: str):
    if name == "Polynomial":
        from .main import Polynomial

        return Polynomial
    raise AttributeError(name)
