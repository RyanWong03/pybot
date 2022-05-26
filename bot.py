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

@client.command()
async def baseball(ctx):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text() 
    team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
    team_1_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
    team_2_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()
    await ctx.send(str(team_1))
    await ctx.send(str(team_2))
    await ctx.send("Score: " + str(team_1_score))
    await ctx.send("score: " + str(team_2_score))

@client.command()
async def score(ctx, team):
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
    teamtest = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")
    away_team = True
    score_index = 0
    team_index = None

    for i in range(num_teams):
        if teamtest[i].get_text() == str(team):
            score_index = i
            await ctx.send(str(team) + " :" + str(i))    

    print(num_teams)
    if num_teams == 30:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('30 team error bypassed.')
    if num_teams == 28:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('28 team error bypassed')
    if num_teams == 26:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    team_index = tea
                    await ctx.send("team playing" + str(team))
                    if team_index % 2 == 0:
                        away_team = True
                    else:
                        away_team = False

            if away_team == True:
                visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
                home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
                away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
                home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
            if away_team == False:
                visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
                home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
                away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text()
                home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()

            text = """```Scores: 
            """ + str(visitors) + """ : """ + str(away_team_score) + """
            """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
            await ctx.send(text)
        except:
            print('26 team error bypassed')
    if num_teams == 24:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except:
            print('24 team error bypassed')
    if num_teams == 22:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('22 team error bypassed')
    if num_teams == 20:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('20 team error bypassed')
    if num_teams == 18:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('18 team error bypassed')
    if num_teams == 16:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('16 team error bypassed')
    if num_teams == 14:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('14 team error bypassed')
    if num_teams == 12:
        try:
           for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('12 team error bypassed')
    if num_teams == 10:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('10 team error bypassed')
    if num_teams == 8:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('8 team error bypassed')
    if num_teams == 6:
        try:
           for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('6 team error bypassed')
    if num_teams == 4:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('4 team error bypassed')
    if num_teams == 2:
        try:
            for tea in range(num_teams):
                if teamtest[tea].get_text() == str(team):
                    await ctx.send("team playing" + str(team))
        except IndexError:
            print('2 team error bypassed')        
    if num_teams == 0:
        await ctx.send("Nobody is playing today.")

client.run(os.environ["DISCORD_TOKEN"])


# #team_1_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
            # #team_2_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()
            # # score_1 = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
            # # score_2 = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()
            # team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text() 
            # team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
            # team_3 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[2].get_text() 
            # team_4 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[3].get_text()
            # team_5 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[4].get_text() 
            # team_6 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[5].get_text()
            # team_7 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[6].get_text() 
            # team_8 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[7].get_text()
            # team_9 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[8].get_text() 
            # team_10 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[9].get_text()
            # team_11 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[10].get_text() 
            # team_12 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[11].get_text()
            # team_13 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[12].get_text() 
            # team_14 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[13].get_text()
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
            # if team_1 == str(team) or team_2 == str(team) or team_3 == str(team) or team_4 == str(team) or team_5 == str(team) or team_6 == str(team) or team_7 == str(team) or team_8 == str(team) or team_9 == str(team)  or team_10 == str(team)  or team_11 == str(team)  or team_12 == str(team)  or team_13 == str(team)  or team_14 == str(team)  or team_15 == str(team)  or team_16  == str(team) or team_17 == str(team) or team_18 == str(team) or team_19 == str(team) or team_20 == str(team) or team_21 == str(team) or team_22 == str(team) or team_23 == str(team) or team_24 == str(team) or team_25 == str(team) or team_26 == str(team):
            #     await ctx.send(str(team) + " is playing")
            #     #await ctx.send("score: " + str(team_1_score))
            #     #await ctx.send("score2 : " + str(team_2_score))
            # else:
            #     await ctx.send(str(team) + " doesn't exist.")