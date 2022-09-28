#!python3.9
from .happi_announce import CmpHappiAnnounce

from application.messages.message import (MessageFile, filepath)
from application.happi_setting import HappiSetting

from logging import getLogger
_log = getLogger(__name__)

class CmpHappiAnnounceEn(CmpHappiAnnounce):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
    
    def run(self) -> None:
        super().run()

        return
    
    def response(self) -> None:

        return super().response()
    
    def clean(self) -> None:
        return super().clean()

    @property
    def fp(self) -> str:
        return filepath(MessageFile.SuiseiCordHappi.guide_en)
    
    @property
    def form_url(self) -> str:
        return super()._create_url(HappiSetting.Form.enform)
    
    @property
    def label(self) -> str:
        return HappiSetting.Form.enlabel