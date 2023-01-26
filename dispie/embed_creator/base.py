from __future__ import annotations

from typing import Optional, Any

from discord import ButtonStyle, CategoryChannel, Embed, ForumChannel, Interaction, StageChannel, TextChannel, SelectOption
from discord.ext.commands import Bot
from discord.ui import Select, select, Button, button, View
from dispie.embed_creator.methods import CreatorMethods
from dispie import ChannelSelectPrompt



__all__ = ("EmbedCreator",)


class EmbedCreator(View, CreatorMethods):
    """
    This class is a subclass of both `discord.ui.View` and `CreatorMethods`.
    It is intended to be used as a base class for creating a panel that allows users to create embeds in a specified Discord TextChannel.
    
    Parameters:
        bot (discord.Client or discord.ext.commands.Bot): An instance of the Discord bot that will be used to access client information such as avatar, name, and ID.
        embed (discord.Embed): An instance of the Discord Embed class that will be used as the main embed.
        timeout (float, optional): An optional argument that is passed to the parent View class. It is used to specify a timeout for the view in seconds.
    """

    def __init__(
        self,
        *,
        bot: Bot,
        embed: Embed,
        timeout: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(timeout=timeout)
        self.bot, self.embed, self.timeout, self._creator_methods = (
            bot,
            embed,
            timeout,
            CreatorMethods(embed),
        )
        self.options_data = [
            {
                "label": kwargs.get("author_label", "Edit Author"),
                "description": kwargs.get(
                    "author_description", "Edits the embed author name, icon."
                ),
                "emoji": kwargs.get("author_emoji", "🔸"),
                "value": "author",
            },
            {
                "label": kwargs.get(
                    "message_label", "Edit Message (title, description)"
                ),
                "description": kwargs.get(
                    "message_description", "Edits the embed title, description."
                ),
                "emoji": kwargs.get("message_emoji", "🔸"),
                "value": "message",
            },
            {
                "label": kwargs.get("thumbnail_label", "Edit Thumbnail"),
                "description": kwargs.get(
                    "thumbnail_description", "Edits the embed thumbnail url."
                ),
                "emoji": kwargs.get("thumbnail_emoji", "🔸"),
                "value": "thumbnail",
            },
            {
                "label": kwargs.get("image_label", "Edit Image"),
                "description": kwargs.get(
                    "image_description", "Edits the embed image url."
                ),
                "emoji": kwargs.get("image_emoji", "🔸"),
                "value": "image",
            },
            {
                "label": kwargs.get("footer_label", "Edit Footer"),
                "description": kwargs.get(
                    "footer_description", "Edits the embed footer text, icon url."
                ),
                "emoji": kwargs.get("footer_emoji", "🔸"),
                "value": "footer",
            },
            {
                "label": kwargs.get("color_label", "Edit Color"),
                "description": kwargs.get(
                    "color_description", "Edits the embed colour."
                ),
                "emoji": kwargs.get("color_emoji", "🔸"),
                "value": "color",
            },
            {
                "label": kwargs.get("addfield_label", "Add Field"),
                "description": kwargs.get(
                    "addfield_description", "Adds a field to the embed."
                ),
                "emoji": kwargs.get("addfield_emoji", "🔸"),
                "value": "addfield",
            },
            {
                "label": kwargs.get("removefield_label", "Remove Field"),
                "description": kwargs.get(
                    "removefield_description", "Removes a field from the embed."
                ),
                "emoji": kwargs.get("removefield_emoji", "🔸"),
                "value": "removefield",
            },
        ]
        
        self.children[0].options = [SelectOption(**option) for option in self.options_data]  # type: ignore
        self.children[1].label, self.children[1].emoji, self.children[1].style = kwargs.get("send_label", 'Send'), kwargs.get("send_emoji", None), kwargs.get("send_style", ButtonStyle.blurple) # type: ignore
        self.children[2].label, self.children[2].emoji, self.children[2].style = kwargs.get("cancel_label", 'Cancel'), kwargs.get("cancel_emoji", None), kwargs.get("cancel_style", ButtonStyle.red) # type: ignore
        
    
    async def update_embed(self, interaction: Interaction):
        """This function will update the whole embed and edit the message and view."""
        return await interaction.message.edit(embed=self.embed, view=self)  # type: ignore

    @select(placeholder="Edit a section")
    async def edit_select_callback(
        self, interaction: Interaction, select: Select
    ) -> None:
        """
        This method is a callback function for the `select` interaction.
        It is triggered when a user selects an option from the select menu. 
        The method uses the `callbacks` attribute of the `CreatorMethods` class to call the appropriate callback function based on the user's selection.

        Parameters:
            interaction (discord.Interaction): The interaction object representing the current interaction.
            select (discord.Select): The select object representing the select menu.

        """
        await self._creator_methods.callbacks[select.values[0]](interaction)
        await self.update_embed(interaction)

    @button()
    async def send_callback(self, interaction: Interaction, button: Button) -> None:
        """
        This method is a callback function for the `button` interaction. It is triggered when a user clicks on the "send" button. 
        The method creates a `ChannelSelectPrompt` object and sends it as an ephemeral message to the user. It then waits for the user to select a channel.
        If a channel is selected, the method sends the embed to the selected channel and deletes the original interaction message.

        Parameters:
            interaction (discord.Interaction): The interaction object representing the current interaction.
            button (discord.Button): The button object representing the "send" button.
        """
        prompt = ChannelSelectPrompt("Select a channel to send this embed...", True, 1)
        await interaction.response.send_message(view=prompt, ephemeral=True)
        await prompt.wait()
        if prompt.values:
            if not isinstance(prompt.values[0], (StageChannel, ForumChannel, CategoryChannel)):
                await prompt.values[0].send(embed=self.embed) # type: ignore
                await interaction.message.delete() # type: ignore


    @button()
    async def cancel_callback(self, interaction: Interaction, button: Button) -> None:
        """
        This method is a callback function for the `button` interaction. It is triggered when a user clicks on the "cancel" button. 
        The method deletes the original interaction message and stops the current interaction.

        Parameters:
            interaction (Interaction): The interaction object representing the current interaction.
            button (Button): The button object representing the "cancel" button.
        """
        await interaction.message.delete() # type: ignore
        self.stop()
