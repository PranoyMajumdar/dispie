from __future__ import annotations

from typing import Any, Callable, Dict, List
from dispie import ModalInput
from discord import Interaction, Embed, InteractionMessage, TextStyle
from discord.ui import TextInput
from contextlib import suppress


class CreatorMethods:
    """
    This class contains all the methods for editing an embed. It is intended to be inherited by the main `EmbedCreator` class.

    Attributes:
        embed (discord.Embed): The embed object being edited.

    """

    def __init__(self, embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail
        }

    async def edit_author(self, interaction: Interaction) -> None:
        """This method edits the embed's author"""
        modal = ModalInput(title="Edit Embed Author")
        modal.add_item(
            TextInput(
                label="Author Name",
                max_length=100,
                default=self.embed.author.name,
                placeholder="Author name to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Icon Url",
                default=self.embed.author.icon_url,
                placeholder="Author icon to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Url",
                default=self.embed.author.url,
                placeholder="URL to set as the embed's author link",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_author(
            name=str(modal.children[0]),
            icon_url=str(modal.children[1]),
            url=str(modal.children[2]),
        )

    async def edit_message(self, interaction: Interaction) -> None:
        """This method edits the embed's message (discord.Embed.title and discord.Embed.description)"""
        modal = ModalInput(title="Edit Embed Message")
        modal.add_item(
            TextInput(
                label="Embed Title",
                max_length=255,
                default=self.embed.title,
                placeholder="Title to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Embed Description",
                default=self.embed.description,
                placeholder="Description to display in the embed",
                style=TextStyle.paragraph,
                required=False,
                max_length=2000,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.title, self.embed.description = str(modal.children[0]), str(
            modal.children[1]
        )


    async def edit_thumbnail(self, interaction: Interaction) -> None:
        """This method edits the embed's thumbnail"""
        modal = ModalInput(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Thumbnail Url",
                default=self.embed.title,
                placeholder="Thumbnail you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_thumbnail(url=str(modal.children[0]))


    