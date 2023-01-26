from discord.ext import commands
from dispie import EmbedCreator
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.command()
async def test(ctx: commands.Context):
    embed = discord.Embed(title='This is title',description="Use the dropdown menu to edit my sections!")
    embed.set_author(name='Welcome to embed builder.', icon_url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?")
    embed.set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?")
    embed.set_image(url="https://imageup.me/images/e44472bd-d742-4d39-8e25-b8ae762160ae.png")
    embed.set_footer(text='Footer', icon_url="https://cdn.iconscout.com/icon/premium/png-512-thumb/panel-6983404-5721235.png?")
    view = EmbedCreator(bot=bot, embed=embed)
    await ctx.send(embed=embed, view=view)

