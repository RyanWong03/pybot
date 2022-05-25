import discord
import os
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from sympy import *
import requests
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

# @tasks.loop(hours = 0.25)
# async def send_pm():
#     id = 318132313672384512
#     user = client.get_user(id)
#     await user.send("Daily Message")

@client.event
async def on_ready():
    id = 318132313672384512
    discordUser = client.get_user(id)
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
    await discordUser.send('Bot Online')
    print('Bot is ready.')
    #send_pm.start()

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
    team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text() #TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL  tigers
    team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
    team_1_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
    team_2_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[2].get_text()
    await ctx.send(str(team_1))
    await ctx.send(str(team_2))
    await ctx.send("Score: " + str(team_1_score))
    await ctx.send("score: " + str(team_2_score))
    #TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL  twins

@client.command()
async def games(ctx):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text() 
    team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
    team_3 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[2].get_text() 
    team_4 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[3].get_text()
    team_5 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[4].get_text() 
    team_6 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[5].get_text()
    team_7 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[6].get_text() 
    team_8 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[7].get_text()
    team_9 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[8].get_text() 
    team_10 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[9].get_text()
    team_11 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[10].get_text() 
    team_12 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[11].get_text()
    team_13 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[12].get_text() 
    team_14 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[13].get_text()
    # team_15 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[14].get_text()
    # team_16 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[15].get_text() 
    # team_17 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[16].get_text()
    # team_18 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[17].get_text() 
    # team_19 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[18].get_text()
    # team_20 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[19].get_text()
    # team_21 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[20].get_text() 
    # team_22 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[21].get_text()
    # team_23 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[22].get_text() 
    # team_24 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[23].get_text()
    # team_25 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[24].get_text()
    # team_26 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[25].get_text() 
    # team_27 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[26].get_text()
    # team_28 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[27].get_text() 
    # team_29 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[28].get_text()
    team_1_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
    print("games one")
    await ctx.send(str(team_1))
    await ctx.send(str(team_2))
    await ctx.send(str(team_3))
    await ctx.send(str(team_4))
    await ctx.send(str(team_5))
    await ctx.send(str(team_6))
    await ctx.send(str(team_7))
    await ctx.send(str(team_8))
    await ctx.send(str(team_9))
    await ctx.send(str(team_10))
    await ctx.send(str(team_11))
    await ctx.send(str(team_12))
    await ctx.send(str(team_13))
    await ctx.send(str(team_14))

@client.command()
async def gametwo(ctx):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    team_15 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[14].get_text()
    team_16 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[15].get_text() 
    team_17 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[16].get_text()
    team_18 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[17].get_text() 
    team_19 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[18].get_text()
    team_20 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[19].get_text()
    team_21 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[20].get_text() 
    team_22 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[21].get_text()
    team_23 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[22].get_text() 
    team_24 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[23].get_text()
    team_25 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[24].get_text()
    team_26 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[25].get_text() 
    # team_27 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[26].get_text()
    # team_28 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[27].get_text() 
    # team_29 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[28].get_text()
    print("games two")
    await ctx.send(str(team_15))
    await ctx.send(str(team_16))
    await ctx.send(str(team_17))
    await ctx.send(str(team_18))
    await ctx.send(str(team_19))
    await ctx.send(str(team_20))
    await ctx.send(str(team_21))
    await ctx.send(str(team_22))
    await ctx.send(str(team_23))
    await ctx.send(str(team_24))
    await ctx.send(str(team_25))
    await ctx.send(str(team_26))
    # await ctx.send(str(team_27))
    # await ctx.send(str(team_28))
    # await ctx.send(str(team_29))

client.run(os.environ["DISCORD_TOKEN"])