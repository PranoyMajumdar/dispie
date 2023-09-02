from __future__ import annotations
from typing import TYPE_CHECKING, Any, Self, Sequence

from dispie import View
from dispie.prompts import ChannelSelectPrompt
from discord import Embed, ButtonStyle, SelectOption, ui
from discord.ext import commands

from .methods import CreatorMethods
from .config import BaseConfig

if TYPE_CHECKING:
    from typing_extensions import Self
    from discord import User, Member, Interaction, TextChannel
    from discord.ui.item import V

__all__: Sequence[str] = ("EmbedCreator",)


class EmbedCreator(View):
    def __init__(
        self,
        *,
        timeout: float | None = None,
        auto_delete: bool = False,
        auto_disable: bool = False,
        author: User | Member | None = None,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        config: BaseConfig | None = None,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.embed: Embed = Embed(title="Embed", description="Embed Description")
        self.buttons: list[ui.Button[Self]] = list()
        self.methods: CreatorMethods = CreatorMethods(self)
        self.content: str | None = None
        self.config = config or BaseConfig()
        for i in range(5):
            self.embed.add_field(name=f"Field {i}", value=f"Field value {i}")

    def update_selects(self) -> Self:
        self.update_select(self._edit_embed_select, self.config.selects.embed_sections.options())
        self.update_select(self._edit_embed_fields_select, self.config.selects.embed_fields_sections.options())

        return self

    def update_select(self, select: ui.Select[V], options: list[SelectOption]) -> Self:
        select.options = options
        return self

    async def refresh_creator(self, interaction: Interaction) -> Self:
        assert (
            interaction.message
        )  # We know that message components always have a message
        await interaction.message.edit(
            content=self.content, embed=self.embed, view=self
        )
        return self

    async def start(self, ctx: Interaction | commands.Context[Any]) -> Self:
        self.update_selects()
        if isinstance(ctx, commands.Context):
            self.message = await ctx.send(embed=self.embed, view=self)
        else:
            if not ctx.response.is_done():
                await ctx.response.defer()

            self.message = await ctx.followup.send(embed=self.embed, view=self)

        return self

    @ui.select()
    async def _edit_embed_select(
        self, interaction: Interaction, select: ui.Select[V]
    ) -> Any:
        if (callback := getattr(self.methods, select.values[0], None)) is not None:
            await self.refresh_creator(interaction)
            return await callback(interaction)

        else:
            await interaction.response.send_message("Not Implimented", ephemeral=True)

    @ui.select()
    async def _edit_embed_fields_select(
        self, interaction: Interaction, select: ui.Select[V]
    ) -> Any:
        if (callback := getattr(self.methods, select.values[0], None)) is not None:
            return await callback(interaction)

        else:
            await interaction.response.send_message("Not Implimented", ephemeral=True)

    @ui.button(label="Send")
    async def _send_button(self, interaction: Interaction, _: ui.Button[Self]) -> Any:
        prompt = ChannelSelectPrompt(
            interaction.user,
            auto_delete=True,
            placeholder="Select a prompt to send this embed.",
        )
        await interaction.response.send_message(view=prompt)
        await prompt.wait()

        view = View()
        for i in self.buttons:
            view.add_item(i)

        if prompt.channels is not None:
            channel = await prompt.channels[0].fetch()
            if isinstance(channel, (TextChannel)):
                await channel.send(content=self.content, embed=self.embed, view=view)

    @ui.button(label="Webhook")
    async def _send_as_webhook_button(
        self, interaction: Interaction, _: ui.Button[Self]
    ) -> Any:
        ...

    @ui.button(label="Components")
    async def _load_json_button(
        self, interaction: Interaction, _: ui.Button[Self]
    ) -> Any:
        ...

    @ui.button(label="More")
    async def _more_button(self, interaction: Interaction, _: ui.Button[Self]) -> Any:
        ...
