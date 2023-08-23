from typing import Any
import discord
from discord.ext import commands
from dispie.prompts import (
    ButtonPrompt,
    TextSelectPrompt,
    ChannelSelectPrompt,
    RoleSelectPrompt,
    UserSelectPrompt,
    MentionableSelectPrompt,
    ModalPrompt,
)

from dispie.embed_creator import EmbedCreator

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is online.")
    await bot.tree.sync()


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
        return await ctx.send(f"You choosed: {prompt.value}")

    await ctx.send("Time out...")


@bot.command()
async def sp(ctx: commands.Context[Any]):
    prompt = TextSelectPrompt(
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


@bot.command()
async def cp(ctx: commands.Context[Any]):
    prompt = ChannelSelectPrompt(
        ctx.author, max_values=10, min_values=3, placeholder="Choose a channel"
    )

    msg = await ctx.send("Select a message!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.channels != None:
        return await ctx.send(
            f"You choosed: {prompt.channels[0].mention if len(prompt.channels) == 1 else ', '.join(i.mention for i in prompt.channels)}"
        )
    await ctx.send("Time out...")


@bot.command()
async def rp(ctx: commands.Context[Any]):
    prompt = RoleSelectPrompt(
        ctx.author, max_values=10, min_values=3, placeholder="Choose a role"
    )

    msg = await ctx.send("Select a role!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.roles != None:
        return await ctx.send(
            f"You choosed: {prompt.roles[0].mention if len(prompt.roles) == 1 else ', '.join(i.mention for i in prompt.roles)}"
        )
    await ctx.send("Time out...")


@bot.command()
async def up(ctx: commands.Context[Any]):
    prompt = UserSelectPrompt(ctx.author, max_values=10, placeholder="Choose an user")

    msg = await ctx.send("Select an user!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.users != None:
        return await ctx.send(
            f"You choosed: {prompt.users[0].mention if len(prompt.users) == 1 else ', '.join(i.mention for i in prompt.users)}"
        )
    await ctx.send("Time out...")


@bot.command()
async def mp(ctx: commands.Context[Any]):
    prompt = MentionableSelectPrompt(
        ctx.author, max_values=10, placeholder="Choose an option"
    )

    msg = await ctx.send("Select an option!", view=prompt)
    prompt.message = msg
    await prompt.wait()
    if prompt.values != None:
        return await ctx.send(
            f"You choosed: {prompt.values[0].mention if len(prompt.values) == 1 else ', '.join(i.mention for i in prompt.values)}"
        )
    await ctx.send("Time out...")


@bot.tree.command()
async def mop(interaction: discord.Interaction):
    prompt = ModalPrompt(title="Test Modal")
    name = prompt.add_input(discord.ui.TextInput(label="Okk"))
    await interaction.response.send_modal(prompt)
    await prompt.wait()
    await interaction.followup.send(f"Your name: {name}")


@bot.command()
async def c(ctx: commands.Context[Any]):
    await EmbedCreator(author=ctx.author).start(ctx)

