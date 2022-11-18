#!python3.9

from application.commands import (
    VSongAwardYear
)

from .vsong_award import VSongAward
from .vsong_award_2022 import VSongAward2022

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict, bot_token: str) -> VSongAward:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    year: str = _commands[2].lower()
    _log.debug("year: {}".format(year))
    if year == VSongAwardYear.vsa_2022:
        _log.debug(year == VSongAwardYear.vsa_2022)
        return VSongAward2022(rawdata, bot_token)
