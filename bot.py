import discord
import os
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
from sympy import *
import requests
from bs4 import BeautifulSoup
import datetime
import lxml

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

def print_lineup(list, str):
    str += "{0}"
    list = [str.format(i) for i in list]
    return list

@client.event
async def on_ready():
    DM = 538897701522112514
    USER = client.get_user(DM)
    id = 318132313672384512
    channel = client.get_channel(789273776105193472) 
    discordUser = client.get_user(id)
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
    await discordUser.send('Bot Online')
    print('Bot is ready.')
    away_score = 0
    away_team_score = 0
    home_score = 0
    home_team_score = 0
    url = 'https://www.mlb.com/'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
    teamtest = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")
    away_team = None
    team_index = None
    yanks_scoring_url = "https://www.espn.com/mlb/playbyplay/_/gameId/401354995" #most likely will need to change daily
    request = requests.get(yanks_scoring_url)
    soup_score = BeautifulSoup(request.text, 'html.parser')
 
    #lineups
    today = datetime.datetime.now()
    test_date = datetime.datetime(2022, 6, 2)
    hrd_date = datetime.datetime(2022, 7, 18, 7, 55)
    asg_date = datetime.datetime(2022, 7, 19)
    lineup_url = "https://www.baseballpress.com/lineups/" 
    r = requests.get(lineup_url)
    soup_lineup = BeautifulSoup(r.text, 'lxml') 
    lineup_list = []
    batting_order = 1
    pitchers = []
    
    #while True: #potential while statement if time is between 5am and 8am or something

    for tea in range(num_teams):
        if teamtest[tea].get_text() == 'Yankees':
            team_index = tea
            if team_index % 2 == 0:
                away_team = True
            else:
                away_team = False

    # if today == hrd_date:
    #     away_team = None
    #     await channel.send("Home Run Derby starts in 5 minutes.")

    # if today == asg_date:
    #     visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text()
    #     home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
    #     away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
    #     home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()

    #     for item in soup_lineup.select("[data-league='NL]:-soup-contains('NL All Stars') .player > a.player-link"):
    #         player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
    #         lineup_list.append(player_name)

    #     pitchers.append(lineup_list[0])
    #     pitchers.append(lineup_list[1])

    #     await channel.send('Starting pitchers:\nAL All Stars: ' + pitchers[0] + '\nNL All Stars: ' + pitchers[1])

    #     lineup_list.pop(0)
    #     lineup_list.pop(0)
    #     n = 9
    #     home_list = lineup_list[n:]
    #     away_list = lineup_list[:-n]

    #     await channel.send('')

    if away_team == True:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-zsc-uqs6qh-0 iNsMPL")[team_index].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapperz-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
        away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
        home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
        
        for item in soup_lineup.select("[data-league='AL']:-soup-contains('Guardians') .player > a.player-link"):
            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
            lineup_list.append(player_name)
        
        pitchers.append(lineup_list[0])
        pitchers.append(lineup_list[1])

        await channel.send('Starting Pitchers:\nYankees: ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])
        
        lineup_list.pop(0)
        lineup_list.pop(0)
        n = 9
        home_list = lineup_list[n:]
        away_list = lineup_list[:-n]

        await channel.send('Yankees Lineup:\n')
        for player in away_list:
            await USER.send(str(batting_order) + ': ' + player)
            await channel.send(str(batting_order) + ': ' + player)
            batting_order += 1
        
        batting_order = 1

        await channel.send(str(home_team) + ' lineup:\n')
        for player in home_list:
            await USER.send(str(batting_order) + ': ' + player)
            await channel.send(str(batting_order) + ': ' + player)
            batting_order += 1

        if away_team_score != away_score:
            scoring_play = soup_score.find_all(class_ = "play atbat-result")[0].get_text()
            await channel.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
            away_score = away_team_score
            
        if home_team_score != home_score:
            scoring_play = soup_score.find_all(class_ = "play atbat-result")[0].get_text()
            await channel.send(str(scoring_play) + str(away_team_score + " - " + str(home_team_score)))
            home_score = home_team_score
            
    if away_team == False:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()

        for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
            if item.get('data-razz') == '':
                player_name = 'Unknown Player'
                lineup_list.append(player_name)
            else:
                player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                lineup_list.append(player_name)
       
        pitchers.append(lineup_list[0])
        pitchers.append(lineup_list[1])
        
        await channel.send('Starting Pitchers:\n' + str(home_team) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

        lineup_list.pop(0)
        lineup_list.pop(0)
        n = 9
        home_list = lineup_list[n:]
        away_list = lineup_list[:-n]

        # away_lineup = print_lineup(away_list, str(batting_order))
        # print(str(visitors) + ' lineup:\n' + '\n'.join(away_lineup))
        # await channel.send(str(visitors) + ' lineup:\n' + '\n'.join(away_lineup))

        # for player in away_list:
        #     await channel.send(str(batting_order) + ': ' + player)
        #     batting_order += 1
        # batting_order = 1

        away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3:""" + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
        await channel.send(away_lineup)
        # home_lineup = print_lineup(home_list, str(batting_order))
        # print('Yankees Lineup:\n' + '\n'.join(home_lineup))
        # await channel.send('Yankees Lineup:\n' + '\n'.join(home_lineup))

        # for player in home_list:
        #     await channel.send(str(batting_order) + ': ' + player)
        #     batting_order += 1

        home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3:""" + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
        await channel.send(home_lineup)

        #while True:
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            #game_stat = soup.find_all(class_="GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[team_index].get_text()
            # if game_stat == 'Final':
            #     await channel.send("Mets game over")
            away_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text())
            home_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text())

        if away_team_score != away_score:
            scoring_play = soup_score.find_all(class_ = "headline scoring")[0].get_text() #play atbat-result
            await channel.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
            #await USER.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
            away_score = away_team_score
            
        if home_team_score != home_score:
            scoring_play = soup_score.find_all(class_ = "headline scoring")[0].get_text()
            await channel.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
            #await USER.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
            home_score = home_team_score

@client.event
async def on_message(message: discord.Message):
    channel = client.get_channel(978743346287759390)
    if message.guild is None and not message.author.bot:
        await channel.send(str(message.author.mention) + " sent " + " "" " + message.content + " "" ")
    await client.process_commands(message)

@client.command()
async def pm(ctx, userId, msg):
    id = userId 
    user = client.get_user(id)
    await ctx.send("Message Sent to " + str(user))
    await user.send(msg)

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
    away_team = None
    team_index = None
    game_start_time = None
    DM = 538897701522112514
    USER = client.get_user(DM)

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

        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index:
            time_index = team_index / 2
            game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index]
            await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
        
        text = """```Scores: 
        """ + str(visitors) + """ : """ + str(away_team_score) + """
        """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
        await ctx.send(text)
        
    if away_team == False:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
        #if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
        away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text()
        home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()

        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index - 1:
            time_index = team_index // 2
            game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index].get_text()
            await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
        
        text = """```Scores: 
        """ + str(visitors) + """ : """ + str(away_team_score) + """
        """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
        await ctx.send(text)
    
client.run(os.environ["DISCORD_TOKEN"])