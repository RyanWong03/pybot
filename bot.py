import discord
import os
from discord.ext import commands
from discord.ext import tasks
import requests
import datetime
from datetime import timedelta
import time
import statsapi
import json
import players
import sys
import dateutil.parser
import calendar
from bs4 import BeautifulSoup
import lxml
 #add click more button for pitching line fix local time
# intents = discord.Intents.default()
# intents.members = True
# client = commands.Bot(command_prefix = '$', intents=intents)

class TestFunctions:
    async def wait_for_response(self, message, user_response, wait_time):
        response_found = False
        message_time = datetime.datetime.utcnow()
        message_time = message_time - timedelta(seconds = 2)

        for wait in range(1, wait_time):
            if response_found:
                break;
            
            time.sleep(1)
            raw_msg_list = await message.channel.history(limit = 5).flatten()
            msg_list = []
            for msgs in raw_msg_list:
                if msgs.author.bot == False and msgs != message:
                    msg_list.append(msgs)
            
            if not response_found:
                for history in range(0, len(msg_list)):
                    if msg_list[history].author == message.author:
                        if msg_list[history].created_at > message_time:
                            if user_response.upper() in msg_list[history].content.upper():
                                response_found = True
                                return True
        
        return False

    async def prompt_team(self, message, search_term, teams):
        if len(teams) > 1:
            discord_formatted_string = '>>> I found ' + str(len(teams)) + ' matches for \'' + search_term + '\' Enter the number for the team you want \n'

            for index in range(len(teams)):
                if index < len(teams):
                    append_string = ' ' + str(index + 1) + ': ' + teams[index]['name'] + '\n'
                else:
                    append_string = ' ' + str(index + 1) + ': ' + teams[index]['name']
                
                discord_formatted_string = discord_formatted_string + append_string
            await message.channel.send(discord_formatted_string)

            message_time = datetime.datetime.utcnow()
            time.sleep(2)
            team_selected_index = 0

            for wait in range(1,10):
                if team_selected_index != 0:
                    break;
                
                time.sleep(1)
                message_list = await message.channel.history(limit=2).flatten()

                if team_selected_index == 0:
                    for history in range(0, len(message_list)):
                        if message_list[history].author == message.author:
                            if message_list[history].created_at > message_time:
                                if message_list[history].content.isdigit():
                                    if int(message_list[history].content) <= len(teams) and int(message_list[history].content) != 0:
                                        team_selected_index = int(message_list[history].content)
                                        team_selected = teams[team_selected_index - 1]
                                        break
                                    else:
                                        await message.channel.send('%s is not a valid number start over' % str(message_list[history].content))
                                        return
                                else:
                                    await message.channel.send('%s is not a number start over' % message_list[history].content)
                                    return
            
            if team_selected_index == 0:
                await message.channel.send('start over when ready blah')
                return
            else:
                return team_selected

    async def get_team(self, search_name, message):
        teams_returned = statsapi.lookup_team(search_name)
        if len(teams_returned) > 1:
            team_selected = await self.prompt_team(message, search_name, teams_returned)
        elif len(teams_returned) == 1:
            team_selected = teams_returned[0]
        elif len(teams_returned) == 0:
            await message.channel.send('i cant find teams using\'' + search_name + '\'')
            return
        return team_selected

    async def get_team_no_msg(self, team_name):
        teams_returned = statsapi.lookup_team(team_name)
        team_selected = teams_returned[0]
        return team_selected

    async def wait_for_number(self, message, limit, waitTime):
        response_num = -1
        message_time = datetime.datetime.utcnow()
        message_time = message_time - timedelta(seconds=2)

        for wait in range(1, waitTime):
            if response_num != -1:
                break;
            raw_message_list = await message.channel.history(limit=5).flatten()
            message_list = []

            for messages in raw_message_list:
                if messages.author.bot is False and messages.content != message.content:
                    message_list.append(messages)

            if response_num == -1 and len(message_list) > 0:
                for history in range(0, len(message_list)):
                    if message_list[history].author == message.author:
                        if message_list[history].created_at > message_time:
                            if message_list[history].content.isdigit():
                                if int(message_list[history].content) <= limit and int(message_list[history].content) > 0:
                                    response_num = int(message_list[history].content)
                                    return response_num
                                else:
                                    await message.channel.send('%s is not a valid num, start over' % str(message_list[history].content))
                                    return
                            else:
                                await message.channel.send('%s is not a num, start over' % message_list[history].content)
                                return
            
            time.sleep(1)
        
        if response_num == -1:
            await message.channel.send('I\'m getting bored waiting for you, start over when you\'re ready.')
            return
            
    async def send_get_request(self, url):
        requests_headers = {'Content-Type': 'application/json'}
        response = requests.get(url, requests_headers)
        return response
    
    def get_local_time(self, date_time_string):
        game_time_utc = dateutil.parser.parse(date_time_string)
        game_time_utc = game_time_utc.replace(tzinfo=dateutil.tz.tzutc())
        return game_time_utc.astimezone(dateutil.tz.tzlocal()) 

