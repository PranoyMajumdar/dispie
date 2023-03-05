from __future__ import annotations

import pomice
import math


from discord import VoiceProtocol
from discord import Message, Member, Interaction
from discord.ext.commands import Context
from typing_extensions import Self


__all__ = (
    "MusicPlayer",
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
        "Sets context for the player."
        self.context = context
        self.dj = context.author if isinstance(
            context, Context) else context.user

    async def get_vc_player(self) -> VoiceProtocol:
        "Returns the guild's voice client."
        if isinstance(self.context, Context):
            return self.context.voice_client

        return self.context.guild.voice_client

    async def required(self, context: Context | Interaction) -> int:
        """Method which returns required votes based on amount of members in a channel."""
        player: Self = self.get_vc_player(context)
        channel = self.bot.get_channel(int(player.channel.id))
        return math.ceil((len(channel.members) - 1) / 2.5)

