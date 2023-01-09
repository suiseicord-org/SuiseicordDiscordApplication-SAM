#!python3.9
import os, shutil
import requests
from typing import Optional, Dict, Any

from application.mytypes.snowflake import Snowflake
from application.mytypes.message import (
    Attachment as AttachmentPayload
)
from .exception import (
    HttpException,
    Forbidden,
    NotFound
)

from logging import getLogger
_log = getLogger(__name__)

class Attachment:
    def __init__(self, payload: AttachmentPayload, *, use_cached: bool = False) -> None:
        self.id: Snowflake = payload['id']
        self.filename: str = payload['filename']
        self.size: int = payload['size']
        self.url: str = payload['url']
        self.proxy_url: str = payload['proxy_url']
        self.height: Optional[int] = payload.get('height')
        self.width: Optional[int] = payload.get('width')
        self.description: Optional[str] = payload.get('description')
        self.content_type: Optional[str] = payload.get('content_type')
        self.ephemeral: bool = payload.get('ephemeral', False)

        self.opened: bool = False
        self._closer = None

    def save(self, file_path: str, *, use_cached: bool = False) -> str:
        if use_cached:
            url = self.proxy_url
        else:
            url = self.url
        _log.info("Save file; url: {}".format(url))
        
        if not self.opened:
            file_obj = self.open(use_cached=use_cached)
        
        raw: Any = file_obj
            
        _log.info("Start save to '{}'".format(file_path))
        with open(file_path, 'wb') as f:
            raw.decode_content = True
            shutil.copyfileobj(raw, f) 
            
        _log.info("Seved to '{}'".format(file_path))
        
        self.close()
        return file_path
    
    def open(self, *, use_cached: bool = False) -> Any:
        if use_cached:
            url = self.proxy_url
        else:
            url = self.url
        _log.info("Open http file; url: {}".format(url))
        resp: requests.Response = requests.request(method='GET', url=url, stream=True)
        _log.info("Open http file; status_code: {}".format(resp.status_code))

        if resp.status_code == requests.codes.ok:
            self.opened = True
            self._closer = resp.close
            return resp.raw
        elif resp.status_code == 404:
            resp.close()
            raise NotFound(resp, 'asset not found')
        elif resp.status_code == 403:
            resp.close()
            raise Forbidden(resp, 'cannot retrieve asset')
        else:
            resp.close()
            raise HttpException(resp, 'failed to get asset')
    
    def close(self) -> bool:
        if self._closer is None:
            return False
        try:
            _log.info("Close http file; url: {}".format(self.url))
            self._closer()
            self._closer = None
            _log.debug("Closed.")
            self.opened = False
            return True
        except:
            _log.warning("Faild to close http file.")
            return False
    
    def to_dict(self, index: int) -> Dict[str, Any]:
        payload = {
            'id': index,
            'filename': self.filename,
        }

        if self.description is not None:
            payload['description'] = self.description

        return payload
    
    @classmethod
    def file_content_types(cls) -> tuple[str, ...]:
        return (
            "image/png", 
            "image/jpeg", 
            "image/webp", 
            "image/gif", 
            "image/lottie"
        )
