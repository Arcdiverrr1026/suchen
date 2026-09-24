"""Experiment 5: social network graph."""

__all__ = ["SocialNetwork"]


def __getattr__(name: str):
    if name == "SocialNetwork":
        from .main import SocialNetwork

        return SocialNetwork
    raise AttributeError(name)
