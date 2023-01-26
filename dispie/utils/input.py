from __future__ import annotations
from typing import List, Optional


from discord.ui import ChannelSelect, Modal, Select, View, select
from discord import Interaction, SelectOption
from contextlib import suppress

__all__ = ("ModalInput", "SelectPrompt", "ChannelSelectPrompt")


class ModalInput(Modal):
    """
    This class is a subclass of the `Modal` class that is intended to be used as a base class for creating modals that require user input.

    Parameters:
        title (str): The title of the modal.
        timeout (float, optional): An optional argument that is passed to the parent Modal class. It is used to specify a timeout for the modal in seconds.
        custom_id (str, optional): An optional argument that is passed to the parent Modal class. It is used to specify a custom ID for the modal.
        ephemeral (bool, optional): A boolean indicating whether the modal will be sent as an ephemeral message or not.
    """
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
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the select prompt.
        options (List[SelectOption]): A list of `SelectOption` instances that will be displayed as options in the select prompt.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
    """
    def __init__(
        self, placeholder: str, options: List[SelectOption], max_values: int = 1, ephemeral: bool = False
    ) -> None:
        super().__init__()
        self.children[0].placeholder, self.children[0].max_values, self.children[0].options = placeholder, max_values, options  # type: ignore
        self.values = None
        self.ephemeral = ephemeral

    @select()
    async def select_callback(self, interaction: Interaction, select: Select):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = select.values
        self.stop()

class ChannelSelectPrompt(View):
    """
    This class is a subclass of the `View` class that is intended to be used as a base class for creating a channel select prompt.

    Parameters:
        placeholder (str): The placeholder text that will be displayed in the channel select prompt.
        ephemeral (bool, optional): A boolean indicating whether the select prompt will be sent as an ephemeral message or not. Default is False.
        max_values (int, optional): The maximum number of options that can be selected by the user. Default is 1.
    """
    def __init__(
        self, placeholder: str, ephemeral: bool = False, max_values: int = 1
    ) -> None:
        super().__init__()
        self.values = None
        self.ephemeral = ephemeral
        self.children[0].placeholder, self.children[0].max_values = placeholder, max_values# type: ignore

    @select(cls=ChannelSelect)
    async def callback(self, interaction: Interaction, select: ChannelSelect):
        await interaction.response.defer(ephemeral=self.ephemeral)
        if self.ephemeral:
            await interaction.delete_original_response()
        else:
            with suppress(Exception):
                await interaction.message.delete()  # type: ignore
        self.values = [interaction.guild.get_channel(i.id) for i in select.values] # type: ignore
        self.stop()
        