from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from discord import ui, Message, WebhookMessage
from contextlib import suppress

if TYPE_CHECKING:
    from discord import Client


__all__ = ("View",)


class View(ui.View):
    if TYPE_CHECKING:
        bot: Client | None
        message: Message | WebhookMessage | None

    def __init__(
        self,
        *,
        timeout: Optional[float] = 180,
        auto_delete: Optional[bool] = False,
        auto_disable: Optional[bool] = False
    ):
        super().__init__(timeout=timeout)
        self.message = None
        self.bot = None
        self.auto_delete = auto_delete
        self.auto_disable = auto_disable

    async def on_timeout(self) -> Any:
        if self.message is not None and (self.auto_delete or self.auto_disable):
            for child in self.children:
                if isinstance(child, (ui.Button, ui.Select)):
                    child.disabled = True

            with suppress(Exception):
                if self.auto_delete:
                    return await self.message.delete()
                if self.auto_disable:
                    return await self.message.edit(view=self)

