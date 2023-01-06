#!python3.9
import os
import json
import requests
from datetime import datetime
from typing import Optional, Union

from application.utils import parse_time, isotimestamp

from application.mytypes.snowflake import Snowflake
from application.mytypes.message import (
    MessageActivity as MessageActivityPayload,
    MessageApplication as MessageApplicationPayload,
    MessageInteraction as MessageInteractionPayload,
    MessageReference as MessageReferencePayload,
    Message as MessagePayload,
)
from application.mytypes.components import (
    Component as ComponentPayload
)
from application.mytypes.embed import (
    Embed as EmbedPayload
)

from . import DiscordUrl
from .attachment import Attachment
from .channel import Channel
from .member import Member, get_member_or_user
from .reaction import Reaction
from .sticker import StickerItem, Sticker
from .user import User
from .http import Route

from logging import getLogger
_log = getLogger(__name__)

class MessageReference:
    def __init__(self, payload: MessageReferencePayload) -> None:
        _log.debug("payload: {}".format(json.dumps(payload, ensure_ascii=False)))
        self.message_id: Optional[Snowflake] = payload.get("message_id")
        self.channel_id: Optional[Snowflake] = payload.get("channel_id")
        self.guild_id: Optional[Snowflake]   = payload.get("guild_id")
        self.fail_if_not_exists: Optional[bool] = payload.get("fail_if_not_exists")
    
    @property
    def url(self) -> Optional[str]:
        if (self.message_id is None) or (self.channel_id is None):
            return None
        if self.guild_id is None:
            return DiscordUrl + f'/@me/{self.channel_id}/{self.message_id}'
        return DiscordUrl + f'/channels/{self.guild_id}/{self.channel_id}/{self.message_id}'

class PartiaMessage:
    def __init__(self, ch_id: Snowflake, msg_id: Snowflake):
        self.id: Snowflake = msg_id
        self.channel: Channel = Channel(ch_id)
    
    def edit(self, payload: Optional[dict] = None, **kwargs) -> requests.Response:
        if kwargs.get("json_payload") and payload is not None:
            kwargs["json_payload"] = payload
        route = Route('PATCH', f"/channels/{self.channel.id}/messages/{self.id}", **kwargs)
        r = route.requets()
        return r

