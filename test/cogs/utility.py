from discord.ext import commands
import discord

class Utility(commands.Cog):
    """The description for Utility goes here."""
    EMOJI = '🔮'
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx):
        ...
    @commands.command()
    async def userinfo(self, ctx):
        ...
    
    @commands.command()
    async def serverinfo(self, ctx):
        ...
    
    @commands.command()
    async def roleinfo(self, ctx):
        ...
    
    @commands.command()
    async def ownerinfo(self, ctx):
        ...
    
    @commands.command()
    async def botinfo(self, ctx):
        ...
    @commands.group()
    async def group(self, ctx):
        ...
    
    @group.command()
    async def subgroup2(self, ctx):
        ...
    
    @group.command()
    async def subgroup3(self, ctx):
        ...

async def setup(bot):
    await bot.add_cog(Utility(bot))
