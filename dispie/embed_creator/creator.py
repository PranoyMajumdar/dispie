from __future__ import annotations
from typing import TYPE_CHECKING, Any, Coroutine, Callable, Self


from discord import ButtonStyle, Colour, SelectOption, TextStyle
from discord.ui import button, select, TextInput
from discord.ext import commands
from dispie import View
from dispie.prompts.modal import ModalPrompt


from .embed import Embed
from .config import EmbedCreatorConfig

if TYPE_CHECKING:
    from discord import Member, User, Interaction
    from discord.ui import Select, Button

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
        embed: Embed = Embed(),
        config: EmbedCreatorConfig = EmbedCreatorConfig(),
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.embed = embed
        self.config = config
        self.embeds: list[Embed] = list()
        self._update_embeds_options()
        self._update_creator()

    def _update_embeds_options(self) -> None:
        options = [SelectOption(label=i.name) for i in self.embeds]
        self._embeds_select.options = options

    def _update_creator(self) -> None:
        self._embeds_select.placeholder = self.config.placeholder

        self._send_button.label = self.config.send_button_label
        self._send_button.style = self.config.send_button_style
        self._send_button.emoji = self.config.send_button_emoji

        self._add_embed_button.label = self.config.add_embed_button_label
        self._add_embed_button.style = self.config.add_embed_button_style
        self._add_embed_button.emoji = self.config.add_embed_button_emoji

    @property
    def total_embed(self) -> int:
        return len(self.embeds)

    def get_embed(self, name: str) -> Embed | None:
        return next((x for x in self.embeds if x.name == name), None)

    def add_embed(self, embed: Embed) -> Embed:
        self.embeds.append(embed)
        embed.name = f"Embed {self.total_embed}"
        return embed

    async def send(
        self,
        ctx: Interaction | commands.Context[Any],
        embed: Embed = Embed(),
    ):
        self.add_embed(embed)
        self._update_embeds_options()
        if isinstance(ctx, commands.Context):
            await ctx.send(embeds=self.embeds, view=self)
        else:
            await ctx.response.send_message(embeds=self.embeds, view=self)

    async def refresh_creator(self, interaction: Interaction):
        self._update_embeds_options()
        await interaction.edit_original_response(embeds=self.embeds, view=self)

    @select()
    async def _embeds_select(self, interaction: Interaction, select: Select[Any]):
        assert interaction.message is not None
        selected_embed = self.get_embed(select.values[0])
        if selected_embed:
            await interaction.response.defer()
            await interaction.edit_original_response(
                embed=selected_embed,
                view=EmbedEditor(self, embed=selected_embed, author=interaction.user),
            )

    @button()
    async def _send_button(self, interaction: Interaction, button: Button[Self]):
        ...

    @button()
    async def _add_embed_button(
        self, interaction: Interaction, button: Button[EmbedCreator]
    ):
        if self.total_embed == 10:
            return await interaction.response.send_message(
                self.config.messages.max_embed_error, ephemeral=True
            )
        self.add_embed(Embed())
        await interaction.response.defer()
        await self.refresh_creator(interaction)


