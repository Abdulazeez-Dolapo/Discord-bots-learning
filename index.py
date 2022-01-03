import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

# This - intents - is required to grant all permissions to the bot
all_intents = discord.Intents.all()
client = discord.Client(intents=all_intents)


@client.event
async def on_ready() -> None:
    """Handles the event when the Client connects to Discord successfully"""

    guild = discord.utils.get(client.guilds, name=GUILD)
    members = "\n - ".join([member.name for member in guild.members])

    print(f"Guild Members:\n - {members}")
    print(f"{client.user} has connected to {guild.name} with {guild.id} on Discord.")


@client.event
async def on_member_join(member) -> None:
    """Handles the event when a new member joins the Server"""

    print(member)
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi there ${member.name}. Welcome to my Discord server."
    )


@client.event
async def on_message(message) -> None:
    """Handles the event when a new message is sent on the Server"""

    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        "I'm the human form of the 💯 emoji.",
        "Bingpot!",
        (
            "Cool. Cool cool cool cool cool cool cool, "
            "no doubt no doubt no doubt no doubt."
        ),
    ]

    if "99" in message.content.lower():
        random_quote = random.choice(brooklyn_99_quotes)
        await message.channel.send(random_quote)
    elif message.content == "raise-exception":
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs) -> None:
    """Handles the event when any error occurs on the Server."""

    with open("error.log", "a") as f:
        if event == "on_message":
            f.write(f'An error occurred when sending the message "{args[0]}"\n')
        else:
            raise


# Creating a custom Discord client using the class method.
# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f"{self.user} has connected to Discord.")


# client = CustomClient()

client.run(TOKEN)
