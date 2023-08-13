from __future__ import annotations
from typing import TYPE_CHECKING, Any


from dispie.embed_creator import EmbedCreatorConfig
from discord import ButtonStyle, Embed, SelectOption, Colour
from discord.ui import select, button
from discord.ext import commands
from dispie import View


if TYPE_CHECKING:
    from discord import User, Member, Interaction, Message, WebhookMessage
    from discord.ui import Select, Button
    from discord.ui.item import V


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
        embed: Embed | None = None,
        config: EmbedCreatorConfig = EmbedCreatorConfig(),
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
            button_disable_style=button_disable_style,
        )
        self.config = config
        self.embed = embed or self.get_default_embed
        self._init_creator()
        self.message: Message | WebhookMessage | None = None

    @property
    def get_default_embed(self) -> Embed:
        """Creates a default embed for the creator."""
        embed = Embed(
            title="This is title",
            description="Use the dropdown menu to edit my sections!",
            colour=Colour.blurple(),
        )
        embed.set_author(
            name="Welcome to embed builder.",
            icon_url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?",
        )
        embed.set_thumbnail(
            url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?"
        )
        embed.set_image(
            url="https://imageup.me/images/e44472bd-d742-4d39-8e25-b8ae762160ae.png"
        )
        embed.set_footer(
            text="Footer",
            icon_url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?",
        )
        return embed

    def _init_creator(self) -> None:
        """Initialize the creator."""
        self.creator_select.placeholder = self.config.placeholder
        self.creator_select.options = [
            SelectOption(**i) for i in self.config.options.get_list()
        ]
        self.send_button.label = self.config.send_button_label
        self.send_button.style = self.config.send_button_style
        self.send_button.emoji = self.config.send_button_emoji

        self.cancel_button.label = self.config.cancel_button_label
        self.cancel_button.style = self.config.cancel_button_style
        self.cancel_button.emoji = self.config.cancel_button_emoji

    async def send(
        self, ctx: Interaction | commands.Context[Any]
    ) -> Message | WebhookMessage | None:
        """Send the creator."""
        if isinstance(ctx, commands.Context):
            self.message = await ctx.send(embed=self.embed, view=self)
        else:
            await ctx.response.send_message(
                "Embed creator has been sent successfully.", ephemeral=True
            )
            self.message = await ctx.followup.send(embed=self.embed, view=self)

        return self.message

    @select()
    async def creator_select(self, interaction: Interaction, select: Select[V]):
        ...

    @button()
    async def send_button(self, interactio: Interaction, _: Button[V]):
        ...

    @button()
    async def cancel_button(self, interactio: Interaction, _: Button[V]):
        ...

    async def edit_author(self, interaction: Interaction) -> None:
        # Implement the edit_author functionality here
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
