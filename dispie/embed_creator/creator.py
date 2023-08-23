from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, TypeAlias, Union
from dispie import View
from discord import ButtonStyle, SelectOption, ui, Emoji, PartialEmoji
from .embed import Embed
from discord.ext import commands

if TYPE_CHECKING:
    from discord import User, Member, Interaction
    from typing_extensions import Self

__all__ = ("EmbedCreator",)

EmojiType: TypeAlias = Union[str, Emoji, PartialEmoji, None]


class EmbedCreator(View):
    def __init__(
        self,
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
        self.embeds: list[Embed] = list()

    def add_embed(self) -> Embed:
        embed = Embed(description="Embed")
        self.embeds.append(embed)
        if len(self.embeds) == 0:
            embed.name = "Embed 1"
        else:
            embed.name = f"Embed {len(self.embeds)}"
        return embed

    def get_embed(self, name: str) -> Embed:
        return next((x for x in self.embeds if x.name == name))

    def update_select_options(self):
        self._embed_select.options = [SelectOption(label=x.name) for x in self.embeds]

    async def start(
        self,
        ctx: commands.Context[Any] | Interaction,
        content: str = "Click on `Add Embed` button to add a new embed.",
    ) -> Any:
        self.add_embed()
        self.update_select_options()
        if isinstance(ctx, commands.Context):
            await ctx.send(content=content, embeds=self.embeds, view=self)
        else:
            if ctx.response.is_done():
                await ctx.response.defer()

            await ctx.followup.send(content=content, embeds=self.embeds, view=self)

    async def refresh_creator(self, interaction: Interaction) -> Any:
        if not interaction.response.is_done():
            await interaction.response.defer()
        self.update_select_options()
        await interaction.edit_original_response(embeds=self.embeds, view=self)

    @ui.select(row=2)
    async def _embed_select(self, interaction: Interaction, select: ui.Select[Any]):
        await interaction.response.defer()
        embed = self.get_embed(select.values[0])
        await interaction.edit_original_response(embed=embed, view=EditorView())

    @ui.button(label="Add Embed")
    async def _add_embed_button(
        self, interaction: Interaction, button: ui.Button[Self]
    ):
        if len(self.embeds) == 10:
            return await interaction.response.send_message(
                "Embed limit reached! (limit: 10)", ephemeral=True
            )
        self.add_embed()
        await self.refresh_creator(interaction)

    @ui.button(label="Remove Embed")
    async def _remove_embed_button(
        self, interaction: Interaction, button: ui.Button[Self]
    ):
        ...

    @ui.button(label="Send")
    async def _send_button(self, interaction: Interaction, button: ui.Button[Self]):
        ...


class EditorView(EmbedCreator):
    def __init__(
        self,
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
        self.callbacks: dict[
            str, Callable[[Interaction], Coroutine[Any, Any, Any]]
        ] = dict()
        self._init_editor()

    def _init_editor(self):
        ...

    @ui.select()
    async def _embed_select(self, interaction: Interaction, select: ui.Select[Any]):
        ...

    @ui.button(label="Back")
    async def _back_button(self, interaction: Interaction, button: ui.Button[Self]):
        ...
