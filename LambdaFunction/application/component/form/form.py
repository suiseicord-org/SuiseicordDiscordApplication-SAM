#!python3.9
from urllib.parse import urlencode, quote_plus
from ..component import Component

from logging import getLogger
_log = getLogger(__name__)

class Form(Component):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.form_url: str = ''
        self.entrys: dict[str : str] = dict()

    def check(self) -> bool:
        return self.check_permission()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        super().response()
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    @property
    def inputed_url(self) -> str:
        query: dict[str: str] = dict()
        string_query: list[str] = []
        for k, v in self.entrys.items():
            # query[f'entry.{k}'] = quote_plus(v)
            # query[f'entry.{k}'] = v
            string_query.append(f'entry.{k}={v}')
        
        return '%s?%s' % (self.form_url, '&'.join(string_query))
        # return '%s?%s' % (self.form_url, urlencode(query))
