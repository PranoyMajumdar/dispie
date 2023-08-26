from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass, field

from discord import Embed


if TYPE_CHECKING:
    from discord import PartialEmoji, Emoji

__all__ = (
    "BaseConfig",
    "EditOptions",
    "ActionOptions",
    "Option",
    "ModalField",
    "Modals",
    "Messages",
)


@dataclass(kw_only=True, slots=True, eq=True)
class Option:
    label: str
    description: str | None = field(default=None)
    emoji: str | Emoji | PartialEmoji | None = field(default=None)


@dataclass(kw_only=True, slots=True, eq=True)
class EditOptions:
    content: Option = field(default_factory=lambda: Option(label="Edit Content"))
    body: Option = field(default_factory=lambda: Option(label="Edit Body"))
    images: Option = field(default_factory=lambda: Option(label="Edit Images"))
    misc: Option = field(default_factory=lambda: Option(label="Misc"))
    add_field: Option = field(default_factory=lambda: Option(label="Add Field"))
    remove_field: Option = field(default_factory=lambda: Option(label="Remove Field"))
    edit_field: Option = field(default_factory=lambda: Option(label="Edit Field"))
    rearrange_field: Option = field(
        default_factory=lambda: Option(label="Rearrange Fields")
    )

    def get_list(self, embed: Embed) -> list[dict[str, Any]]:
        base = [
            {
                "label": self.content.label,
                "description": self.content.description,
                "emoji": self.content.emoji,
                "value": "content",
            },
            {
                "label": self.body.label,
                "description": self.body.description,
                "emoji": self.body.emoji,
                "value": "body",
            },
            {
                "label": self.images.label,
                "description": self.images.description,
                "emoji": self.images.emoji,
                "value": "images",
            },
            {
                "label": self.misc.label,
                "description": self.misc.description,
                "emoji": self.misc.emoji,
                "value": "misc",
            },
        ]
        if len(embed.fields) <= 25:
            base.append(
                {
                    "label": self.add_field.label,
                    "description": self.add_field.description,
                    "emoji": self.add_field.emoji,
                    "value": "add_field",
                }
            )
        if len(embed.fields) > 0:
            base.append(
                {
                    "label": self.remove_field.label,
                    "description": self.remove_field.description,
                    "emoji": self.remove_field.emoji,
                    "value": "remove_field",
                }
            )
            base.append(
                {
                    "label": self.edit_field.label,
                    "description": self.edit_field.description,
                    "emoji": self.edit_field.emoji,
                    "value": "edit_field",
                },
            )
        if len(embed.fields) > 1:
            base.append(
                {
                    "label": self.rearrange_field.label,
                    "description": self.rearrange_field.description,
                    "emoji": self.rearrange_field.emoji,
                    "value": "rearrange_fields",
                },
            )
        return base


@dataclass(kw_only=True, slots=True, eq=True)
class ActionOptions:
    send: Option = field(default_factory=lambda: Option(label="Send"))
    save: Option = field(default_factory=lambda: Option(label="Save as json"))
    load_embed: Option = field(default_factory=lambda: Option(label="Load Embed"))
    variables: Option = field(default_factory=lambda: Option(label="Variables"))

    def get_list(self) -> list[dict[str, Any]]:
        return [
            {
                "label": self.send.label,
                "description": self.send.description,
                "emoji": self.send.emoji,
                "value": "send",
            },
            {
                "label": self.save.label,
                "description": self.save.description,
                "emoji": self.save.emoji,
                "value": "save",
            },
            {
                "label": self.load_embed.label,
                "description": self.load_embed.description,
                "emoji": self.load_embed.emoji,
                "value": "load_embed",
            },
            {
                "label": self.variables.label,
                "description": self.variables.description,
                "emoji": self.variables.emoji,
                "value": "variables",
            },
        ]


@dataclass(kw_only=True, slots=True, eq=True)
class ModalField:
    label: str
    placeholder: str
    default: str | None = field(default=None)

    def get_kwargs(self, default: str | None = None) -> Any:
        return {
            "label": self.label,
            "placeholder": self.placeholder,
            "default": self.default or default,
            "required": False,
        }


@dataclass(kw_only=True, slots=True, eq=True)
class Modals:
    content_title: str = field(default="Edit Message Content")
    content_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Content", placeholder="The content of the message"
        )
    )

    body_title: str = field(default="Edit Embed Body")
    body_title_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Title", placeholder="The title of the body."
        )
    )
    body_description_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Description", placeholder="The description of the body."
        )
    )
    body_color_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Color", placeholder="The color of the embed. (example: #fff)"
        )
    )

    images_title: str = field(default="Edit Embed Images")
    images_thumbnail_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Thumbnail url", placeholder="The thumbnail url of the embed."
        )
    )
    images_image_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Image url", placeholder="The image url of the embed."
        )
    )

    add_field_title: str = field(default="Add a new field")
    add_field_name_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Field Name", placeholder="The name of the field."
        )
    )
    add_field_value_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Field Value", placeholder="The value of the field."
        )
    )
    add_field_inline_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Inline", placeholder="True or False.", default="True"
        )
    )

    misc_title: str = field(default="Misc")
    misc_author_name_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Author Name", placeholder="The name of the embed author."
        )
    )

    misc_author_icon_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Author Icon Url", placeholder="The author icon url."
        )
    )

    misc_footer_text_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Footer Text", placeholder="The footer text of the embed."
        )
    )

    misc_footer_icon_field: ModalField = field(
        default_factory=lambda: ModalField(
            label="Footer Icon Url", placeholder="The icon url of the embed footer."
        )
    )


@dataclass(kw_only=True, slots=True, eq=True)
class Messages:
    color_convert_error: str = field(
        default="The string could not be converted into a colour."
    )


@dataclass(kw_only=True, slots=True, eq=True)
class Prompts:
    remove_field_content: str = field(default="Select a field to remove!")
    remove_field_description: str | None = field(default=None)
    remove_field_emoji: str | Emoji | PartialEmoji | None = field(default=None)


@dataclass(kw_only=True, slots=True, eq=True)
class BaseConfig:
    edit_options: EditOptions = field(default_factory=EditOptions)
    action_options: ActionOptions = field(default_factory=ActionOptions)
    modals: Modals = field(default_factory=Modals)
    prompts: Prompts = field(default_factory=Prompts)
    messages: Messages = field(default_factory=Messages)
    edit_select_placeholder: str = field(default="Edit this embed...")
    action_select_placeholder: str = field(default="Click here to perform an action...")
