#!python3.9
from datetime import datetime

from .slash_command import SlashCommand

from application.interaction import parse_to_dict_value
from application.utils import isotimestamp
from application.enums import (
    InteractionResponseType,
    MessageFlags,
    CommandColor
)

from logging import getLogger
_log = getLogger(__name__)

class SlashUnixtimestamp(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        self.values: dict[str, str] = parse_to_dict_value(self._data["options"])
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        return
    
    def response(self) -> None:
        dt_str: str = self.values["datetime"] + self.values.get("timezone", '+0000')
        _log.debug('dt_str: {}'.format(dt_str))
        try:
            dt: datetime = datetime.strptime(dt_str, '%Y%m%d-%H%M%S%z')
        except ValueError:
            _log.warning(f'datetime format error; dt_str {dt_str}')
            payload = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : "不正なフォーマットの日付です。 Illegal datetime format.\n" \
                        + f"　入力値 (Inputed Value): `{self.values['datetime']}` \n" \
                        +  "　正しいフォーマット (Correct Format): `yyyymmdd-HHMMSS`"
                }
            }
            self.callback(payload)
            return
        unixtime: str = str(int(dt.timestamp()))
        _log.debug('unixtime: {}'.format(unixtime))
        discord_timestamp: str = '<t:{0}{1}>'.format(
            unixtime,
            self.values.get('style', '')
        )
        _log.debug('discord_timestamp: {}'.format(discord_timestamp))

        payload = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : discord_timestamp,
                "embeds" : [{
                    "color" : CommandColor.mint.value,
                    "fields" : [
                        {
                            "name" : "Input (with timezone)",
                            "value" : f'`{dt_str}`'
                        },
                        {
                            "name" : "Unix time",
                            "value" : f'`{unixtime}`'
                        },
                        {
                            "name" : "Unix Timestamp (Discord)",
                            "value" : f'`{discord_timestamp}`'
                        }
                    ],
                    "footer" : {
                        "text" : f"commanded by {str(self.commander)}",
                        "icon_url" : self.commander.avatar_url
                    },
                    "timestamp" : isotimestamp(datetime.now())
                }]
            }
        }
        self.callback(payload)
        return
    
    def clean(self) -> None:
        super().clean()
        return
