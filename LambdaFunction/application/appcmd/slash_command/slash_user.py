#!python3.9
from requests import Response
from datetime import datetime

from typing import Optional, Union

from application.utils import isotimestamp

from .slash_command import SlashCommand

from application.discord.member import Member, get_member_or_user
from application.discord.user import User

from application.commands import (
    SlashUserCommand as SlashUserCommandName,
    SlashUserCommandOption as SlashUserCommandOptionName
)
from application.enums import (
    InteractionResponseType,
    CommandColor
)
from application.interaction import get_options
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
            name = SlashUserCommandOptionName.target
        )
        self.target_id: Snowflake = _targets[0]['value']

    def run(self) -> None:
        self.deferred_channel_message()
        super().run()
        self.target: Optional[Union[Member, User]] = None
        if self.sub_command_name == SlashUserCommandName.mention:
            resolved: Optional[dict] = self._data.get('resolved')
            member_payload = resolved["members"][self.target_id]
            member_payload["user"] = resolved["users"][self.target_id]
            self.target = Member(member_payload, self._guild_id)
        elif self.sub_command_name == SlashUserCommandName.id:
            self.target = get_member_or_user(
                self.target_id,
                self._guild_id
            )
        if isinstance(self.target, Member):
            # get guild roles
            self.target.set_guild_roles()
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
                "title" : "?????????????????????ID",
                "type"  : "rich",
                "color" : CommandColor.fail.value,
                "description" : "???????????????ID???????????????????????????????????????????????????"
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
            "name" : "?????????????????????ID",
            "value" : f"{str(self.target)}\n<@{self.target.id}>\nID: {self.target.id}",
            "inline" : False
        })
        embed["fields"].append({
            "name" : "????????????????????????",
            "value" : self.target.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            "inline" : False
        })

        if isinstance(self.target, Member):
            embed["title"] = "??????????????????????????????????????????"
            if self.target.nick is not None:
                embed["fields"].append({
                    "name" : "??????????????????",
                    "value" : self.target.nick,
                    "inline" : False
                })
            embed["fields"].append({
                "name" : "????????????????????????",
                "value" : self.target.joind_at.strftime("%Y/%m/%d %H:%M:%S"),
                "inline" : False
            })
            if self.target.premium_since is not None:
                embed["fields"].append({
                    "name" : "????????????????????????????????????",
                    "value" : self.target.premium_since.strftime("%Y/%m/%d %H:%M:%S"),
                    "inline" : False
                })
            embed["fields"].append({
                "name" : "?????????????????????",
                "value" : "\n".join(
                    ["`{0:0>2}`| {1} ({2})".format(r.position, r.name, r.mention) \
                        for r in self.target.roles]
                ),
                "inline" : False
            })
            if self.target.pending is not None:
                embed["fields"].append({
                    "name" : "??????????????????????????????????????????",
                    "value" : "?????????" if self.target.pending else "????????????",
                    "inline" : False
                })
            avatar_url_texts: list[str] = []
            avatar_url_texts.append(f'[????????????????????????URL]({self.target.user_avatar_url})')
            if self.target.guild_avatar_url is not None:
                avatar_url_texts.append(f'[?????????????????????URL]({self.target.guild_avatar_url})')
            embed["fields"].append({
                "name" : "????????????URLs",
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
            embed["title"] = "??????????????????????????????"
            embed["color"] = CommandColor.mint.value
            embed["fields"].append({
                "name" : "????????????URLs",
                "value" : f'[????????????????????????URL]({self.target.user_avatar_url})',
                "inline" : False
            })

        embed["footer"] = {
            "text" : f"commanded by {str(self.commander)}",
            "icon_url" : self.commander.avatar_url
        }
        embed["timestamp"] = isotimestamp(datetime.now())
        return embed
