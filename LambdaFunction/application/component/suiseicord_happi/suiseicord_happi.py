#!python3.9
from requests import Response

from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

class CmpSuiseicordHappi(Component):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def happi_error(self, r: Response):
        pass


