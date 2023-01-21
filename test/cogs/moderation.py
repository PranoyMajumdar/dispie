from discord.ext import commands
import discord

class Moderation(commands.Cog):
    """The description for Moderation goes here."""
    EMOJI = '🔨'
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx):
        ...
    @commands.command()
    async def unban(self, ctx):
        ...
    @commands.command()
    async def kick(self, ctx):
        ...
    
    @commands.command()
    async def mute(self, ctx):
        ...
    
    @commands.command()
    async def unmute(self, ctx):
        ...
    
    @commands.command()
    async def role(self, ctx):
        ...
async def setup(bot):
    await bot.add_cog(Moderation(bot))
