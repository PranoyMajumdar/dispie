from typing import TYPE_CHECKING, Any, Optional
from dispie import View
from discord import ButtonStyle
from discord.ui import button

if TYPE_CHECKING:
    from discord import User, Member, Interaction
    from discord.ui import Button


__all__ = ("ButtonPrompt",)


class ButtonPrompt(View):
    """A custom View to create an interactive button prompt.

    Parameters
    ----------
    author: User | Member
        The user or member who triggered the prompt.
    timeout: Optional[float]
        Timeout for the view in seconds. Defaults to 180 seconds.
    button_disable_style: ButtonStyle
        The style of the buttons when they are disabled. Defaults to ButtonStyle.gray.
    auto_delete: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the message will be deleted after completion of the timeout.
    auto_disable: bool
        If set to `True` and this view has a `discord.Message` and `discord.WebhookMessage` attribute,
        then the buttons will be disabled after completion of the timeout.
    **data: Any
        Additional data for the buttons.

    Attributes
    ----------
    value: bool | None
        The result of the button prompt, either True, False, or None.

    Example
    -------
    To create a ButtonPrompt and wait for the user to click a button:

    ```
    prompt = ButtonPrompt(author, auto_delete=True)
    message = await ctx.send("Choose an option!", view=prompt)
    prompt.message = message
    await prompt.wait()
    if prompt.value is not None:
        await ctx.send(f"You chose: {prompt.value}!")
    else:
        await ctx.send("Timeout...")
    ```

    Note
    ----
    The prompt will be active until the user clicks one of the buttons.

    """

    def __init__(
        self,
        author: User | Member,
        *,
        timeout: Optional[float] = 180,
        button_disable_style: ButtonStyle = ButtonStyle.gray,
        auto_delete: bool = False,
        auto_disable: bool = False,
        **data: Any,
    ):
        super().__init__(
            timeout=timeout,
            button_disable_style=button_disable_style,
            auto_delete=auto_delete,
            auto_disable=auto_disable,
            author=author,
        )

        self.value: bool | None = None
        self.init_buttons(data)

    def init_buttons(self, data: dict[str, Any]) -> None:
        """Initialize the button data such as label, style, and emoji.

        Parameters
        ----------
            data: dict[str, Any]
                Keyword arguments for the buttons.

        """
        button_data = {"true": self.true_button, "false": self.false_button}

        for button_type, button_obj in button_data.items():
            label_key = f"{button_type}_button_label"
            style_key = f"{button_type}_button_style"
            emoji_key = f"{button_type}_button_emoji"

            label_value = data.get(label_key)
            style_value = data.get(style_key)
            emoji_value = data.get(emoji_key)

            if label_value is not None:
                button_obj.label = label_value

            if style_value is not None:
                button_obj.style = style_value

            if emoji_value is not None:
                button_obj.emoji = emoji_value

    @button(label="Yes", style=ButtonStyle.green)
    async def true_button(self, interaction: Interaction, button: Button[View]):
        self.value = True
        self.stop()

    @button(label="No", style=ButtonStyle.red)
    async def false_button(self, interaction: Interaction, button: Button[View]):
        self.value = False
        self.stop()
