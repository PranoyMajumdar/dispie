import discord
from discord.ext import commands
from dispie.paginator import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")



@bot.command()
async def field(ctx:commands.Context):
    """
    Pagination using embed fields

    """
    entries = [(f"Tuple Name: - {i}", f"Tuple Value: - {i}") for i in range(100)]
    paginator = Paginator(source=FieldPagePaginator(
        entries=entries,
        description='Pagination with embed fields.',
        title='Dispie Paginator',
        color = 0x303236
    ), ctx=ctx)
    await paginator.paginate()

@bot.command()
async def description(ctx:commands.Context):
    """
    Pagination using embed description

    """
    entries = [f"Number: {i}" for i in range(100)]
    paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        description='Pagination with embed description.',
        title='Dispie Paginator',
        color = 0x303236
    ), ctx=ctx)
    await paginator.paginate()

@bot.command()
async def text(ctx : commands.Context):
    """
    Pagination using text

    """
    text = '\n'.join(f"Number: {i}" for i in range(10000))
    paginator = Paginator(source=TextPaginator(text), ctx=ctx)
    await paginator.paginate()

if __name__ == "__main__":
    bot.run('token')