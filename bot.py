import os
import random
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


help_message = "Sends a random Brooklyn 99 quote"


@bot.command(name="b99", help=help_message)
async def nine_nine(ctx) -> None:
    """Handles the command called by $b99"""
    brooklyn_99_quotes = [
        "I'm the human form of the 💯 emoji.",
        "Bingpot!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
        ),
    ]

    random_quote = random.choice(brooklyn_99_quotes)

    await ctx.send(random_quote)


@bot.command(name="roll_dice", help="Simulates rolling dice.")
async def roll(ctx, number_of_dice: int, number_of_sides: int) -> None:
    dice = [
        str(random.choice(range(1, number_of_sides + 1))) for _ in range(number_of_dice)
    ]

    await ctx.send(", ".join(dice))


@roll.error
async def roll_error(ctx, error) -> None:
    """Handles any error from the `roll_dice` command."""

    if isinstance(error, commands.BadArgument):
        await ctx.send("Arguments not correct...")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")
    else:
        await ctx.send("An error occurred")

    with open("error.log", "a") as f:
        f.write(f"An error occurred when running the command !roll_dice - {error}\n")


@bot.command(name="create-channel")
@commands.has_role("admin")
async def create_channel(ctx, channel_name="real-python"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)

    if not existing_channel:
        print(f"Creating a new channel: {channel_name}")
        await guild.create_text_channel(channel_name)
        await ctx.send(f"Channel - {channel_name} - created successfully 🎉")
    else:
        await ctx.send(
            f"Channel - {channel_name} - already exists. Please try another name."
        )


@create_channel.error
async def create_channel_error(ctx, error) -> None:
    """Handles any error from the `create-channel` command."""

    if isinstance(error, commands.BadArgument):
        await ctx.send("Arguments not correct...")
    elif isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")
    else:
        await ctx.send("An error occurred")

    with open("error.log", "a") as f:
        f.write(
            f"An error occurred when running the command !create-channel - {error}\n"
        )


bot.run(TOKEN)

