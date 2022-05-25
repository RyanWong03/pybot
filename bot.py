import discord
import os
from discord.ext import commands
from discord.utils import get
from sympy import *
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

@client.event
async def on_ready():
    id = 318132313672384512
    discordUser = client.get_user(id)
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
    await discordUser.send('Bot Online')
    print('Bot is ready.')

@client.event
async def on_message(message: discord.Message):
    channel = client.get_channel(978743346287759390)
    if message.guild is None and not message.author.bot:
        await channel.send(str(message.author.mention) + " sent " + " "" " + message.content + " "" ")
    await client.process_commands(message)

@client.command()
async def pm(ctx, userId: int, msg: str):
    id = userId 
    user = client.get_user(id)
    await ctx.send("Message Sent to " + str(user))
    await user.send(msg)

@client.command()
async def add(ctx, a: int, b: int):
    print('adding')
    await ctx.send(a + b)

@client.command()
async def diff(ctx, expression: str, letter: str):
    #init_printing()
    x, y, z = symbols('x y z')
    exp = expression
    print('differentiating')
    await ctx.send(diff(exp, letter))

# @client.command()
# async def test(ctx, *, exp: str):
#     #calc = eval(exp)
#     #await ctx.send('Math: {}\nAnswer: {}'.format(exp, calc))
#     return None

@client.command()
async def cricket(ctx):
    
    # cricbuzz url to get score
    url='https://www.cricbuzz.com/'
    # request data from cricbuzz
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    team_1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[2].get_text()
    team_2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[3].get_text()
    team_1_score = soup.find_all(class_ = "cb-ovr-flo")[9].get_text()
    team_2_score = soup.find_all(class_ = "cb-ovr-flo")[11].get_text()
    # print team names and scores
    print(team_1, ":", team_1_score)
    print(team_2, ":", team_2_score)
    await ctx.send(str(team_1) + ":" + str(team_1_score))
    await ctx.send(str(team_2) + ":" + str(team_2_score))

@client.command()
async def baseball(ctx):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[4].get_text() #TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL  tigers
    team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[5].get_text()
    await ctx.send(str(team_1))
    await ctx.send(str(team_2))
    #TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL  twins

client.run(os.environ["DISCORD_TOKEN"])