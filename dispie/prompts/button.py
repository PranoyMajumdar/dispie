from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional
from dispie import View
from discord import ButtonStyle

if TYPE_CHECKING:
    from discord import User, Member 


__all__ = ("ButtonPrompt",)


class ButtonPrompt(View):
    def __init__(
        self,
        author: User | Member,
        *,
        timeout: Optional[float] = 180,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        auto_delete: Optional[bool] = False,
        auto_disable: Optional[bool] = False,
        **kwargs: Any
    ):
        super().__init__(
            timeout=timeout,
            button_disable_style=button_disable_style,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )

