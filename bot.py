import discord
import os
import requests
from discord.utils import find
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
import copy
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

    def get_team_no_msg(self, team_name):
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
    async def scoring_plays_embed(self, game, channel, team, away_team_score, home_team_score):
        if type(game) == list:
            game = game[0]
        
        game_type = game['game_type']
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        away_team_code = away_team[0]['fileCode'].upper()
        home_team_code = home_team[0]['fileCode'].upper()
        # away_team_score = int(game['away_score'])
        # home_team_score = int(game['home_score'])
        scoring_embed = discord.Embed()
        scoring_embed.title = '**%s Scored**' % team
        scoring_embed.type = 'rich'
        scoring_embed.color = discord.Color.dark_blue()
        #scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'], inline=False)

        if game_type != 'S':
            scoringPlaysList = statsapi.game_scoring_play_data(game['game_id'])
            scoringPlays = scoringPlaysList['plays']
            if len(scoringPlays) > 0:
                scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'] + str(away_team_code) + ': ' +
                str(away_team_score) + ' - ' + str(home_team_code) + ': ' + str(home_team_score), inline=False)
            await channel.send(embed=scoring_embed, tts=False)
            return
        else:
            await channel.send(embed=scoring_embed, tts=False)
            return
            
    async def scoring_plays_embed_message(self, message, game, team, away_team_score, home_team_score):
        if type(game) == list:
            game = game[0]
        
        game_type = game['game_type']
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        away_team_code = away_team[0]['fileCode'].upper()
        home_team_code = home_team[0]['fileCode'].upper()
        # away_team_score = int(game['away_score'])
        # home_team_score = int(game['home_score'])
        scoring_embed = discord.Embed()
        scoring_embed.title = '**%s Scored**' % team
        scoring_embed.type = 'rich'
        scoring_embed.color = discord.Color.dark_blue()
        #scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'], inline=False)

        if game_type != 'S':
            scoringPlaysList = statsapi.game_scoring_play_data(game['game_id'])
            scoringPlays = scoringPlaysList['plays']
            if len(scoringPlays) > 0:
                scoring_embed.add_field(name='**Latest scoring play**', value=scoringPlays[len(scoringPlays) - 1]['result']['description'] + str(away_team_code) + ': ' +
                str(away_team_score) + ' - ' + str(home_team_code) + ': ' + str(home_team_score), inline=False)
            await message.channel.send(embed=scoring_embed, tts=False)
            return
        else:
            await message.channel.send(embed=scoring_embed, tts=False)
            return

    async def box_score(self, game, channel):
        if type(game) == list:
            game = game[0]
        
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        away_team_code = away_team[0]['fileCode'].upper()
        home_team_code = home_team[0]['fileCode'].upper()
        game_id = game['game_id']
        away_box = statsapi.boxscore_data(int(game_id))['awayPitchers']
        home_box = statsapi.boxscore_data(int(game_id))['homePitchers']
        box_score_embed = discord.Embed()
        box_score_embed.title = '**' + str(away_team_code) + ' box score ' + '**'
        box_score_embed.type = 'rich'
        box_score_embed.color = discord.Color.dark_blue()
        var = 1
        #box_score_embed.add_field(name = away_box[0]['namefield'], value = None, inline=False)
        for pitcher in range(len(away_box)):
            box_score_embed.add_field(name = away_box[pitcher]['namefield'], value = away_box[pitcher]['era'], inline=False)
            #box_score_embed.add_field(name = away_box[pitcher]['namefield'], value = away_box[pitcher]['ip'], inline=True)
            #box_score_embed.add_field(name = away_box[pitcher]['ip'], inline = True)

        await channel.send(content = 'Box Scores ', embed = box_score_embed)
        print(away_box)
    async def scheduled_game_embed(self, game, message):
        if type(game) == list:
            game = game[0]

        game_time_local = self.testFunctions.get_local_time(game['game_datetime']) - timedelta(hours=4)
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
    
    async def boxscore(self, gamePk, pitchingBox=True, timecode = None):
        boxData = self.boxscore_data(gamePk, timecode)
        rowLen = 79
        fullRowLen = rowLen * 2 + 3
        boxscore = ""
        home_pitchers_list = []
        away_pitchers_list = []
        pitchers_list = []
        if pitchingBox:
            awayPitchers = boxData["awayPitchers"]
            homePitchers = boxData["homePitchers"]
            blankPitcher = {
                "namefield": "",
                "ip": "",
                "h": "",
                "r": "",
                "er": "",
                "bb": "",
                "k": "",
                "hr": "",
                "era": "",
            }

            while len(awayPitchers) > len(homePitchers):
                homePitchers.append(blankPitcher)

            while len(awayPitchers) < len(homePitchers):
                awayPitchers.append(blankPitcher)

            awayPitchers.append(boxData["awayPitchingTotals"])
            homePitchers.append(boxData["homePitchingTotals"])

            for i in range(0, len(awayPitchers)):
                if i == 0 or i == len(awayPitchers) - 1:
                    boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"

                boxscore += "{namefield:<43}| ".format(
                    **awayPitchers[i]
                )
                boxscore += "{namefield:<43} \n".format(
                    **homePitchers[i]
                )
                if i == 0 or i == len(awayPitchers) - 1:
                    boxscore += "-" * rowLen + " | " + "-" * rowLen + "\n"
            # print(homePitchers)
            # print(awayPitchers)
            for home_pitcher in range(1, len(homePitchers)):
                if homePitchers[home_pitcher]['namefield'] not in home_pitchers_list:
                    home_pitchers_list.append(homePitchers[home_pitcher]['namefield'])
            
            for away_pitcher in range(1, len(awayPitchers)):
                if awayPitchers[away_pitcher]['namefield'] not in away_pitchers_list:
                    away_pitchers_list.append(awayPitchers[away_pitcher]['namefield'])
            
            away_pitchers_list = [i for i in away_pitchers_list if i != '']
            home_pitchers_list = [i for i in home_pitchers_list if i != '']
            pitchers_list.append(away_pitchers_list)
            pitchers_list.append(home_pitchers_list)
            #print(away_pitchers_list)
            #print(home_pitchers_list)
            return pitchers_list

    def boxscore_data(self, gamePk, timecode=None):
        boxData = {}
        params = {
            "gamePk": gamePk,
            "fields": "gameData,game,teams,teamName,shortName,teamStats,batting,atBats,runs,hits,doubles,triples,homeRuns,rbi,stolenBases,strikeOuts,baseOnBalls,leftOnBase,pitching,inningsPitched,earnedRuns,homeRuns,players,boxscoreName,liveData,boxscore,teams,players,id,fullName,allPositions,abbreviation,seasonStats,batting,avg,ops,obp,slg,era,pitchesThrown,numberOfPitches,strikes,battingOrder,info,title,fieldList,note,label,value,wins,losses,holds,blownSaves",
        }
        if timecode:
            params.update({"timecode": timecode})

        r = statsapi.get("game", params)

        boxData.update({"teamInfo": r["gameData"]["teams"]})
        boxData.update({"playerInfo": r["gameData"]["players"]})
        boxData.update({"away": r["liveData"]["boxscore"]["teams"]["away"]})
        boxData.update({"home": r["liveData"]["boxscore"]["teams"]["home"]})

        sides = ["away", "home"]
       
        pitcherColumns = [
            {
                "namefield": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
                "name": boxData["teamInfo"]["away"]["teamName"] + " Pitchers",
            }
        ]
        awayPitchers = copy.deepcopy(pitcherColumns)
        homePitchers = copy.deepcopy(pitcherColumns)
        homePitchers[0]["namefield"] = boxData["teamInfo"]["home"]["teamName"] + " Pitchers"
        homePitchers[0]["name"] = boxData["teamInfo"]["away"]["teamName"] + " Pitchers"
        pitchers = [awayPitchers, homePitchers]

        for i in range(0, len(sides)):
            side = sides[i]
            for pitcherId_int in boxData[side]["pitchers"]:
                pitcherId = str(pitcherId_int)
                if not boxData[side]["players"].get("ID" + pitcherId) or not len(
                    boxData[side]["players"]["ID" + pitcherId]
                    .get("stats", {})
                    .get("pitching", {})
                ):
                    continue

                namefield = boxData["playerInfo"]["ID" + pitcherId]["fullName"]
               
                pitcher = {
                    "namefield": namefield,
                    "name": boxData["playerInfo"]["ID" + pitcherId]["fullName"],
                }
                pitchers[i].append(pitcher)

        boxData.update({"awayPitchers": awayPitchers})
        boxData.update({"homePitchers": homePitchers})

        pitchingTotals = ["awayPitchingTotals", "homePitchingTotals"]
        for i in range(0, len(sides)):
            side = sides[i]
            boxData.update(
                {
                    pitchingTotals[i]: {
                        "namefield": "",
                        "name": "",
                    }
                }
            )
        return boxData
    
    async def pitching_change(self, channel, team, new_pitcher, old_pitcher, inning):
        pitching_change_embed = discord.Embed()
        pitching_change_embed.title = '**Pitching Change**'
        pitching_change_embed.type = 'rich'
        pitching_change_embed.color = discord.Color.dark_blue()
        pitching_change_embed.add_field(name='**%s**' % team, value=str(new_pitcher) + " replaces " + str(old_pitcher) + " in the " + inning + " inning.", inline=False)
        await channel.send(embed=pitching_change_embed)

    # def get_temperature(self, city):
    #     city = city.replace(" ", "+")
    #     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    #     res = requests.get(
    #     f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    #     print("Searching...\n")
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     location = soup.select('#wob_loc')[0].getText().strip()
    #     time = soup.select('#wob_dts')[0].getText().strip()
    #     info = soup.select('#wob_dc')[0].getText().strip()
    #     weather = soup.select('#wob_tm')[0].getText().strip()
    #     print(location)
    #     print(time)
    #     print(info)
    #     print(weather+"°C")
    
    # def print_temperature(self, city):
    #     city = city + " weather"
    #     return self.get_temperature(city)
    def file_code(self, game):
        if type(game) == list:
            game = game[0]
        
        game_type = game['game_type']
        home_team = statsapi.lookup_team(game['home_name'])
        away_team = statsapi.lookup_team(game['away_name'])
        away_team_code = away_team[0]['fileCode'].upper()
        home_team_code = home_team[0]['fileCode'].upper()

        file_code_list = []
        file_code_list.append(away_team_code)
        file_code_list.append(home_team_code)

        return file_code_list
    
    async def team_notifications(self, team, channel_id, error):
        channel = client.get_channel(int(channel_id))
        lineup_url = "https://www.baseballpress.com/lineups/" 
        r = requests.get(lineup_url)
        soup_lineup = BeautifulSoup(r.text, 'lxml') 
        lineup_list = []
        pitchers = []
        hour_var = 0
        away_team = None
        error_var = 0
        await channel.send(team)
        while True and error_var < 1:
            await channel.send('team_notif')
            # target_date_time = datetime.datetime.now() - timedelta(hours=4)
            # team_selected = await self.testFunctions.get_team_no_msg(str(team))
            # queried_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(team_selected['id'])) #'%Y-%m-%d
            # now = datetime.datetime.now() - timedelta(hours=4)
            # game_time_local = self.testFunctions.get_local_time(queried_schedule[0]['game_datetime'])
            # new_hour = game_time_local - timedelta(hours=4)
            # visitors = queried_schedule[0]['away_name']
            # home_team = queried_schedule[0]['home_name']
            # if visitors == 'New York Yankees':
            #     away_team = True
            # elif home_team == 'New York Yankees':
            #     away_team = False
            # if away_team == True:
            #     if (now.hour == (new_hour.hour - 1)) and (hour_var < 1):
            #         for item in soup_lineup.select("[data-league='%s']:-soup-contains('%s') .player > a.player-link" % ()):
            #             if item.get('data-razz') == '':
            #                 player_name = 'Unknown Player'
            #                 lineup_list.append(player_name)
            #             else:
            #                 player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
            #                 lineup_list.append(player_name)
            #         pitchers.append(lineup_list[0])
            #         pitchers.append(lineup_list[1])
                    
            #         await channel.send('Starting Pitchers:\n' + str(visitors) + ': ' + pitchers[0] + '\n' + str(home_team) + ': ' + pitchers[1])

            #         lineup_list.pop(0)
            #         lineup_list.pop(0)
            #         n = 9
            #         home_list = lineup_list[n:]
            #         away_list = lineup_list[:-n]

            #         away_lineup = """```1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
            #         await channel.send(away_lineup)

            #         home_lineup = """```1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
            #         await channel.send(home_lineup)
            #         hour_var = 1

            #         if now.hour != (new_hour.hour - 1):
            #             hour_var = 0
            # elif away_team == False:
            #     pass
            
            # if (new_hour.hour <= now.hour <= (new_hour.hour + 4)):
            #     away_team_score = int(queried_schedule[0]['away_score'])
            #     home_team_score = int(queried_schedule[0]['home_score'])
            #     if away_score != away_team_score:
            #        # await self.scoring_plays_embed(queried_schedule[0], channel)
            #         away_score = away_team_score
                    
            #     if home_score != home_team_score:
            #         #await self.scoring_plays_embed(queried_schedule[0], channel)
            #         home_score = home_team_score


            #
            if error == False:
                return

