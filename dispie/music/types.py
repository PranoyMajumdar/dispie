from __future__ import annotations

from typing import TypedDict
from discord.ext.commands import Context
from discord import Interaction

__all__ = (
    "Node", "PlayerContext"
)


class Node(TypedDict):
    host: str
    port: int
    password: str
    identifier: str

class PlayerContext(Interaction, Context):
    pass