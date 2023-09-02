from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, TypeAlias, Union
from dataclasses import dataclass, field
from discord.ui import TextInput
from discord import TextStyle, SelectOption
from enum import StrEnum

if TYPE_CHECKING:
    from discord import ButtonStyle, Emoji, PartialEmoji

__all__: Sequence[str] = ("BaseConfig",)


EmojiType: TypeAlias = Union[Emoji, PartialEmoji, str, None]


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
    ...


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
            self.edit_message, self.edit_author, self.edit_body, self.edit_images, self.edit_footer
        ]


@dataclass
class EmbedFieldsSectionSelect:
    default: SelectOption = field(
        default=SelectOption(label="Embed Fields", default=True)
    )
    add_field: SelectOption = field(
        default=SelectOption(label="Edit Message", value=FieldValue.ADD_FIELD)
    )
    remove_field: SelectOption = field(
        default=SelectOption(label="Edit Author", value=FieldValue.REMOVE_FIELD)
    )
    edit_field: SelectOption = field(
        default=SelectOption(label="Edit Body", value=FieldValue.EDIT_FIELD)
    )

    def options(self) -> list[SelectOption]:
        return [
            self.add_field, self.remove_field, self.edit_field
        ]


@dataclass
class Selects:
    embed_sections: EmbedSectionSelect = field(default_factory=EmbedSectionSelect)
    embed_fields_sections: EmbedFieldsSectionSelect = field(
        default_factory=EmbedFieldsSectionSelect
    )


@dataclass
class Button:
    label: str
    style: ButtonStyle = field(default=ButtonStyle.gray)
    emoji: EmojiType = field(default=None)


@dataclass
class Buttons:
    send_button: Button = field(default=Button(label="Send"))
    webhook_button: Button = field(default=Button(label="Webhook"))
    components_button: Button = field(default=Button(label="Components"))
    more_button: Button = field(default=Button(label="More"))


@dataclass
class BaseConfig:
    selects: Selects = field(default_factory=Selects)
    buttons: Buttons = field(default_factory=Buttons)
    modals: Modals = field(default_factory=Modals)
