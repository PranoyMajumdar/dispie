from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from discord import (
    ButtonStyle,
    Forbidden,
    HTTPException,
    NotFound,
    ui,
    Message,
    WebhookMessage,
)
from contextlib import suppress


if TYPE_CHECKING:
    from discord import User, Member, Interaction


__all__ = ("View",)


class View(ui.View):
    if TYPE_CHECKING:
        message: Message | WebhookMessage | None

    def __init__(
        self,
        *,
        timeout: Optional[float] = 180,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        auto_delete: Optional[bool] = False,
        auto_disable: Optional[bool] = False,
        author: Optional[User | Member | None] = None,
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
