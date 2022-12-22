#!python3.9
import os
import json
import requests
from urllib.parse import (
    urlencode,
    quote as _uriquote
)

from typing import (
    Optional
)

from . import ApiBaseUrl
from .attachment import Attachment
from .file import File

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

BOT_TOKEN = os.getenv('DISCORD_TOKEN')

from logging import getLogger
_log = getLogger(__name__)

class Route:
    def __init__(
        self,
        method: str,
        path: str,
        *,
        query: Optional[dict[str, str]] = None,
        json_payload: Optional[dict] = None,
        files: Optional[list[File]] = None,
        attachments: Optional[list[Attachment]] = None,
        reason: Optional[str] = None,
        **kwargs
    ):
        self.method: str = method
        self.path: str = path
        self.query: Optional[dict[str, str]] = query
        self.json_payload: Optional[dict] = json_payload
        self.files: Optional[list[File]] = files
        self.attachments: Optional[list[Attachment]] = attachments
        self.reason: Optional[str] = reason

    def requets(self, *, appcmd_response: bool = False, _raise: bool = False) -> requests.Response:
        url: str = ApiBaseUrl + self.path

        # headers
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }
        if self.reason:
            _log.debug("Add X-Audit-Log-Reason: {}".format(self.reason))
            headers['X-Audit-Log-Reason'] = _uriquote(self.reason, safe='/ ')

        files: Optional[dict] = None
        simple_payload: Optional[dict] = None

        # attachments, files
        if (self.files is not None) or (self.attachments is not None):
            index = 0
            attachments_payload: list = []
            files_data: dict = {}
            if self.files is not None:
                for file in self.files:
                    attachments_payload.append(file.to_dict(index))
                    files_data[f"files[{index}]"] = (file.filename, file.fp)
                    index += 1
            if self.attachments is not None:
                for attachment in self.attachments:
                    attachments_payload.append(attachment.to_dict(index))
                    files_data[f"files[{index}]"] = (attachment.filename, attachment.open(), attachment.content_type)
                    index += 1
            
            if self.json_payload is None:
                self.json_payload = {}
            if appcmd_response:
                if not bool(self.json_payload.get('data')):
                    self.json_payload["data"] = {}
                self.json_payload["data"]["attachments"] = attachments_payload
            else:
                self.json_payload["attachments"] = attachments_payload

            files = files_data
            files["payload_json"] = (None, json.dumps(self.json_payload), 'application/json')
            _log.debug("payload_json: {}".format(self.json_payload))
        elif self.json_payload is not None:
            simple_payload = self.json_payload
            _log.debug("simple_payload: {}".format(simple_payload))
        else:
            pass

        _log.info("method: '{0}'; url: '{1}'; params: {2};".format(self.method, url, str(self.query)))
        _log.debug("files: {}".format(files))
        res: requests.Response = requests.request(
            method=self.method,
            url = url,
            headers=headers,
            params = self.query,
            files = files,
            json = simple_payload
        )
        _log.info("status_code: {}".format(res.status_code))
        _log.info("response: {}".format(res.text))

        if _raise:
            res.raise_for_status()
        
        return res