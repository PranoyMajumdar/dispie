from discord.ext import commands
from dispie import EmbedCreator
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.command()
async def test(ctx: commands.Context):
    embed = discord.Embed(description="Customize me!")
    view = EmbedCreator(channel=ctx.channel, bot=bot, embed=embed)  # type: ignore
    await ctx.send(embed=embed, view=view)



