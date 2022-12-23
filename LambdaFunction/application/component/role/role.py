#!python3.9
from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

class CmpRole(Component):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def check(self) -> bool:
        return super().check()
    
    def run(self) -> None:
        return super().run()

    def response(self) -> None:
        return super().response()
    
    def clean(self) -> None:
        return super().clean()