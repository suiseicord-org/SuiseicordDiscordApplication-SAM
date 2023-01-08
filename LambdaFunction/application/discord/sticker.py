#!python3.9
import os, shutil
import requests
from typing import Any, Dict, Optional

from application.enums import (
    StickerFormatType
)

from . import ImageBaseUrl
from .attachment import Attachment
from .user import User
from .exception import (
    HttpException,
    Forbidden,
    NotFound
)

from application.mytypes.snowflake import Snowflake
from application.mytypes.sticker import (
    StickerItem as StickerItemPayload,
    Sticker as StickerPayload,
    StickerFormatType as StickerFormatTypePayload,
    StickerType
)

from logging import getLogger
_log = getLogger(__name__)

class StickerItem:
    def __init__(self, payload: StickerItemPayload) -> None:
        _log.debug("payload: {}".format(payload))
        self.id: Snowflake = payload['id']
        self.name: str = payload['name']
        self.format_type: StickerFormatType = StickerFormatType(payload['format_type'])

        if self.format_type == StickerFormatType.png:
            self.content_type: str = 'image/png'
        elif self.format_type == StickerFormatType.apng:
            self.content_type: str = 'image/png'
        elif self.format_type == StickerFormatType.lottie:
            self.content_type: str = 'image/lottie'
        else:
            self.content_type = None

        self.opened: bool = False
        self._closer = None

    def save(self, file_path: str) -> str:
        url = self.url
        _log.info("Save file; url: {}".format(url))
        
        if not self.opened:
            file_obj = self.open()
        
        raw: Any = file_obj
            
        _log.info("Start save to '{}'".format(file_path))
        with open(file_path, 'wb') as f:
            raw.decode_content = True
            shutil.copyfileobj(raw, f) 
            
        _log.info("Seved to '{}'".format(file_path))
        
        self.close()
        return file_path
    
    def open(self) -> Any:
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

        return payload
    
    @property
    def url(self) -> str:
        return ImageBaseUrl + f'stickers/{self.id}.{self.format_type.file_extension}'

    @property
    def filename(self) -> str:
        return f'stickers_{self.id}.{self.format_type.file_extension}'

class Sticker(StickerItem):
    def __init__(self, payload: StickerPayload) -> None:
        _log.debug("payload: {}".format(payload))
        super().__init__(payload)
        self.description: Optional[str] = payload.get('description')
        self.tags: Optional[str] = payload.get('tags')
        self.type: Optional[StickerType] = payload.get('type')
        self.available: Optional[bool] = payload.get("available")
        self.guild_id: Optional[Snowflake] = payload.get("guild_id")
        self.user: Optional[User] = User(payload['user']) if payload.get('user') else None
        self.sort_value: Optional[int] = payload.get("sort_value")
