from __future__ import annotations

from typing import TYPE_CHECKING
from discord.ui import Modal, TextInput
from contextlib import suppress

if TYPE_CHECKING:
    from discord import Interaction
    from typing_extensions import Self

__all__ = ("ModalPrompt",)


class ModalPrompt(Modal):
    """This class is a subclass of the :class:`discord.ui.Modal` class
    that is intended to be used as a base class for creating modals that require user input.

    Parameters
    ----------
    title: str
        The title of the modal. Can only be up to 45 characters.
    timeout: float | None
        Timeout in seconds from last interaction with the UI before no longer accepting input.
        If ``None`` then there is no timeout.
    custom_id: str
        The ID of the modal that gets received during an interaction.
        If not given then one is generated for you.
        Can only be up to 100 characters.

    Note
    ----
    The prompt will be active until the user clicks one of the buttons.

    """
    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str = "modal_input",
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        
    def add_input(self, item: TextInput[Self]):
        self.add_item(item)
        return item
    

    async def on_submit(self, interaction: Interaction, /) -> None:
        with suppress(Exception):
            await interaction.response.defer()



