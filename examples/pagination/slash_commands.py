import discord
from discord.ext import commands
from dispie.paginator import Paginator, DescriptionEmbedPaginator, FieldPagePaginator, TextPaginator
from discord import app_commands
intents = discord.Intents.default()
intents.message_content = True


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)


    async def setup_hook(self):
        await self.tree.sync()
        print(f"Logged in as {self.user.name} (ID: {self.user.id})")
    


bot = Bot()



@bot.tree.command()
async def field(interaction: discord.Interaction):
    """
    Pagination using embed fields
    """
    ephemeral = False # If you want to make the response ephemeral then changed it to True
    entries = [(f"Tuple Name: - {i}", f"Tuple Value: - {i}") for i in range(100)]
    paginator = Paginator(source=FieldPagePaginator(
        entries=entries,
        description='Pagination with embed fields.',
        title='Dispie Paginator',
        color = 0x303236
    ), ctx=interaction)
    await paginator.paginate(ephemeral=ephemeral)


@bot.tree.command()
async def description(interaction: discord.Interaction):
    """
    Pagination using embed description

    """
    ephemeral = False # If you want to make the response ephemeral then changed it to True [f"Number: {i}" for i in range(100)]
    entries = [f"Number: {i}" for i in range(100)]
    paginator = Paginator(source=DescriptionEmbedPaginator(
        entries=entries,
        description='Pagination with embed description.',
        title='Dispie Paginator',
        color = 0x303236
    ), ctx=interaction)
    await paginator.paginate(ephemeral=ephemeral)

@bot.tree.command()
async def text(interaction : discord.Interaction):
    """
    Pagination using text

    """
    ephemeral = False # If you want to make the response ephemeral then changed it to True [f"Number: {i}" for i in range(100)]
    text = '\n'.join(f"Number: {i}" for i in range(10000))
    paginator = Paginator(source=TextPaginator(text), ctx=interaction)
    await paginator.paginate(ephemeral=ephemeral)
if __name__ == "__main__":
    bot.run('token')