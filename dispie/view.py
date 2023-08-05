from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from discord import ButtonStyle, Forbidden, HTTPException, NotFound, ui
from contextlib import suppress


if TYPE_CHECKING:
    from discord import User, Member, Interaction, Message, WebhookMessage


__all__ = ("View",)


class View(ui.View):
    """A custom view class that inherits from the :class:`discord.ui.View` and adds extra features.

    Parameters
    ----------
    timeout Optional[float]:
        Timeout in seconds from the last interaction with the UI before no longer accepting input.
        If ``None``, there is no timeout.

    button_disable_style ButtonStyle:
        The style of the buttons while they are disabled.
    
    auto_delete Optional[bool]:
        If set to ``True`` and this view has a :class:`discord.Message` or :class:`discord.WebhookMessage` attribute,
        the message will be deleted after the completion of the timeout.

    auto_disable Optional[bool]:
        If set to ``True`` and this view has a :class:`discord.Message` or :class:`discord.WebhookMessage` attribute,
        the components will be disabled after the completion of the timeout.

    author Optional[User | Member]:
        If provided, this view can only be controlled by the provided author.
    
    Example:
        Creating a custom view with a timeout of 120 seconds and auto-disabling buttons:

        ```
        view = View(timeout=120, auto_disable=True, author=ctx.author)
        view.add_item(ui.Button(label="Click me!", style=ButtonStyle.primary))
        await ctx.send("Please click the button!", view=view)
        ```
    """
    if TYPE_CHECKING:
        message: Message | WebhookMessage | None

    def __init__(
        self,
        *,
        timeout: Optional[float] = 180,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        auto_delete: bool = False,
        auto_disable: bool = False,
        author: Optional[User | Member] = None,
    ):
        super().__init__(timeout=timeout)
        self.message = None
        self.author = author
        self.button_disable_style = button_disable_style
        self.auto_delete = auto_delete
        self.auto_disable = auto_disable

    async def interaction_check(self, interaction: Interaction, /) -> bool:
        return False if self.author is None else self.author.id == interaction.user.id

    async def on_timeout(self) -> Any:
        if self.message is not None and (self.auto_delete or self.auto_disable):
            for child in self.children:
                if isinstance(child, ui.Select):
                    child.disabled = True

                if isinstance(child, ui.Button):
                    child.style = self.button_disable_style
                    child.disabled = True

            with suppress(NotFound, HTTPException, Forbidden):
                if self.auto_delete:
                    self.stop()
                    return await self.message.delete()
                if self.auto_disable:
                    return await self.message.edit(view=self)
