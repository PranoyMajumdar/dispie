from __future__ import annotations

import pomice

from discord import Message, Interaction, Member
from discord.ext.commands import Context

__all__ = (
    "MusicPlayer"
)


class MusicPlayer(pomice.Player):
    """Custom pomice Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = pomice.Queue()
        self.controller: Message | None = None
        self.context: Context | Interaction | None = None
        self.dj: Member | None = None

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def set_context(self, context: Context | Interaction) -> None:
        "Sets context for the player"
        self.context = context
        self.dj = context.author if isinstance(
            context, Context) else context.user
