import pomice
import math

from discord import Message, Member, Interaction


__all__ = ("MusicPlayer",)


class MusicPlayer(pomice.Player):
    """Custom pomice Player class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = pomice.Queue()
        self.controller: Message | None = None
        self.context: Interaction | None = None
        self.dj: Member | None = None

        self.pause_votes = set()
        self.resume_votes = set()
        self.skip_votes = set()
        self.shuffle_votes = set()
        self.stop_votes = set()

    async def set_context(self, context: Interaction) -> None:
        "Sets context for the player."
        self.context = context

    async def required(self, context: Interaction) -> int:
        """Method which returns required votes based on amount of members in a channel."""
        assert context.guild is not None
        player: pomice.Player = context.guild.voice_client
        required = math.ceil((len(player.channel.members) - 1) / 2.5)
        return required
