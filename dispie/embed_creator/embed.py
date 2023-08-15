from __future__ import annotations

from typing import TYPE_CHECKING, Any
from discord import Embed as OriginalEmbed

if TYPE_CHECKING:
    from discord import Colour
    from discord.types.embed import EmbedType
    from datetime import datetime


__all__ = ("Embed",)


class Embed(OriginalEmbed):
    def __init__(
        self,
        *,
        colour: int | Colour | None = None,
        color: int | Colour | None = None,
        title: Any | None = None,
        type: EmbedType = "rich",
        url: Any | None = None,
        description: Any | None = "\u200B",
        timestamp: datetime | None = None,
    ):
        super().__init__(
            colour=colour,
            color=color,
            title=title,
            type=type,
            url=url,
            description=description,
            timestamp=timestamp,
        )
        self._name: str

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> str:
        self._name = new_name
        return self.name