class EmbedFunctions:
    testFunctions = TestFunctions()
    async def scoring_plays_embed(self, game, channel):
        if type(game) == list:
            game = game[0]
        
        game_time_local = self.testFunctions.get_local_time(game['game_datetime'])
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        game_type = game['game_type']

        scoring_embed = discord.Embed()
        scoring_embed.title = '**Somebody Scored**'
        scoring_embed.type = 'rich'
        scoring_embed.color = discord.Color.dark_blue()
        #scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'], inline=False)

        if game_type != 'S':
            scoringPlaysList = statsapi.game_scoring_play_data(game['game_id'])
            scoringPlays = scoringPlaysList['plays']

            if len(scoringPlays) > 0:
                scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'],
                                     inline=False)
            await channel.send(embed=scoring_embed, tts=False)
            return
        else:
            await channel.send(embed=scoring_embed, tts=False)
            return

    async def scheduled_game_embed(self, game, message):
        if type(game) == list:
            game = game[0]

        game_time_local = self.testFunctions.get_local_time(game['game_datetime'])
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        game_type = game['game_type']

        if len(home_team) > 0:
            home_team_short = home_team[0]['fileCode'].upper()
            home_prob = game['home_probable_pitcher']
        else:
            home_team_short = 'N/A'
            home_prob = 'N/A'
        
        if len(away_team) > 0:
            away_team_short = away_team[0]['fileCode'].upper()
            away_prob = game['away_probable_pitcher']
        else:
            away_team_short = 'N/A'
            away_prob = 'N/A'
        
        scheduled_embed = discord.Embed()
        scheduled_embed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
        scheduled_embed.type = 'rich'
        scheduled_embed.color = discord.Color.dark_blue()
        scheduled_embed.add_field(name = 'Game Status:', value = game['status'], inline = False)
        scheduled_embed.add_field(name = 'Start Time: ', value = game_time_local.strftime('%-I:%M%p' + ' ET'), inline = False)
        
        if not home_prob:
            home_prob = 'Unannounced'
        
        scheduled_embed.add_field(name = home_team_short + ' Probable:', value = home_prob, inline = True)
        
        if not away_prob:
            away_prob = 'Unannounced'
        
        scheduled_embed.add_field(name = away_team_short + ' Probable:', value = away_prob, inline = True)

        await message.channel.send(content = 'Scheduled Game on ' + game_time_local.strftime('%m/%d/%Y') + ':', embed = scheduled_embed)
        await message.channel.send(game_time_local.strftime('%m/%d/%Y'))

    async def final_game_embed(self, game, message):
        if type(game) == list:
            game = game[0]

        game_time_local = self.testFunctions.get_local_time(game['game_datetime'])
        final_status_list = ["Final", "Game Over", "Completed Early"]

        if any(game_status in game['status'] for game_status in final_status_list):
            finalGameEmbed = discord.Embed()
            finalGameEmbed.type = 'rich'
            finalGameEmbed.color = discord.Color.dark_blue()

            # Add the fields with game info
            finalGameEmbed.add_field(name='**' + game['away_name'] + '** vs **' + game['home_name'] + '**\n',
                                        value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
            # Check for a valid key and value
            if 'winning_pitcher' in game and game['winning_pitcher'] != None:
                finalGameEmbed.add_field(name='Winning Pitcher:', value=game['winning_pitcher'], inline=True)
            if 'losing_pitcher' in game and game['losing_pitcher'] != None:
                finalGameEmbed.add_field(name='Losing Pitcher:', value=game['losing_pitcher'], inline=True)
            if 'save_pitcher' in game and game['save_pitcher'] != None:
                finalGameEmbed.add_field(name='Save:', value=game['save_pitcher'], inline=False)

            await message.channel.send(content='Final score from ' + game_time_local.strftime('%m/%d/%Y'),
                                        embed=finalGameEmbed, tts=False)
        else:
            finalScoreString = '**' + game['home_name'] + '** vs **' + game['away_name'] + '**\n'

            finalScoreString = finalScoreString + 'Game on ' + game_time_local.strftime('%m/%d/%Y') + ' **' + game[
                'status'] + '**'

            await message.channel.send(content=finalScoreString, tts=False)

    async def live_game_embed(self, game, message):
        if type(game) == list:game = game[0]

        homeTeam = statsapi.lookup_team(game['home_name'])
        awayTeam = statsapi.lookup_team(game['away_name'])

        homeTeamShort = homeTeam[0]['fileCode'].upper()
        awayTeamShort = awayTeam[0]['fileCode'].upper()
        
        context_params = {'gamePk': game['game_id']}
        game_context_metrics = statsapi.get(endpoint = 'game_contextMetrics', params=context_params)
        game_type = game_context_metrics['game']['gameType']

        scoreEmbed = discord.Embed()

        # Regular Season
        if game_type == 'R':
            scoreEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
        # Wildcard
        elif game_type == 'F':
            # Check if the game is a tiebreaker
            if game_context_metrics['game']['tiebreaker'] == 'N':
                scoreEmbed.title = '**Wildcard Game**\n\n**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
            else:
                scoreEmbed.title = '**Wildcard Tiebreaker Game**\n\n**' + game['away_name'] + '** vs **' + game[
                    'home_name'] + '**'
        # Division Series
        elif game_type == 'D':
            homeRecordString = str(game_context_metrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['home']['leagueRecord']['losses'])
            awayRecordString = str(game_context_metrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['away']['leagueRecord']['losses'])
            scoreEmbed.title = '**Division Series Game ' + str(
                game_context_metrics['game']['seriesGameNumber']) + '**\n\n**' + game[
                                   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
                                   'home_name'] + '**(' + homeRecordString + ')'
        # League Championship Series
        elif game_type == 'L':
            homeRecordString = str(game_context_metrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['home']['leagueRecord']['losses'])
            awayRecordString = str(game_context_metrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['away']['leagueRecord']['losses'])
            scoreEmbed.title = '**League Championship Series Game ' + str(
                game_context_metrics['game']['seriesGameNumber']) + '**\n\n**' + game[
                                   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
                                   'home_name'] + '**(' + homeRecordString + ')'
        # World Series
        elif game_type == 'W':
            homeRecordString = str(game_context_metrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['home']['leagueRecord']['losses'])
            awayRecordString = str(game_context_metrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['away']['leagueRecord']['losses'])
            scoreEmbed.title = '**World Series Game ' + str(
                game_context_metrics['game']['seriesGameNumber']) + '**\n\n**' + game[
                                   'away_name'] + '**(' + awayRecordString + ') vs ' + '**' + game[
                                   'home_name'] + '**(' + homeRecordString + ')'
        # Spring Training
        elif game_type == 'S':
            homeRecordString = str(game_context_metrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['home']['leagueRecord']['losses'])
            awayRecordString = str(game_context_metrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
                game_context_metrics['game']['teams']['away']['leagueRecord']['losses'])
            scoreEmbed.title = '**Spring Training**\n\n**' + game['away_name'] + '** vs **' + game['home_name'] + '**'
        else:
            scoreEmbed.title = '**' + game['away_name'] + '** vs **' + game['home_name'] + '**'

        scoreEmbed.type = 'rich'
        scoreEmbed.color = discord.Color.dark_blue()

        scoreEmbed.add_field(name='**' + game['inning_state'] + ' ' + str(game['current_inning']) + '**',
                             value='```js\n' + statsapi.linescore(game['game_id']) + '```', inline=False)
        homeWinProb = '{:.1f}'.format(game_context_metrics['homeWinProbability'])
        awayWinProb = '{:.1f}'.format(game_context_metrics['awayWinProbability'])
        scoreEmbed.add_field(name='**Win Probability**',
                             value=awayTeamShort + ' ' + awayWinProb + ' - ' + homeTeamShort + ' ' + homeWinProb + '%')
        
        if game_type != 'S':

            scoringPlaysList = statsapi.game_scoring_play_data(game['game_id'])
            scoringPlays = scoringPlaysList['plays']

            if len(scoringPlays) > 0:
                scoreEmbed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'],
                                     inline=False)
                if len(scoringPlays) > 1:
                    scoreEmbed.set_footer(text='Reply with \'more\' in 30 seconds to see all scoring plays')
            await message.channel.send(embed=scoreEmbed, tts=False)

            if len(scoringPlays) > 1:
                if await self.testFunctions.wait_for_response(message, 'more', 30):
                    allPlaysEmbed = discord.Embed()
                    allPlaysEmbed.type = 'rich'
                    allPlaysEmbed.color = discord.Color.dark_blue()
                    scoring_plays_string = ""
                    for index, plays in enumerate(scoringPlays):
                        scoring_plays_string = scoring_plays_string + str(index + 1) + '. ' + plays['result']['description'] + '\n\n'
                    allPlaysEmbed.add_field(name='**All scoring plays**',
                                            value=scoring_plays_string, inline=False)
                    await message.channel.send(embed=allPlaysEmbed, tts=False)
                    return
                else:
                    return
            return
        else:
            await message.channel.send(embed=scoreEmbed, tts=False)
            return
    
    async def generic_Game_Embed(self, game, message):
        # If for some reason we get a list, take the first object
        if type(game) == list:
            game = game[0]

        # Get the UTC datetime string
        gameTimeLocal = self.testFunctions.get_Local_Time(game['game_datetime'])

        # Create the final game embed object
        genricGameEmbed = discord.Embed()
        genricGameEmbed.type = 'rich'
        genricGameEmbed.color = discord.Color.dark_blue()

        # Add the fields with game info
        genricGameEmbed.add_field(name='**' + game['away_name'] + '** vs **' + game['home_name'] + '**\n',
                                 value='Game on ' + gameTimeLocal.strftime('%m/%d/%Y') + ' Status: ' + game['status'], inline=False)

        await message.channel.send(embed=genricGameEmbed)

    async def playoff_Series_Embed(self, series, message):
        try:
            # Create a list of the games in the series
            seriesGames = series['games']

            # Get the game ID of the last game in the series
            #lastGameId = seriesGames[len(seriesGames) - 1]['gamePk']


            #contextParams = {'gamePk': lastGameId}
            #game_contextMetrics = statsapi.get(endpoint='game_contextMetrics', params=contextParams)

            homeRecordString = '(' + str(
                seriesGames[0]['teams']['home']['leagueRecord']['wins']) + '-' + str(
                    seriesGames[0]['teams']['home']['leagueRecord']['losses']) + ')'

            awayRecordString = '(' + str(
                seriesGames[0]['teams']['away']['leagueRecord']['wins']) + '-' + str(
                    seriesGames[0]['teams']['away']['leagueRecord']['losses']) + ')'

            #homeRecordString = '(' + str(game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']) + '-' + str(
            #	game_contextMetrics['game']['teams']['home']['leagueRecord']['losses']) + ')'

            #awayRecordString = '(' + str(game_contextMetrics['game']['teams']['away']['leagueRecord']['wins']) + '-' + str(
            #	game_contextMetrics['game']['teams']['away']['leagueRecord']['losses']) + ')'

            titleString = seriesGames[0]['seriesDescription'] + '\n**' + \
                          seriesGames[0]['teams']['home']['team']['name'] + homeRecordString + '** vs **' \
                          + seriesGames[0]['teams']['away']['team']['name'] + awayRecordString + '**'

            # game_contextMetrics['game']['teams']['home']['leagueRecord']['wins']

            playoffEmbed = discord.Embed()
            playoffEmbed.title = titleString
            playoffEmbed.type = 'rich'
            playoffEmbed.color = discord.Color.dark_blue()

            for games in seriesGames:

                # Get the team names from the game
                homeTeam = statsapi.lookup_team(games['teams']['home']['team']['name'])
                awayTeam = statsapi.lookup_team(games['teams']['away']['team']['name'])
                # Get the short team names
                # If the team isn't decided yet then pull it from the response
                if homeTeam:
                    homeTeamShort = homeTeam[0]['fileCode'].upper()
                else:
                    homeTeamShort = games['teams']['home']['team']['name']

                if awayTeam:
                    awayTeamShort = awayTeam[0]['fileCode'].upper()
                else:
                    awayTeamShort = games['teams']['away']['team']['name']

                if games['status']['detailedState'] == 'Final' or games['status']['detailedState'] == 'Game Over':
                    homeScore = games['teams']['home']['score']
                    homeScoreString = str(homeScore)
                    awayScore = games['teams']['away']['score']
                    awayScoreString = str(awayScore)

                    if homeScore > awayScore:
                        homeScoreString = '**' + homeScoreString + '**'
                    elif awayScore > homeScore:
                        awayScoreString = '**' + awayScoreString + '**'

                    finalGameString = homeTeamShort + ' ' + homeScoreString + ' - ' + awayTeamShort + ' ' + awayScoreString + ' **F**'  # \n' + \
                    # homeTeamShort + '(' + str(games['teams']['home']['leagueRecord']['wins']) + '-' + str(games['teams']['home']['leagueRecord']['losses']) + ') - ' + \
                    # awayTeamShort + '(' + str(games['teams']['away']['leagueRecord']['wins']) + '-' + str(games['teams']['away']['leagueRecord']['losses']) + ')'

                    playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']), value=finalGameString,
                                           inline=False)
                elif games['status']['detailedState'] == 'Scheduled' or games['status']['detailedState'] == 'Pre-Game':

                    gameLocalTime = self.testFunctions.get_Local_Time(games['gameDate'])

                    valueString = awayTeamShort + ' vs ' + homeTeamShort + '\n'
                    valueString = valueString + calendar.day_name[gameLocalTime.weekday()] + '\n' + gameLocalTime.strftime(
                        '%m/%d/%Y') + ' at ' + gameLocalTime.strftime('%-I:%M%p') + ' EST'

                    if games['ifNecessary'] == 'N':
                        playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']), value=valueString,
                                               inline=False)
                    else:
                        playoffEmbed.add_field(name=games['description'] + ' (If Necessary)', value=valueString,
                                               inline=False)
                elif games['status']['detailedState'] == 'In Progress' or games['status']['detailedState'] == 'Live':
                    homeScore = games['teams']['home']['score']
                    homeScoreString = str(homeScore)
                    awayScore = games['teams']['away']['score']
                    awayScoreString = str(awayScore)

                    if homeScore > awayScore:
                        homeScoreString = '**' + homeScoreString + '**'
                    elif awayScore > homeScore:
                        awayScoreString = '**' + awayScoreString + '**'

                    liveGameString = awayTeamShort + ' ' + awayScoreString + ' - ' + homeTeamShort + ' ' + homeScoreString + '\n' + \
                                     games['status']['detailedState']
                    playoffEmbed.add_field(name='Game ' + str(games['seriesGameNumber']) + '\nLive Game',
                                           value=liveGameString, inline=False)

            await message.channel.send(embed=playoffEmbed)
        except ConnectionError as ce:
            print('DEBUG: Request failed in playoff_Series_Embed | {}'.format(ce))

