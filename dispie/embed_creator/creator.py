from __future__ import annotations
from typing import TYPE_CHECKING, Any, Coroutine, Callable, Self
from discord import ButtonStyle, SelectOption
from discord.ext import commands
from discord.ui import button, select
from dispie import View
from .embed import Embed
from .config import EmbedCreatorConfig
from discord.ui import Button, Select

if TYPE_CHECKING:
    from discord import Member, User, Interaction

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
        self.current_embed = 0
        self._init_select_options()
        self._init_creator()

    def _init_select_options(self) -> None:
        options = [SelectOption(label=i.name) for i in self.embeds]
        self._embeds_select.options = options

    def _init_creator(self) -> None:
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

    @property
    def get_current_embed(self) -> Embed:
        return self.embeds[self.current_embed]

    def get_embed(self, name: str) -> Embed | None:
        return next((x for x in self.embeds if x.name == name), None)

    def add_embed(self, embed: Embed) -> Embed:
        self.embeds.append(embed)
        embed.name = f"Embed {self.total_embed}"
        self.current_embed = self.total_embed - 1
        return embed

    async def send(
        self,
        ctx: Interaction | commands.Context[Any],
        embed: Embed = Embed(),
    ):
        self.add_embed(embed)
        self._init_select_options()
        if isinstance(ctx, commands.Context):
            await ctx.send(embed=self.get_current_embed, view=self)
        else:
            await ctx.response.send_message(embeds=self.embeds, view=self)

    async def refresh_creator(self, interaction: Interaction):
        assert interaction.message is not None
        self._init_select_options()
        await interaction.message.edit(embeds=self.embeds, view=self)

    @select()
    async def _embeds_select(self, interaction: Interaction, select: Select[Any]):
        assert interaction.message is not None
        selected_embed = self.get_embed(select.values[0])
        if selected_embed:
            await interaction.response.defer()
            await interaction.message.edit(
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
        self._saved: bool = False
        self._update_maker()
        self.callbacks: dict[str, Callable[[Interaction], Coroutine[Any, Any, Any]]] = {
            "author": self.edit_author
        }
        self.embed = embed

    def _update_maker(self) -> None:
        self._save_button.label = self.embed_creator.config.maker.save_button_label
        self._save_button.style = self.embed_creator.config.maker.save_button_style
        self._save_button.emoji = self.embed_creator.config.maker.save_button_emoji

        self._back_button.label = self.embed_creator.config.maker.back_button_label
        self._back_button.style = (
            self.embed_creator.config.maker.back_button_style
            if self._saved
            else ButtonStyle.danger
        )
        self._back_button.emoji = self.embed_creator.config.maker.back_button_emoji

        self._embed_edit_menu.placeholder = self.embed_creator.config.maker.placeholder
        self._embed_edit_menu.options = [
            SelectOption(**i)
            for i in self.embed_creator.config.maker.options.get_list()
        ]

    async def refresh_maker(self, interaction: Interaction, refresh: bool = False):
        assert interaction.message is not None
        if refresh:
            self._update_maker()
        await interaction.message.edit(embed=self.embed, view=self)

    @select()
    async def _embed_edit_menu(self, interaction: Interaction, select: Select[Any]):
        await self.callbacks[select.values[0]](interaction)
        self._saved = False

    @button()
    async def _save_button(self, interaction: Interaction, button: Button[Self]):
        for emb_no, emb in enumerate(self.embed_creator.embeds):
            if emb.name == self.embed.name:
                self.embed_creator.embeds[emb_no] = self.embed
                break
        await interaction.response.defer()
        self._saved = True
        await self.refresh_maker(interaction, True)

    @button()
    async def _back_button(self, interaction: Interaction, button: Button[Self]):
        assert interaction.message is not None
        await interaction.response.defer()
        await interaction.message.edit(
            embeds=self.embed_creator.embeds, view=self.embed_creator
        )

    async def edit_author(self, interaction: Interaction) -> None:
        # Implement the edit_message functionality here
        pass

    async def edit_message(self, interaction: Interaction) -> None:
        # Implement the edit_message functionality here
        pass

    async def edit_color(self, interaction: Interaction) -> None:
        # Implement the edit_color functionality here
        pass

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
