from discord.ext import commands
from dispie import EmbedCreator
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())


@bot.command()
async def test(ctx: commands.Context):
    view = EmbedCreator(bot=bot)
    async def check(interaction: discord.Interaction):
            if interaction.user.id == ctx.author.id:
                return True
            else:
                await interaction.response.send_message(f"Only {ctx.author} can use this interaction!", ephemeral=True)
                return False
    view.interaction_check = check
    await ctx.send(embed=view.get_default_embed, view=view)


