from __future__ import annotations
from typing import TYPE_CHECKING, Any, Sequence

from dispie.prompts import ModalPrompt
from discord import Color, ui

if TYPE_CHECKING:
    from discord import Interaction
    from .creator import EmbedCreator


__all__: Sequence[str] = ("CreatorMethods",)


class CreatorMethods:
    def __init__(self, creator: EmbedCreator) -> None:
        self.creator = creator
        self.config = creator.config

    async def edit_message(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title="Edit Embed Message")
        content = modal.add_input(ui.TextInput(label="Content"))
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.creator.content = str(content)
        await self.creator.refresh_creator(interaction)

    async def edit_author(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title="Edit Embed Author")
        name, icon_url, url = (
            modal.add_input(ui.TextInput(label="Name")),
            modal.add_input(ui.TextInput(label="Icon Url", required=False)),
            modal.add_input(ui.TextInput(label="Author Url", required=False)),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.set_author(name=name, url=url, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def edit_footer(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title="Edit")
        text, icon_url = (
            modal.add_input(ui.TextInput(label="Text")),
            modal.add_input(ui.TextInput(label="Icon Url", required=False)),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.set_footer(text=text, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def edit_body(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title="Edit")
        title, description, color, url = (
            modal.add_input(ui.TextInput(label="Title", required=False)),
            modal.add_input(ui.TextInput(label="Description", required=False)),
            modal.add_input(ui.TextInput(label="Color", required=False)),
            modal.add_input(ui.TextInput(label="Url", required=False)),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.title = str(title)
        self.creator.embed.description = str(description)
        self.creator.embed.url = str(url)
        await self.creator.refresh_creator(interaction)

        if str(color) != "":
            try:
                color_obj = Color.from_str(str(color))
            except:
                await interaction.followup.send("The string could not be converted into a colour.", ephemeral=True)
            else:
                self.creator.embed.color = color_obj
        
        await self.creator.refresh_creator(interaction)

    async def edit_images(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)

    async def add_field(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)

    async def remove_field(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)

    async def edit_field(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)
