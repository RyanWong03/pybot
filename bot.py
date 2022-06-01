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

@client.event
async def on_ready():
    DM = 538897701522112514
    USER = client.get_user(DM)
    id = 318132313672384512
    channel = client.get_channel(789273776105193472) 
    discordUser = client.get_user(id)
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
    yanks_scoring_url = "https://www.mlb.com/gameday/nationals-vs-mets/2022/06/01/662457#game_state=live,game_tab=,game=662457" #most likely will need to change daily
    request = requests.get(yanks_scoring_url)
    soup_score = BeautifulSoup(request.text, 'html.parser')
 
    #lineups
    today = datetime.datetime.now()
    test_date = datetime.datetime(2022, 6, 2)
    hrd_date = datetime.datetime(2022, 7, 18, 7, 55)
    asg_date = datetime.datetime(2022, 7, 19)
    lineup_url = "https://www.baseballpress.com/lineups/2022-05-31" 
    r = requests.get(lineup_url)
    soup_lineup = BeautifulSoup(r.text, 'lxml') 
    lineup_list = []
    batting_order = 1
    pitchers = []
    #example gameday live link  https://www.mlb.com/gameday/orioles-vs-red-sox/2022/05/27/663276#game_state=live,game_tab=,game=663276

    #while True: #potential while statement if time is between 5am and 8am or something
    #if today == test_date:
    await channel.send("Test message. ")
    #else:
        #await channel.send("Today is not today. ")

    for tea in range(num_teams):
        if teamtest[tea].get_text() == 'Mets':
            team_index = tea
            if team_index % 2 == 0:
                away_team = True
            else:
                away_team = False

#sc-hTRkXV jnJnQf
#GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY
    if today == hrd_date:
        away_team = None
        await channel.send("Home Run Derby starts in 5 minutes.")

    if today == asg_date:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
        away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
        home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()

        for item in soup_lineup.select("[data-league='NL]:-soup-contains('NL All Stars') .player > a.player-link"):
            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
            lineup_list.append(player_name)

        pitchers.append(lineup_list[0])
        pitchers.append(lineup_list[1])

        await channel.send('Starting pitchers:\nAL All Stars: ' + pitchers[0] + '\nNL All Stars: ' + pitchers[1])

        lineup_list.pop(0)
        lineup_list.pop(0)
        n = 9
        home_list = lineup_list[n:]
        away_list = lineup_list[:-n]

        await channel.send('')
    if away_team == True:
        visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
        home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
        away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
        home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
        
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
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            
            away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text()
            home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()

        try:
            for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
                if item.get('data-razz') == '':
                    player_name = 'Unknown Player'
                    lineup_list.append(player_name)
                else:
                    player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                    lineup_list.append(player_name)
        except:
            print('soup error')

        pitchers.append(lineup_list[0])
        pitchers.append(lineup_list[1])
        
        await channel.send('Starting Pitchers:\n' + str(home_team) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

        lineup_list.pop(0)
        lineup_list.pop(0)
        n = 9
        home_list = lineup_list[n:]
        away_list = lineup_list[:-n]

        await channel.send(str(visitors) + ' lineup:\n')
        for player in away_list:
            await channel.send(str(batting_order) + ': ' + player)
            batting_order += 1
        text = """```1: 
        """ + away_list[0] + """ : """ + str(away_team_score) + """
        """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
        
        batting_order = 1

        await channel.send('Yankees Lineup:\n')
        for player in home_list:
            await channel.send(str(batting_order) + ': ' + player)
            batting_order += 1
        while True:
            if away_team_score != away_score:
                scoring_play = soup_score.find_all(class_ = "play atbat-result")[0].get_text()
                await channel.send(str(scoring_play) + str(away_team_score + " - " + str(home_team_score)))
                away_score = away_team_score
                
            if home_team_score != home_score:
                scoring_play = soup_score.find_all(class_ = "play atbat-result")[0].get_text()
                await channel.send(str(scoring_play) + str(away_team_score + " - " + str(home_team_score)))
                home_score = home_team_score

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
async def pm(ctx, userId, msg):
    id = userId 
    user = client.get_user(id)
    await ctx.send("Message Sent to " + str(user))
    await user.send(msg)

@client.command()
async def add(ctx, a, b):
    print('adding')
    await ctx.send(a + b)

@client.command()
async def diff(ctx, expression, letter):
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
        if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
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
        
    #await USER.send(str(team) + " game hasn't started yet. They will play at 7:15PM EST")

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