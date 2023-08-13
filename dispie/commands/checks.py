from __future__ import annotations

from typing import Any

from discord.ext import commands


__all__ = ("is_guild_owner",)


def is_guild_owner():
    async def pred(ctx: commands.Context[Any]) -> bool:
        if not ctx.guild:
            raise commands.NoPrivateMessage()

        if ctx.guild.owner_id == ctx.author.id:
            return True
        raise commands.CheckFailure("The user is not a owner of the guild.")

    return commands.check(pred)
