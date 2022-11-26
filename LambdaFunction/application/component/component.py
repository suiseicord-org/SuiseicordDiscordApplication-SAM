#!python3.9
from typing import (
    Optional
)

from ..interaction import Interaction

from logging import getLogger
_log = getLogger(__name__)

class Component(Interaction):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.message_data: dict = rawdata["message"]

    def check(self) -> bool:
        return self.check_permission()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        super().response()
        return 
    
    def clean(self) -> None:
        return super().clean()
