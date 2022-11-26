#!python3.9
import os
import requests

from application.mytypes.snowflake import Snowflake

from . import ApiBaseUrl
from .channel import Channel

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

BOT_TOKEN = os.getenv('DISCORD_TOKEN')

from logging import getLogger
_log = getLogger(__name__)

class Message:
    def __init__(self, ch_id: Snowflake, msg_id: Snowflake):
        self.id: Snowflake = msg_id
        self.channel: Channel = Channel(ch_id)
    
    def edit(self, payload: dict) -> requests.Response:
        url: str = ApiBaseUrl + f"/channels/{self.channel.id}/messages/{self.id}"
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }
        r = requests.patch(url, headers=headers, json=payload)
        return r