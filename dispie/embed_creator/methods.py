from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Sequence

from dispie.prompts import ModalPrompt
from discord import Color

if TYPE_CHECKING:
    from discord import Interaction
    from .creator import EmbedCreator


__all__: Sequence[str] = ("CreatorMethods",)


class CreatorMethods:
    def __init__(self, creator: EmbedCreator) -> None:
        self.creator = creator
        self.buttons_config = creator.config.buttons
        self.selects_config = creator.config.selects
        self.modals_config = creator.config.modals
        self.error_messages = creator.config.errors

    async def edit_message(self, interaction: Interaction) -> Any:
        assert (
            interaction.message is not None
        )  # We know that message component always have a message
        modal = ModalPrompt(title=self.modals_config.message)
        content = modal.add_input(
            self.modals_config.message_content.value(
                default=interaction.message.content, required=False
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.creator.content = str(content)
        await self.creator.refresh_creator(interaction)

    async def edit_author(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals_config.author)
        name, icon_url, url = (
            modal.add_input(
                self.modals_config.author_name.value(
                    self.creator.embed.author.name, required=False
                )
            ),
            modal.add_input(
                self.modals_config.author_icon_url.value(
                    self.creator.embed.author.icon_url
                )
            ),
            modal.add_input(
                self.modals_config.author_url.value(self.creator.embed.author.url)
            ),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.set_author(name=name, url=url, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def edit_body(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals_config.body)
        title, description, color, url = (
            modal.add_input(
                self.modals_config.body_title.value(self.creator.embed.title)
            ),
            modal.add_input(
                self.modals_config.body_description.value(
                    self.creator.embed.description
                )
            ),
            modal.add_input(self.modals_config.body_color.value(required=False)),
            modal.add_input(self.modals_config.body_url.value(self.creator.embed.url)),
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
                await interaction.followup.send(
                    self.error_messages.color_conversion_error, ephemeral=True
                )
            else:
                self.creator.embed.color = color_obj

        await self.creator.refresh_creator(interaction)

    async def edit_images(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals_config.images)
        image, thumbnail = (
            modal.add_input(
                self.modals_config.images_image.value(
                    default=self.creator.embed.image.url, required=False
                )
            ),
            modal.add_input(
                self.modals_config.images_thumbnail.value(
                    default=self.creator.embed.thumbnail.url, required=False
                )
            ),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.set_image(url=image).set_thumbnail(url=thumbnail)
        await self.creator.refresh_creator(interaction)

    async def edit_footer(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals_config.footer)
        text, icon_url = (
            modal.add_input(
                self.modals_config.footer_text.value(
                    default=self.creator.embed.footer.text, required=False
                )
            ),
            modal.add_input(
                self.modals_config.footer_icon_url.value(
                    default=self.creator.embed.footer.icon_url, required=False
                )
            ),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()

        self.creator.embed.set_footer(text=text, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def add_field(self, interaction: Interaction) -> Any:
        if len(self.creator.embed.fields) == 25:
            return await interaction.response.send_message(
                self.error_messages.max_fields_reached_error, ephemeral=True
            )
        modal = ModalPrompt(title=self.modals_config.addfield)
        name, value, inline = (
            modal.add_input(self.modals_config.addfield_name.value()),
            modal.add_input(self.modals_config.addfield_value.value()),
            modal.add_input(self.modals_config.addfield_inline.value()),
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        convert_to_bool: Callable[[str], bool] = (
            lambda value: True if value.lower() == "true" else False
        )
        self.creator.embed.add_field(
            name=name, value=value, inline=convert_to_bool(str(inline))
        )
        await self.creator.refresh_creator(interaction)

    async def remove_field(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)

    async def edit_field(self, interaction: Interaction) -> Any:
        await interaction.response.send_message("Wow!", ephemeral=True)
