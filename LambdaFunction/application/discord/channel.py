#!python3.9
import os, shutil, glob, re
import csv, json
from typing import Any, Optional, Type, TypedDict, Union
import requests
from datetime import datetime
from urllib.parse import urlencode

from application.enums import (
    ChannelType
)
from application.mytypes.snowflake import Snowflake
from application.mytypes.channel import (
    Channel as ChannelPayload,
    PartialChannel as PartialChannelPayload,
    InteractionPartialChannel as InteractionPartialChannelPayload,
    PermissionOverwrite as PermissionOverwritePayload,
)
from application.mytypes.threads import (
    ThreadMetadata as ThreadMetadataPayload,
    ThreadMember as ThreadMemberPayload
)
from application.mytypes.user import (
    User as UserPayload
)
from application.mytypes.message import (
    Message as MessagePayload,
    Attachment as AttachmentPayload
)

from .http import Route

from logging import getLogger
_log = getLogger(__name__)

TMP_DIR = "/tmp"

class ChannelLogOptional(TypedDict):
    member_count: int
    message_count: int
    oldest: Snowflake
    latest: Snowflake

class ChannelLog(TypedDict):
    fp: Optional[str]
    data: Optional[ChannelLogOptional]

class PartialChannel:
    def __init__(self, payload: PartialChannelPayload):
        self.id: Snowflake = payload["id"]
        self.name: str = payload["name"]
        self.type: int = payload["type"]

class InteractionPartialChannel(PartialChannel):
    def __init__(self, payload: InteractionPartialChannelPayload):
        super().__init__(payload)
        self.permissions: int = int(payload["permissions"])
        self.parent_id: Snowflake = payload["parent_id"]

