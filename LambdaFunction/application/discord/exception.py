#!python3.9
import os
from requests import Response
from typing import Dict, List, Optional, TYPE_CHECKING, Any, Tuple, Union

from logging import getLogger
_log = getLogger(__name__)

class DiscordException(Exception):
    """Base exception class"""

    pass

def _flatten_error_dict(d: Dict[str, Any], key: str = '') -> Dict[str, str]:
    items: List[Tuple[str, str]] = []
    for k, v in d.items():
        new_key = key + '.' + k if key else k

        if isinstance(v, dict):
            try:
                _errors: List[Dict[str, Any]] = v['_errors']
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, ' '.join(x.get('message', '') for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)

class HttpException(DiscordException):
    def __init__(self, response: Response, message: Optional[Union[str, Dict[str, Any]]]):
        self.response: Response = response
        self.status: int = response.status_code  # type: ignore # This attribute is filled by the library even if using requests
        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get('code', 0)
            base = message.get('message', '')
            errors = message.get('errors')
            if errors:
                errors = _flatten_error_dict(errors)
                helpful = '\n'.join('In %s: %s' % t for t in errors.items())
                self.text = base + '\n' + helpful
            else:
                self.text = base
        else:
            self.text = message or ''
            self.code = 0

        fmt = '{0.status} {0.reason} (error code: {1})'
        if len(self.text):
            fmt += ': {2}'

        super().__init__(fmt.format(self.response, self.code, self.text))

class Forbidden(HttpException):
    """Exception that's raised for when status code 403 occurs.

    Subclass of :exc:`HttpException`
    """

    pass


class NotFound(HttpException):
    """Exception that's raised for when status code 404 occurs.

    Subclass of :exc:`HttpException`
    """

    pass