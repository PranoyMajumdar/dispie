from typing import Any
import discord
from discord.ext import commands
from dispie.prompts import ButtonPrompt

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
        timeout=2,
    )
    msg = await ctx.send("Choose a bool!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.value != None:
        await ctx.send(f"You choosed: {prompt.value}")
        return await msg.delete()
    await ctx.send("Time out...")


bot.run(
    token="MTA5MjM3NDk5MjA3Njk0NzUwOA.GEjah4.6dU3JGacZTRQ47IecynQSVx-7NZG9etrRSrTm4"
)
