from discord.ext import commands
from dispie import EmbedCreator
from dispie.music import MusicClient, Node
from config import token
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())
client = MusicClient(
     bot=bot,
    nodes={
     "host": "jklef",
     "port": 90,
     "identifier": "ok",
     "password": "ok"
    }

)

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
@bot.event
async def on_ready():
    print("Logged in")
bot.run(token)
