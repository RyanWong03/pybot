import discord
import os
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

@client.event()
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.listening, name = "Spotify"))
    print('Bot is ready.')

@client.command()
async def pm(self, ctx, user: discord.Member = None, *, message = None):
    if user is None:
        await ctx.send("Need person to send message to.")
    if user is not None:
        if message is None:
            await ctx.send("Need message to send.")
        if message is not None:
            myembed = discord.Embed()
            myembed.add_field(name=f"(ctx.author) sent you:", value=f"(message)")
            myembed.set_footer(text="Testing message")
            await user.send(embed=myembed)

@client.command()
async def talk(ctx):
    await ctx.send("Hello")

client.run(os.environ["DISCORD_TOKEN"])