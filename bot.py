import discord
import os
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

@client.event
async def on_ready():
    id = 318132313672384512
    discordUser = client.get_user(id)
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.listening, name = "Spotify"))
    await discordUser.send('Bot Online')
    print('Bot is ready.')

@client.event
async def on_message(message: discord.Message):
    channel = client.get_channel(978743346287759390)
    if message.guild is None and not message.author.bot:
        await channel.send(str(message.author.mention) + " sent " + message.content)

# @client.command()
# async def pm(self, ctx, user: discord.Member = None, *, message = None):
#     if user is None:
#         await ctx.send("Need person to send message to.")
#     if user is not None:
#         if message is None:
#             await ctx.send("Need message to send.")
#         if message is not None:
#             myembed = discord.Embed()
#             myembed.add_field(name=f"(ctx.author) sent you:", value=f"(message)")
#             myembed.set_footer(text="Testing message")
#             await user.send(embed=myembed)

@client.command()
async def talk(ctx):
    await ctx.send("Hello")

@client.command()
async def test(ctx):
    await ctx.send("bot is working")

@client.command()
async def pm(ctx, userId: int, msg: str):
    id = userId #538897701522112514
    user = client.get_user(id)
    await ctx.send("Message Sent to " + str(user))
    await user.send(msg)

@client.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)

client.run(os.environ["DISCORD_TOKEN"])