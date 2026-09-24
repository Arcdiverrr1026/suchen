"""Experiment 6: sequential storage linear list."""

__all__ = ["SeqList"]


def __getattr__(name: str):
    if name == "SeqList":
        from .main import SeqList

        return SeqList
    raise AttributeError(name)
