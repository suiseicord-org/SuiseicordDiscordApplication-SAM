#!python
from ..modal_submit import ModalSubmit

from logging import getLogger
_log = getLogger(__name__)

class ModalTextInput(ModalSubmit):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.message_data: dict = rawdata["message"]

    def check(self) -> bool:
        return super().check()
    
    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    
    def parse_values(self) -> dict[str, str]:
        result: dict[str, str] = {}
        for comp in self._data["components"]:
            _data: dict = comp["components"][0]
            result[_data["custom_id"]] = _data["value"]
        return result
