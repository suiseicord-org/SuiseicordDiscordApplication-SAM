#!python3.9
import os
import requests
from typing import Optional

from application.mytypes.snowflake import Snowflake
from application.mytypes.message import (
    Message as MessagePayload
)
from application.mytypes.embed import (
    Embed as EmbedPayload
)

from .channel import Channel
from .http import Route

from logging import getLogger
_log = getLogger(__name__)

class PartiaMessage:
    def __init__(self, ch_id: Snowflake, msg_id: Snowflake):
        self.id: Snowflake = msg_id
        self.channel: Channel = Channel(ch_id)
    
    def edit(self, payload: Optional[dict] = None, **kwargs) -> requests.Response:
        if kwargs.get("json_payload") and payload is not None:
            kwargs["json_payload"] = payload
        route = Route('PATCH', f"/channels/{self.channel.id}/messages/{self.id}", **kwargs)
        r = route.requets()
        return r

class Message(PartiaMessage):
    def __init__(self, payload: MessagePayload):
        super().__init__(payload["channel_id"], payload["id"])
    
    def to_embed(self) -> EmbedPayload:
        pass