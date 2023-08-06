from typing import Dict, Optional, Union, List, Any, TYPE_CHECKING, Sequence, Union

from discord import Embed, ButtonStyle, utils, Interaction
from discord.ui import View, button, Button
from discord.ext.commands import Context

if TYPE_CHECKING:
    from discord import Message, InteractionMessage, WebhookMessage

__all__ = ("Paginator",)


class Paginator(View):
    """
    The Paginator class is used for paginating through a list of items, such as list of embeds.
    It allows for easy navigation between pages using the "previous" and "next" buttons.

    Attributes:
    message (Optional[Message]): The message object representing the current page.
    pages (List[Any]): The list of items to be paginated.
    timeout (Optional[float]): The amount of time before the paginator times out and stops. Defaults to 180 seconds.
    delete_message_after (bool): Whether or not to delete the message after the paginator has stopped. Defaults to False.
    per_page (int): The number of items to display per page. Defaults to 1.
    current_page (int): The current page number.
    ctx (Optional[Context]): The context object of the paginator.
    interaction (Optional[Interaction]): The interaction object of the paginator.
    max_pages (int): The maximum number of pages.

    Methods:
    stop(): Stops the paginator and sets all attributes to None.
    get_page(page_number: int): Returns the items for a given page number.
    format_page(page: Any): Formats a page for display.
    get_page_kwargs(page: Any): Returns the keyword arguments for sending a message with the current page.
    update_page(interaction: Interaction): Updates the current page to be displayed.
    previous_page(interaction: Interaction, button: Button): Navigates to the previous page.
    next_page(interaction: Interaction, button: Button): Navigates to the next page.
    start(obj: Union[Context, Interaction]): Starts the paginator and sends the first page. Returns the message object representing the current page.

    """

    message: Optional[Message] = None

    def __init__(
        self,
        pages: List[Any],
        *,
        timeout: Optional[float] = 180.0,
        delete_message_after: bool = False,
        per_page: int = 1,
    ):
        super().__init__(timeout=timeout)
        self.delete_message_after: bool = delete_message_after
        self.current_page: int = 0

        self.ctx: Optional[Context] = None
        self.interaction: Optional[Interaction] = None
        self.per_page: int = per_page
        self.pages: Any = pages
        total_pages, left_over = divmod(len(self.pages), self.per_page)
        if left_over:
            total_pages += 1

        self.max_pages: int = total_pages
        self.next_page.disabled = self.current_page >= self.max_pages - 1

    def stop(self) -> None:
        self.message = None
        self.ctx = None
        self.interaction = None

        super().stop()

    def get_page(self, page_number: int) -> Any:
        if page_number < 0 or page_number >= self.max_pages:
            self.current_page = 0
            return self.pages[self.current_page]

        if self.per_page == 1:
            return self.pages[page_number]
        else:
            base = page_number * self.per_page
            return self.pages[base : base + self.per_page]

    def format_page(self, page: Any) -> Any:
        return page

    async def get_page_kwargs(self, page: Any) -> Dict[str, Any]:
        formatted_page = await utils.maybe_coroutine(self.format_page, page)

        kwargs = {"content": None, "embeds": [], "view": self}
        if isinstance(formatted_page, str):
            kwargs["content"] = formatted_page
        elif isinstance(formatted_page, Embed):
            kwargs["embeds"] = [formatted_page]
        elif isinstance(formatted_page, list):
            if not all(isinstance(embed, Embed) for embed in formatted_page):
                raise TypeError("All elements in the list must be of type Embed")

            kwargs["embeds"] = formatted_page
        elif isinstance(formatted_page, dict):
            return formatted_page

        return kwargs

    async def update_page(self, interaction: Interaction) -> None:
        if self.message is None:
            self.message = interaction.message

        kwargs = await self.get_page_kwargs(self.get_page(self.current_page))
        self.previous_page.disabled = self.current_page <= 0
        self.next_page.disabled = self.current_page >= self.max_pages - 1
        await interaction.response.edit_message(**kwargs)

    @button(label="<", style=ButtonStyle.gray)
    async def previous_page(self, interaction: Interaction, button: Button) -> None:
        self.current_page -= 1
        await self.update_page(interaction)

    @button(label=">", style=ButtonStyle.gray)
    async def next_page(self, interaction: Interaction, button: Button) -> None:
        self.current_page += 1
        await self.update_page(interaction)

    async def start(
        self, obj: Union[Context, Interaction]
    ) -> Optional[Union[Message, InteractionMessage, WebhookMessage]]:
        if isinstance(obj, Context):
            self.ctx = obj
            self.interaction = None
        else:
            self.ctx = None
            self.interaction = obj

        if self.message is not None and self.interaction is not None:
            await self.update_page(self.interaction)
        else:
            self.previous_page.disabled = self.current_page <= 0
            kwargs = await self.get_page_kwargs(self.get_page(self.current_page))
            if self.ctx is not None:
                self.message = await self.ctx.send(**kwargs)
            elif self.interaction is not None:
                if self.interaction.response.is_done():
                    self.message = await self.interaction.followup.send(
                        **kwargs, view=self
                    )
                else:
                    await self.interaction.response.send_message(**kwargs, view=self)
                    self.message = await self.interaction.original_response()
            else:
                raise RuntimeError(
                    "Cannot start a paginator without a context or interaction."
                )

        return self.message
