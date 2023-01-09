#!python3.9
from ..slash_command import SlashCommand

from logging import getLogger
_log = getLogger(__name__)

class SlashChannel(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return
