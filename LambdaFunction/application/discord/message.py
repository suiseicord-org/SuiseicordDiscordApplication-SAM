#!python3.9
import requests

from application.mytypes.snowflake import Snowflake

from . import ApiBaseUrl
from .channel import Channel

from logging import getLogger
_log = getLogger(__name__)

class Message:
    def __init__(self, bot_token: str, ch_id: Snowflake, msg_id: Snowflake):
        self.id: Snowflake = msg_id
        self.channel: Channel = Channel(bot_token, ch_id)
        self.bot_token: str = bot_token
    
    def edit(self, payload: dict) -> requests.Response:
        url: str = ApiBaseUrl + f"/channels/{self.channel.id}/messages/{self.id}"
        headers = {
            "Authorization": f"Bot {self.bot_token}"
        }
        r = requests.patch(url, headers=headers, json=payload)
        return r