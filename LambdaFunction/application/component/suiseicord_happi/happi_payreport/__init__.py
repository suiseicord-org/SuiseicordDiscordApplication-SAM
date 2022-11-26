#!python3.9
from application.commands import HappiPayreportAction

from .happi_payreport import CmpHappiPayreport

from .happi_payreport_bank import CmpHappiPayreportBank
from .happi_payreport_paypal_jp import CmpHappiPayreportPaypalJp
from .happi_payreport_paypal_en import CmpHappiPayreportPaypalEn

from logging import getLogger
_log = getLogger(__name__)

def from_data(rawdata: dict) -> CmpHappiPayreport:
    _commands: list[str] = rawdata["data"]["custom_id"].split("-")
    action: str = _commands[2].lower()
    _log.debug("action: {}".format(action))
    if action == HappiPayreportAction.bank:
        _log.debug("action == HappiPayreportAction.bank")
        return CmpHappiPayreportBank(rawdata)
    elif action == HappiPayreportAction.paypal_jp:
        _log.debug("action == HappiPayreportAction.paypal_jp")
        return CmpHappiPayreportPaypalJp(rawdata)
    elif action == HappiPayreportAction.paypal_en:
        _log.debug("action == HappiPayreportAction.paypal_en")
        return CmpHappiPayreportPaypalEn(rawdata)