import discord
import json
import datetime
from datetime import timedelta
import time
import statsapi
import dateutil.parser
import requests

class TestFunctions:
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
