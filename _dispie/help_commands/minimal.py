from typing import Any, List, Optional, Mapping
from discord.ext import commands
from discord.ext.commands import Cog, Command, Group
from discord import Embed, Color, utils
from dispie import Paginator

__all__ = (
    "MinimalHelpCommand",
)
class MinimalHelpCommand(commands.HelpCommand):
    def __init__(self, **options: Any) -> None:
        super().__init__(**options)
        self.options = options
        self.inline = options.get("inline") == True

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]]) -> None:
        embed = Embed(title=f"{self.context.bot.user.name}'s help",
                      color=self.options.get('color') or Color.blurple())
        embed.description = self.options.get(
            "description") or f"Total Commands: {len(self.context.bot.commands)}\nPrefix for this server is: `{self.context.clean_prefix}`\nType `{self.context.clean_prefix}help <command | module>` for more info."
        embed.set_thumbnail(url=self.context.author.display_avatar.url)
        for cog, _commands in mapping.items():
            if not cog:
                continue
            if len(cog.get_commands()):
                embed.add_field(
                    name=f"{cog.EMOJI if hasattr(cog, 'EMOJI') else ''} {cog.qualified_name if cog else 'No category'}",
                    value=f", ".join(
                        f"`{i.qualified_name}`" for i in _commands),
                    inline=self.inline
                )
        embed.set_footer(
            text=f"Requested by {self.context.author}", icon_url=self.context.author.display_avatar.url)
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog: Cog) -> None:
        embeds = list()
        fields = list()
        temp_fields = list()
        for command in cog.get_commands():
            if isinstance(command, Command):
                fields.append([f"{self.context.clean_prefix}{command.qualified_name}",
                              command.description or 'No description'])
            if isinstance(command, Group):
                fields.append([f"{self.context.clean_prefix}{command.qualified_name} (*)",
                              command.description or 'No description'])

        for index, field in enumerate(fields):
            temp_fields.append(field)
            if (index + 1) % 5 == 0 or index == len(fields) - 1:
                embed = Embed(title=f"{cog.qualified_name.capitalize()} commands",
                              description=cog.__doc__ or None, color=self.options.get('color') or Color.blurple())
                embed.set_footer(text=f"(*) has subcommands")
                embed.set_thumbnail(
                    url=self.context.bot.user.display_avatar.url)
                for tf in temp_fields:
                    embed.add_field(
                        name=tf[0],
                        value=f">>> {tf[1]}",
                        inline=self.inline
                    )
                embeds.append(embed)
                temp_fields.clear()

        pages = Paginator(embeds)
        await pages.start(self.context)

    async def send_group_help(self, group: Group) -> None:
        embeds = list()
        fields = list()
        temp_fields = list()
        for command in group.commands:
            if isinstance(command, Command):
                fields.append([f"{self.context.clean_prefix}{command.qualified_name}",
                              command.description or 'No description'])
            if isinstance(command, Group):
                fields.append([f"{self.context.clean_prefix}{command.qualified_name} (*)",
                              command.description or 'No description'])

        for index, field in enumerate(fields):
            temp_fields.append(field)
            if (index + 1) % 5 == 0 or index == len(fields) - 1:
                embed = Embed(title=f"{group.qualified_name.capitalize()} commands",
                              description=group.description or None, color=self.options.get('color') or Color.blurple())
                embed.set_footer(text=f"(*) has subcommands")
                embed.set_thumbnail(
                    url=self.context.bot.user.display_avatar.url)
                for tf in temp_fields:
                    embed.add_field(
                        name=tf[0],
                        value=f">>> {tf[1]}",
                        inline=self.inline
                    )
                embeds.append(embed)
                temp_fields.clear()

        pages = Paginator(embeds)
        await pages.start(self.context)
        return await super().send_group_help(group)

    async def send_command_help(self, command: Command) -> None:
        embed = Embed(
            title=f"{command.qualified_name.capitalize()} help", color=self.options.get('color') or Color.blurple())
        embed.description = f'> {command.description or "No description"}'
        embed.add_field(
            name="Usage",
            value=f"{self.context.clean_prefix}{command.qualified_name} {command.signature}",
            inline=False
        )
        if len(command.aliases):
            embed.add_field(
                name='Aliases',
                value=' | '.join(f"`{i}`" for i in command.aliases),
                inline=False
            )
        embed.set_footer(text=f"Requested by {self.context.bot.user}")
        await self.context.send(embed=embed)