class Channel:
    def __init__(self, _id: Optional[Snowflake] = None, payload: Optional[ChannelPayload] = None):
        """Either id or payload is required"""
        if _id is None:
            if payload is None:
                _log.error("No parameters.")
                raise "No parameters."
            _id = payload[id]
        self.id: Snowflake = _id
        if payload:
            self.parse_parload(payload)
            
    
    def _get(self) -> requests.Response:
        route: Route = Route('GET', f"/channels/{self.id}")
        r: requests.Response = route.requets()

        if not r.ok:
            _log.error(r.text)
            return r

        _payload: ChannelPayload = r.json()
        self.parse_parload(_payload)
        return r
    
    def parse_parload(self, _payload: ChannelPayload) -> None:
        self.type: ChannelType = ChannelType(_payload["type"])
        # guild channel
        self._guild_id: Optional[Snowflake] = _payload.get("guild_id")
        self.position: Optional[int] = _payload.get("position")
        self.permission_overwrites: Optional[list[PermissionOverwritePayload]] \
            = _payload.get("permission_overwrites")
        self.name: Optional[str] = _payload.get("name")
        self.topic: Optional[str] = _payload.get("topic")
        self.nsfw: Optional[bool] = _payload.get("nsfw")
        self.parent_id: Optional[Snowflake] = _payload.get("parent_id")
        # voice channel
        self.bitrate: Optional[int] = _payload.get("bitrate")
        self.user_limit: Optional[int] = _payload.get("user_limit")
        self.rate_limit_per_user: Optional[int] = _payload.get("rate_limit_per_user")
        self.rtc_region: Optional[str] = _payload.get("rtc_region")
        self.video_quality_mode: Optional[int] = _payload.get("video_quality_mode")
        # DM Channel
        self.recipients: Optional[list[UserPayload]] = _payload.get("recipients")
        # Group DM Channel
        self.icon: Optional[str] = _payload.get("icon")
        self.application_id: Optional[Snowflake] = _payload.get("application_id")
        # Group DM or Thread
        self.owner_id: Optional[Snowflake] = _payload.get("owner_id")
        # thread
        self.message_count: Optional[int] = _payload.get("message_count")
        self.member_count: Optional[int] = _payload.get("member_count")
        self._thread_metadata: Optional[ThreadMemberPayload] = _payload.get("thread_metadata")
        self._thread_member: Optional[ThreadMemberPayload] = _payload.get("member")
        self.default_auto_archive_duration: Optional[int] = _payload.get("default_auto_archive_duration")
        
        self.permissions: Optional[str] = _payload.get("permissions")
        self.flags: Optional[int] = _payload.get("flags")
        self._last_pin_timestamp: str = _payload.get("last_pin_timestamp")
        return 
    
    def send(self, payload: Optional[dict] = None, **kwargs) -> requests.Response:
        if (not kwargs.get("json_payload", False)) and payload is not None:
            kwargs["json_payload"] = payload
        route: Route = Route('POST', f"/channels/{self.id}/messages", **kwargs)
        r = route.requets()
        return r
    
    def logs(
        self, 
        *, 
        limit: Optional[int] = 100, 
        around: Optional[Snowflake] = None,
        before: Optional[Snowflake] = None,
        after:  Optional[Snowflake] = None,
        oldest_first: Optional[bool] = True,
        filename: Optional[str] = None
    ) -> tuple[bool, str]:
        """GET channel messages.
        :return: message file path (csv files)"""
        # init
        if not hasattr(self, 'type'):
            r: requests.Response = self._get()
            if not r.ok:
                # fail
                return (False, r.text)

        
        _timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S%f")
        dir: str = TMP_DIR + f"/{_timestamp}"
        os.mkdir(dir)

        if limit < 1:
            limit = 100
        if filename is None:
            filename: str = f"{self.name}-{_timestamp}.csv"
        logfile = TMP_DIR + filename

        try:
            if around:
                # aroundがある時、100までに変更をする。
                if limit > 100:
                    limit = 100
            if limit > 100:
                if after:
                    # afterがあるときは上から回す
                    _count = 0
                    _after = after
                    while (_count < limit):
                        _limit = 100 if (l := limit - _count) > 100 else l
                        data: list[MessagePayload] = self._log_get(
                            limit  = _limit,
                            before = before,
                            after  = _after
                        )
                        data.sort(key=lambda x: x["id"])
                        self._write_log(dir, data)
                        # Loop Check
                        if len(data) < _limit:
                            # 取得したメッセージ数が指定値よりも小さかった
                            break
                        # _afterを更新
                        _after = data[-1]["id"]
                        if before is not None and _after > before:
                            # _after が before よりも新しくなった (!?)
                            break
                        # _countを更新
                        _count += len(data)
                else:
                    # afterがないので下から回す
                    _count = 0
                    _before = before
                    while (_count < limit):
                        _limit = 100 if (l := limit - _count) > 100 else l
                        data: list[MessagePayload] = self._log_get(
                            limit  = _limit,
                            before = _before,
                            after  = after # None
                        )
                        data.sort(key=lambda x: x["id"])
                        self._write_log(dir, data)
                        # Loop Check
                        if len(data) < _limit:
                            # 取得したメッセージ数が指定値よりも小さかった
                            break
                        # _beforeを更新
                        _before = data[0]["id"]
                        # _countを更新
                        _count += len(data)
            else:
                # 100以下の時には単独ファイルでOK
                data: list[MessagePayload] = self._log_get(
                    limit  = limit,
                    around = around,
                    before = before,
                    after  = after
                )
                data.sort(key=lambda x: x["id"])
                self._write_log(dir, data)
        except Exception as e:
            _log.error(e)
        finally:
            # tmpファイルを統合
            self._marge_files(dir, logfile)
            # remove tmp dir
            shutil.rmtree(dir)
        return logfile
    
    def _log_get(
        self,
        *, 
        limit: Optional[int] = 100, 
        around: Optional[Snowflake] = None,
        before: Optional[Snowflake] = None,
        after:  Optional[Snowflake] = None,
    ) -> list[MessagePayload]:
        if (limit is None) or (limit < 1) or (100 < limit):
            limit = 100
        query = {
            "limit" : limit,
        }
        if around is not None:
            query["around"] = around
        if before is not None:
            query["before"] = before
        if after is not None:
            query["after"] = after
        
        route: Route = Route('GET', f"/channels/{self.id}/messages", query=query)
        r = route.requets()
        
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return []
    
    def _write_log(self, dir: str, data: list[MessagePayload]) -> str:
        first_id = str(data[0]["id"])
        fp = dir + f'/{first_id}.csv'

        with open(fp, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow([
                    d["id"],
                    d["timestamp"],
                    d["edited_timestamp"],
                    d["channel_id"],
                    f'{d["author"]["username"]}#{d["author"]["discriminator"]}',
                    d["author"]["id"],
                    d["content"],
                    '\n'.join([att["url"] for att in d["attachments"]]),
                    json.dumps(d["embeds"], indent=4, ensure_ascii=False),
                ])
        return fp
    
    def _marge_files(self, dir: str, logfile: str) -> str:
        files = [p for p in dir.glob('*.csv') if re.search('\d+\.csv', str(p))]
        files.sort()
        with open(logfile, "w", encoding="utf-8") as mas:
            # write header
            mas.write(','.join([
                "id",
                "timestamp",
                "edited_timestamp",
                "channel_id",
                "author",
                "author_id",
                "content",
                "attachments",
                "embeds"
            ]))
            #marge
            for fp in files:
                with open(fp, "r", encoding="utf-8") as f:
                    mas.write(f.read() + '\n')
        return logfile
    
    def create_thread(
        self,
        name: str,
        *,
        auto_archive_duration: int = None
    ) -> ChannelPayload:
        pass

class DmChannel(Channel):
    def __init__(self, user_id: Snowflake):
        self.user_id: Snowflake = user_id
        self.id, res = self.get_channel_id(user_id)
        if self.id is None:
            raise NoDmChannelError(res)
    
    @classmethod
    def get_channel_id(cls, user_id: Snowflake) ->  tuple[Optional[Snowflake], Optional[requests.Response]]:
        payload = {
            "recipient_id" : str(user_id)
        }
        route: Route = Route('POST', f"/users/@me/channels", json_payload=payload)
        r = route.requets()
        if not r.ok:
            _log.warning(r.status_code)
            _log.warning(r.text)
            return None, r
        data: dict = r.json()
        return data.get("id"), None

class NoDmChannelError(Exception):
    """DMチェンネルがない時に投げる"""
    def __init__(self, res: requests.Response, *args: object):
        super().__init__(*args)
        self.res = res
    
    def __str__(self) -> str:
        if self.res.text is None:
            return str(self.res)
        return self.res.text