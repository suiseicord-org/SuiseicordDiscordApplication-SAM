#!python3.9

from ..interaction import Interaction

from logging import getLogger
_log = getLogger(__name__)

class ModalSubmit(Interaction):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        self.custom_id: str = self._data["custom_id"]
        self.message_data: dict = rawdata["message"]

