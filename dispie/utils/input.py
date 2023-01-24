from __future__ import annotations
from typing import List, Optional

from discord.ui import Modal, Select, View, select
from discord import Interaction, SelectOption
from contextlib import suppress

__all__ = ("ModalInput", "SelectPrompt")


class ModalInput(Modal):
    def __init__(
        self,
        *,
        title: str,
        timeout: Optional[float] = None,
        custom_id: str = "modal_input",
        ephemeral: bool = False,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.ephemeral = ephemeral

    async def on_submit(self, interaction: Interaction) -> None:
        with suppress(Exception):
            await interaction.response.defer(ephemeral=self.ephemeral)


class SelectPrompt(View):
    def __init__(
        self, placeholder: str, options: List[SelectOption], max_values: int = 1, ephemeral: bool = False
    ) -> None:
        super().__init__()
        self.children[0].placeholder, self.children[0].max_values, self.children[0].options = placeholder, max_values, options  # type: ignore
        self.values = None
        self.ephemeral = ephemeral

    @select()
    async def select_callback(self, interaction: Interaction, select: Select):
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = select.values
        self.stop()
