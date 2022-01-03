import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
all_intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=all_intents)


async def fetch_messages(
    channel: dict, descending: bool, include_bot: bool, max_size: int
) -> dict:
    members = {}

    async for message in channel.history(limit=None):
        author = message.author

        if not include_bot and author.bot:
            continue

        if author.id in members:
            count = members[author.id]["count"] + 1
            members[author.id] = {"count": count, "name": author.name}
        else:
            members[author.id] = {"count": 1, "name": author.name}

    sorted_members = dict(
        sorted(members.items(), key=lambda item: item[1]["count"], reverse=descending)[
            :max_size
        ]
    )
    return sorted_members


def format_messages(messages: dict) -> str:
    message = ""

    for channel_name in messages:
        channel_string = f"{channel_name} => "
        author_list = ""

        if not messages[channel_name]:
            author_list += "no messsages"
        else:
            for author_id in messages[channel_name]:
                author = messages[channel_name][author_id]
                name = author["name"]
                count = author["count"]
                message_spelling = "message" if count <= 1 else "messsages"

                author_list += f"\n   - {name} -> {count} {message_spelling}"

        message += f"{channel_string} {author_list} \n"

    return message


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


help_message = "View leaderboard of users with the highest messages posted on the channels of the server"


@bot.command(name="leaderboard", help=help_message)
@commands.has_role("admin")
async def view_leaderboard(
    ctx,
    channel_name: str = "all",
    descending: bool = True,
    include_bot: bool = False,
    max_size: int = 3,
) -> None:
    """View leaderboard of users with the highest messages posted on the channels of the server"""

    channels = {}

    for channel in ctx.guild.text_channels:
        channels[channel.name] = channel

    messages = {}

    if channel_name == "all":
        for channel in channels:
            messages[channel] = await fetch_messages(
                channels[channel], descending, include_bot, max_size
            )
    elif channel_name in channels:
        messages[channel_name] = await fetch_messages(
            channels[channel_name], descending, include_bot, max_size
        )
    else:
        await ctx.send("Channel does not exist")

    message_list = format_messages(messages)
    await ctx.send(message_list)

    print(message_list)


@view_leaderboard.error
async def view_leaderboard_error(ctx, error) -> None:
    """Handles any error from the `leaderboard` command."""

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Supplied arguments not correct")
    else:
        await ctx.send("An error occurred when viewing leaderboard.")

    print(error)


bot.run(TOKEN)

# Message Model
# <Message
#     id=926096509970284556
#     channel=<TextChannel
#         id=923931412481073163
#         name='test-channel'
#         position=1
#         nsfw=False
#         news=False
#         category_id=923914842727936051
#     >
#     type=<MessageType.default: 0>
#     author=<Member
#         id=588331362294038538
#         name='Pernambucano'
#         discriminator='1060'
#         bot=False
#         nick=None
#         guild=<Guild
#             id=923914842727936050
#             name='bot_learning_server'
#             shard_id=None
#             chunked=True
#             member_count=3
#         >
#     >
#     flags=<MessageFlags value=0>
# >
