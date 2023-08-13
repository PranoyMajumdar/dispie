from __future__ import annotations

from typing import TYPE_CHECKING

from discord.app_commands import check, errors

if TYPE_CHECKING:
    from discord import Interaction

__all__ = ("is_guild_owner",)


def is_guild_owner():
    async def pred(interaction: Interaction) -> bool:
        if not interaction.guild:
            raise errors.NoPrivateMessage()

        if interaction.guild.owner_id == interaction.user.id:
            return True
        raise errors.CheckFailure("The user is not a owner of the guild.")

    return check(pred)
