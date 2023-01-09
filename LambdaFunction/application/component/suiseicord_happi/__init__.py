#!python3.9
from application.commands import HappiCommand as HappiCommandName

from .suiseicord_happi import CmpSuiseicordHappi
from .happi_announce import from_data as cha_from_data
from .happi_payreport import from_data as chp_from_data
from .happi_paycheck import CmpHappiPaycheck

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpSuiseicordHappi:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    sub_command: str = _commands[1].lower()
    _log.debug("sub_command: {}".format(sub_command))
    if sub_command == HappiCommandName.announce:
        _log.debug("sub_command == HappiCommandName.announce")
        return cha_from_data(rawdata)
    elif sub_command == HappiCommandName.report:
        _log.debug("sub_command == HappiCommandName.report")
        return chp_from_data(rawdata)
    elif sub_command == HappiCommandName.check:
        _log.debug("sub_command == HappiCommandName.check")
        return CmpHappiPaycheck(rawdata)
