from __future__ import annotations
from typing import Optional

from discord.ui import Modal
from discord import Interaction
from contextlib import suppress

__all__ = (
    "ModalInput",
)

class ModalInput(Modal):
    def __init__(
        self,
        *,
        title: str,
        timeout: Optional[float] = None,
        custom_id: str = "modal_input",
        ephemeral: bool = False
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.ephemeral = ephemeral


    async def on_submit(self, interaction: Interaction) -> None:
        with suppress(Exception):
            await interaction.response.defer(ephemeral=self.ephemeral)



