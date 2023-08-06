from typing import TypedDict


__all__ = ("Node", "MusicVariables")


class Node(TypedDict):
    host: str
    port: int
    password: str
    identifier: str


class MusicVariables:
    title: str = "{title}"
    thumbnail: str = "{thumbnail}"
