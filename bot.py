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
    team_2_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()
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

@client.command()
async def score(ctx, team):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
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
    team_27 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[26].get_text()
    # team_28 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[27].get_text() 
    # team_29 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[28].get_text()
    # team_30 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[29].get_text()

    if num_teams == 30:
        await ctx.send("under 30 teams")
        # if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team) or team_23 == str(team) or team_24 == str(team) or team_25 == str(team) or team_26 == str(team) or team_27 == str(team) or team_28 == str(team) or team_29 == str(team) or team_30 == str(team):
        #     await ctx.send(str(team) + " is playing")
        # else:
        #     await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 28:
        await ctx.send("under 28")
        # if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team) or team_23 == str(team) or team_24 == str(team) or team_25 == str(team) or team_26 == str(team) or team_27 == str(team) or team_28 == str(team):
        #     await ctx.send(str(team) + " is playing")
        # else:
        #     await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 26:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team) or team_23 == str(team) or team_24 == str(team) or team_25 == str(team) or team_26 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 24:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team) or team_23 == str(team) or team_24 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 22:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 20:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 18:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 16:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 14:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 12:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 10:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team) or team_10 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 8:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 6:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 4:
        if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 2:
        if team_1 == str(team) or team_2 == str(team):
            await ctx.send(str(team) + " is playing")
        else:
            await ctx.send(str(team) + " doesn't exist.")
    if num_teams == 0:
        await ctx.send("Nobody is playing today.")
    else:
        await ctx.send("testing")
    
    await ctx.send("Number of games today: " + str(num_teams))
    #await ctx.send(str(team) + " is not playing")
    #await ctx.send(len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")))

@client.command()
async def debug(ctx):
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
    team_27 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[26].get_text()
    team_28 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[27].get_text() 
    team_29 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[28].get_text()
    team_30 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[29].get_text()

    if team_1 or team_2 or team_3 or team_4 or team_5 or team_6 or team_7 or team_8 or team_9 or team_10 or team_11 or team_12 or team_13 or team_14 or team_15 or team_16 or team_17 or team_18 or team_19 or team_20 or team_21 or team_22 or team_23 or team_24 or team_25 or team_26 or team_27 or team_28 or team_29 or team_30 == "test":
        await ctx.send("Nationals are playing")
    await ctx.send("nobody is playing")

client.run(os.environ["DISCORD_TOKEN"])