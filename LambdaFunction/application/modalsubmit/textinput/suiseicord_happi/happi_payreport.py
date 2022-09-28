#!python3.9

from requests import Response, patch
from .suiseicord_happi import TextinputSuiseicordHappi

from application.commands import (
    Commands as CommandName,
    HappiCommand as HappiCommandName
)

from application.messages.message import MessageFile, filepath
from application.enums import (
    ButtonStyle,
    ComponentType,
    InteractionResponseType,
    SuiseiCordColor
)
from application.utils import isotimestamp
from application.happi_setting import HappiSetting
from application.discord.channel import Channel
from application.discord import ApiBaseUrl

from logging import getLogger
_log = getLogger(__name__)

class TextinputHappiPayreport(TextinputSuiseicordHappi):
    """
    企画参加者が入金報告画面から送信をしたときに実行される。
    
    やること
    # run 企画主催者に入金報告を通知 (専用スレッド)
    # res 管理者からの報告を待ってくださいというメッセージを送信 (follow up)
    # cln 入金報告ボタンを無効化 (callback)
    """
    def __init__(self, rawdata: dict, bot_token: str):
        super().__init__(rawdata, bot_token)
        _commands: list[str] = self.custom_id.split("-")
        #Textinput-happi-payreport-{bank|paypal}
        self.way: str = _commands[3].lower()
        values: dict[str, str] = self.parse_values()
        self.amount: str = values.get("amount", "-1")
        self.name: str = values.get("name", "-")
    
    def run(self) -> None:
        # print("happi_payreport: run()")
        #deferred
        self.deferred_channel_message()
        super().run()
        payload: dict = {
            "embeds" : [{
                "title" : "入金報告 (PayPal)" if self.way=="paypal" else "入金報告 (銀行口座振込)",
                "type" : "rich",
                # "timestamp" : isotimestamp(self.timestamp), #
                "color" : SuiseiCordColor.admin.value if self.way=="paypal" else SuiseiCordColor.hoshiyomi.value,
                "author" : {
                    "name" : str(self.commander),
                    "icon_url" : self.commander.avatar_url
                },
                "fields" : [
                    {
                        "name" : "Discord Account",
                        "value" : "<@{0}> (ID: {0})".format(self.commander.id),
                        "inline" : False
                    },
                    {
                        "name" : "入金金額",
                        "value" : self.amount,
                        "inline" : True
                    },
                    {
                        "name" : "名義など",
                        "value" : self.name,
                        "inline" : True
                    },
                    {
                        "name" : "channel id",
                        "value" : self._channel_id,
                        "inline" : False
                    }
                ]
            }],
            "components" : [{
                "type" : ComponentType.action_row.value,
                "components" : [
                    {
                        "type" : ComponentType.button.value,
                        "style" : ButtonStyle.green.value,
                        "label" : "入金確認",
                        "custom_id" : f"{CommandName.happi}-{HappiCommandName.check}-{self._channel_id}-{self.message_data['id']}-{self.amount}"
                    }
                ]
            }]
        }
        channel: Channel = Channel(self._bot_token, HappiSetting.Channel.payreport)
        r: Response = channel.send(payload)
        if self.run_error(r):
            pass
        else:
            pass

    
    def response(self) -> None:
        # print("happi_payreport: response()")
        # load response message
        fp = filepath(MessageFile.SuiseiCordHappi.payreport_response)
        # print(fp)
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
        datas: dict[str, str] = {
            "amount" : self.amount,
            "title" : "PayPal メールアドレス (Your PayPal Address)" if self.way=="paypal" else "振込名義",
            "name" : self.name
        }
        # print(content.format(**datas))
        payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : content.format(**datas)
            }
        }
        r: Response = self.callback(payload)
        if self.response_error(r):
            pass
        else:
            pass
        return
    
    def clean(self) -> None:
        """edit original message."""
        """ print("happi_payreport: clean()")
        components: dict = self.message_data["components"]
        for comp in components[0]["components"]:
            comp["disabled"] = True
        print(components)
        payload: dict = {
            "components" : components
        }
        url = ApiBaseUrl + f"/channels/{self._channel_id}/messages/{self.message_data['id']}"
        r: Response = patch(url, headers=self.headers, json=payload)
        if self.clean_error(r):
            pass
        else:
            pass """
        return super().clean()