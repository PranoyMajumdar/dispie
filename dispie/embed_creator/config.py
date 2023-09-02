from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, TypeAlias, Union
from dataclasses import dataclass, field
from discord.ui import TextInput
from discord import TextStyle, SelectOption, ButtonStyle
from enum import StrEnum
from .button import CreatorButton, CreatorButtonType

if TYPE_CHECKING:
    from discord import Emoji, PartialEmoji
    from .creator import EmbedCreator

    EmojiType: TypeAlias = Union[Emoji, PartialEmoji, str, None]

__all__: Sequence[str] = ("BaseConfig",)


class FieldValue(StrEnum):
    EDIT_MESSAGE = "edit_message"
    EDIT_AUTHOR = "edit_author"
    EDIT_BODY = "edit_body"
    EDIT_IMAGES = "edit_images"
    EDIT_FOOTER = "edit_footer"

    ADD_FIELD = "add_field"
    REMOVE_FIELD = "remove_field"
    EDIT_FIELD = "edit_field"


@dataclass
class ModalInput:
    label: str
    style: TextStyle = field(default=TextStyle.short)
    placeholder: str | None = field(default=None)
    required: bool = field(default=False)
    default: str | None = field(default=None)
    min_length: int | None = field(default=None)
    max_length: int | None = field(default=None)
    row: int | None = field(default=None)

    def value(
        self, default: str | None = None, required: bool | None = None
    ) -> TextInput[Any]:
        return TextInput(
            label=self.label,
            style=self.style,
            placeholder=self.placeholder,
            required=required or self.required,
            default=default or self.default,
            min_length=self.min_length,
            max_length=self.max_length,
            row=self.row,
        )


@dataclass
class Modals:
    message: str = field(default="Edit Message")
    message_content: ModalInput = field(
        default_factory=lambda: ModalInput(
            label="Message Content", style=TextStyle.paragraph
        )
    )

    author: str = field(default="Edit Author")
    author_name: ModalInput = field(default_factory=lambda: ModalInput(label="Name"))
    author_url: ModalInput = field(default_factory=lambda: ModalInput(label="Url"))
    author_icon_url: ModalInput = field(
        default_factory=lambda: ModalInput(label="Icon Url")
    )

    body: str = field(default="Edit Body")
    body_title: ModalInput = field(default_factory=lambda: ModalInput(label="Title"))
    body_description: ModalInput = field(
        default_factory=lambda: ModalInput(
            label="Description", style=TextStyle.paragraph
        )
    )
    body_color: ModalInput = field(default_factory=lambda: ModalInput(label="Color"))
    body_url: ModalInput = field(default_factory=lambda: ModalInput(label="Url"))

    footer: str = field(default="Edit Footer")
    footer_text: ModalInput = field(default_factory=lambda: ModalInput(label="Text"))
    footer_icon_url: ModalInput = field(
        default_factory=lambda: ModalInput(label="Icon Url")
    )

    images: str = field(default="Edit Images")
    images_image: ModalInput = field(
        default_factory=lambda: ModalInput(label="Embed Image Url")
    )
    images_thumbnail: ModalInput = field(
        default_factory=lambda: ModalInput(label="Embed Thumbnail Url")
    )

    addfield: str = field(default="Add a new field")
    addfield_name: ModalInput = field(
        default_factory=lambda: ModalInput(label="Name", required=True)
    )
    addfield_value: ModalInput = field(
        default_factory=lambda: ModalInput(
            label="Value", style=TextStyle.paragraph, required=True
        )
    )
    addfield_inline: ModalInput = field(
        default_factory=lambda: ModalInput(label="Inline", required=True)
    )


@dataclass
class EmbedSectionSelect:
    default: SelectOption = field(
        default=SelectOption(label="Edit Sections", default=True)
    )
    edit_message: SelectOption = field(
        default=SelectOption(label="Edit Message", value=FieldValue.EDIT_MESSAGE)
    )
    edit_author: SelectOption = field(
        default=SelectOption(label="Edit Author", value=FieldValue.EDIT_AUTHOR)
    )
    edit_body: SelectOption = field(
        default=SelectOption(label="Edit Body", value=FieldValue.EDIT_BODY)
    )
    edit_images: SelectOption = field(
        default=SelectOption(label="Edit Images", value=FieldValue.EDIT_IMAGES)
    )
    edit_footer: SelectOption = field(
        default=SelectOption(label="Edit Footer", value=FieldValue.EDIT_FOOTER)
    )

    def options(self) -> list[SelectOption]:
        return [
            self.default,
            self.edit_message,
            self.edit_author,
            self.edit_body,
            self.edit_images,
            self.edit_footer,
        ]


@dataclass
class EmbedFieldsSectionSelect:
    default: SelectOption = field(
        default_factory=lambda: SelectOption(label="Embed Fields", default=True)
    )
    add_field: SelectOption = field(
        default_factory=lambda: SelectOption(
            label="Add Field", value=FieldValue.ADD_FIELD
        )
    )
    remove_field: SelectOption = field(
        default_factory=lambda: SelectOption(
            label="Remove Field", value=FieldValue.REMOVE_FIELD
        )
    )
    edit_field: SelectOption = field(
        default_factory=lambda: SelectOption(
            label="Edit Field", value=FieldValue.EDIT_FIELD
        )
    )

    def options(self) -> list[SelectOption]:
        return [self.default, self.add_field, self.remove_field, self.edit_field]


@dataclass
class Selects:
    embed_sections: EmbedSectionSelect = field(default_factory=EmbedSectionSelect)
    embed_fields_sections: EmbedFieldsSectionSelect = field(
        default_factory=EmbedFieldsSectionSelect
    )


@dataclass
class Button:
    label: str
    button_type: CreatorButtonType
    style: ButtonStyle = field(default=ButtonStyle.gray)
    emoji: EmojiType = field(default=None)
    custom_id: str | None  = field(default=None)
    row: int |None = field(default=None)

    def to_button(self, creator: EmbedCreator) -> CreatorButton[Any]:
        return CreatorButton(
            button_type=self.button_type,
            creator=creator,
            label=self.label,
            style=self.style,
            emoji=self.emoji,
            custom_id=self.custom_id,
            row=self.row
        )


@dataclass
class Buttons:
    send_button: Button = field(default_factory=lambda: Button(label="Send", button_type=CreatorButtonType.SEND))
    webhook_button: Button = field(default_factory=lambda: Button(label="Webhook", button_type=CreatorButtonType.SEND_AS_WEBHOOK))
    load_json: Button = field(
        default_factory=lambda: Button(label="Load Json", button_type=CreatorButtonType.LOAD_JSON)
    )
    more_button: Button = field(default_factory=lambda: Button(label="More", button_type=CreatorButtonType.MORE))


    def values(self, creator: EmbedCreator) -> list[CreatorButton[Any]]:
        return [
            self.send_button.to_button(creator),
            self.webhook_button.to_button(creator),
            self.load_json.to_button(creator),
            self.more_button.to_button(creator)
        ]
@dataclass
class ErrorMessage:
    color_conversion_error: str = field(
        default="The string could not be converted into a color."
    )

    max_fields_reached_error: str = field(
        default="You have reached the maximum limit of 25 fields for this embed."
    )


@dataclass
class BaseConfig:
    selects: Selects = field(default_factory=Selects)
    buttons: Buttons = field(default_factory=Buttons)
    modals: Modals = field(default_factory=Modals)
    errors: ErrorMessage = field(default_factory=ErrorMessage)
