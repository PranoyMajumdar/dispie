from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, Sequence, TypeAlias, Union
from enum import StrEnum

from discord.ui import Button
from discord.ui.item import V
from discord import ButtonStyle
if TYPE_CHECKING:
    from discord import  Emoji, PartialEmoji, Interaction
    from .creator import EmbedCreator

    EmojiType: TypeAlias = Union[Emoji, PartialEmoji, str, None]

__all__: Sequence[str] = ("CreatorButton",)


class CreatorButtonType(StrEnum):
    SEND = "send"
    SEND_AS_WEBHOOK = "send_as_webhook"
    LOAD_JSON = "load_json"
    MORE = "more"


class CreatorButton(Button[V]):
    def __init__(
        self,
        *,
        button_type: CreatorButtonType,
        creator: EmbedCreator,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: EmojiType = None,
        row: int | None = None,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.button_type = button_type
        self.creator = creator
        self.callbacks: dict[str, Callable[[Interaction], Coroutine[Any, Any, Any]]] = {
            CreatorButtonType.SEND: self.send_callback,
            CreatorButtonType.SEND_AS_WEBHOOK: self.send_as_webhook_callback,
            CreatorButtonType.LOAD_JSON: self.load_json_callback,
            CreatorButtonType.MORE: self.more_callback,
        }

    async def callback(self, interaction: Interaction) -> Any:
        return await self.callbacks[self.button_type](interaction)

    async def send_callback(self, interaction: Interaction) -> Any:
        ...

    async def send_as_webhook_callback(self, interaction: Interaction) -> Any:
        ...
    
    async def load_json_callback(self, interaction: Interaction) -> Any:
        ...
    
    async def more_callback(self, interaction: Interaction) -> Any:
        ...