# @client.event
# async def on_ready():
#     DM = 538897701522112514
#     USER = client.get_user(DM)
#     id = 318132313672384512
#     channel = client.get_channel(789273776105193472) 
#     discordUser = client.get_user(id)
#     await client.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
#     await discordUser.send('Bot Online')
#     print('Bot is ready.')

class Bot(discord.Client):
    embedFunctions = EmbedFunctions()
    testFunctions = TestFunctions()
    async def on_ready(self):
        user_id = 538897701522112514
        dm = client.get_user(int(538897701522112514))
        channel = client.get_channel(789273776105193472) 
        await self.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
        print('Bot is ready.')
        #await dm.send('I will be sending you the Mets lineup in a few minutes.')
        var = 0
        mlb_url = 'https://www.mlb.com/'
        req = requests.get(mlb_url)
        soup = BeautifulSoup(req.text, 'html.parser')
        num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
        teamtest = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")
        away_team = None
        team_index = None
        away_score = 0
        home_score = 0
        lineup_url = "https://www.baseballpress.com/lineups/" 
        r = requests.get(lineup_url)
        soup_lineup = BeautifulSoup(r.text, 'lxml') 
        lineup_list = []
        pitchers = []

        for tea in range(num_teams):
            if teamtest[tea].get_text() == 'Cardinals':
                team_index = tea
                if team_index % 2 == 0:
                    away_team = True
                else:
                    away_team = False

        target_date_time = datetime.datetime.now()
        team_selected = await self.testFunctions.get_team_no_msg('cardinals')
        queried_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(team_selected['id']))
    
        while var < 1:
            #now = datetime.datetime.now()
            if away_team == True:
                visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
                home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
                away_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text())
                home_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text())
                if away_score != away_team_score:
                    print('away score diff')
                    await self.embedFunctions.scoring_plays_embed(queried_schedule[0], channel)
                    away_score = away_team_score
                    break
                    
                # if home_score != home_team_score:
                #     print('home score diff')
                #     await self.embedFunctions.scoring_plays_embed(queried_schedule[0], channel)
                #     home_score = home_team_score
                    
            #if now.minute == '535353' or now.minute == 534545:
                # for item in soup_lineup.select("[data-league='NL']:-soup-contains('Mets') .player > a.player-link"):
                #     if item.get('data-razz') == '':
                #         player_name = 'Unknown Player'
                #         lineup_list.append(player_name)
                #     else:
                #         player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                #         lineup_list.append(player_name)
                # visitors = 'team'
                # pitchers.append(lineup_list[0])
                # pitchers.append(lineup_list[1])
                
                # await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

                # lineup_list.pop(0)
                # lineup_list.pop(0)
                # n = 9
                # home_list = lineup_list[n:]
                # away_list = lineup_list[:-n]

                # away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                # await channel.send(away_lineup)

                # home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                # await channel.send(home_lineup)
                # #await dm.send(away_lineup)
                # var = 1


    async def on_message(self, message):
        if(message.author == self.user) or message.author.bot:
            return
        else:
            message_array = message.content.split()
            if len(message_array) > 0:
                if ('BOT' in message_array[0].upper() and len(message_array) > 1) or (str(self.user.id) in message_array[0].upper()):
                    if 'PLAYER' in message_array[1].upper():
                        try:
                            now = datetime.datetime.now()
                            stat_year = now.year

                            if len(message_array) < 2:
                                await message.channel.send('Send Player Name.')
                                return
                            else:
                                if message_array[len(message_array) - 1].isdigit() and len(message_array) > 3:
                                    if int(message_array[len(message_array) - 1]) > now.year:
                                        await message.channel.send('cant predict future')
                                        return
                                    elif int(message_array[len(message_array) - 1]) < 1900:
                                        await message.channel.send("cant work with year 1900 or before")
                                        return
                                    else:
                                        stat_year = message_array[len(message_array) - 1]
                                
                                name_to_search = ""
                                display_name_to_search = ""

                                if message_array[len(message_array) - 1].isdigit():
                                    for index in range(2, len(message_array) - 1):
                                        name_to_search = name_to_search + message_array[index] + ' '
                                        display_name_to_search = display_name_to_search + message_array[index] + ' '
                                    
                                    name_to_search = name_to_search.strip()
                                    display_name_to_search = display_name_to_search.strip()
                                    name_to_search = name_to_search + '%25'
                                else:
                                    for index in range(2, len(message_array)):
                                        name_to_search = name_to_search + message_array[index] + ' '
                                        display_name_to_search = display_name_to_search + message_array[index] + ' '
                                    
                                    name_to_search = name_to_search.strip()
                                    display_name_to_search = display_name_to_search.strip()
                                    name_to_search = name_to_search + '%25'
                            
                            if name_to_search is None or name_to_search == '':
                                await message.channel.send('I didn\'t get a name to search. Something went wrong, Sorry')
                                return
                            
                            activePlayerSearchURL = 'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&active_sw=\'Y\'&name_part=\'' + name_to_search + '\''
                            player_search = await self.testFunctions.send_get_request(activePlayerSearchURL)
                            player_search_json = json.loads(player_search.text)
                            num_players = player_search_json['search_player_all']['queryResults']['totalSize']

                            if num_players == "0":
                                inactive_player_search_url = 'http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&active_sw=\'N\'&name_part=\'' + name_to_search + '\''
                                player_search = await self.testFunctions.send_get_request(inactive_player_search_url)
                                player_search_json = json.loads(player_search.text)
                                num_players = player_search_json['search_player_all']['queryResults']['totalSize']
                            
                            player_search_results = []
                            for search_index in range(int(num_players)):
                                player_found = players.PlayerSearchInfo()
                                player_found.ParseJson(player_search_json, search_index)
                                player_search_results.append(player_found)
                            
                            if len(player_search_results) > 1:
                                if len(player_search_results) > 50:
                                    await message.channel.send('too many matches for ' + display_name_to_search)
                                    return
                                
                                player_info_list = []
                                for player in player_search_results:
                                    player_info = players.PlayerInfo()
                                    player_info_url = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + player.player_id + '\''
                                    player_info_request = await self.testFunctions.send_get_request(player_info_url)
                                    player_info_json = json.loads(player_info_request.text)
                                    player_info.ParseJson(player_info_json)
                                    player_info_list.append(player_info)
                                
                                discord_formatted_string = '>>> I found ' + str(len(player_search_results)) + ' players matching **' + display_name_to_search + '** in ' + str(
                                    stat_year) + '\n Enter the number for the player you want \n\n'
                                
                                for index in range(len(player_search_results)):
                                    if index < len(player_search_results):
                                        append_string = ' ' + str(index + 1) + ': ' + player_info_list[index].name_display_first_last + ' - ' + player_info_list[
                                            index].team_name + ' (' + player_info_list[index].primary_position_txt + ' )' + '\n'
                                    else:
                                        appendString = ' ' + str(index + 1) + ': ' + player_info_list[index].name_display_first_last + ' - ' + player_info_list[
											index].team_name + ' (' + player_info_list[index].primary_position_txt + ')'
                                    
                                    discord_formatted_string = discord_formatted_string + append_string
                                
                                await message.channel.send(discord_formatted_string)
                                message_time = datetime.utcnow()
                                time.sleep(2)

                                player_info = players.PlayerInfo()
                                player_selected_index = await self.testFunctions.wait_for_number(message, len(player_search_results), 30)

                                if player_selected_index:
                                    player_info = player_info_list[player_selected_index - 1]
                                else:
                                    return
                            elif len(player_search_results) == 1:
                                player_info = players.PlayerInfo()
                                player_info_url = 'http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code=\'mlb\'&player_id=\'' + \
                                    player_search_results[0].player_id + '\''
                                player_info_header = {'Content-Type': 'application/json'}
                                player_info_request = requests.get(player_info_url, player_info_header)
                                player_info_json = json.loads(player_info_request.text)
                                player_info.ParseJson(player_info_json)
                            elif len(player_search_results) == 0:
                                await message.channel.send('I couldn\'t find any players with the name %s in the year %s' % (display_name_to_search, stat_year))
                                return
                            
                            if player_info.primary_position_txt != 'P':
                                stats_lookup = statsapi.player_stat_data(player_info.player_id, group="[hitting]", type="yearByYear")
                                stats_lookup_return = None

                                for stats_list_data in stats_lookup['stats']:
                                    if stats_list_data['season'] == str(stat_year):
                                        stats_lookup_return = stats_list_data
                                
                                if stats_lookup_return is None:
                                    await message.channel.send('%s doesn\'t appear to have any stats for %s' % (player_info.name_display_first_last, stat_year))
                                    return
                                
                                player_embed = discord.Embed()
                                player_embed.title = '**' + player_info.name_display_first_last + '\'s** Stats for **' + str(stat_year) + '**'
                                player_embed.type = 'rich'
                                player_embed.color = discord.Color.dark_blue()

                                valueString = ' Batting Avg: %s\n' \
														  ' HomeRuns: %s\n' \
														  ' Slugging: %s\n' \
														  ' OPS: %s\n' \
														  ' RBI: %s' % (
															  stats_lookup_return['stats']['avg'],
															  stats_lookup_return['stats']['homeRuns'],
                                                              stats_lookup_return['stats']['slg'],
                                                              stats_lookup_return['stats']['ops'],
                                                              stats_lookup_return['stats']['rbi'])
                                player_embed.add_field(name="Hitting Stats",
																  value=valueString)
                                await message.channel.send(embed=player_embed)
                            else:
                                player_stats_url = 'http://lookup-service-prod.mlb.com/json/named.sport_pitching_tm.bam?league_list_id=\'mlb\'&game_type=\'R\'&season=\'' + str(
												stat_year) + '\'&player_id=\'' + player_info.player_id + '\''
                                player_stats_header = {'Content-Type': 'application/json'}
                                player_stats_request = requests.get(player_stats_url, player_stats_header)
                                player_stats_json = json.loads(player_stats_request.text)

                                if int(player_stats_json['sport_pitching_tm']['queryResults']['totalSize']) == 0:
                                    await message.channel.send('%s doesn\'t appear to have any stats for %s' % (player_info.name_display_first_last, stat_year))
                                    return
                                
                                season_pitching_info = players.SeasonPitchingStats()
                                season_pitching_info.ParseJson(player_stats_json)
                                pitcher_embed = discord.Embed()
                                pitcher_embed.title = '**' + player_info.name_display_first_last + '\'s** Stats for **' + str(stat_year) + '**'
                                pitcher_embed.type = 'rich'
                                pitcher_embed.color = discord.Color.dark_blue()

                                for index in range(0, season_pitching_info.totalSize):
                                    valueString = ' ERA: %s\n' \
															  ' Wins/Losses: %s/%s\n' \
															  ' Games: %s\n' \
															  ' WHIP: %s' % (
																  season_pitching_info.era[index],
																  season_pitching_info.w[index],
																  season_pitching_info.l[index],
																  season_pitching_info.gs[index],
																  season_pitching_info.whip[index])
                                    pitcher_embed.add_field(name=season_pitching_info.team_abbrev[index],value=valueString)

                                await message.channel.send(embed=pitcher_embed)
                                return
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            filename = exception_traceback.tb_frame.f_code.co_filename
                            line_num = exception_traceback.tb_lineno
                            print("Exception type: ", exception_type)
                            print("File name: ", filename)
                            print("Line number: ", line_num)
                            print('DEBUG: Exception in PLAYER. Input was %s' % message.content)
                            print('DEBUG: Exception is %s' % e)
                            await message.channel.send("Sorry, I've encountered an error :(")
                    elif 'SCORE' in message_array[1].upper():
                        try:
                            if len(message_array) < 3:
                                await message.channel.send("I need a team to check the score for")
                                return
                            
                            team_selected = None
                            team_to_search = ''
                            team_to_search = message_array[2]
                            if len(message_array) > 3:
                                for message_data in range(3, len(message_array)):
                                    team_to_search = team_to_search + ' ' + message_array[message_data]
                            
                            team_selected = await self.testFunctions.get_team(team_to_search, message)
                            target_date_time = datetime.datetime.now()

                            if team_selected is None:
                                await message.channel.send('I couldn\'t find a team with the name %s. Please try again.' % team_to_search)
                                print('DEBUG: Failed to get the team in time in SCORE function')
                                print('DEBUG: Input was: ' + team_to_search)
                                print('DEBUG: Message content was: ' + message.content)
                                return
                            
                            queried_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(team_selected['id']))
                            past_day = datetime.datetime.today() - timedelta(1)
                            past_week = datetime.datetime.today() - timedelta(7)
                            past_games = statsapi.schedule(start_date = past_week.strftime('%m/%d/%Y'), end_date = past_day.strftime('%m/%d/%Y'), team=team_selected['id'])

                            next_day = datetime.datetime.today() + timedelta(1)
                            next_week = datetime.datetime.today() + timedelta(7)
                            next_games = statsapi.schedule(start_date = next_day.strftime('%m/%d/%Y'), end_date = next_week.strftime('%m/%d/%Y'), team = team_selected['id'])

                            if len(past_games) > 0:
                                previous_game = past_games[len(past_games) - 1]
                            else:
                                previous_game = None
                            
                            if type(queried_schedule) is list:
                                final_status_list = ["Final", "Game Over", "Completed Early"]
                                scheduled_status_list = ["Scheduled", "Pre-Game"]
                                live_status_list = ["In Progress", "Delayed"]
                                other_status_list = ["Postponed"]

                                if previous_game is not None:
                                    if previous_game['status'] == 'In Progress' and queried_schedule[0]['status'] == 'Scheduled':
                                        queried_schedule[0] = previous_game
                                
                                if len(queried_schedule) > 2:
                                    for game in queried_schedule:
                                        if any(game_status in game['status'] for game_status in final_status_list):
                                            await self.embedFunctions.final_game_embed(game, message)
                                        elif any(game_status in game['status'] for game_status in scheduled_status_list):
                                            await self.embedFunctions.scheduled_game_embed(game, message)
                                        elif any(game_status in game['status'] for game_status in live_status_list):
                                            await self.embedFunctions.live_game_embed(game, message)
                                        elif any(game_status in game['status'] for game_status in other_status_list):
                                            await self.embedFunctions.generic_Game_Embed(game, message)
                                
                                elif len(queried_schedule) == 2:
                                    #game 1
                                    if any(game_status in queried_schedule[0]['status'] for game_status in final_status_list): await self.embedFunctions.final_game_embed(queried_schedule[0], message)
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in scheduled_status_list):
                                        await self.embedFunctions.scheduled_game_embed(queried_schedule[0], message)
                                        if previous_game is not None: await self.embedFunctions.final_game_embed(previous_game, message)
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in live_status_list):
                                        await self.embedFunctions.live_game_embed(queried_schedule[0], message)
                                        return
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in other_status_list): await self.embedFunctions.generic_Game_Embed(queried_schedule[0], message)
                                    #game 2
                                    if any(game_status in queried_schedule[1]['status'] for game_status in final_status_list):
                                        await self.embedFunctions.final_game_embed(queried_schedule[1], message)
                                        if len(next_games) > 0:
                                            await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                                    elif any(game_status in queried_schedule[1]['status'] for game_status in scheduled_status_list):
                                        await self.embedFunctions.scheduled_game_embed(queried_schedule[1], message)
                                        if previous_game is not None:
                                            await self.embedFunctions.final_game_embed(previous_game, message)
                                    elif any(game_status in queried_schedule[1]['status'] for game_status in live_status_list):
                                        await self.embedFunctions.live_game_embed(queried_schedule[1], message)
                                        return
                                    elif any(game_status in queried_schedule[1]['status'] for game_status in other_status_list): await self.embedFunctions.generic_Game_Embed(queried_schedule[0], message)
                                    if len(next_games) > 0: await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                                
                                elif len(queried_schedule) == 1:
                                    if any(game_status in queried_schedule[0]['status'] for game_status in final_status_list):
                                        await self.embedFunctions.final_game_embed(queried_schedule[0], message)
                                        if len(next_games) > 0: await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in scheduled_status_list):
                                        await self.embedFunctions.scheduled_game_embed(queried_schedule[0], message)
                                        if previous_game is not None: await self.embedFunctions.final_game_embed(previous_game, message)
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in live_status_list):
                                        await self.embedFunctions.live_game_embed(queried_schedule[0], message)
                                    elif any(game_status in queried_schedule[0]['status'] for game_status in  other_status_list):
                                        await self.embedFunctions.generic_Game_Embed(queried_schedule[0], message)
                                        if len(next_games) > 0:
                                            await self.embedFunctions.scheduled_Game_Embed(next_games[0],  message)
                                elif len(queried_schedule) <= 0:
                                    if len(past_games) > 0:
                                        previous_game = past_games[len(past_games) - 1]
                                    else:
                                        await message.channel.send('no recent games')
                                        return
                                    
                                    if previous_game['status'] == 'In Progress':
                                        print('prev game still in progress')
                                        await self.embedFunctions.live_game_embed(previous_game, message)
                                    
                                    final_status_list = ["Final", "Game Over", "Completed Early"]
                                    if any(game_status in previous_game['status'] for game_status in final_status_list):
                                        await self.embedFunctions.final_game_embed(previous_game, message)
                                        if len(next_games) > 0:
                                            await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                        except Exception as e:
                            exception_type, exception_object, exception_traceback = sys.exc_info()
                            filename = exception_traceback.tb_frame.f_code.co_filename
                            line_num = exception_traceback.tb_lineno
                            print("Exception type: ", exception_type)
                            print("File name: ", filename)
                            print("Line number: ", line_num)
                            print('DEBUG: Exception in SCORE. Input was %s' % message.content)
                            print('DEBUG: Exception was %s' % e)
                            await message.channel.send('Sorry, something went wrong :( %s' % e)                     
                elif message_array[0].upper() == 'BOT' and len(message_array) == 1:
                    await message.channel.send('test')
                    print('test')
                    return
            else:
                return
    

                                    
                        































































































