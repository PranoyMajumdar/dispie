from discord.ext import commands
import discord

class Images(commands.Cog):
    """The description for Images goes here."""
    EMOJI = '🖼️'
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blure(self, ctx):
        ...
    
    @commands.command()
    async def bw(self, ctx):
        ...
    
    @commands.command()
    async def colour(self, ctx):
        ...
    
    @commands.command()
    async def image(self, ctx):
        ...
        
    @commands.command()
    async def crop(self, ctx):
        ...
async def setup(bot):
    await bot.add_cog(Images(bot))
