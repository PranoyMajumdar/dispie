from __future__ import annotations

from typing import TYPE_CHECKING

from discord import ChannelType, NotFound, Forbidden, HTTPException
from discord.ui import ChannelSelect, select
from contextlib import suppress
from dispie import View
if TYPE_CHECKING:
    from discord.app_commands import AppCommandChannel, AppCommandThread
    from discord import User, Member, SelectOption, Interaction
    from discord.ui.select import V
    from discord.ui import Select
    

__all__ = ("SelectPrompt", "ChannelSelectPrompt")


class SelectPrompt(View):
    """A custom View to create an interactive select prompt.

    Parameters
    ----------
    author: User | None
        The user or member who triggered the prompt.
    timeout: float | None
        Timeout for the view in seconds. Defaults to 180 seconds.
    auto_delete: bool
        If set to `True` and this view has a `discord.Message` or `discord.WebhookMessage` attribute,
        then the message will be deleted after completion of the timeout.
    auto_disable: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the buttons will be disabled after completion of the timeout.
    placeholder: str | None
        The placeholder text that is shown if nothing is selected, if any.
    min_values: int
        The minimum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 0 and 25.
    max_values: int
        The maximum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    delete_after: bool
        If set to `True` and this view has a `discord.Message` or `discord.WebhookMessage` attribute,
        then the message will be delete after the interaction.

    Attributes
    ----------
    value : list[str] | None
        The result of the button prompt, either True, False, or None.

    Note
    ----
    The prompt will be active until the user select one or more options.

    """

    def __init__(
        self,
        author: User | Member,
        options: list[SelectOption],
        *,
        timeout: float | None = 180,
        auto_delete: bool = False,
        auto_disable: bool = False,
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        delete_after: bool = True,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )
        self.values: list[str] | None = None
        self.options = options
        self.delete_after = delete_after
        self._init_prompt(min_values, max_values, placeholder)

    def _init_prompt(
        self, min_values: int, max_values: int, placeholder: str | None = None
    ) -> None:
        self.select_prompt.options = self.options
        self.select_prompt.placeholder = placeholder
        self.select_prompt.min_values = min_values
        self.select_prompt.max_values = max_values

    @select()
    async def select_prompt(self, interaction: Interaction, select: Select[V]):
        self.values = select.values
        self.stop()
        if self.delete_after and interaction.message is not None:
            with suppress(NotFound, Forbidden, HTTPException):
                return await interaction.message.delete()


class ChannelSelectPrompt(View):
    """A custom View to create an interactive channel select prompt.

    Parameters
    ----------
    author: User | None
        The user or member who triggered the prompt.
    timeout: float | None
        Timeout for the view in seconds. Defaults to 180 seconds.
    auto_delete: bool
        If set to `True` and this view has a `discord.Message` or `discord.WebhookMessage` attribute,
        then the message will be deleted after completion of the timeout.
    auto_disable: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the buttons will be disabled after completion of the timeout.
    placeholder: str | None
        The placeholder text that is shown if nothing is selected, if any.
    min_values: int
        The minimum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 0 and 25.
    max_values: int
        The maximum number of items that must be chosen for this select menu.
        Defaults to 1 and must be between 1 and 25.
    delete_after: bool
        If set to `True` and this view has a `discord.Message` or `discord.WebhookMessage` attribute,
        then the message will be delete after the interaction.
    channel_types: list[ChannelType] | None
        The types of channels to show in the select menu. Defaults to all channels.

    Attributes
    ----------
    value : list[str] | None
        The result of the button prompt, either True, False, or None.

    Note
    ----
    The prompt will be active until the user select one or more channels.

    """
    def __init__(
        self,
        author: User | Member,
        *,
        timeout: float | None = 180,
        auto_delete: bool = False,
        auto_disable: bool = False,
        placeholder: str | None = None,
        min_values: int = 1,
        max_values: int = 1,
        delete_after: bool = True,
        channel_types: list[ChannelType] | None = None,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )
        self.channels: list[AppCommandChannel | AppCommandThread] | None = None
        self.delete_after = delete_after
        self._init_prompt(min_values, max_values, channel_types, placeholder)

    def _init_prompt(
        self,
        min_values: int,
        max_values: int,
        channel_types: list[ChannelType] | None,
        placeholder: str | None,
    ):
        self.channel_prompt.max_values = max_values  # type: ignore
        self.channel_prompt.min_values = min_values  # type: ignore
        self.channel_prompt.placeholder = placeholder  # type: ignore
        if channel_types is not None:
            self.channel_prompt.channel_types = channel_types  # type: ignore

    @select(cls=ChannelSelect)
    async def channel_prompt(self, interaction: Interaction, select: ChannelSelect[V]):
        self.channels = select.values
        self.stop()
        if self.delete_after and interaction.message is not None:
            with suppress(NotFound, Forbidden, HTTPException):
                await interaction.message.delete()