#     #await general.send('L')
#     away_score = 0
#     away_team_score = 0
#     home_score = 0
#     home_team_score = 0
#     url = 'https://www.mlb.com/'
#     req = requests.get(url)
#     soup = BeautifulSoup(req.text, 'html.parser')
#     num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
#     teamtest = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")
#     away_team = None
#     team_index = None
#     yanks_scoring_url = "https://www.espn.com/mlb/playbyplay/_/gameId/401443623" #most likely will need to change daily
#     request = requests.get(yanks_scoring_url)
#     soup_score = BeautifulSoup(request.text, 'html.parser')
    
#     lineup_url = "https://www.baseballpress.com/lineups/" 
#     r = requests.get(lineup_url)
#     soup_lineup = BeautifulSoup(r.text, 'lxml') 
#     lineup_list = []
#     pitchers = []

#     for tea in range(num_teams):
#         if teamtest[tea].get_text() == 'Mets':
#             team_index = tea
#             if team_index % 2 == 0:
#                 away_team = True
#             else:
#                 away_team = False

#     while True:
#         now = datetime.datetime.now().strftime("%H:%M:%S") #24 hour clock, discord time always 4 hours ahead of NA EAST
#         time.sleep(1)

#         #await channel.send("Message every second")
#         #await channel.send(now)

