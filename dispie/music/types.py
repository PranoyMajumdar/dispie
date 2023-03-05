from __future__ import annotations

from typing import TypedDict

__all__ = (
    "Node",
)


class Node(TypedDict):
    host: str
    port: int
    password: str
    identifier: str