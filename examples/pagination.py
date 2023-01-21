from discord.ext import commands
import discord
from dispie import Paginator

bot = commands.Bot(command_prefix='',intents=discord.Intents.all())

@bot.command()
async def page1(ctx: commands.Context):
    """Embeds paginator."""
    embeds = list()
    for i in range(1000):
        embeds.append(discord.Embed(title=f"Page {i+1}"))
    
    pages = Paginator(embeds)
    await pages.start(ctx)


@bot.command()
async def page2(ctx: commands.Context):
    """Description paginator."""
    lst = [f"Number {i+1}" for i in range(100)]
    embeds = list()
    for lines in discord.utils.as_chunks(lst, 5):
        embed = discord.Embed(title='Description paginator', description=f"\n".join(lines))
        embeds.append(embed)
    
    pages = Paginator(embeds)
    await pages.start(ctx)