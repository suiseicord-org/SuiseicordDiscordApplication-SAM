#!python3.9
from typing import Optional
from requests import Response

from .slash_command import SlashCommand

from application.discord.channel import InteractionPartialChannel
from application.discord.member import Member
from application.discord.user import PartiaUser

from application.commands import (
    SlashCommand as SlashCommandName,
    SendCommand as SendCommandName,
    SendCommandOption as SendCommandOptionName
)
from application.components import Button, CustomID
from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle
)
from application.interaction import get_options, get_resolved_data
from application.mytypes.snowflake import Snowflake

from logging import getLogger
_log = getLogger(__name__)

class SlashSend(SlashCommand):
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        self.sub_command: dict = self._data['options'][0]
        self.resolved: dict = self._data['resolved']
        self.sub_command_name: str = self.sub_command['name']
        _targets = get_options(
            self.sub_command['options'],
            name = SendCommandOptionName.target
        )
        self.target_id: Snowflake = _targets[0]['value']
        _log.debug("target_id: {}".format(self.target_id))
        self._input_custom_id: str = CustomID.set_permission(
            CustomID.modal_send.format(
                sub_command = self.sub_command_name.lower(),
                target = self.target_id
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("input_custom_id: {}".format(self._input_custom_id))
        self._start_custom_id: str = CustomID.set_permission(
            CustomID.start_send.format(
                sub_command = self.sub_command_name.lower(),
                target = self.target_id,
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("start_custom_id: {}".format(self._start_custom_id))
    
    def run(self) -> None:
        super().run()
        return

    
    def response(self) -> None:
        self.payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "embeds" : [
                    self._create_embed()
                ],
                "components" : [
                    {
                        "type" : ComponentType.action_row.value,
                        "components" : [
                            {
                                "type" : ComponentType.button.value,
                                "style" : ButtonStyle.primary.value,
                                "label" : "Input (本文入力)",
                                "custom_id" : self._input_custom_id
                            },
                            {
                                "type" : ComponentType.button.value,
                                "style" : ButtonStyle.green.value,
                                "label" : "Start (送信)",
                                "custom_id" : self._start_custom_id
                            },
                            Button.cansell(
                                CustomID.PermissionType.command,
                                self.id
                            )
                        ]
                    }
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
        embed: dict = {"title" : "メッセージ送信コマンド"} # set title
        # set target information
        embed["fields"] = []
        if self.sub_command_name.lower() == SendCommandName.dm:
            user: PartiaUser = PartiaUser(self.resolved["users"].get(self.target_id))
            # member = None if (_member := self.resolved.get("members")) is None else _member.get(self.target_id)
            embed["fields"].append({
                "name" : "送信先",
                "value" : "{name} ( <@{id}> )".format(
                    name = str(user),
                    id = user.id
                )
            })
            embed["thumbnail"] = {
                "url" : user.avatar_url
            }
        elif self.sub_command_name.lower() == SendCommandName.channel:
            channel: InteractionPartialChannel
            channel = InteractionPartialChannel(self.resolved["channels"][self.target_id])
            embed["fields"].append({
                "name" : "送信先",
                "value" : "{name} ( <#{id}> )".format(
                    name = channel.name,
                    id = channel.id
                )
            })
            # check send permissions
            
            permission = channel.permissions
            embed["fields"].append({
                "name" : "送信権限",
                "value" : "OK" if permission & (1 << 11) else "**NG (修正が必要)**"
            })
        elif self.sub_command_name.lower() == SendCommandName.happi:
            channel: InteractionPartialChannel
            channel = InteractionPartialChannel(self.resolved["channels"][self.target_id])
            embed["fields"].append({
                "name" : "送信先",
                "value" : "{name} ( <#{id}> )".format(
                    name = channel.name,
                    id = channel.id
                )
            })
            # check send permissions
            permission = channel.permissions
            embed["fields"].append({
                "name" : "送信権限",
                "value" : "OK" if permission & 1 << 11 else "**NG (修正が必要)**"
            })
        # attachments
        attachments: Optional[dict] = self.resolved.get("attachments")
        if attachments is not None:
            urls: list[str] = []
            for attachment in attachments.values():
                urls.append(attachment["url"])
            embed["fields"].append({
                "name" : SendCommandOptionName.attachments,
                "value" : "\n".join(urls)
            })
            for attachment in attachments.values():
                if attachment["content_type"] in ("image/png", "image/jpeg", "image/webp", "image/gif", "image/lottie"):
                    embed["image"] = {
                        "url" : attachment["url"]
                    }
        
        return embed

