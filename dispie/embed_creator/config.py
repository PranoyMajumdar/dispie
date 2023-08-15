from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypeAlias, Union

from discord import ButtonStyle
from discord import Emoji, PartialEmoji


__all__ = ("EmbedCreatorConfig", "SelectOptionData")


EmojiType: TypeAlias = Union[str, Emoji, PartialEmoji, None]


@dataclass(eq=False, slots=True, kw_only=True)
class ModalData:
    author_title: str = field(default="Edit Embed Author")
    author_name_label: str = field(default="Author Name")
    author_url_label: str = field(default="Author Url")


@dataclass(eq=False, slots=True, kw_only=True)
class SelectOptionData:
    author_label: str = field(default="Edit Author")
    author_description: str | None = field(default="Edits the embed author name.")
    author_emoji: EmojiType = field(default="🔸")

    message_label: str = field(default="Edit Message")
    message_description: str | None = field(
        default="Edits the embed title, description."
    )
    message_emoji: EmojiType = field(default="🔸")

    color_label: str = field(default="Edit Color")
    color_description: str | None = field(default="Edits the embed color.")
    color_emoji: EmojiType = field(default="🔸")

    footer_label: str = field(default="Edit Footer")
    footer_description: str | None = field(default="Edits the embed footer text.")
    footer_emoji: EmojiType = field(default="🔸")

    icon_label: str = field(default="Edit Icons")
    icon_description: str | None = field(
        default="Edits the embed author and footer icon."
    )
    icon_emoji: EmojiType = field(default="🔸")

    thumbnail_label: str = field(default="Thumbnail")
    thumbnail_description: str | None = field(default="Edits the embed thumbnail.")
    thumbnail_emoji: EmojiType = field(default="🔸")

    image_label: str = field(default="Image")
    image_description: str | None = field(default="Edits the embed image.")
    image_emoji: EmojiType = field(default="🔸")

    addfield_label: str = field(default="Add Field")
    addfield_description: str | None = field(default="Adds a field to the embed.")
    addfield_emoji: EmojiType = field(default="🔸")

    removefield_label: str = field(default="Remove Field")
    removefield_description: str | None = field(
        default="Remove a field from the embed."
    )
    removefield_emoji: EmojiType = field(default="🔸")

    def get_list(self) -> list[dict[str, Any]]:
        return [
            {
                "label": self.author_label,
                "description": self.author_description,
                "emoji": self.author_emoji,
                "value": "author",
            },
            {
                "label": self.message_label,
                "description": self.message_description,
                "emoji": self.message_emoji,
                "value": "message",
            },
            {
                "label": self.color_label,
                "description": self.color_description,
                "emoji": self.color_emoji,
                "value": "color",
            },
            {
                "label": self.footer_label,
                "description": self.footer_description,
                "emoji": self.footer_emoji,
                "value": "footer",
            },
            {
                "label": self.icon_label,
                "description": self.icon_description,
                "emoji": self.icon_emoji,
                "value": "icon",
            },
            {
                "label": self.thumbnail_label,
                "description": self.thumbnail_description,
                "emoji": self.thumbnail_emoji,
                "value": "thumbnail",
            },
            {
                "label": self.image_label,
                "description": self.image_description,
                "emoji": self.image_emoji,
                "value": "image",
            },
            {
                "label": self.addfield_label,
                "description": self.addfield_description,
                "emoji": self.addfield_emoji,
                "value": "addfield",
            },
            {
                "label": self.removefield_label,
                "description": self.removefield_description,
                "emoji": self.removefield_emoji,
                "value": "removefield",
            },
        ]


@dataclass(eq=False, slots=True, kw_only=True)
class EmbedCreatorMessages:
    max_embed_error: str = field(default="You cannot add more than 10 embeds.")



@dataclass(eq=False, slots=True, kw_only=True)
class EmbedMakerConfig:

    save_button_label: str | None = field(default="Save")
    save_button_style: ButtonStyle = field(default=ButtonStyle.blurple)
    save_button_emoji: str | None = field(default=None)

    back_button_label: str | None = field(default="Back")
    back_button_style: ButtonStyle = field(default=ButtonStyle.blurple)
    back_button_emoji: str | None = field(default=None)

    placeholder: str | None = field(default="Choose an option...")
    options: SelectOptionData = field(default_factory=SelectOptionData)
    modal: ModalData = field(default_factory=ModalData)


@dataclass(eq=False, slots=True, kw_only=True)
class EmbedCreatorConfig:
    placeholder: str | None = field(default="Choose an option...")

    send_button_label: str | None = field(default="Send")
    send_button_style: ButtonStyle = field(default=ButtonStyle.blurple)
    send_button_emoji: str | None = field(default=None)

    add_embed_button_label: str | None = field(default="Add Embed")
    add_embed_button_style: ButtonStyle = field(default=ButtonStyle.blurple)
    add_embed_button_emoji: str | None = field(default=None)

    options_emoji: EmojiType = field(default="🔸")
    options_description: str | None = field(default=None)

    maker: EmbedMakerConfig = field(default_factory=EmbedMakerConfig)
    messages: EmbedCreatorMessages = field(default_factory=EmbedCreatorMessages)
