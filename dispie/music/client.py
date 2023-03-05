from __future__ import annotations

from discord import Client
from dispie.music.types import Node


__all__ = (
    "MusicClient",
)

class MusicClient:
    def __init__(self, bot: Client, nodes: list[Node]) -> None:
        self.bot = bot
        self.nodes = nodes

    


    