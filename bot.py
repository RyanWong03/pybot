import discord
import os
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get
import requests
from bs4 import BeautifulSoup
import datetime
import lxml
import time
import statsapi
import testfunctions
import json
import players
import sys

# intents = discord.Intents.default()
# intents.members = True
# client = commands.Bot(command_prefix = '$', intents=intents)

def print_lineup(list, str):
    str += "{0}"
    list = [str.format(i) for i in list]
    return 

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
    testFunctions = testfunctions.TestFunctions()
    async def on_ready(self):
        id = 318132313672384512
        discordUser = self.get_user(id)
        await self.change_presence(status = discord.Status.idle, activity = discord.Activity(type = discord.ActivityType.playing, name = "$help"))
        await discordUser.send('Bot Online')
        print('Bot is ready.')

    async def on_message(self, message):
        if(message.author == self.user) or message.author.bot:
            return
        else:
            message_array = message.content.split()
            if len(message_array) > 0:
                if ('BOT' in message_array[0].upper() and len(message_array) > 1) or (str(self.user.id) in message_array[0].upper()):
                    if 'PLAYER' in message_array[1].upper():
                        try:
                            now = datetime.now()
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