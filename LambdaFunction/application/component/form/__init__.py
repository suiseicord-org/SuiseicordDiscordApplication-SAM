#!python3.9
from application.commands import (
    FormCategory as FormCategoryName
)

from .form import Form

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> Form:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    category_name: str = _commands[1].lower()
    _log.debug("category_name: {}".format(category_name))
    if category_name == FormCategoryName.vsong_award:
        _log.debug(category_name == FormCategoryName.vsong_award)
        from .vtuber_song_award import from_data as vsa_from_data
        return vsa_from_data(rawdata)
