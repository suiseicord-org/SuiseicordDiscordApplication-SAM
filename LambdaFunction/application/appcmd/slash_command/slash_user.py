#!python3.9
from typing import Optional, Union
from requests import Response
from datetime import datetime

from application.utils import isotimestamp

from .slash_command import SlashCommand

from application.discord import ApiBaseUrl
from application.discord.channel import InteractionPartialChannel
from application.discord.member import Member, get_member_or_user
from application.discord.user import User

from application.commands import (
    SlashCommand as SlashCommandName,
    UserCommand as UserCommandName,
    UserCommandOption as UserCommandOptionName
)
from application.components import Button, CustomID
from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle,
    CommandColor
)
from application.interaction import get_options, get_resolved_data
from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class SlashUser(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.sub_command: dict = self._data['options'][0]
        self.sub_command_name: str = self.sub_command['name']
        _targets = get_options(
            self.sub_command['options'],
            name = UserCommandOptionName.target
        )
        self.target_id: Snowflake = _targets[0]['value']

    def run(self) -> None:
        self.deferred_channel_message()
        super().run()
        self.target: Optional[Union[Member, User]] = None
        if self.sub_command_name == UserCommandName.mention:
            resolved: Optional[dict] = self._data.get('resolved')
            member_payload = resolved["members"][self.target_id]
            member_payload["user"] = resolved["users"][self.target_id]
            self.target = Member(member_payload, self._guild_id)
        elif self.sub_command_name == UserCommandName.id:
            self.target = get_member_or_user(
                self.target_id,
                self._guild_id,
                self.headers
            )
        if isinstance(self.target, Member):
            # get guild roles
            self.target.set_guild_roles(self.headers)
        return

    
    def response(self) -> None:
        self.payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "embeds" : [
                    self._create_embed()
                ]
            }
        }
        r: Response = self.callback(self.payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    def _create_embed(self) -> dict:
        if self.target is None:
            embed = {
                "title" : "不明なユーザーID",
                "type"  : "rich",
                "color" : CommandColor.fail.value,
                "description" : "指定されたIDに該当するユーザーが存在しません。"
            }
            embed["footer"] = {
                "text" : f"commanded by {str(self.commander)}",
                "icon_url" : self.commander.avatar_url
            }
            embed["timestamp"] = isotimestamp(datetime.now())
            return embed

        
        embed = {"type" : "rich"}
        embed["thumbnail"] = {
            "url" : self.target.avatar_url
        }
        embed["fields"] = []
        embed["fields"].append({
            "name" : "アカウント名・ID",
            "value" : f"{str(self.target)}\n<@{self.target.id}>\nID: {self.target.id}",
            "inline" : False
        })
        embed["fields"].append({
            "name" : "アカウント作成日",
            "value" : self.target.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            "inline" : False
        })

        if isinstance(self.target, Member):
            embed["title"] = "サーバーメンバー情報取得結果"
            if self.target.nick is not None:
                embed["fields"].append({
                    "name" : "ニックネーム",
                    "value" : self.target.nick,
                    "inline" : False
                })
            embed["fields"].append({
                "name" : "サーバー参加日時",
                "value" : self.target.joind_at.strftime("%Y/%m/%d %H:%M:%S"),
                "inline" : False
            })
            embed["fields"].append({
                "name" : "所属ロール一覧",
                "value" : "\n".join(
                    ["`{0:0>2}`| {1} ({2})".format(r.position, r.name, r.mention) \
                        for r in self.target.roles]
                ),
                "inline" : False
            })
            if self.target.premium_since is not None:
                embed["fields"].append({
                    "name" : "サーバーブースト開始日時",
                    "value" : self.target.premium_since.strftime("%Y/%m/%d %H:%M:%S"),
                    "inline" : False
                })
            if self.target.pending is not None:
                embed["fields"].append({
                    "name" : "サーバールール同意ステータス",
                    "value" : "未同意" if self.target.pending else "同意済み",
                    "inline" : False
                })
            for role in self.target.roles:
                if role.color > 0:
                    embed["color"] = role.color
                    break
            else:
                embed["color"] = CommandColor.cyan.value
        elif isinstance(self.target, User):
            embed["title"] = "ユーザー情報取得結果"
            embed["color"] = CommandColor.mint.value

        embed["footer"] = {
            "text" : f"commanded by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }
        embed["timestamp"] = isotimestamp(datetime.now())
        return embed

