#!Python3.9

from ..textinput import ModalTextInput

from logging import getLogger
_log = getLogger(__name__)

class TextinputSuiseicordHappi(ModalTextInput):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
