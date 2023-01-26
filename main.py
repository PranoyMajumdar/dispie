from discord.ext import commands
from dispie import EmbedCreator
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.command()
async def test(ctx: commands.Context):
    view = EmbedCreator(bot=bot)
    await ctx.send(embed=view.get_default_embed, view=view)


