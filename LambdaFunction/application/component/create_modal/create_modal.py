#!python3.9

from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

class CmpCreateModal(Component):

    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        super().response()
        return 
    
    def clean(self) -> None:
        return super().clean()