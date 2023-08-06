from typing import TYPE_CHECKING, Any
from dispie import View
from discord import Forbidden, HTTPException, Interaction, NotFound
from discord.ui import select
from contextlib import suppress

if TYPE_CHECKING:
    from discord import User, Member, SelectOption
    from discord.ui import Select

__all__ = ("SelectPrompt",)


class SelectPrompt(View):
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
        delete_after_interaction: bool = True,
    ):
        super().__init__(
            timeout=timeout,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )
        self.values: list[str] | None = None
        self.options = options
        self.delete_after_interaction = delete_after_interaction
        self.init_prompt(min_values, max_values, placeholder)

    def init_prompt(
        self, min_values: int, max_values: int, placeholder: str | None = None
    ) -> None:
        self.select_prompt.options = self.options
        self.select_prompt.placeholder = placeholder
        self.select_prompt.min_values = min_values
        self.select_prompt.max_values = max_values

    @select()
    async def select_prompt(self, interaction: Interaction, select: Select[Any]):
        self.values = select.values
        self.stop()
        if self.delete_after_interaction and self.message is not None:
            with suppress(NotFound, Forbidden, HTTPException):
                return await self.message.delete()
