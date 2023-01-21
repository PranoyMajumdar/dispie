from discord.ext import commands
import discord

class Nocmd(commands.Cog):
    """The description for Nocmd goes here."""

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Nocmd(bot))
