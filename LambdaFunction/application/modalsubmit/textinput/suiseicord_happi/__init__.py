#!python3.9

from application.commands import HappiCommand as HappiCommandName

from .suiseicord_happi import TextinputSuiseicordHappi
from .happi_payreport import TextinputHappiPayreport

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> TextinputSuiseicordHappi:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    happi_command: str = _commands[2].lower()
    _log.debug("happi_command: {}".format(happi_command))
    if happi_command == HappiCommandName.report:
        _log.debug("happi_command == HappiCommandName.report")
        return TextinputHappiPayreport(rawdata)