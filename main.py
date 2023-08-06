from typing import Any
import discord
from discord.ext import commands
from dispie.prompts import ButtonPrompt, SelectPrompt

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def bp(ctx: commands.Context[Any]):
    prompt = ButtonPrompt(
        author=ctx.author,
        true_button_label="Hmmmmm",
        false_button_emoji="🖕",
        auto_disable=True,
        timeout=2
    )
    msg = await ctx.send("Choose a bool!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.value != None:
        return await ctx.send(f"You choosed: {prompt.value}")

    await ctx.send("Time out...")


@bot.command()
async def sp(ctx: commands.Context[Any]):
    prompt = SelectPrompt(
        ctx.author,
        [
            discord.SelectOption(label="Ok"),
            discord.SelectOption(label="Not Okay"),
        ],
    )

    msg = await ctx.send("Select a message!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.values != None:
        return await ctx.send(f"You choosed: {prompt.values[0]}")
    await ctx.send("Time out...")


