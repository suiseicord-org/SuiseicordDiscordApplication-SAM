#!python3.9

from application.commands import (
    HappiAnnounceLanguage
)

from .happi_announce import CmpHappiAnnounce
from .happi_announce_jp import CmpHappiAnnounceJp
from .happi_announce_en import CmpHappiAnnounceEn

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpHappiAnnounce:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    #happi-announce-{jp|en}
    lang: str = _commands[2].lower()
    _log.debug("lang: {}".format(lang))
    if lang == HappiAnnounceLanguage.jp:
        _log.debug("lang == HappiAnnounceLanguage.jp")
        return CmpHappiAnnounceJp(rawdata)
    elif lang == HappiAnnounceLanguage.en:
        _log.debug("lang == HappiAnnounceLanguage.en")
        return CmpHappiAnnounceEn(rawdata)