#         # if away_team == True:
#         #     #print('before game stat')
#         #     game_stat = soup.find_all(class_="GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[team_index // 2].get_text()
#         #     #print('after game stat: ' + game_stat)
#         # elif away_team == False:
#         #     #print('before game stat')
#         #     game_stat = soup.find_all(class_="GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[(team_index - 1) // 2].get_text()
#         #     #print('after game stat: ' + game_stat)
#         # if game_stat == 'Final':
#         #     await channel.send("Yankees game over")
#         # elif game_stat == 'WARMUP' or game_stat == 'Warmup':
#         #     await channel.send("Yankees game starting soon.")
#         # elif game_stat == '1:05 PM ET' or game_stat == '1:07 PM ET':
#         #     if now == '12:30:00':
#         #         await channel.send(' 12 30')
#         #         if away_team == True:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-zsc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapperz-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
#         #             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#         #             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
                    
#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Guardians') .player > a.player-link"):
#         #                 player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                 lineup_list.append(player_name)
                    
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])

#         #             await channel.send('Starting Pitchers:\nYankees: ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])
                    
#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]
#         #         elif away_team == False:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()

#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
#         #                 if item.get('data-razz') == '':
#         #                     player_name = 'Unknown Player'
#         #                     lineup_list.append(player_name)
#         #                 else:
#         #                     player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                     lineup_list.append(player_name)
                
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])
                    
