"""Experiment 13: stack and queue applications."""

__all__ = ["is_english_palindrome", "card_game"]


def __getattr__(name: str):
    from . import main
    obj = getattr(main, name, None)
    if obj is not None:
        return obj
    raise AttributeError(name)
