#!python3.9
import json
from typing import Optional, Union
from requests import Response
from datetime import datetime

from application.utils import isotimestamp

from .slash_command import SlashCommand

from application.discord.attachment import Attachment
from application.discord.member import Member, get_member_or_user
from application.discord.user import User

from application.dynamodb import SettingDynamoDB

from application.commands import (
    SlashBanCommand as SlashBanCommandName,
    SlashBanCommandOption as SlashBanCommandOptionName
)
from application.components import CustomID
from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle,
    CommandColor
)
from application.interaction import parse_to_dict_value

from logging import getLogger
_log = getLogger(__name__)

class SlashBan(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.command: str = self._data['name'].split(' ')[0]
        self.resolved: Optional[dict] = self._data.get('resolved')
        self.sub_command: dict = self._data['options'][0]
        self.sub_command_name: str = self.sub_command['name']
        self.options: dict = parse_to_dict_value(self.sub_command['options'])
        self.target_id = self.options[SlashBanCommandOptionName.target]
        self.ban_permission_check: bool = True

    def run(self) -> None:
        # self.deferred_channel_message()
        super().run()
        self.target: Optional[Union[Member, User]] = None
        if self.sub_command_name == SlashBanCommandName.mention:
            member_payload = self.resolved["members"][self.target_id]
            member_payload["user"] = self.resolved["users"][self.target_id]
            self.target = Member(member_payload, self._guild_id)
        elif self.sub_command_name == SlashBanCommandName.id:
            self.target = get_member_or_user(
                self.target_id,
                self._guild_id
            )

        if self.target is None:
            _log.warning("The target's user is not found!")
            return

        if isinstance(self.target, Member):
            # get guild roles
            self.target.set_guild_roles()
        
        self.ban_permission_check = self.check_ban_permission()
        if not self.ban_permission_check:
            _log.warning("BOT can not ban the target user!")
            return
        
        self.reason: str = self.options[SlashBanCommandOptionName.reason]
        _log.debug("reason: {}".format(self.reason))
        self.custom_reason: Optional[str] = self.options.get(SlashBanCommandOptionName.custom_reason)
        _log.debug("custom_reason: {}".format(self.custom_reason))

        # get setting.
        self.db = SettingDynamoDB()
        _log.debug("dynamoDB get_item()")
        data: dict = self.db.get_item(
            command=self.command,
            target_id=self._guild_id
        )

        self.delete_message_days: int = self.options.get(
            SlashBanCommandOptionName.delete_message_days,
            int(
                data.get(
                    SlashBanCommandOptionName.delete_message_days,
                    1 # default
                )
            )
        )
        _log.debug("delete_message_days: {}".format(self.delete_message_days))
        self.accept_count: int = int(
            data.get(
                SlashBanCommandOptionName.accept_count,
                1 # default
            )
        )
        _log.debug("accept_count: {}".format(self.accept_count))
        self.cancel_count: int = int(
            data.get(
                SlashBanCommandOptionName.cancel_count,
                1 # default
            )
        )
        _log.debug("cancel_count: {}".format(self.cancel_count))
        _mentions = data.get(
            SlashBanCommandOptionName.mentions,
            set() # default
        )
        self.mentions: set[int] = {int(i) for i in _mentions}
        _log.debug("mentions: {}".format(self.mentions))

        self.dm: bool = self.options.get(
            SlashBanCommandOptionName.dm,
            data.get(
                SlashBanCommandOptionName.dm,
                False # default
            )
        )
        _log.debug("dm: {}".format(self.dm))
        if self.dm and isinstance(self.target, Member):
            self.dm_text: Optional[str] = data.get(
                SlashBanCommandOptionName.dm_text
            )
            _log.debug("dm_text: {}".format(self.dm_text))


        # custom id
        self._start_custom_id: str = CustomID.set_permission(
            CustomID.start_ban.format(
                count = self.accept_count,
                target = self.target_id,
                del_day = str(self.delete_message_days),
                dm = str(True).lower() if self.dm and isinstance(self.target, Member) else str(False).lower()
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("_start_custom_id: {}".format(self._start_custom_id))
        self._cancel_custom_id: str = CustomID.set_permission(
            CustomID.cancel_ban.format(
                count = self.cancel_count
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("_cancel_custom_id: {}".format(self._cancel_custom_id))
        self._input_custom_id: str = CustomID.set_permission(
            CustomID.modal_ban,
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("_input_custom_id: {}".format(self._input_custom_id))

        return

    
    def response(self) -> None:
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
            self.payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "embeds" : [
                        embed
                    ]
                }
            }
        elif not self.ban_permission_check:
            text = "BOT????????????????????????????????????BAN?????????????????????????????????\n"
            text += "??????????????????????????????????????????BOT???????????????????????????????????????????????????"
            embed = {
                "title" : "???????????????",
                "type"  : "rich",
                "color" : CommandColor.fail.value,
                "description" : text
            }
            embed["footer"] = {
                "text" : f"commanded by {str(self.commander)}",
                "icon_url" : self.commander.avatar_url
            }
            embed["timestamp"] = isotimestamp(datetime.now())
            self.payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "embeds" : [
                        embed
                    ]
                }
            }
        else:
            embeds: list = []
            embeds.append(self._baninfo_embed())
            embeds.append(self._userinfo_embed())
            if self.dm and isinstance(self.target, Member):
                embeds.append(self._dminfo_embed())
            self.payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "content" : "???BAN???????????????????????????????????????{}".format(
                        " ".join(
                            [f'<@&{i}>' for i in self.mentions]
                        )
                    ),
                    "embeds" : embeds,
                    "components" : [
                        {
                            "type" : ComponentType.action_row.value,
                            "components" : self._create_components_button()
                        }
                    ],
                    "allowed_mentions" : {
                        "parse" : ["roles", "users"],
                        #"roles" : [str(i) for i in self.mentions]
                    }
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
    
    def _create_components_button(self) -> list[dict]:
        components: list = []
        components.append(
            {
                "type" : ComponentType.button.value,
                "style" : ButtonStyle.green.value,
                "label" : "Start (BAN??????)",
                "custom_id" : self._start_custom_id
            }
        )
        components.append(
            {
                "type" : ComponentType.button.value,
                "style" : ButtonStyle.red.value,
                "label" : "Cancel (??????)",
                "custom_id" : self._cancel_custom_id
            }
        )
        if self.dm and isinstance(self.target, Member):
            components.append(
                {
                    "type" : ComponentType.button.value,
                    "style" : ButtonStyle.primary.value,
                    "label" : "DM Input (DM????????????)",
                    "custom_id" : self._input_custom_id
                }
            )
        return components

    def _baninfo_embed(self) -> dict:
        embed = {"type" : "rich"}
        # embed["author"] = {
        #     "name" : str(self.commander),
        #     "icon_url" : self.commander.avatar_url
        # }
        embed["title"] = "BAN??????????????????"
        embed["color"] = CommandColor.red.value
        embed["fields"] = []
        reason_text: str = self.reason
        if self.custom_reason is not None:
            reason_text += "\n\t{}".format(self.custom_reason)
        embed["fields"].append({
            "name" : "BAN?????????",
            "value" : reason_text,
            "inline" : False
        })
        embed["fields"].append({
            "name" : "???????????????????????????",
            "value" : "{} ???".format(self.delete_message_days),
            "inline" : False
        })
        embed["fields"].append({
            "name" : "{0}: {1} ???".format(
                SlashBanCommandOptionName.accept_title,
                self.accept_count
            ),
            "value" : "????????????????????????:",
            "inline" : True
        })
        embed["fields"].append({
            "name" : "{0}: {1} ???".format(
                SlashBanCommandOptionName.cancel_title,
                self.cancel_count
            ),
            "value" : "????????????????????????:",
            "inline" : True
        })
        return embed

    def _userinfo_embed(self) -> dict:    
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
            embed["title"] = "BAN????????????????????????"
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
            embed["title"] = "BAN????????????????????????"
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

    def _dminfo_embed(self) -> dict:
        embed: dict = {"title" : "DM????????????"} # set title
        embed["fields"] = []
        embed["fields"].append({
            "name" : "?????????",
            "value" : "{name} ( <@{id}> )".format(
                name = str(self.target),
                id = self.target.id
            )
        })
        if self.dm_text is not None:
            embed["description"] = self.dm_text
        embed["color"] = CommandColor.mint.value

        # attachments
        if self.resolved is None:
            return embed
        attachments: Optional[dict] = self.resolved.get("attachments")
        if attachments is not None:
            index: int = 0
            urls: list[str] = []
            for attachment in attachments.values():
                embed["fields"].append({
                    "name" : SlashBanCommandOptionName.attachments + f'[{index}]',
                    "value" : "```json\n{}\n```".format(json.dumps(attachment, ensure_ascii=False, indent=4))
                })
                urls.append(attachment["url"])
                if (not embed.get("image", False)) and attachment["content_type"] in Attachment.file_content_types():
                    embed["image"] = {
                        "url" : attachment["url"]
                    }
                index += 1
            embed["fields"].append({
                "name" : "url_" + SlashBanCommandOptionName.attachments,
                "value" : "\n".join(urls)
            })
        
        return embed
    
    def check_ban_permission(self) -> bool:
        if not isinstance(self.target, Member):
            # not setber member.
            return True

        if self.target.is_owner:
            return  False
        
        bot: Member = get_member_or_user(self.application_id, self._guild_id)
        bot.set_guild_roles()

        if bot.roles[0].position > self.target.roles[0].position:
            return True
        return False