class EmbedEditor(View):
    def __init__(
        self,
        embed_creator: EmbedCreator,
        embed: Embed,
        *,
        timeout: float | None = 180,
        auto_delete: bool = False,
        auto_disable: bool = False,
        author: User | Member | None = None,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.embed_creator = embed_creator
        self.config = embed_creator.config
        self._update_maker()
        self.callbacks: dict[str, Callable[[Interaction], Coroutine[Any, Any, Any]]] = {
            "body": self.edit_body,
        }
        self.embed = embed

    def _update_maker(self) -> None:
        self._back_button.label = self.config.maker.back_button_label
        self._back_button.style = self.config.maker.back_button_style

        self._back_button.emoji = self.config.maker.back_button_emoji

        self._embed_edit_menu.placeholder = self.config.maker.placeholder
        self._embed_edit_menu.options = [
            SelectOption(**i) for i in self.config.maker.options.get_list()
        ]

    async def refresh_maker(self, interaction: Interaction):
        await interaction.edit_original_response(embed=self.embed, view=self)

    @select()
    async def _embed_edit_menu(self, interaction: Interaction, select: Select[Any]):
        await self.callbacks[select.values[0]](interaction)

    @button()
    async def _back_button(self, interaction: Interaction, button: Button[Self]):
        await interaction.response.defer()
        await interaction.edit_original_response(
            embeds=self.embed_creator.embeds, view=self.embed_creator
        )

    async def edit_body(self, interaction: Interaction) -> Any:
        prompt = ModalPrompt(title=self.config.maker.modal.body_title)
        title = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.body_title_label,
                default=self.embed.title,
                required=False,
                placeholder=self.config.maker.modal.body_title_placeholder,
            )
        )
        description = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.body_description_label,
                default=self.embed.description,
                required=False,
                style=TextStyle.long,
                placeholder=self.config.maker.modal.body_description_placeholder,
            )
        )

        colour = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.body_colour_label,
                required=False,
                placeholder=self.config.maker.modal.body_colour_placeholder,
                default=str(self.embed.colour),
            )
        )

        await interaction.response.send_modal(prompt)
        await prompt.wait()

        try:
            colour_obj = Colour.from_str(str(colour))
        except ValueError:
            return await interaction.followup.send(
                self.config.messages.colour_convert_error, ephemeral=True
            )
        else:
            self.embed.title = str(title)
            self.embed.description = str(description)
            self.embed.colour = colour_obj
        finally:
            await self.refresh_maker(interaction)

    async def edit_author(self, interaction: Interaction) -> None:
        prompt = ModalPrompt(title=self.config.maker.modal.author_title)
        name = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.author_name_label,
                default=self.embed.author.name,
                required=False,
                placeholder=self.config.maker.modal.author_name_placeholder,
            )
        )
        url = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.author_url_label,
                default=self.embed.author.url,
                required=False,
                placeholder=self.config.maker.modal.author_url_placeholder,
            )
        )
        await interaction.response.send_modal(prompt)
        await prompt.wait()
        self.embed.set_author(name=name, icon_url=self.embed.author.icon_url, url=url)
        await self.refresh_maker(interaction)

    async def edit_message(self, interaction: Interaction) -> None:
        prompt = ModalPrompt(title=self.config.maker.modal.message_title)
        title = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.message_name_label,
                default=self.embed.title,
                required=False,
                placeholder=self.config.maker.modal.message_name_placeholder,
            )
        )
        description = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.message_description_label,
                default=self.embed.description,
                required=False,
                style=TextStyle.long,
                placeholder=self.config.maker.modal.message_description_placeholder,
            )
        )

        await interaction.response.send_modal(prompt)
        await prompt.wait()
        self.embed.title = str(title)
        self.embed.description = str(description)
        await self.refresh_maker(interaction)

    async def edit_colour(self, interaction: Interaction) -> None:
        prompt = ModalPrompt(title=self.config.maker.modal.colour_title)
        colour = prompt.add_input(
            TextInput(
                label=self.config.maker.modal.colour_label,
                required=False,
                placeholder=self.config.maker.modal.colour_placeholder,
            )
        )

        await interaction.response.send_modal(prompt)
        await prompt.wait()
        try:
            colour_obj = Colour.from_str(str(colour))
        except ValueError:
            return await interaction.followup.send(
                self.config.messages.colour_convert_error, ephemeral=True
            )

        else:
            self.embed.colour = colour_obj

        finally:
            await self.refresh_maker(interaction)

    async def edit_footer(self, interaction: Interaction) -> None:
        # Implement the edit_footer functionality here
        pass

    async def edit_icon(self, interaction: Interaction) -> None:
        # Implement the edit_footer functionality here
        pass

    async def edit_thumbnail(self, interaction: Interaction) -> None:
        # Implement the edit_thumbnail functionality here
        pass

    async def edit_image(self, interaction: Interaction) -> None:
        # Implement the edit_image functionality here
        pass

    async def add_field(self, interaction: Interaction) -> None:
        # Implement the add_field functionality here
        pass

    async def remove_field(self, interaction: Interaction) -> None:
        # Implement the remove_field functionality here
        pass
