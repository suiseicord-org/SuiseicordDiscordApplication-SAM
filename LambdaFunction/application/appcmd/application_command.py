#!python3.9
from ..interaction import Interaction

from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class ApplicationCommand(Interaction):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.command_id: Snowflake = self._data["id"]
        self.command_name: str = self._data["name"]
        self.command_type: int = self._data["type"]

    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return
