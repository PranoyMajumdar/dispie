from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine

from discord.utils import MISSING

from dispie import View
from dispie.prompts import ModalPrompt, TextSelectPrompt
from discord import ButtonStyle, Color, Embed, SelectOption, ui
from discord.ext import commands
from .config import BaseConfig

if TYPE_CHECKING:
    from discord import User, Member, Interaction, WebhookMessage, Message
    from typing_extensions import Self


__all__ = ("EmbedCreator",)


class EmbedCreator(View):
    def __init__(
        self,
        *,
        timeout: float | None = 180,
        auto_delete: bool = False,
        auto_disable: bool = False,
        author: User | Member | None = None,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        config: BaseConfig = BaseConfig(),
        embed: Embed | None = None,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.config = config
        self.embed = embed or Embed(description="Edit this embed.").add_field(
            name="1", value="1"
        ).add_field(name="2", value="2").add_field(name="3", value="3")
        self._update_options()
        self.edit_callbacks: dict[
            str, Callable[[Interaction], Coroutine[Any, Any, Any]]
        ] = {
            "content": self.edit_content,
            "body": self.edit_body,
            "images": self.edit_images,
            "misc": self.edit_misc,
            "add_field": self.add_field,
            "remove_field": self.remove_field,
            "rearrange_fields": self.rearrange_fields,
            "edit_field": self.edit_field,
        }
        self.action_callbacks: dict[
            str, Callable[[Interaction], Coroutine[Any, Any, Any]]
        ] = {}
        self.content: str | None = MISSING

    def _update_options(self) -> None:
        self._set_select_options(
            self._embed_edit_select,
            self.config.edit_options.get_list(self.embed),
            self.config.edit_select_placeholder,
        )

        self._set_select_options(
            self._embed_actions_select,
            self.config.action_options.get_list(),
            self.config.action_select_placeholder,
        )

    def _set_select_options(
        self, select: ui.Select[Any], options: list[dict[str, Any]], placeholder: str
    ) -> None:
        select.placeholder = placeholder
        select.options = [SelectOption(**x) for x in options]

    async def start(
        self,
        ctx: commands.Context[Any] | Interaction,
        content: str = "Interact with the menus to edit the embed.",
    ) -> Self:
        self.message = await self._send_message(ctx, content)
        return self

    async def _send_message(
        self, ctx: commands.Context[Any] | Interaction, content: str
    ) -> Message | WebhookMessage | None:
        if isinstance(ctx, commands.Context):
            return await ctx.send(content=content, embed=self.embed, view=self)

        if not ctx.response.is_done():
            await ctx.response.defer()
        return await ctx.followup.send(content=content, embed=self.embed, view=self)

    async def refresh_creator(self, interaction: Interaction) -> Any:
        assert interaction.message is not None
        self._update_options()
        await interaction.message.edit(
            content=self.content, embed=self.embed, view=self
        )

    async def edit_content(self, interaction: Interaction) -> Any:
        assert interaction.message is not None
        modal = ModalPrompt(title=self.config.modals.content_title)
        content = modal.add_input(
            ui.TextInput(
                **self.config.modals.content_field.get_kwargs(
                    interaction.message.content
                )
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.content = str(content)
        await self.refresh_creator(interaction)

    async def edit_body(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.config.modals.body_title)
        title, description, color = (
            modal.add_input(
                ui.TextInput(
                    **self.config.modals.body_title_field.get_kwargs(self.embed.title)
                )
            ),
            modal.add_input(
                ui.TextInput(
                    **self.config.modals.body_description_field.get_kwargs(
                        self.embed.description
                    )
                )
            ),
            modal.add_input(
                ui.TextInput(
                    **self.config.modals.body_color_field.get_kwargs(
                        str(self.embed.color) if self.embed.color is not None else None
                    )
                )
            ),
        )

        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.title = str(title)
        self.embed.description = str(description)
        if (color := str(color)) != "":
            try:
                color = Color.from_str(color)
            except ValueError:
                await interaction.followup.send(
                    content=self.config.messages.color_convert_error, ephemeral=True
                )

            else:
                self.embed.color = color

        return await self.refresh_creator(interaction)

    async def edit_images(self, interaction: Interaction) -> Any:
        ...

    async def edit_misc(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.config.modals.misc_title)
        author_name, author_icon = modal.add_input(
            ui.TextInput(
                **self.config.modals.misc_author_name_field.get_kwargs(
                    self.embed.author.name
                )
            )
        ), modal.add_input(
            ui.TextInput(
                **self.config.modals.misc_author_icon_field.get_kwargs(
                    self.embed.author.icon_url
                )
            )
        )

        footer_text, footer_icon = modal.add_input(
            ui.TextInput(
                **self.config.modals.misc_footer_text_field.get_kwargs(
                    self.embed.footer.text
                )
            )
        ), modal.add_input(
            ui.TextInput(
                **self.config.modals.misc_footer_icon_field.get_kwargs(
                    self.embed.footer.icon_url
                )
            )
        )

        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_author(
            name=str(author_name), icon_url=str(author_icon)
        ).set_footer(text=str(footer_text), icon_url=str(footer_icon))

        return await self.refresh_creator(interaction)

    async def add_field(self, interaction: Interaction) -> Any:
        modal = ModalPrompt(title=self.config.modals.add_field_title)
        name, value, inline = (
            modal.add_input(
                ui.TextInput(**self.config.modals.add_field_name_field.get_kwargs())
            ),
            modal.add_input(
                ui.TextInput(**self.config.modals.add_field_value_field.get_kwargs())
            ),
            modal.add_input(
                ui.TextInput(**self.config.modals.add_field_inline_field.get_kwargs())
            ),
        )

        await interaction.response.send_modal(modal)
        await modal.wait()
        inline_bool: bool = True if str(inline).lower() == "true" else False

        self.embed.add_field(name=name, value=value, inline=inline_bool)
        return await self.refresh_creator(interaction)

    async def remove_field(self, interaction: Interaction) -> Any:
        select = TextSelectPrompt(
            interaction.user,
            [
                SelectOption(
                    label=x.name if isinstance(x.name, str) else f"Field {no}",
                    description=self.config.prompts.remove_field_description,
                    emoji=self.config.prompts.remove_field_emoji,
                    value=str(no),
                )
                for no, x in enumerate(self.embed.fields)
            ],
            auto_delete=True,
            timeout=60,
        )
        await interaction.response.send_message(
            content=self.config.prompts.remove_field_content, view=select
        )
        await select.wait()
        if select.values == None:
            return await self.refresh_creator(interaction)

        self.embed.remove_field(int(select.values[0]))
        return await self.refresh_creator(interaction)



        

    async def edit_field(self, interaction: Interaction) -> Any:
        ...

    @ui.select()
    async def _embed_edit_select(
        self, interaction: Interaction, select: ui.Select[Any]
    ) -> Any:
        await self.refresh_creator(interaction)
        return await self.edit_callbacks[select.values[0]](interaction)

    @ui.select()
    async def _embed_actions_select(
        self, interaction: Interaction, select: ui.Select[Any]
    ) -> Any:
        await self.refresh_creator(interaction)
        return await self.action_callbacks[select.values[0]](interaction)
