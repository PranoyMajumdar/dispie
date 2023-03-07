from discord.ext import commands
from dispie.music import MusicClient, Node
from config import token
from pomice import Track
from rich.logging import Handler, RichHandler, Highlighter
import discord

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

music = MusicClient(
    bot=bot,
    nodes=
        {
        "host": "127.0.0.1",
        "port": 3030,
        "password":"youshallnotpass",
        "identifier":"MAIN"
    }
)


discord.utils.setup_logging(
    handler=RichHandler(
        show_time=False
    )
)

database = {
    "channel_id": ...,
    "message_id": ...
}

@bot.event
async def on_message(message: discord.Message):
    if message.id == database['message_id'] and message.channel.id == database['channel_id']:
        await music.handle_on_message(message, database['message_id'])

@bot.event
async def on_ready():
    await music.start_nodes()

@bot.command()
async def setup(ctx: commands.Context, channel: discord.TextChannel):
    msg = await music.setup_player_embed(channel)
    print(msg.id, channel.id)

async def main():
    await bot.start(token)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
