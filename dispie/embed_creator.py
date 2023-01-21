from __future__ import annotations

from typing import List, Optional, Any, Union

from discord import Embed, Interaction, TextChannel, SelectOption
from discord.ext.commands import Bot
from discord.ui import Select, select, Button, button, View
from dispie import ModalInput

__all__ = ("EmbedCreator",)


class EmbedCreator(View):
    """
    This class inherits from the View class in discord.py.
    This class is meant to be used as a base class for creating a panel that allows users to create embeds in a specified Discord TextChannel.
    The class takes in 3 required arguments:

    channel: A TextChannel instance where the embeds will be created.
    bot: A discord.Client or discord.ext.commands.Bot instance that will be used to get some details of the client like (avatar, name, id).
    embed: A discord.Embed instance that will be used as a main embed.
    timeout: An optional argument that is passed to the parent View class. It is used to specify a timeout for the view in seconds.
    """

    def __init__(
        self,
        *,
        channel: TextChannel,
        bot: Bot,
        embed: Embed,
        timeout: Optional[float] = None,
    ) -> None:
        super().__init__(timeout=timeout)
        self.channel, self.bot, self.embed, self.timeout = channel, bot, embed, timeout

        self.children[1].options = [  # type: ignore
            SelectOption(
                label="Edit Author",
                description="Edits the embed author name, icon.",
                emoji="❓",
                value="author",
            ),
            SelectOption(
                label="Edit Message (title, description)",
                description="Edits the embed title, description.",
                emoji="❓",
                value="message",
            ),
            SelectOption(
                label="Edit Thumbnail",
                description="Edits the embed thumbnail url.",
                emoji="❓",
                value="thumbnail",
            ),
            SelectOption(
                label="Edit Image",
                description="Edits the embed image url.",
                emoji="❓",
                value="image",
            ),
            SelectOption(
                label="Edit Footer",
                description="Edits the embed footer text, icon url.",
                emoji="❓",
                value="footer",
            ),
            SelectOption(
                label="Edit Color",
                description="Edits the embed colour.",
                emoji="❓",
                value="color",
            ),
            SelectOption(
                label="Add Field",
                description="Edits the embed colour.",
                emoji="❓",
                value="addfield",
            ),
            SelectOption(
                label="Remove Field",
                description="Edits the embed colour.",
                emoji="❓",
                value="removefield",
            ),
        ]


    @select(placeholder="Edit a section")
    async def edit_select_callback(self, interaction: Interaction, select: Select) -> None:
        ...

    @button(label="Send", emoji="✅")
    async def send_callback(self, interaction: Interaction, button: Button) -> None:
        ...

    @button(label="Cancel", emoji="❎")
    async def cancel_callback(self, interaction: Interaction, button: Button) -> None:
        ...