#         #             await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]

#         #             away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
#         #             await channel.send(away_lineup)

#         #             home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
#         #             await channel.send(home_lineup)
#         # elif game_stat == '4:05 PM ET' or game_stat == '4:10 PM ET':
#         #     if now == '15:30:00':
#         #         await channel.send('3 30')
#         #         if away_team == True:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-zsc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapperz-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
#         #             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#         #             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
                    
#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Guardians') .player > a.player-link"):
#         #                 player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                 lineup_list.append(player_name)
                    
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])

#         #             await channel.send('Starting Pitchers:\nYankees: ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])
                    
#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]
#         #         elif away_team == False:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()

#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
#         #                 if item.get('data-razz') == '':
#         #                     player_name = 'Unknown Player'
#         #                     lineup_list.append(player_name)
#         #                 else:
#         #                     player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                     lineup_list.append(player_name)
                
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])
                    
#         #             await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]

#         #             away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
#         #             await channel.send(away_lineup)

#         #             home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
#         #             await channel.send(home_lineup)
#         # elif game_stat == '7:05 PM ET' or game_stat == '7:07 PM ET' or game_stat == '7:10 PM ET':
#         #     if now == '18:30:00':
#         #         await channel.send('6 30')
#         #         if away_team == True:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-zsc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapperz-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
#         #             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#         #             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
                    