class Message(PartiaMessage):
    def __init__(self, payload: MessagePayload, guild_id: int = None):
        _log.debug("payload: {}".format(json.dumps(payload, ensure_ascii=False)))
        super().__init__(
            payload["channel_id"], 
            payload["id"]
        )

        self.author: Union[User, Member] = User(payload["author"])
        self.content: Optional[str] = payload["content"]
        self.timestamp: datetime = parse_time(payload["timestamp"])
        self.edited_timestamp: Optional[datetime] = parse_time(payload.get("edited_timestamp"))
        self.tts: bool = payload['tts']
        self.mention_everyone: bool = payload["mention_everyone"]
        self.mentions: list[User] = [User(d) for d in payload["mentions"]]
        self._mention_roles: list[Snowflake] = payload["mention_roles"]
        self.mention_channels: list[Channel] = [Channel(payload=d) for d in payload.get("mention_channels", [])]
        self.attachments: list[Attachment] = [Attachment(d) for d in payload["attachments"]]
        self._embeds_payload: list[EmbedPayload] = payload["embeds"]
        self.reactions: list[Reaction] = [Reaction(d) for d in payload.get("reactions", [])]
        self.nonce: Optional[Union[int, str]] = payload.get("nonce")
        self.pinned: bool = payload["pinned"]
        self.webhook_id: Optional[Snowflake] = payload.get("webhook_id")
        self.type: int = payload["type"]
        self._activity: Optional[MessageActivityPayload] = payload.get("activity")
        self._application: Optional[MessageApplicationPayload] = payload.get("application")
        self.application_id: Optional[Snowflake] = payload.get("application_id")
        self.reference: Optional[MessageReference] = MessageReference(payload.get("message_reference", {}))
        self._interaction: Optional[MessageInteractionPayload] = payload.get("interaction")
        self.thread: Optional[Channel] = Channel(payload=payload["thread"]) if payload.get("thread") else None
        self._components_payload: list[ComponentPayload] = payload.get("components", [])
        self.sticker_items: list[Sticker] = [Sticker(d) for d in payload.get("sticker_items", [])]
        self.position: Optional[int] = payload.get("position")

        self.guild_id: Optional[int] = guild_id

    @property
    def url(self):
        if self.guild_id is None:
            guild = '@me'
        else:
            guild = self.guild_id
        return DiscordUrl + f'/channels/{guild}/{self.channel.id}/{self.id}'

    
    def to_embeds(
        self, 
        *, 
        detail: bool = False,
        transfer_files: bool = False
    ) -> tuple[list[EmbedPayload], Optional[list[Union[Attachment, Sticker]]]]:
        embed: EmbedPayload = {}
        embeds: list[EmbedPayload] = []
        embeds.append(embed)

        files: list[Union[Attachment, Sticker]] = []

        embed["title"] = "メッセージリンク (Message Link)"
        embed["url"] = self.url
        timestamp = isotimestamp(datetime.now())
        embed["timestamp"] = timestamp

        if not isinstance(self.author, Member):
            if self.guild_id is not None:
                self.author = get_member_or_user(
                    self.author.id,
                    self.guild_id
                )
        embed["author"] = {
            "name" : str(self.author),
            "icon_url" : self.author.avatar_url
        }

        color = self.author.color
        embed["color"] = color

        if self.content:
            embed["description"] = self.content
        
        embed["fields"] = []

        embed["fields"].append({
            "name" : "送信日時",
            "value" : self.timestamp.strftime('%Y/%m/%d %H:%M:%S'),
            "inline" : True
        })
        if self.edited_timestamp is not None:
            embed["fields"].append({
                "name" : "最終編集日時",
                "value" : self.edited_timestamp.strftime('%Y/%m/%d %H:%M:%S'),
                "inline" : True
            })
        
        if self.reference is not None:
            url: Optional[str] = self.reference.url
            value: str = ''
            if url is not None:
                value += f'[メッセージリンク]({url})'
                if self.reference.fail_if_not_exists:
                    value += ' (削除済み)'
                embed["fields"].append({
                    "name" : "メッセージ返信先",
                    "value" : value,
                    "inline" : False
                })
        
        if len(self.reactions) > 0:
            embed["fields"].append({
                "name" : "リアクション",
                "value" : '\n'.join(["count: `{0:>3}` | {1}".format(r.count, str(r.emoji)) \
                    for r in self.reactions]),
                "inline" : False
            })

        if self.guild_id is not None:
            embed["fields"].append({
                "name" : "チャンネル",
                "value" : self.channel.mention,
                "inline" : True
            })
        
        embed["fields"].append({
            "name" : "送信者",
            "value" : self.author.mention,
            "inline" : True
        })

        if len(self.attachments) > 0:
            urls: list[str] = []
            for attachment in self.attachments:
                urls.append(f'[{attachment.filename}]({attachment.url})')
                if not (len(embeds) < 10):
                    continue
                if attachment.content_type is None:
                    continue
                if 'image' in attachment.content_type.lower():
                    if transfer_files:
                        attachment.filename = f'{self.id}_' + attachment.filename
                        files.append(attachment)
                        url = 'attachment://' + attachment.filename
                    else:
                        url = attachment.ur
                    e = {
                        'title' : '添付ファイル (画像)',
                        'url' : attachment.url,
                        'image' : {
                            'url' : url
                        },
                        'color' : color
                    }
                    embeds.append(e)
                    _log.debug("embeds: {}".format(json.dumps(embeds, ensure_ascii=False)))
                elif 'video' in attachment.content_type.lower():
                    if transfer_files:
                        attachment.filename = f'{self.id}_' + attachment.filename
                        files.append(attachment)
                        url = 'attachment://' + attachment.filename
                    else:
                        url = attachment.url
                    e = {
                        'title' : '添付ファイル (動画)',
                        'url' : attachment.url,
                        'video' : {
                            'url' : url
                        },
                        'color' : color
                    }
                    embeds.append(e)
                    _log.debug("embeds: {}".format(json.dumps(embeds, ensure_ascii=False)))
            embed["fields"].append({
                "name" : "添付ファイル (オリジナル)",
                "value" : '\n'.join(urls),
                "inlune" : False
            })

        if len(self.sticker_items) > 0:
            urls: list[str] = []
            for sticker in self.sticker_items:
                urls.append(f'[{sticker.name}]({sticker.url})')
                if not (len(embeds) < 10):
                    continue
                if transfer_files:
                    files.append(sticker)
                    url = 'attachment://' + sticker.filename
                else:
                    url = sticker.url
                e = {
                    'title' : 'ステッカー',
                    'url' : sticker.url,
                    'image' : {
                        'url' : url
                    },
                    'color' : color
                }
                embeds.append(e)
                _log.debug("embeds: {}".format(json.dumps(embeds, ensure_ascii=False)))
            embed["fields"].append({
                "name" : "ステッカー",
                "value" : '\n'.join(urls),
                "inlune" : False
            })
        
        if detail:
            value: str = ''

            value += 'ピン留め状態: ピン留め{}\n'.format(
                "されている" if self.pinned else "されていない"
            )

            value += '有効なメンション:\n'
            value += '　全体メンション: {}\n'.format(
                "有効" if self.mention_everyone else "無効"
            )
            value += '　ユーザーメンション: \n'
            if len(self.mentions) > 0:
                value += '\n'.join([
                    f'　　{str(u)}' for u in self.mentions
                ])
                value += '\n'
            value += '　ロールメンション: \n'
            if len(self._mention_roles) > 0:
                value += '\n'.join([
                    f'　　<@&{r}>' for r in self._mention_roles
                ])
                value += '\n'

            embed["fields"].append({
                "name" : "追加情報",
                "value" : value,
                "inline" : False
            })

        if len(files) > 0:
            return embeds[:10], files

        return embeds[:10], None
