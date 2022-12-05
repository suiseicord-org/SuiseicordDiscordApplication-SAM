#!python3.9
from requests import Response
from .slash_channel import SlashChannel
from application.commands import (
    ChannelCommandOption as ChannelCommandOptionName
)
from application.components import Button, CustomID
from application.discord.channel import Channel
from application.enums import (
    InteractionResponseType,
    ComponentType,
    ButtonStyle,
    CommandColor,
    SuiseiCordColor
)
from application.interaction import get_options
from application.mytypes.snowflake import Snowflake
from application.mytypes.channel import Channel as ChannelPayload

from logging import getLogger
_log = getLogger(__name__)

class SlashChannelTopic(SlashChannel):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.sub_command: dict = self._data['options'][0]
        self.resolved: dict = self._data['resolved']
        _targets = get_options(
            self.sub_command['options'],
            name = ChannelCommandOptionName.channel
        )
        self.target_id: Snowflake = _targets[0]['value']
        self.channel_resolved: ChannelPayload = self.resolved["channels"][self.target_id]
        _log.debug("target_id: {}".format(self.target_id))
        self._input_custom_id: str = CustomID.set_permission(
            CustomID.modal_channel_topic.format(
                target = self.target_id
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("input_custom_id: {}".format(self._input_custom_id))
        self._start_custom_id: str = CustomID.set_permission(
            CustomID.start_channel_topic.format(
                target = self.target_id,
            ),
            CustomID.PermissionType.command,
            self.id
        )
        _log.debug("start_custom_id: {}".format(self._start_custom_id))
    
    def run(self) -> None:
        self.deferred_channel_message()
        super().run()
        self.target: Channel = Channel(_id = self.target_id)
        self.target._get()
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
                                "label" : "Input (内容入力)",
                                "custom_id" : self._input_custom_id
                            },
                            {
                                "type" : ComponentType.button.value,
                                "style" : ButtonStyle.green.value,
                                "label" : "Start (編集実行)",
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
        super().clean()
        return
    
    def _create_embed(self) -> dict:
        embed: dict = {
            "title" : "チャンネルトピック編集コマンド"
        }
        embed["color"] = SuiseiCordColor.admin.value
        if self.target.topic:
            embed["description"] = self.target.topic
        # set target information
        embed["fields"] = []
        embed["fields"].append({
            "name" : "ターゲットチャンネル",
            "value" : "{0}\n<#{1}>".format(
                self.channel_resolved["name"],
                self.target_id
            )
        })
        return embed

