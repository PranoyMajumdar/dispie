from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from dispie import View
from discord import ButtonStyle
from discord.ui import button
from contextlib import suppress

if TYPE_CHECKING:
    from discord import User, Member, Interaction
    from discord.ui import Button
    from typing_extensions import Self


__all__ = ("ButtonPrompt",)


class ButtonPrompt(View):
    """A custom View to create an interactive button prompt.

    Parameters
    ----------
    author: User | Member
        The user or member who triggered the prompt.
    timeout: Optional[float]
        Timeout for the view in seconds. Defaults to 180 seconds.
    button_disable_style: ButtonStyle
        The style of the buttons when they are disabled. Defaults to ButtonStyle.gray.
    auto_delete: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the message will be deleted after completion of the timeout.
    auto_disable: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the buttons will be disabled after completion of the timeout.
    **data: Any
        Additional data for the buttons.

    Attributes
    ----------
    value: bool | None
        The result of the button prompt, either True, False, or None.

    Note
    ----
    The prompt will be active until the user clicks one of the buttons.

    """

    def __init__(
        self,
        author: User | Member,
        *,
        timeout: Optional[float] = 180,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        auto_delete: bool = False,
        auto_disable: bool = False,
        ephemeral: bool = False,
        **data: Any,
    ):
        super().__init__(
            timeout=timeout,
            button_disable_style=button_disable_style,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )

        self.value: bool | None = None
        self.init_buttons(data)
        self.ephemeral = ephemeral

    def init_buttons(self, data: dict[str, Any]) -> None:
        """Initialize the button data such as label, style, and emoji.

        Parameters
        ----------
            data: dict[str, Any]
                Keyword arguments for the buttons.

        """
        button_data = {"true": self.true_button, "false": self.false_button}

        for button_type, button_obj in button_data.items():
            label_value = data.get(f"{button_type}_button_label")
            style_value = data.get(f"{button_type}_button_style")
            emoji_value = data.get(f"{button_type}_button_emoji")
            row_value = data.get(f"{button_type}_button_row")

            if label_value is not None:
                button_obj.label = label_value

            if style_value is not None:
                button_obj.style = style_value

            if emoji_value is not None:
                button_obj.emoji = emoji_value

            if row_value is not None:
                button_obj.row = row_value


    @button(label="Yes", style=ButtonStyle.green)
    async def true_button(self, interaction: Interaction, button: Button[Self]):
        self.value = True
        self.stop()
        await interaction.response.defer()
        if interaction.message is not None:
            with suppress(Exception):
                if not self.ephemeral:
                    return await interaction.message.delete()
                self.disable_all_items()
                return await interaction.edit_original_response(view=self)

    @button(label="No", style=ButtonStyle.red)
    async def false_button(self, interaction: Interaction, button: Button[Self]):
        self.value = False
        self.stop()
        await interaction.response.defer()
        if interaction.message is not None:
            with suppress(Exception):
                if not self.ephemeral:
                    return await interaction.message.delete()
                self.disable_all_items()
                return await interaction.edit_original_response(view=self)
