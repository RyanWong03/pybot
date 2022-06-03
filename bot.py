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
import time

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '$', intents=intents)

def print_lineup(list, str):
    str += "{0}"
    list = [str.format(i) for i in list]
    return list

@client.event
async def on_ready():
    general = client.get_channel(771373922192195627)
    DM = 538897701522112514
    USER = client.get_user(DM)
    id = 318132313672384512
    channel = client.get_channel(789273776105193472) 
    discordUser = client.get_user(id)
    await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
    await discordUser.send('Bot Online')
    print('Bot is ready.')
    #await general.send('L')
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
    yanks_scoring_url = "https://www.espn.com/mlb/playbyplay/_/gameId/401443623" #most likely will need to change daily
    request = requests.get(yanks_scoring_url)
    soup_score = BeautifulSoup(request.text, 'html.parser')
    
    lineup_url = "https://www.baseballpress.com/lineups/" 
    r = requests.get(lineup_url)
    soup_lineup = BeautifulSoup(r.text, 'lxml') 
    lineup_list = []
    pitchers = []

    for tea in range(num_teams):
        if teamtest[tea].get_text() == 'Mets':
            team_index = tea
            if team_index % 2 == 0:
                away_team = True
            else:
                away_team = False

    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S") #24 hour clock, discord time always 4 hours ahead of NA EAST
        time.sleep(1)
        #await channel.send("Message every second")
        #await channel.send(now)

        if away_team == True:
            #print('before game stat')
            game_stat = soup.find_all(class_="GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[team_index // 2].get_text()
            #print('after game stat: ' + game_stat)
        elif away_team == False:
            #print('before game stat')
            game_stat = soup.find_all(class_="GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[(team_index - 1) // 2].get_text()
            #print('after game stat: ' + game_stat)
        if game_stat == 'Final':
            await channel.send("Yankees game over")
        elif game_stat == 'WARMUP' or game_stat == 'Warmup':
            await channel.send("Yankees game starting soon.")
        elif game_stat == '1:05 PM ET' or game_stat == '1:07 PM ET':
            if now == '12:30:00':
                await channel.send(' 12 30')
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
                elif away_team == False:
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
                    
                    await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

                    lineup_list.pop(0)
                    lineup_list.pop(0)
                    n = 9
                    home_list = lineup_list[n:]
                    away_list = lineup_list[:-n]

                    away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    await channel.send(away_lineup)

                    home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    await channel.send(home_lineup)
        elif game_stat == '4:05 PM ET' or game_stat == '4:10 PM ET':
            if now == '15:30:00':
                await channel.send('3 30')
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
                elif away_team == False:
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
                    
                    await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

                    lineup_list.pop(0)
                    lineup_list.pop(0)
                    n = 9
                    home_list = lineup_list[n:]
                    away_list = lineup_list[:-n]

                    away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    await channel.send(away_lineup)

                    home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    await channel.send(home_lineup)
        elif game_stat == '7:05 PM ET' or game_stat == '7:07 PM ET' or game_stat == '7:10 PM ET':
            if now == '18:30:00':
                await channel.send('6 30')
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
                elif away_team == False:
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
                    
                    await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

                    lineup_list.pop(0)
                    lineup_list.pop(0)
                    n = 9
                    home_list = lineup_list[n:]
                    away_list = lineup_list[:-n]

                    away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    await channel.send(away_lineup)

                    home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    await channel.send(home_lineup)
        elif game_stat == '10:05 PM ET' or game_stat == '10:10 PM ET':
            if now == '21:30:00':
                await channel.send('9 30')
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
                elif away_team == False:
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
                    
                    await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

                    lineup_list.pop(0)
                    lineup_list.pop(0)
                    n = 9
                    home_list = lineup_list[n:]
                    away_list = lineup_list[:-n]

                    away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    await channel.send(away_lineup)

                    home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    await channel.send(home_lineup)
        elif game_stat == 'TOP 1':
            await channel.send("Yankees game has started.")
        elif game_stat == 'BOT 5':
            await channel.send('bottom 5 inning')
        
       
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            
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
async def pm(ctx, userId: int, msg: str):
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
            print('yankees team index :' + str(team_index))
            if team_index % 2 == 0:
                away_team = True
            else:
                away_team = False
    
    if away_team == True:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
            home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
            text = """```Scores: 
            """ + str(visitors) + """ : """ + str(away_team_score) + """
            """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
            await ctx.send(text)

        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index:
            time_index = team_index // 2
            print('team index mets: ' + str(team_index))
            print('time index mets: ' + str(time_index))
            game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index].get_text()
            await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
        
    if away_team == False:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            print('yanks team index' + str(team_index))
            away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text()
            home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
            text = """```Scores: 
            """ + str(visitors) + """ : """ + str(away_team_score) + """
            """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
            await ctx.send(text)

        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index: #team index - 1
            time_index = team_index // 2
            print('yankees team index: ' + str(team_index))
            print('yankees time index: ' + str(time_index))
            game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index].get_text()
            await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
        
client.run(os.environ["DISCORD_TOKEN"])