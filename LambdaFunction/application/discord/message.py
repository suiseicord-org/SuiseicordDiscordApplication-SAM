#!python3.9
import os
import requests
from typing import Optional

from application.mytypes.snowflake import Snowflake

from .channel import Channel
from .http import Route

from logging import getLogger
_log = getLogger(__name__)

class Message:
    def __init__(self, ch_id: Snowflake, msg_id: Snowflake):
        self.id: Snowflake = msg_id
        self.channel: Channel = Channel(ch_id)
    
    def edit(self, payload: Optional[dict] = None, **kwargs) -> requests.Response:
        if kwargs.get("json_payload") and payload is not None:
            kwargs["json_payload"] = payload
        route = Route('PATCH', f"/channels/{self.channel.id}/messages/{self.id}", **kwargs)
        r = route.requets()
        return r