#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Guardians') .player > a.player-link"):
#         #                 player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                 lineup_list.append(player_name)
                    
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])

#         #             await channel.send('Starting Pitchers:\nYankees: ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])
                    
#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]
#         #         elif away_team == False:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()

#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
#         #                 if item.get('data-razz') == '':
#         #                     player_name = 'Unknown Player'
#         #                     lineup_list.append(player_name)
#         #                 else:
#         #                     player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                     lineup_list.append(player_name)
                
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])
                    
#         #             await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]

#         #             away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
#         #             await channel.send(away_lineup)

#         #             home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
#         #             await channel.send(home_lineup)
#         # elif game_stat == '10:05 PM ET' or game_stat == '10:10 PM ET':
#         #     if now == '21:30:00':
#         #         await channel.send('9 30')
#         #         if away_team == True:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-zsc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapperz-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
#         #             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#         #             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrazpper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
                    
#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Guardians') .player > a.player-link"):
#         #                 player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                 lineup_list.append(player_name)
                    
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])

#         #             await channel.send('Starting Pitchers:\nYankees: ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])
#         #         elif away_team == False:
#         #             visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
#         #             home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()

#         #             for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
#         #                 if item.get('data-razz') == '':
#         #                     player_name = 'Unknown Player'
#         #                     lineup_list.append(player_name)
#         #                 else:
#         #                     player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
#         #                     lineup_list.append(player_name)
                
