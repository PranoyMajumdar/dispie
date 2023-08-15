from typing import Callable, Dict
from dispie import ModalInput, SelectPrompt
from discord import Colour, Embed, HTTPException, Interaction, SelectOption, TextStyle
from discord.ui import TextInput


class CreatorMethods:
    """
    This class contains all the methods for editing an embed. It is intended to be inherited by the main `EmbedCreator` class.

    Attributes:
        embed (discord.Embed): The embed object being edited.

    """

    def __init__(self, embed: Embed) -> None:
        self.embed = embed
        self.callbacks: Dict[str, Callable] = {
            "author": self.edit_author,
            "message": self.edit_message,
            "thumbnail": self.edit_thumbnail,
            "image": self.edit_image,
            "footer": self.edit_footer,
            "colour": self.edit_colour,
            "addfield": self.add_field,
            "removefield": self.remove_field,
        }

    async def edit_author(self, interaction: Interaction) -> None:
        """This method edits the embed's author"""
        modal = ModalInput(title="Edit Embed Author")
        modal.add_item(
            TextInput(
                label="Author Name",
                max_length=100,
                default=self.embed.author.name,
                placeholder="Author name to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Icon Url",
                default=self.embed.author.icon_url,
                placeholder="Author icon to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Author Url",
                default=self.embed.author.url,
                placeholder="URL to set as the embed's author link",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            self.embed.set_author(
                name=str(modal.children[0]),
                icon_url=str(modal.children[1]),
                url=str(modal.children[2]),
            )
        except HTTPException:
            self.embed.set_author(name=str(modal.children[0]))

    async def edit_message(self, interaction: Interaction) -> None:
        """This method edits the embed's message (discord.Embed.title and discord.Embed.description)"""
        modal = ModalInput(title="Edit Embed Message")
        modal.add_item(
            TextInput(
                label="Embed Title",
                max_length=255,
                default=self.embed.title,
                placeholder="Title to display in the embed",
                required=False,
            )
        )
        modal.add_item(
            TextInput(
                label="Embed Description",
                default=self.embed.description,
                placeholder="Description to display in the embed",
                style=TextStyle.paragraph,
                required=False,
                max_length=2000,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.title, self.embed.description = str(modal.children[0]), str(
            modal.children[1]
        )

    async def edit_thumbnail(self, interaction: Interaction) -> None:
        """This method edits the embed's thumbnail"""
        modal = ModalInput(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Thumbnail Url",
                default=self.embed.thumbnail.url,
                placeholder="Thumbnail you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_thumbnail(url=str(modal.children[0]))

    async def edit_image(self, interaction: Interaction) -> None:
        """This method edits the embed's image"""
        modal = ModalInput(title="Edit Embed Thumbnail")
        modal.add_item(
            TextInput(
                label="Image Url",
                default=self.embed.image.url,
                placeholder="Image you want to display in the embed",
                required=False,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_image(url=str(modal.children[0]))

    async def edit_footer(self, interaction: Interaction) -> None:
        """This method edits the embed's footer (text, icon_url)"""
        modal = ModalInput(title="Edit Embed Footer")
        modal.add_item(
            TextInput(
                label="Footer Text",
                max_length=255,
                required=False,
                default=self.embed.footer.text,
                placeholder="Text you want to display on embed footer",
            )
        )
        modal.add_item(
            TextInput(
                label="Footer Icon",
                required=False,
                default=self.embed.footer.icon_url,
                placeholder="Icon you want to display on embed footer",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        self.embed.set_footer(
            text=str(modal.children[0]), icon_url=str(modal.children[1])
        )

    async def edit_colour(self, interaction: Interaction) -> None:
        """This method is edits the embed's colour"""
        modal = ModalInput(title="Edit Embed Colour")
        modal.add_item(
            TextInput(
                label="Embed Colour",
                placeholder="The colour you want to display on embed (e.g: #303236)",
                max_length=20,
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            colour = Colour.from_str(str(modal.children[0]))
        except:
            await interaction.followup.send(
                "Please provide a valid hex code.", ephemeral=True
            )
        else:
            self.embed.colour = colour

    async def add_field(self, interaction: Interaction) -> None:
        if len(self.embed.fields) >= 25:
            return await interaction.response.send_message(
                "You can not add more than 25 fields.", ephemeral=True
            )
        modal = ModalInput(title="Add a new field")
        modal.add_item(
            TextInput(
                label="Field Name",
                placeholder="The name you want to display on the field",
                max_length=255,
            )
        )
        modal.add_item(
            TextInput(label="Field Value", max_length=2000, style=TextStyle.paragraph)
        )
        modal.add_item(
            TextInput(
                label="Field Inline (True/False)",
                default="True",
                max_length=5,
                placeholder="The inline for the field either True or False",
            )
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        try:
            inline = False
            if str(modal.children[2]).lower() == "true":
                inline = True
            elif str(modal.children[2]).lower() == "false":
                inline = False
            else:
                raise Exception("Bad Bool Input.")
        except:
            await interaction.followup.send(
                "Please provide a valid input in `inline` either True Or False.",
                ephemeral=True,
            )
        else:
            self.embed.add_field(
                name=str(modal.children[0]), value=str(modal.children[1]), inline=inline
            )

    async def remove_field(self, interaction: Interaction) -> None:
        if not self.embed.fields:
            return await interaction.response.send_message(
                "There is no fields to remove.", ephemeral=True
            )
        field_options = list()
        for index, field in enumerate(self.embed.fields):
            field_options.append(
                SelectOption(
                    label=str(field.name)[0:30], value=str(index), emoji="\U0001f5d1"
                )
            )
        select = SelectPrompt(
            placeholder="Select a field to remove...",
            options=field_options,
            max_values=len(field_options),
            ephemeral=True,
        )
        await interaction.response.send_message(view=select, ephemeral=True)
        await select.wait()

        if vals := select.values:
            for value in vals:
                self.embed.remove_field(int(value))
