#!python3.9
from ..application_command import ApplicationCommand

from application.discord.message import Message

from logging import getLogger
_log = getLogger(__name__)

class MessageCommand(ApplicationCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.target_id: str = self._data['target_id']
        self.target_message: Message = Message(
            self._data['resolved']['messages'][self.target_id],
            self._guild_id
        )
    
    def check(self) -> bool:
        """Slash Commands is always 'True'."""
        return True

    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        super().response()
        return
    
    def clean(self) -> None:
        super().clean()
        return