#         #             pitchers.append(lineup_list[0])
#         #             pitchers.append(lineup_list[1])
                    
#         #             await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[1] + '\nYankees: ' + pitchers[0])

#         #             lineup_list.pop(0)
#         #             lineup_list.pop(0)
#         #             n = 9
#         #             home_list = lineup_list[n:]
#         #             away_list = lineup_list[:-n]

#         #             away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
#         #             await channel.send(away_lineup)

#         #             home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
#         #             await channel.send(home_lineup)
#         # elif game_stat == 'TOP 1':
#         #     await channel.send("Yankees game has started.")
#         # elif game_stat == 'BOT 5':
#         #     await channel.send('bottom 5 inning')
        
#         # if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
            
#         #     away_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text())
#         #     home_team_score = int(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text())

#         # if away_team_score != away_score:
#         #     scoring_play = soup_score.find_all(class_ = "headline scoring")[0].get_text() #play atbat-result
#         #     await channel.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
#         #     #await USER.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
#         #     away_score = away_team_score
            
#         # if home_team_score != home_score:
#         #     scoring_play = soup_score.find_all(class_ = "headline scoring")[0].get_text()
#         #     await channel.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
#         #     #await USER.send(str(scoring_play) + str(away_team_score) + " - " + str(home_team_score))
#         #     home_score = home_team_score

# @client.event
# async def on_message(message: discord.Message):
#     channel = client.get_channel(978743346287759390)
#     if message.guild is None and not message.author.bot:
#         await channel.send(str(message.author.mention) + " sent " + " "" " + message.content + " "" ")
#     await client.process_commands(message)

# @client.command()
# async def pm(ctx, userId: int, msg: str):
#     id = userId 
#     user = client.get_user(id)
#     await ctx.send("Message Sent to " + str(user))
#     await user.send(msg)

# @client.command()
# async def baseball(ctx):
#     url = 'https://www.mlb.com/'
#     req = requests.get(url)
#     soup = BeautifulSoup(req.text, 'html.parser')
#     team_1 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[0].get_text() 
#     team_2 = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[1].get_text()
#     team_1_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[0].get_text()
#     team_2_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[1].get_text()
#     await ctx.send(str(team_1))
#     await ctx.send(str(team_2))
#     await ctx.send("Score: " + str(team_1_score))
#     await ctx.send("score: " + str(team_2_score))

# @client.command()
# async def score(ctx, team):
#     url = 'https://www.mlb.com/'
#     req = requests.get(url)
#     soup = BeautifulSoup(req.text, 'html.parser')
#     num_teams = len(soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL"))
#     teamtest = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")
#     away_team = None
#     team_index = None
#     game_start_time = None
#     DM = 538897701522112514
#     USER = client.get_user(DM)

#     for tea in range(num_teams):
#         if teamtest[tea].get_text() == str(team):
#             team_index = tea
#             print('yankees team index :' + str(team_index))
#             if team_index % 2 == 0:
#                 away_team = True
#             else:
#                 away_team = False
    
#     if away_team == True:
#         visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index + 1].get_text()
#         if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
#             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index + 1].get_text()
#             text = """```Scores: 
#             """ + str(visitors) + """ : """ + str(away_team_score) + """
#             """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
#             await ctx.send(text)

#         if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index:
#             time_index = team_index // 2
#             print('team index mets: ' + str(team_index))
#             print('time index mets: ' + str(time_index))
#             game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index].get_text()
#             await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
        
#     if away_team == False:
#         visitors = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index - 1].get_text()
#         home_team = soup.find_all(class_ = "TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0 iNsMPL")[team_index].get_text()
#         if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) >= team_index:
#             print('yanks team index' + str(team_index))
#             away_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index - 1].get_text()
#             home_team_score = soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")[team_index].get_text()
#             text = """```Scores: 
#             """ + str(visitors) + """ : """ + str(away_team_score) + """
#             """ + str(home_team) + """ : """ + str(home_team_score) + """```"""
#             await ctx.send(text)

#         if len(soup.find_all(class_ = "TeamMatchupLayerstyle__ScoreWrapper-sc-3lvmzz-3 cLonxp")) < team_index: #team index - 1
#             time_index = team_index // 2
#             print('yankees team index: ' + str(team_index))
#             print('yankees time index: ' + str(time_index))
#             game_start_time = soup.find_all(class_ = "GameDataLayerstyle__GameStateBaseLabelWrapper-sc-1vhdg11-5 jxEhSY")[time_index].get_text()
#             await ctx.send(str(team) + " game hasn't started yet. They will play at " + str(game_start_time))
client = Bot()  
client.run(os.environ["DISCORD_TOKEN"])