class Bot(discord.Client):
    embedFunctions = EmbedFunctions()
    testFunctions = TestFunctions()
    async def on_ready(self):
        try:
            channel = client.get_channel(983204319564288151) 
            dump = client.get_channel(983209443770642462)
            await self.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.watching, name = "you cry"))
            print('Bot is ready.')
            var = 0
            away_team = True
            yankees_away_score = 0
            yankees_home_score = 0
            mets_away_score = 0
            mets_home_score = 0
            lineup_url = "https://www.baseballpress.com/lineups/" 
            r = requests.get(lineup_url)
            soup_lineup = BeautifulSoup(r.text, 'lxml') 
            lineup_list = []
            lineup_list_game_2 = []
            pitchers = []
            pitchers_game_2 = []
            hour_var = 0
            hour_var_game_2 = 0
            final_yan = 0
            final_yan_game_2 = 0
            final_met = 0
            final_met_game_2 = 0
            yankees_pitcher_var = 0
            mets_pitcher_var = 0
            nl_teams = ["New York Mets", "Washington Nationals", "Atlanta Braves", "Philadelphia Phillies", "Miami Marlins", "Milwaukee Brewers", "Pittsburgh Pirates",
            "Cincinatti Reds", "Chicago Cubs", "St. Louis Cardinals", "Los Angeles Dodgers", "San Diego Padres", "San Francisco Giants", "Colorado Rockies", "Arizona Diamondbacks"]
            al_teams = ["New York Yankees", "Toronto Blue Jays", "Boston Red Sox", "Baltimore Orioles", "Tampa Bay Rays", "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals",
            "Chicago White Sox", "Minnesota Twins", "Oakland Athletics", "Houston Astros", "Texas Rangers", "Los Angeles Angels", "Seattle Mariners"]
            yankees_interleague = None
            mets_interleague = None
            
            while var < 1:
                target_date_time = datetime.datetime.now() - timedelta(hours=10) #changing from 4 to 8/10
                yankees = self.testFunctions.get_team_no_msg('nationals')
                mets = self.testFunctions.get_team_no_msg('orioles')
                mets_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(mets['id']))
                yankees_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(yankees['id'])) #'%Y-%m-%d
                await dump.send('msg')
                now = datetime.datetime.now() - timedelta(hours=10) #changing from 4 to 8/10
                    
                if len(mets_schedule) > 0:
                    mets_game_id = mets_schedule[0]['game_id']
                    mets_visitors = mets_schedule[0]['away_name']
                    mets_home_team = mets_schedule[0]['home_name']
                    mets_game_time_local = self.testFunctions.get_local_time(mets_schedule[0]['game_datetime'])
                    mets_new_hour = mets_game_time_local - timedelta(hours=10)
                    mets_new_minute = mets_game_time_local - timedelta(minutes=5)
                    mets_away_team_code = self.embedFunctions.file_code(mets_schedule[0])[0]
                    mets_home_team_code = self.embedFunctions.file_code(mets_schedule[0])[1]
                    if mets_pitcher_var < 1:
                        mets_home_prob = mets_schedule[0]['home_probable_pitcher']
                        mets_away_prob = mets_schedule[0]['away_probable_pitcher']
                        mets_pitcher_var = 1
                        if now.hour == 4:
                            mets_pitcher_var = 0

                    if away_team == True and (mets_new_hour.hour <= now.hour <= (mets_new_hour.hour + 5)):
                        mets_away_team_score = int(mets_schedule[0]['away_score'])
                        mets_home_team_score = int(mets_schedule[0]['home_score'])
                        mets_pitchers = await self.embedFunctions.boxscore(int(mets_game_id))
                        away_mets_pitchers = mets_pitchers[0]
                        home_mets_pitchers = mets_pitchers[1]

                        if away_mets_pitchers[len(away_mets_pitchers) - 1] != mets_away_prob:
                            await channel.send(mets_away_prob + ' has been replaced by ' + str(away_mets_pitchers[len(away_mets_pitchers) - 1]))
                            mets_away_prob = away_mets_pitchers[len(away_mets_pitchers) - 1]
                    
                        if home_mets_pitchers[len(home_mets_pitchers) - 1] != mets_home_prob:
                            await channel.send(mets_home_prob + ' has been replaced by ' + str(home_mets_pitchers[len(home_mets_pitchers) - 1]))
                            mets_home_prob = home_mets_pitchers[len(home_mets_pitchers) - 1]

                        if mets_away_score != mets_away_team_score:
                            await self.embedFunctions.scoring_plays_embed(mets_schedule[0], channel, mets_visitors, mets_away_team_score, mets_home_team_score)
                            mets_away_score = mets_away_team_score
                            time.sleep(15)
                        
                        if mets_home_score != mets_home_team_score:
                            await self.embedFunctions.scoring_plays_embed(mets_schedule[0], channel, mets_home_team, mets_away_score, mets_home_team_score)
                            mets_home_score = mets_home_team_score
                            time.sleep(15)

                    if (now.hour == (mets_new_hour.hour - 1)) and hour_var < 1:                
                        for item in soup_lineup.select("[data-league='AL']:-soup-contains('Orioles') .player > a.player-link"):
                            if item.get('data-razz') == '':
                                player_name = 'Unknown Player'
                                lineup_list.append(player_name)
                            else:
                                player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                                lineup_list.append(player_name)
                        pitchers.append(lineup_list[0])
                        pitchers.append(lineup_list[1])
                        
                        await channel.send('Starting Pitchers:\n' + str(mets_visitors) + ': ' + pitchers[0] + '\n' + str(mets_home_team) + ': ' + pitchers[1])

                        lineup_list.pop(0)
                        lineup_list.pop(0)
                        n = 9
                        home_list = lineup_list[n:]
                        away_list = lineup_list[:-n]

                        away_lineup = """```""" + str(mets_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                        await channel.send(away_lineup)

                        home_lineup = """```""" + str(mets_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                        await channel.send(home_lineup)
                        hour_var = 1

                        if now.hour != (mets_new_hour.hour - 1):
                            hour_var = 0
                    
                if type(yankees_schedule) is list:
                    final_status_list = ["Final", "Game Over", "Completed Early"]
                    scheduled_status_list = ["Scheduled", "Pre-Game"]
                    live_status_list = ["In Progress", "Delayed"]
                    other_status_list = ["Postponed"]
                    
                    if len(yankees_schedule) > 0:
                        yankees_visitors = yankees_schedule[0]['away_name']
                        yankees_home_team = yankees_schedule[0]['home_name']
                        yankees_away_team_code = self.embedFunctions.file_code(yankees_schedule[0])[0]
                        yankees_home_team_code = self.embedFunctions.file_code(yankees_schedule[0])[1]

                        for team in nl_teams:
                            if yankees_home_team == team:
                                yankees_interleague = True
                            else:
                                yankees_interleague = False

                        if len(yankees_schedule) == 2:
                            #Note for DoubleHeader Lineups: 45 minutes before first pitch of game 1 both teams should have their lineups and starting pitchers announced. 
                            # The game 2 lineups and starting lineups most likely won't be announced yet. Game 2 lineups don't get released until after game 1 has ended which helps
                            # alot. Before game 1 ends, we'll check if the length of the lineup list is equal to 19 or 20 after we've removed the game 1 starting pitchers.
                            #When printing game 1 lineups, we'll remove the starting pitcher(s) for game 2. Once game 1 ends, we can start looking for game 2 lineups
                            # and starting pitchers. We'll make the message once we are 45 minutes before first pitch to avoid any list index errors. Once both lineups and starting
                            # pitchers are released for game 2, we will remove game 1 lineups and starting lineups from the list. 
                            #GAME 1
                            yankees_game_id = yankees_schedule[0]['game_id']
                            yankees_game_time_local = self.testFunctions.get_local_time(yankees_schedule[0]['game_datetime'])
                            yankees_new_hour = yankees_game_time_local - timedelta(hours=10)
                            yankees_current_inning = str(yankees_schedule[0]['current_inning'])
                            yankees_half_inning = yankees_schedule[0]['inning_state']
                            yankees_current_inning_text = ''

                            if yankees_current_inning[-1] == '1':
                                yankees_current_inning += 'st'
                                yankees_current_inning_text = yankees_half_inning + ' of the ' + yankees_current_inning
                            elif yankees_current_inning[-1] == '2':
                                yankees_current_inning_text = 'nd'
                            elif yankees_current_inning[-1] == '3':
                                yankees_current_inning_text = 'rd'
                            elif 4 <= int(yankees_current_inning[-1]) <= 10:
                                yankees_current_inning += 'th'
                                yankees_current_inning_text = yankees_half_inning + ' of the ' + yankees_current_inning
                            
                            if (now.hour == yankees_new_hour.hour) and hour_var < 1:    #change to 45 minutes before first pitch  
                                if yankees_interleague == True:
                                    for item in soup_lineup.select("[data-league='NL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name = 'Unknown Player'
                                            lineup_list.append(player_name)
                                        else:
                                            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list.append(player_name)
                                    pitchers.append(lineup_list[0])
                                    pitchers.append(lineup_list[1])
                                    
                                    await channel.send('Starting Pitchers for Game 1:\n' + str(yankees_visitors) + ': ' + pitchers[0] + '\n' + str(yankees_home_team) + ': ' + pitchers[1])

                                    lineup_list.pop(0)
                                    lineup_list.pop(0)

                                    if len(lineup_list) == 19: #one starting pitcher announced for game 2
                                        lineup_list.pop()
                                        n = 9
                                        home_list = lineup_list[n:]
                                        away_list = lineup_list[:-n]
                                    elif len(lineup_list) == 20: #both starting pitchers announced for game 2
                                        lineup_list.pop()
                                        lineup_list.pop()
                                        n = 9
                                        home_list = lineup_list[n:]
                                        away_list = lineup_list[:-n]

                                    away_lineup = """```Game 1 """ + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                                    await channel.send(away_lineup)

                                    home_lineup = """```Game 1 """ + str(yankees_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                                    await channel.send(home_lineup)
                                    hour_var = 1

                                    if now.hour != (yankees_new_hour.hour):
                                        hour_var = 0
                                elif yankees_interleague == False:
                                    for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name = 'Unknown Player'
                                            lineup_list.append(player_name)
                                        else:
                                            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list.append(player_name)
                                    pitchers.append(lineup_list[0])
                                    pitchers.append(lineup_list[1])
                                    
                                    await channel.send('Starting Pitchers for Game 1:\n' + str(yankees_visitors) + ': ' + pitchers[0] + '\n' + str(yankees_home_team) + ': ' + pitchers[1])

                                    lineup_list.pop(0)
                                    lineup_list.pop(0)

                                    if len(lineup_list) == 19: #one starting pitcher announced for game 2
                                        lineup_list.pop()
                                        n = 9
                                        home_list = lineup_list[n:]
                                        away_list = lineup_list[:-n]
                                    elif len(lineup_list) == 20: #both starting pitchers announced for game 2
                                        lineup_list.pop()
                                        lineup_list.pop()
                                        n = 9
                                        home_list = lineup_list[n:]
                                        away_list = lineup_list[:-n]

                                    away_lineup = """```Game 1 """ + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                                    await channel.send(away_lineup)

                                    home_lineup = """```Game 1 """ + str(yankees_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                                    await channel.send(home_lineup)
                                    hour_var = 1

                                    if now.hour != (yankees_new_hour.hour):
                                        hour_var = 0

                            if yankees_pitcher_var < 1:
                                #Example: Gerrit Cole is starting today. Once we get this pitcher we will skip over this if statement since it is no longer needed until the next day
                                #Since the game has not started yet, Gerrit Cole is the only pitcher in the list. Therefore the corresponding if statement is never true until the first
                                #pitching change is made. Let's say Michael King replaces him. Once we see King gets added to the list the if statement becomes true. We print the pitching
                                #change, then set the home pitcher to be King to avoid the bot from printing the pitching change infinite times. This will continue for every other pitching
                                #change, like when Clay Holmes comes in, King is not equal to Holmes, so we print the next pitching change and so on and so forth. As soon as we hit
                                #sometime in the morning, the new starting pitchers will get updated. 
                                yankees_home_prob = yankees_schedule[0]['home_probable_pitcher'] 
                                yankees_away_prob = yankees_schedule[0]['away_probable_pitcher']
                                yankees_pitcher_var = 1
                                if now.hour == (yankees_new_hour.hour - 1):
                                    yankees_pitcher_var = 0
                            # if away_team == True and (yankees_new_hour.hour <= now.hour <= (yankees_new_hour.hour + 6)):
                            if any(game_status in yankees_schedule[0]['status'] for game_status in live_status_list):
                                yankees_away_team_score = int(yankees_schedule[0]['away_score'])
                                yankees_home_team_score = int(yankees_schedule[0]['home_score'])

                                yankees_pitchers = await self.embedFunctions.boxscore(int(yankees_game_id))
                                away_yankees_pitchers = yankees_pitchers[0]
                                home_yankees_pitchers = yankees_pitchers[1]

                                if away_yankees_pitchers[len(away_yankees_pitchers) - 1] != yankees_away_prob:
                                    await self.embedFunctions.pitching_change(channel, yankees_visitors, away_yankees_pitchers[len(away_yankees_pitchers) - 1], yankees_away_prob, yankees_current_inning_text)
                                    yankees_away_prob = away_yankees_pitchers[len(away_yankees_pitchers) - 1]
                                
                                if home_yankees_pitchers[len(home_yankees_pitchers) - 1] != yankees_home_prob:
                                    await self.embedFunctions.pitching_change(channel, yankees_home_team, home_yankees_pitchers[len(home_yankees_pitchers) - 1], yankees_home_prob, yankees_current_inning_text)
                                    yankees_home_prob = home_yankees_pitchers[len(home_yankees_pitchers) - 1]

                                if yankees_away_score != yankees_away_team_score:
                                    await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_visitors, yankees_away_team_score, yankees_home_team_score)
                                    yankees_away_score = yankees_away_team_score
                                    time.sleep(15)
                                    
                                if yankees_home_score != yankees_home_team_score:
                                    await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_home_team, yankees_away_team_score, yankees_home_team_score)
                                    yankees_home_score = yankees_home_team_score
                                    time.sleep(15)

                            if any(game_status in yankees_schedule[0]['status'] for game_status in final_status_list) and final_yan < 1: 
                                yankees_game_time_local_game_2 = self.testFunctions.get_local_time(yankees_schedule[1]['game_datetime'])
                                await channel.send("Game 1 of the " + str(yankees_visitors) + ' vs ' + str(yankees_home_team) + ' DH has ended. The final score is ' 
                                + str(yankees_away_team_code) + ': ' + str(yankees_away_team_score) + ' - ' + str(yankees_home_team_code) + ': ' + str(yankees_home_team_score) + '. Game 2 will \
                                    start at ' + str(yankees_game_time_local_game_2))
                                yankees_home_score = 0
                                yankees_away_score = 0
                                final_yan = 1
                                time.sleep(15)

                            elif any(game_status in yankees_schedule[0]['status'] for game_status in other_status_list) and final_yan < 1:
                                channel.send("Game 1 of the " + yankees_visitors + ' vs ' + yankees_home_team + ' DH is postponed.')
                                yankees_home_score = 0
                                yankees_away_score = 0
                                final_yan = 1
                                time.sleep(15)
                            
                            if any(game_status in yankees_schedule[0]['status'] for game_status in scheduled_status_list):
                                final_yan = 0
                            
                            #GAME 2
                            yankees_game_2_id = yankees_schedule[1]['game_id']
                            yankees_new_hour_game_2 = yankees_game_time_local_game_2 - timedelta(hours=10)
                            yankees_current_inning_game_2 = str(yankees_schedule[1]['current_inning'])
                            yankees_half_inning_game_2 = yankees_schedule[1]['inning_state']
                            yankees_current_inning_text_game_2 = ''

                            if yankees_current_inning_game_2[-1] == '1':
                                yankees_current_inning_game_2 += 'st'
                                yankees_current_inning_text_game_2 = yankees_half_inning_game_2 + ' of the ' + yankees_current_inning_game_2
                            elif yankees_current_inning_game_2[-1] == '2':
                                yankees_current_inning_text_game_2 = 'nd'
                            elif yankees_current_inning_game_2[-1] == '3':
                                yankees_current_inning_text_game_2 = 'rd'
                            elif 4 <= int(yankees_current_inning_game_2[-1]) <= 10:
                                yankees_current_inning_game_2 += 'th'
                                yankees_current_inning_text_game_2 = yankees_half_inning_game_2 + ' of the ' + yankees_current_inning_game_2
                            
                            if (now.hour == yankees_new_hour_game_2.hour) and hour_var_game_2 < 1:      
                                if yankees_interleague == True:
                                    for item in soup_lineup.select("[data-league='NL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name_game_2 = 'Unknown Player'
                                            lineup_list_game_2.append(player_name_game_2)
                                        else:
                                            player_name_game_2 = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list_game_2.append(player_name_game_2)
                                    
                                    num = 20
                                    del lineup_list_game_2[:num]
                                    pitchers_game_2.append(lineup_list_game_2[0])
                                    pitchers_game_2.append(lineup_list_game_2[1])
                                    lineup_list_game_2.pop(0)
                                    lineup_list_game_2.pop(0)
                                    await channel.send('Starting Pitchers for Game 2:\n' + str(yankees_visitors) + ': ' + pitchers_game_2[0] + '\n' + str(yankees_home_team) + ': ' + 
                                    pitchers_game_2[1])

                                    n_2 = 9
                                    home_list_game_2 = lineup_list_game_2[n:]
                                    away_list_game_2 = lineup_list_game_2[:-n]

                                    away_lineup_game_2 = """```Game 2 """ + str(yankees_visitors) + """ lineup\n1: """ + away_list_game_2[0] + """\n2: """ + away_list_game_2[1] + \
                                    """\n3: """ + away_list_game_2[2] + """\n4: """ + away_list_game_2[3] + """\n5: """ + away_list_game_2[4] + """\n6: """ + away_list_game_2[5] + \
                                    """\n7: """ + away_list_game_2[6] + """\n8: """ + away_list_game_2[7] + """\n9: """ + away_list_game_2[8] + """```"""
                                    await channel.send(away_lineup_game_2)

                                    home_lineup_game_2 = """```Game 2 """ + str(yankees_home_team) + """ lineup\n1: """ + home_list_game_2[0] + """\n2: """ + home_list_game_2[1] + \
                                    """\n3: """ + home_list_game_2[2] + """\n4: """ + home_list_game_2[3] + """\n5: """ + home_list_game_2[4] + """\n6: """ + \
                                    home_list_game_2[5] + """\n7: """ + home_list_game_2[6] + """\n8: """ + home_list_game_2[7] + """\n9: """ + home_list_game_2[8] + """```"""
                                    await channel.send(home_lineup_game_2)
                                    hour_var_game_2 = 1

                                    if now.hour != (yankees_new_hour_game_2.hour):
                                        hour_var_game_2 = 0
                                elif yankees_interleague == False:
                                    for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name_game_2 = 'Unknown Player'
                                            lineup_list_game_2.append(player_name_game_2)
                                        else:
                                            player_name_game_2 = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list_game_2.append(player_name_game_2)
                                    
                                    num = 20
                                    del lineup_list_game_2[:num]
                                    pitchers_game_2.append(lineup_list_game_2[0])
                                    pitchers_game_2.append(lineup_list_game_2[1])
                                    lineup_list_game_2.pop(0)
                                    lineup_list_game_2.pop(0)
                                    await channel.send('Starting Pitchers for Game 2:\n' + str(yankees_visitors) + ': ' + pitchers_game_2[0] + '\n' + str(yankees_home_team) + 
                                    ': ' + pitchers_game_2[1])

                                    lineup_list.pop(0)
                                    lineup_list.pop(0)
                                    n = 9
                                    home_list = lineup_list[n:]
                                    away_list = lineup_list[:-n]

                                    away_lineup = """```Game 2 """ + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                                    await channel.send(away_lineup)

                                    home_lineup = """```Game 2 """ + str(yankees_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                                    await channel.send(home_lineup)
                                    hour_var = 1

                                    if now.hour != (yankees_new_hour.hour - 1):
                                        hour_var = 0
                            if any(game_status in yankees_schedule[1]['status'] for game_status in final_status_list) and final_yan_game_2 < 1:
                                if yankees_away_team_score > yankees_home_team_score:
                                    await channel.send("""```Game 2 of the """ + str(yankees_visitors) + """ vs """ + str(yankees_home_team) + """ DH has ended. The final score is """ 
                                    + yankees_away_team_code + ": " + str(yankees_away_team_score) + """ - """ + yankees_home_team_code + ": " + str(yankees_home_team_score) + """```""")
                                elif yankees_home_team_score > yankees_away_team_score:
                                    await channel.send("""```Game 2 of the """ + str(yankees_visitors) + """ vs """ + str(yankees_home_team) + """ DH has ended. The final score is """
                                    + yankees_home_team_code + ": " + str(yankees_home_team_score) + """ - """ + yankees_away_team_code + ": " + str(yankees_away_team_score) + """```""")
                                final_yan_game_2 = 1
                                yankees_home_score = 0
                                yankees_away_score = 0
                                time.sleep(15)
                            elif any(game_status in yankees_schedule[1]['status'] for game_status in other_status_list) and final_yan_game_2 < 1:
                                final_yan_game_2 = 0
                                yankees_home_score = 0
                                yankees_away_score = 0
                                time.sleep(15)
                            
                            if any(game_status in yankees_schedule[1]['status'] for game_status in scheduled_status_list):
                                final_yan_game_2 = 0
                        elif len(yankees_schedule) == 1:
                            yankees_game_id = yankees_schedule[0]['game_id']
                            yankees_game_time_local = self.testFunctions.get_local_time(yankees_schedule[0]['game_datetime'])
                            yankees_new_hour = yankees_game_time_local - timedelta(hours=10)
                            yankees_current_inning = str(yankees_schedule[0]['current_inning'])
                            yankees_half_inning = yankees_schedule[0]['inning_state']
                            yankees_current_inning_text = ''

                            if yankees_current_inning[-1] == '1':
                                yankees_current_inning += 'st'
                                yankees_current_inning_text = yankees_half_inning + ' of the ' + yankees_current_inning
                            elif yankees_current_inning[-1] == '2':
                                yankees_current_inning_text = 'nd'
                            elif yankees_current_inning[-1] == '3':
                                yankees_current_inning_text = 'rd'
                            elif 4 <= int(yankees_current_inning[-1]) <= 10:
                                yankees_current_inning += 'th'
                                yankees_current_inning_text = yankees_half_inning + ' of the ' + yankees_current_inning

                            if (now.hour == yankees_new_hour.hour) and hour_var < 1:    #change to 45 minutes before first pitch  
                                if yankees_interleague == True:
                                    for item in soup_lineup.select("[data-league='NL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name = 'Unknown Player'
                                            lineup_list.append(player_name)
                                        else:
                                            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list.append(player_name)
                                    pitchers.append(lineup_list[0])
                                    pitchers.append(lineup_list[1])
                                    
                                    await channel.send('Starting Pitchers:\n' + str(yankees_visitors) + ': ' + pitchers[0] + '\n' + str(yankees_home_team) + ': ' + pitchers[1])

                                    lineup_list.pop(0)
                                    lineup_list.pop(0)

                                    away_lineup = """```""" + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                                    await channel.send(away_lineup)

                                    home_lineup = """```""" + str(yankees_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                                    await channel.send(home_lineup)
                                    hour_var = 1

                                    if now.hour != (yankees_new_hour.hour):
                                        hour_var = 0
                                elif yankees_interleague == False:
                                    for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
                                        if item.get('data-razz') == '':
                                            player_name = 'Unknown Player'
                                            lineup_list.append(player_name)
                                        else:
                                            player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                                            lineup_list.append(player_name)
                                    pitchers.append(lineup_list[0])
                                    pitchers.append(lineup_list[1])
                                    
                                    await channel.send('Starting Pitchers:\n' + str(yankees_visitors) + ': ' + pitchers[0] + '\n' + str(yankees_home_team) + ': ' + pitchers[1])

                                    lineup_list.pop(0)
                                    lineup_list.pop(0)

                                    away_lineup = """```""" + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                                    await channel.send(away_lineup)

                                    home_lineup = """```""" + str(yankees_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                                    await channel.send(home_lineup)
                                    hour_var = 1

                                    if now.hour != (yankees_new_hour.hour):
                                        hour_var = 0
                        
                            if any(game_status in yankees_schedule[0]['status'] for game_status in live_status_list):
                                yankees_away_team_score = int(yankees_schedule[0]['away_score'])
                                yankees_home_team_score = int(yankees_schedule[0]['home_score'])

                                yankees_pitchers = await self.embedFunctions.boxscore(int(yankees_game_id))
                                away_yankees_pitchers = yankees_pitchers[0]
                                home_yankees_pitchers = yankees_pitchers[1]

                                if away_yankees_pitchers[len(away_yankees_pitchers) - 1] != yankees_away_prob:
                                    await self.embedFunctions.pitching_change(channel, yankees_visitors, away_yankees_pitchers[len(away_yankees_pitchers) - 1], yankees_away_prob, yankees_current_inning_text)
                                    yankees_away_prob = away_yankees_pitchers[len(away_yankees_pitchers) - 1]
                                
                                if home_yankees_pitchers[len(home_yankees_pitchers) - 1] != yankees_home_prob:
                                    await self.embedFunctions.pitching_change(channel, yankees_home_team, home_yankees_pitchers[len(home_yankees_pitchers) - 1], yankees_home_prob, yankees_current_inning_text)
                                    yankees_home_prob = home_yankees_pitchers[len(home_yankees_pitchers) - 1]

                                if yankees_away_score != yankees_away_team_score:
                                    await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_visitors, yankees_away_team_score, yankees_home_team_score)
                                    yankees_away_score = yankees_away_team_score
                                    time.sleep(15)
                                    
                                if yankees_home_score != yankees_home_team_score:
                                    await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_home_team, yankees_away_team_score, yankees_home_team_score)
                                    yankees_home_score = yankees_home_team_score
                                    time.sleep(15)

                            if any(game_status in yankees_schedule[0]['status'] for game_status in final_status_list) and final_yan < 1: 
                                yankees_game_time_local_game_2 = self.testFunctions.get_local_time(yankees_schedule[1]['game_datetime'])
                                await channel.send("Game 1 of the " + str(yankees_visitors) + ' vs ' + str(yankees_home_team) + ' DH has ended. The final score is ' 
                                + str(yankees_away_team_code) + ': ' + str(yankees_away_team_score) + ' - ' + str(yankees_home_team_code) + ': ' + str(yankees_home_team_score) + '. Game 2 will \
                                    start at ' + str(yankees_game_time_local_game_2))
                                yankees_home_score = 0
                                yankees_away_score = 0
                                final_yan = 1
                                time.sleep(15)

                            elif any(game_status in yankees_schedule[0]['status'] for game_status in other_status_list) and final_yan < 1:
                                channel.send("Game 1 of the " + yankees_visitors + ' vs ' + yankees_home_team + ' DH is postponed.')
                                yankees_home_score = 0
                                yankees_away_score = 0
                                final_yan = 1
                                time.sleep(15)
                            
                            if any(game_status in yankees_schedule[0]['status'] for game_status in scheduled_status_list):
                                final_yan = 0

                if type(mets_schedule) is list:
                    final_status_list = ["Final", "Game Over", "Completed Early"]
                    scheduled_status_list = ["Scheduled", "Pre-Game"]
                    live_status_list = ["In Progress", "Delayed"]
                    other_status_list = ["Postponed"]
                    
                    if len(mets_schedule) == 2:
                        #game 1
                        if any(game_status in mets_schedule[0]['status'] for game_status in final_status_list): 
                            await channel.send("Game 1 of the " + str(mets_visitors) + ' vs ' + str(mets_home_team) + ' DH has ended. The final score is ' 
                            + str(mets_away_team_code) + ': ' + str(mets_away_team_score) + ' - ' + str(mets_home_team_code) + ': ' + str(mets_home_team_score) + '. Game 2 will \
                                start at ' + str(yankees_game_time_local))
                            mets_home_score = 0
                            mets_away_score = 0
                            time.sleep(15)
                        elif any(game_status in mets_schedule[0]['status'] for game_status in other_status_list):
                            channel.send(mets_schedule[0]['away_name'] + ' vs ' + mets_schedule[0]['home_name'] + ' game is postponed.')
                            mets_home_score = 0
                            mets_away_score = 0
                            time.sleep(15)

                        # #game 2
                        # if any(game_status in queried_schedule[1]['status'] for game_status in final_status_list):
                        #     await self.embedFunctions.final_game_embed(queried_schedule[1], message)
                        #     if len(next_games) > 0:
                        #         await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                        # elif any(game_status in queried_schedule[1]['status'] for game_status in scheduled_status_list):
                        #     await self.embedFunctions.scheduled_game_embed(queried_schedule[1], message)
                        #     if previous_game is not None:
                        #         await self.embedFunctions.final_game_embed(previous_game, message)
                        # elif any(game_status in queried_schedule[1]['status'] for game_status in live_status_list):
                        #     await self.embedFunctions.live_game_embed(queried_schedule[1], message)
                        #     return
                        # elif any(game_status in queried_schedule[1]['status'] for game_status in other_status_list): await self.embedFunctions.generic_Game_Embed(queried_schedule[0], message)
                        # if len(next_games) > 0: await self.embedFunctions.scheduled_game_embed(next_games[0], message)
                    
                    elif ((len(mets_schedule) == 1) and (final_met < 1)):
                        if any(game_status in mets_schedule[0]['status'] for game_status in final_status_list):
                            if mets_away_team_score > mets_home_team_score:
                                await channel.send("""```The """ + str(mets_visitors) + """ vs """ + str(mets_home_team) + """ game has ended. The final score is """ 
                                + str(mets_away_team_score) + """ - """ + str(mets_home_team_score) + """```""")
                            elif mets_home_team_score > mets_away_team_score:
                                await channel.send("""```The """ + str(mets_visitors) + """ vs """ + str(mets_home_team) + """ game has ended. The final score is """
                                + str(mets_home_team_score) + """```""")
                            final_met = 1
                            mets_home_score = 0
                            mets_away_score = 0
                            time.sleep(15)
                        
                        if any(game_status in mets_schedule[0]['status'] for game_status in scheduled_status_list):
                            final_met = 0
                            mets_home_score = 0
                            mets_away_score = 0
                            time.sleep(15)
                   
                    #         if previous_game is not None: await self.embedFunctions.final_game_embed(previous_game, message)
                    #     elif any(game_status in queried_schedule[0]['status'] for game_status in  other_status_list):
                    #         await self.embedFunctions.generic_Game_Embed(queried_schedule[0], message)
                    #         if len(next_games) > 0:
                    #             await self.embedFunctions.scheduled_Game_Embed(next_games[0],  message)

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_num = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_num)
            print('DEBUG: Exception is %s' % e)
            await channel.send('Error: ' + str(e))

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
                    elif 'BREAK' in message_array[1].upper():
                        await message.channel.send('breaking loop')
                        var = 1
                    # elif message_array[1].upper() == 'ACTIVATE':
                    #     while break_var != True:
                    #         await message.channel.send('team activated. you will now receive notifs')
                    #     # while break_var != True:
                    #     #     await self.embedFunctions.team_notifications('padres', 789273776105193472, True)
                    # if message_array[0].upper() == 'BOT' and message_array[1].upper() == 'DEACTIVATE':
                    #     await message.channel.send('team deactiviating. no more notifs')
                    #     break_var = False
                    #     #await self.embedFunctions.team_notifications('padres', 789273776105193472, False)
                    # teams = [x['name'] for x in statsapi.get('teams',{'sportIds':1,'activeStatus':'Yes','fields':'teams,name'})['teams']]
                    # for team in teams:
                    #     for name in statsapi.lookup_team(team):
                    #         upper_team = name['teamName'].upper()
                    #         if message_array[0].upper() == 'BOT' and message_array[1].upper() == upper_team:
                    #             if len(message_array) > 1:
                    #                 if message_array[2].upper() == 'ON':
                    #                     #await message.channel.send(message_array[1] + ('notifs are now on'))
                    #                     var = 0
                    #                     away_team = True
                    #                     yankees_away_score = 0
                    #                     yankees_home_score = 0
                    #                     mets_away_score = 0
                    #                     mets_home_score = 0
                    #                     lineup_url = "https://www.baseballpress.com/lineups/" 
                    #                     r = requests.get(lineup_url)
                    #                     soup_lineup = BeautifulSoup(r.text, 'lxml') 
                    #                     lineup_list = []
                    #                     pitchers = []
                    #                     hour_var = 0
                                        
                    #                     while var < 1:
                    #                         target_date_time = datetime.datetime.now() - timedelta(hours=4) #changing from 4 to 8
                    #                         yankees = self.testFunctions.get_team_no_msg('yankees')
                    #                         mets = self.testFunctions.get_team_no_msg('mets')
                    #                         mets_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(mets['id']))
                    #                         yankees_schedule = statsapi.schedule(date = target_date_time.strftime('%Y-%m-%d'), team = int(yankees['id'])) #'%Y-%m-%d
                    #                         now = datetime.datetime.now() - timedelta(hours=4) #changing from 4 to 8
                                            
                    #                         if len(yankees_schedule) > 0:
                    #                             yankees_game_id = yankees_schedule[0]['game_id']
                    #                             yankees_visitors = yankees_schedule[0]['away_name']
                    #                             yankees_home_team = yankees_schedule[0]['home_name']
                    #                             yankees_game_time_local = self.testFunctions.get_local_time(yankees_schedule[0]['game_datetime'])
                    #                             yankees_new_hour = yankees_game_time_local - timedelta(hours=4)
                    #                             yankees_new_minute = yankees_game_time_local - timedelta(minutes=5)
                    #                             yankees_away_team_code = self.embedFunctions.file_code(yankees_schedule[0])[0]
                    #                             yankees_home_team_code = self.embedFunctions.file_code(yankees_schedule[0])[1]
                    #                             yankees_home_prob = yankees_schedule[0]['home_probable_pitcher']
                    #                             yankees_away_prob = yankees_schedule[0]['away_probable_pitcher']
                    #                             #yankees_pitchers = await self.embedFunctions.boxscore(int(yankees_game_id))

                    #                             if yankees_visitors == 'New York Yankees':
                    #                                 away_team = True
                    #                             elif yankees_home_team == 'New York Yankees':
                    #                                 away_team = False

                    #                             if away_team == True and (yankees_new_hour.hour <= now.hour <= (yankees_new_hour.hour + 4)):
                    #                                 yankees_away_team_score = int(yankees_schedule[0]['away_score'])
                    #                                 yankees_home_team_score = int(yankees_schedule[0]['home_score'])
                    #                                 if yankees_away_score != yankees_away_team_score:
                    #                                     await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_visitors, yankees_away_team_score, yankees_home_team_score)
                    #                                     yankees_away_score = yankees_away_team_score
                    #                                     time.sleep(15)
                                                        
                    #                                 if yankees_home_score != yankees_home_team_score:
                    #                                     await self.embedFunctions.scoring_plays_embed(yankees_schedule[0], channel, yankees_home_team, yankees_away_team_score, yankees_home_team_score)
                    #                                     yankees_home_score = yankees_home_team_score
                    #                                     time.sleep(15)
                                                    
                    #                                 # if yankees_pitchers[len(yankees_pitchers) - 1] != yankees_away_prob:
                    #                                 #     await channel.send(yankees_away_prob) + ' has been replaced by ' + str(yankees_pitchers[len(yankees_pitchers) - 1])
                    #                                 #     yankees_away_prob = yankees_pitchers[len(yankees_pitchers) - 1]
                                                    
                    #                             if (now.hour == (yankees_new_hour.hour - 1)) and hour_var < 1:                
                    #                                 for item in soup_lineup.select("[data-league='AL']:-soup-contains('Yankees') .player > a.player-link"):
                    #                                     if item.get('data-razz') == '':
                    #                                         player_name = 'Unknown Player'
                    #                                         lineup_list.append(player_name)
                    #                                     else:
                    #                                         player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                    #                                         lineup_list.append(player_name)
                    #                                 pitchers.append(lineup_list[0])
                    #                                 pitchers.append(lineup_list[1])
                                                    
                    #                                 await message.channel.send('Starting Pitchers:\n' + str(yankees_visitors) + ': ' + pitchers[0] + '\n' + str(yankees_home_team) + ': ' + pitchers[1])

                    #                                 lineup_list.pop(0)
                    #                                 lineup_list.pop(0)
                    #                                 n = 9
                    #                                 home_list = lineup_list[n:]
                    #                                 away_list = lineup_list[:-n]

                    #                                 away_lineup = """```""" + str(yankees_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    #                                 await message.channel.send(away_lineup)

                    #                                 home_lineup = """```""" + str(yankees_home_team) + """lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    #                                 await message.channel.send(home_lineup)
                    #                                 hour_var = 1

                    #                                 if now.hour != (yankees_new_hour.hour - 1):
                    #                                     hour_var = 0

                    #                         if len(mets_schedule) > 0:
                    #                             mets_game_id = mets_schedule[0]['game_id']
                    #                             mets_visitors = mets_schedule[0]['away_name']
                    #                             mets_home_team = mets_schedule[0]['home_name']
                    #                             mets_game_time_local = self.testFunctions.get_local_time(mets_schedule[0]['game_datetime'])
                    #                             mets_new_hour = mets_game_time_local - timedelta(hours=4)
                    #                             mets_new_minute = mets_game_time_local - timedelta(minutes=5)
                    #                             mets_home_prob = mets_schedule[0]['home_probable_pitcher']
                    #                             mets_away_prob = mets_schedule[0]['away_probable_pitcher']
                    #                             #mets_pitchers = await self.embedFunctions.boxscore(int(mets_game_id))
                    #                             if away_team == True and (mets_new_hour.hour <= now.hour <= (mets_new_hour.hour + 3)):
                    #                                 mets_away_team_score = int(mets_schedule[0]['away_score'])
                    #                                 mets_home_team_score = int(mets_schedule[0]['home_score'])
                    #                                 if mets_away_score != mets_away_team_score:
                    #                                     await self.embedFunctions.scoring_plays_embed(mets_schedule[0], channel, mets_visitors, mets_away_team_score, mets_home_team_score)
                    #                                     mets_away_score = mets_away_team_score
                    #                                     time.sleep(15)
                                                    
                    #                                 if mets_home_score != mets_home_team_score:
                    #                                     await self.embedFunctions.scoring_plays_embed(mets_schedule[0], channel, mets_home_team, mets_away_score, mets_home_team_score)
                    #                                     mets_home_score = mets_home_team_score
                    #                                     time.sleep(15)

                    #                             if (now.hour == (mets_new_hour.hour - 1)) and hour_var < 1:                
                    #                                 for item in soup_lineup.select("[data-league='NL']:-soup-contains('Mets') .player > a.player-link"):
                    #                                     if item.get('data-razz') == '':
                    #                                         player_name = 'Unknown Player'
                    #                                         lineup_list.append(player_name)
                    #                                     else:
                    #                                         player_name = item.get('data-razz').split("/")[-2].replace("+"," ")
                    #                                         lineup_list.append(player_name)
                    #                                 pitchers.append(lineup_list[0])
                    #                                 pitchers.append(lineup_list[1])
                                                    
                    #                                 await message.channel.send('Starting Pitchers:\n' + str(mets_visitors) + ': ' + pitchers[0] + '\n' + str(mets_home_team) + ': ' + pitchers[1])

                    #                                 lineup_list.pop(0)
                    #                                 lineup_list.pop(0)
                    #                                 n = 9
                    #                                 home_list = lineup_list[n:]
                    #                                 away_list = lineup_list[:-n]

                    #                                 away_lineup = """```""" + str(mets_visitors) + """ lineup\n1: """ + away_list[0] + """\n2: """ + away_list[1] + """\n3: """ + away_list[2] + """\n4: """ + away_list[3] + """\n5: """ + away_list[4] + """\n6: """ + away_list[5] + """\n7: """ + away_list[6] + """\n8: """ + away_list[7] + """\n9: """ + away_list[8] + """```"""
                    #                                 await message.channel.send(away_lineup)

                    #                                 home_lineup = """```""" + str(mets_home_team) + """ lineup\n1: """ + home_list[0] + """\n2: """ + home_list[1] + """\n3: """ + home_list[2] + """\n4: """ + home_list[3] + """\n5: """ + home_list[4] + """\n6: """ + home_list[5] + """\n7: """ + home_list[6] + """\n8: """ + home_list[7] + """\n9: """ + home_list[8] + """```"""
                    #                                 await message.channel.send(home_lineup)
                    #                                 hour_var = 1

                    #                                 if now.hour != (mets_new_hour.hour - 1):
                    #                                     hour_var = 0
                elif message_array[0].upper() == 'BOT' and len(message_array) == 1:
                    await message.channel.send('test')
                    print('test')
                    return
            else:
                return
    
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('Hi there.')
            break

client = Bot()  
client.run(os.environ["DISCORD_TOKEN"])