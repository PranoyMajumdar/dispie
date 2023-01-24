from __future__ import annotations

from typing import List, Optional, Any, Union

from discord import Embed, Interaction, InteractionMessage, TextChannel, SelectOption
from discord.ext.commands import Bot
from discord.ui import Select, select, Button, button, View
from contextlib import suppress
from dispie.embed_creator.methods import CreatorMethods

__all__ = ("EmbedCreator",)

# options = [
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Section",
#         'description': "Edit the main text of the embed",
#         'value': "default",
#         'default': True,
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Author",
#         'description': "Edit embed author name and icon",
#         'value': "author",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Title & Description",
#         'description': "Edit embed title and description",
#         'value': "message",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Thumbnail",
#         'description': "Edit embed thumbnail",
#         'value': "thumbnail",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Image",
#         'description': "Edit embed image",
#         'value': "image",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Footer",
#         'description': "Edit embed footer text and icon",
#         'value': "footer",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Colour",
#         'description': "Edit embed colour",
#         'value': "colour",
#     },
#     # field options
#     {
#         'emoji': custom_emojis.get("plus"),
#         'label': "Add Field",
#         'description': "Add a new field",
#         'value': "field",
#     },
#     {
#         'emoji': custom_emojis.get("edit"),
#         'label': "Edit Field",
#         'description': "Edit a field",
#         'value': "editfield",
#     },
#     {
#         'emoji': custom_emojis.get("minus"),
#         'label': "Remove Field",
#         'description': "Remove a field",
#         'value': "removefield",
#     },
# ]


class EmbedCreator(View, CreatorMethods):
    """
    This class inherits from the `discord.ui.View` class and `CreatorMethods`.
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
        self.channel, self.bot, self.embed, self.timeout, self._creator_methods = (
            channel,
            bot,
            embed,
            timeout,
            CreatorMethods(embed),
        )

        self.children[0].options = [  # type: ignore
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

    async def update_embed(self, interaction: Interaction):
        """This function will update the whole embed and edit the message and view."""
        if isinstance(interaction.message, InteractionMessage):
            return await interaction.message.edit(embed=self.embed, view=self)
        

        # If interaction.message = None
        await interaction.edit_original_response(embed=self.embed, view=self)

    @select(placeholder="Edit a section")
    async def edit_select_callback(
        self, interaction: Interaction, select: Select
    ) -> None:

        await self._creator_methods.callbacks[select.values[0]](interaction)
        await self.update_embed(interaction)

    @button(label="Send", emoji="✅")
    async def send_callback(self, interaction: Interaction, button: Button) -> None:
        ...

    @button(label="Cancel", emoji="❎")
    async def cancel_callback(self, interaction: Interaction, button: Button) -> None:
        ...
