#!python3.9
import json
import requests
from datetime import datetime
from typing import Optional
from .start_command import CmpStartCommand

from application.utils import isotimestamp
from application.commands import (
    SlashBanCommandOption as SlashBanCommandOptionName
)
from application.mytypes.components import (
    Component as ComponentPayload
)
from application.mytypes.message import (
    Message as MessagePayload
)
from application.enums import (
    InteractionResponseType,
    ComponentType,
    MessageFlags,
    CommandColor
)
from application.discord.attachment import Attachment
from application.discord.channel import DmChannel, NoDmChannelError
from application.discord.member import BaseMember

from logging import getLogger
_log = getLogger(__name__)

class CmpStartBan(CmpStartCommand):

    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.commands: list[str] = self.custom_id.split('-')
        self.count: int = int(self.commands[2])
        self.target_id: str = self.commands[3]
        self.delete_message_days: int = int(self.commands[4])
        _dm_str: str = self.commands[5]
        self.dm: bool = True if str(True).lower() == _dm_str else False
        _log.info("BAN start count: {}".format(self.count))
        _log.debug("target_id: {}".format(self.target_id))
        _log.debug("delete_message_days: {}".format(self.delete_message_days))
        _log.debug("dm: {}".format(self.dm))
    
    def check(self) -> bool:
        return self.check_permission(defferd_func=self.deferred_update_message)

    def run(self) -> None:
        return super().run()
    
    def response(self) -> None:
        for field in self.message_data["embeds"][0]["fields"]:
            field: dict[str, str]
            if field["name"].startswith(SlashBanCommandOptionName.accept_title):
                start_members_text: str = field["value"]
                break
        else:
            start_members_text: str = ""
        if str(self.commander.id) in start_members_text:
            payload: dict = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : "既にこのボタンを押しています。"
                }
            }
        else:
            self.embeds = self.message_data["embeds"]
            for field in self.embeds[0]["fields"]:
                if field["name"].startswith(SlashBanCommandOptionName.accept_title):
                    field["value"] += "\n<@{0}> (ID: {0})".format(
                        self.commander.id
                    )
            self.count -= 1
            self.commands[2] = str(self.count)
            custom_id = '-'.join(self.commands)
            components = self.message_data["components"]
            components[0]["components"][0]["custom_id"] = custom_id
            if self.count > 0:
                pass
            else:
                self.deferred_update_message()
                self.do_command()
                self.disable_components(components)
            payload: dict = {
                "type" : InteractionResponseType.message_update.value,
                "data" : {
                    "embeds" : self.embeds,
                    "components" : components
                }
            }
        r= self.callback(payload)
        if self.response_error(r):
            pass
        else:
            pass
        return 
    
    def clean(self) -> None:
        return super().clean()
    
    def do_command(self) -> None:
        if self.dm:
            dm_result, dm_response = self.send_dm()
            if dm_result:
                _log.debug("send dm success: {}".format(dm_response.text))
                self.embeds[-1]["title"] = "送信成功"
                self.embeds[-1]["color"] = CommandColor.success.value
                payload: MessagePayload = dm_response.json()
                attachments: list[Attachment] = []
                image_url: Optional[str] = None
                for attachment_payload in payload['attachments']:
                    attachment: Attachment = Attachment(attachment_payload)
                    attachments.append(attachment)
                    if (image_url is None) and attachment.content_type in Attachment.file_content_types():
                        image_url = attachment.url
                if image_url is not None:
                    self.embeds[-1]['image']['url'] = image_url
                remove_index: list[int] = []
                for index, fild in enumerate(self.embeds[-1].get("fields", [])):
                    if fild['name'].startswith(SlashBanCommandOptionName.attachments):
                        remove_index.append(index)
                    elif fild['name'].startswith("url_" + SlashBanCommandOptionName.attachments):
                        remove_index.append(index)
                remove_index.sort(reverse=True)
                for i in remove_index:
                    self.embeds[-1]["fields"].pop(i)
                self.embeds[-1]["fields"].append({
                    "name" : "message_id",
                    "value" : payload["id"]
                })
                if len(attachments) > 0:
                    self.embeds[-1]["fields"].append({
                        "name" : 'sent_' + SlashBanCommandOptionName.attachments + '_url',
                        "value" : "\n".join(a.url for a in attachments)
                    })
            else:
                _log.warning("Send dm fail: {}".format(dm_response.text))
                self.embeds[-1]["title"] = "送信失敗"
                text = json.dumps(dm_response.json(), ensure_ascii=False, indent=4)
                text = text[:1000]
                if not self.embeds[-1].get("fields", False):
                    self.embeds[-1]["fields"] = []
                self.embeds[-1]["fields"].append({
                    "name" : "詳細",
                    "value" : f"```json\n{text}\n```"
                })
                self.embeds[-1]["color"] = CommandColor.fail.value
            self.embeds[-1]["footer"] = {
                "text" : f"started by {str(self.commander)}",
                "icon_url" : self.commander.avatar_url
            }
            self.embeds[-1]["timestamp"] = isotimestamp(datetime.now())
        
        ban_result, ban_response = self.ban()
        if ban_result:
            _log.info("BAN success: {}".format(ban_response.text))
            self.embeds[0]["title"] = "【成功】" + self.embeds[0]["title"]
            self.embeds[-1]["color"] = CommandColor.success.value
        else:
            _log.warning("BAN fail: {}".format(ban_response.text))
            self.embeds[0]["title"] = "【失敗】" + self.embeds[0]["title"]
            text = json.dumps(ban_response.json(), ensure_ascii=False, indent=4)
            text = text[:1000]
            if not self.embeds[0].get("fields", False):
                self.embeds[0]["fields"] = []
            self.embeds[0]["fields"].append({
                "name" : "詳細",
                "value" : f"```json\n{text}\n```"
            })
            self.embeds[0]["color"] = CommandColor.fail.value
        
        self.embeds[0]["timestamp"] = isotimestamp(datetime.now())
    
    def send_dm(self) -> tuple[bool, requests.Response]:
        try:
            self.target = DmChannel(self.target_id)
        except NoDmChannelError as e:
            res: requests.Response = e.res
            return False, res
        embed = self.message_data["embeds"][-1]
        fields = dict()
        for field in embed["fields"]:
            fields[field["name"]] = field["value"]
        self.attachments: Optional[list[Attachment]] = []
        for key, value in fields.items():
            key: str; value: str
            if key.startswith(SlashBanCommandOptionName.attachments):
                self.attachments.append(Attachment(
                    json.loads(value.strip('`json'))
                ))
        if len(self.attachments) < 1:
            self.attachments = None
        send_payload = {
            "content" : embed.get("description")
        }
        res: requests.Response = self.target.send(send_payload, attachments=self.attachments)
        if res.ok:
            return True, res
        else:
            return False, res

    def ban(self) -> tuple[bool, requests.Response]:
        target: BaseMember = BaseMember(self.target_id, self._guild_id)
        reason: str = "Application BAN; reason: {}".format(
            self.message_data["embeds"][0]["fields"][0]["value"]
        )
        res: requests.Response = target.ban(
            self.delete_message_days,
            reason = reason
        )
        if res.ok:
            return True, res
        else:
            return False, res


    def disable_components(self, payload: list[ComponentPayload]) -> None:
        for component in payload:
            if component.get('type') is None:
                continue
            _type = ComponentType(component["type"])
            if _type == ComponentType.action_row:
                self.disable_components(component["components"])
            elif _type == ComponentType.button or \
                 _type == ComponentType.select or \
                 _type == ComponentType.user_select or \
                 _type == ComponentType.role_select or \
                 _type == ComponentType.mentionable_select or \
                 _type == ComponentType.channel_select:
                component["disabled"] = True
