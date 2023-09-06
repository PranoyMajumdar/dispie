from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Sequence

from discord.ui import select
from dispie.prompts import ModalPrompt
from discord import Color, ButtonStyle, Forbidden, HTTPException, NotFound, SelectOption
from dispie import View
from contextlib import suppress

from dispie.prompts.select import TextSelectPrompt

if TYPE_CHECKING:
    from discord import Interaction, User, Member, Embed
    from .creator import EmbedCreator
    from discord.ui.item import V
    from discord.ui import Select


__all__: Sequence[str] = ("CreatorMethods",)


class FieldSelect(View):
    def __init__(
        self,
        embed: Embed,
        author: User | Member,
        creator: EmbedCreator,
        interaction: Interaction,
        *,
        timeout: float | None = 180,
        auto_delete: bool = False,
        auto_disable: bool = False,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.index: int | None = None
        self.creator = creator
        self.embed = creator.embed
        self.interaction = interaction
        self.modals = creator.config.modals
        self.prompts = creator.config.prompts
        self._init_select()

    def _init_select(self):
        for count, field in enumerate(self.embed.fields, start=1):
            self.select_fields.add_option(
                label=f"{count} {field.name[:20] if field.name else self.prompts.edit_field.default_field_name}",
                value=str(count - 1),
            )
        self.select_fields.placeholder = self.prompts.edit_field.placeholder

    @select()
    async def select_fields(self, interaction: Interaction, select: Select[V]) -> Any:
        assert interaction.message is not None
        with suppress(Forbidden, NotFound, HTTPException):
            await interaction.message.delete()

        field = self.embed.fields[int(select.values[0])]
        modal = ModalPrompt(title=self.modals.edit_field)

        name, value, inline = (
            modal.add_input(self.modals.edit_field_name.value(field.name)),
            modal.add_input(self.modals.edit_field_value.value(field.value)),
            modal.add_input(self.modals.edit_field_inline.value(str(field.inline))),
        )

        await interaction.response.send_modal(modal)
        await modal.wait()

        convert_to_bool: Callable[[str], bool] = (
            lambda value: True if value.lower() == "true" else False
        )
        self.embed.remove_field(int(select.values[0]))
        self.embed.insert_field_at(
            int(select.values[0]),
            name=name,
            value=value,
            inline=convert_to_bool(str(inline)),
        )
        await self.creator.refresh_creator(self.interaction)


class CreatorMethods:
    def __init__(self, creator: EmbedCreator) -> None:
        self.creator = creator
        self.buttons = creator.config.buttons
        self.selects = creator.config.selects
        self.modals = creator.config.modals
        self.errors = creator.config.errors
        self.prompts = creator.config.prompts
        self.embed = creator.embed

    async def _send_modal(self, interaction: Interaction, modal: ModalPrompt) -> None:
        await interaction.response.send_modal(modal)
        await modal.wait()

    async def edit_message(self, interaction: Interaction) -> Any:
        assert (
            interaction.message is not None
        )  # We know that message component always have a message
        modal = ModalPrompt(title=self.modals.message)
        content = modal.add_input(
            self.modals.message_content.value(
                default=interaction.message.content, required=False
            )
        )
        await self._send_modal(interaction, modal)
        self.creator.content = str(content)
        await self.creator.refresh_creator(interaction)

    async def edit_author(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals.author)
        name, icon_url, url = (
            modal.add_input(
                self.modals.author_name.value(self.embed.author.name, required=False)
            ),
            modal.add_input(
                self.modals.author_icon_url.value(self.embed.author.icon_url)
            ),
            modal.add_input(self.modals.author_url.value(self.embed.author.url)),
        )
        await self._send_modal(interaction, modal)

        self.embed.set_author(name=name, url=url, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def edit_body(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals.body)
        title, description, color, url = (
            modal.add_input(self.modals.body_title.value(self.embed.title)),
            modal.add_input(self.modals.body_description.value(self.embed.description)),
            modal.add_input(self.modals.body_color.value(str(self.embed.color or ""))),
            modal.add_input(self.modals.body_url.value(self.embed.url)),
        )
        await self._send_modal(interaction, modal)

        self.embed.title, self.embed.description, self.embed.url = (
            str(title),
            str(description),
            str(url),
        )

        color_str = str(color)
        if color_str:
            try:
                self.embed.color = Color.from_str(color_str)
            except:
                await interaction.followup.send(
                    self.errors.color_conversion_error, ephemeral=True
                )

        await self.creator.refresh_creator(interaction)

    async def edit_images(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals.images)
        image, thumbnail = (
            modal.add_input(
                self.modals.images_image.value(
                    default=self.embed.image.url, required=False
                )
            ),
            modal.add_input(
                self.modals.images_thumbnail.value(
                    default=self.embed.thumbnail.url, required=False
                )
            ),
        )
        await self._send_modal(interaction, modal)

        self.embed.set_image(url=image).set_thumbnail(url=thumbnail)
        await self.creator.refresh_creator(interaction)

    async def edit_footer(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.modals.footer)
        text, icon_url = (
            modal.add_input(
                self.modals.footer_text.value(
                    default=self.embed.footer.text, required=False
                )
            ),
            modal.add_input(
                self.modals.footer_icon_url.value(
                    default=self.embed.footer.icon_url, required=False
                )
            ),
        )
        await self._send_modal(interaction, modal)

        self.embed.set_footer(text=text, icon_url=icon_url)
        await self.creator.refresh_creator(interaction)

    async def add_field(self, interaction: Interaction) -> Any:
        if len(self.embed.fields) == 25:
            return await interaction.response.send_message(
                self.errors.max_fields_reached_error, ephemeral=True
            )

        modal = ModalPrompt(title=self.modals.addfield)

        name, value, inline = (
            modal.add_input(self.modals.addfield_name.value()),
            modal.add_input(self.modals.addfield_value.value()),
            modal.add_input(self.modals.addfield_inline.value(default="False")),
        )
        await self._send_modal(interaction, modal)

        convert_to_bool: Callable[[str], bool] = (
            lambda value: True if value.lower() == "true" else False
        )
        self.embed.add_field(
            name=name, value=value, inline=convert_to_bool(str(inline))
        )
        await self.creator.refresh_creator(interaction)

    async def remove_field(self, interaction: Interaction) -> Any:
        select = TextSelectPrompt(
            author=interaction.user,
            options=[
                SelectOption(
                    label=f"{count} {field.name[:20] if field.name else self.prompts.remove_field.default_field_name}",
                    value=str(count - 1),
                )
                for count, field in enumerate(self.embed.fields, start=1)
            ],
        )

        await interaction.response.send_message(
            content=self.prompts.remove_field.message_content, view=select
        )
        await select.wait()
        if select.values:
            self.embed.remove_field(int(select.values[0]))
        await self.creator.refresh_creator(interaction)

    async def edit_field(self, interaction: Interaction) -> Any:
        select = FieldSelect(
            embed=self.embed,
            author=interaction.user,
            creator=self.creator,
            interaction=interaction,
        )
        await interaction.response.send_message(
            content=self.prompts.edit_field.message_content, view=select
        )
