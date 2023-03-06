from discord.ext import commands
from dispie.music import MusicClient, Node
from config import token
from pomice import Track
import discord

bot = commands.Bot(command_prefix="", intents=discord.Intents.all())

music = MusicClient(
    bot=bot,
    nodes={
        "host": "127.0.0.1",
        "port"=3030,
        "password"="youshallnotpass",
        "identifier"="MAIN"
    }
)

@bot.event
async def on_ready():
    print("Logged in")

    
bot.run(token)
