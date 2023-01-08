#!python3.9
from requests import Response
from datetime import datetime

from .user_command import UserCommand

from application.utils import isotimestamp

from application.discord.member import Member
from application.discord.user import User

from application.enums import (
    InteractionResponseType,
    MessageFlags,
    CommandColor
)

from logging import getLogger
_log = getLogger(__name__)

class UserInfo(UserCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        if isinstance(self.target, Member):
            # get guild roles
            self.target.set_guild_roles()
        return
    
    def response(self) -> None:
        self.payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "flags" : MessageFlags.ephemeral.value,
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
        return
    
    def clean(self) -> None:
        super().clean()
        return
    
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
            if self.target.premium_since is not None:
                embed["fields"].append({
                    "name" : "サーバーブースト開始日時",
                    "value" : self.target.premium_since.strftime("%Y/%m/%d %H:%M:%S"),
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
            if self.target.pending is not None:
                embed["fields"].append({
                    "name" : "サーバールール同意ステータス",
                    "value" : "未同意" if self.target.pending else "同意済み",
                    "inline" : False
                })
            avatar_url_texts: list[str] = []
            avatar_url_texts.append(f'[ユーザーアバターURL]({self.target.user_avatar_url})')
            if self.target.guild_avatar_url is not None:
                avatar_url_texts.append(f'[ギルドアバターURL]({self.target.guild_avatar_url})')
            embed["fields"].append({
                "name" : "アイコンURLs",
                "value" : "\n".join(avatar_url_texts),
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
            embed["fields"].append({
                "name" : "アイコンURLs",
                "value" : f'[ユーザーアバターURL]({self.target.user_avatar_url})',
                "inline" : False
            })

        embed["footer"] = {
            "text" : f"commanded by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }
        embed["timestamp"] = isotimestamp(datetime.now())
        return embed
