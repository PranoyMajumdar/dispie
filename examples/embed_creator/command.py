import discord
from discord.ext import commands
from dispie import EmbedCreator
from examples.embed_creator.embed_options import options

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.command()
async def embed(ctx: commands.Context):
    """Embed Generator With Default Embed"""
    # Creates a instance of EmbedCreator class
    view = EmbedCreator(bot=bot)
    await ctx.send(embed=view.get_default_embed, view=view)


@bot.command()
async def embed2(ctx: commands.Context):
    """Embed Generator With Default Embed And Author Check So Only The Invoker Can Use The Editor"""
    # Creates a instance of EmbedCreator class
    view = EmbedCreator(bot=bot)

    async def check(interaction: discord.Interaction):
        if interaction.user.id == ctx.author.id:
            return True
        else:
            await interaction.response.send_message(
                f"Only {ctx.author} can use this interaction!", ephemeral=True
            )
            return False

    view.interaction_check = check
    await ctx.send(embed=view.get_default_embed, view=view)


@bot.command()
async def embed3(ctx: commands.Context):
    """Embed Generator With Default Embed And Customized Options
    You can view it in the embed_options.py file also you can customize everything in the embed creator (excepts message responses.)
    """
    # Creates a instance of EmbedCreator class
    view = EmbedCreator(bot=bot, **options)
    await ctx.send(embed=view.get_default_embed, view=view)
