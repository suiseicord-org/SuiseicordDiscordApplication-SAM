#!python3.9
from datetime import datetime

from .slash_command import SlashCommand

from application.interaction import parse_to_dict_value
from application.utils import snowflake_time, isotimestamp
from application.enums import (
    InteractionResponseType,
    MessageFlags,
    CommandColor
)

from logging import getLogger
_log = getLogger(__name__)

class SlashSnowflaketime(SlashCommand):
    def __init__(self, rawdata: dict):
        super().__init__(rawdata)
        values: dict[str, str] = parse_to_dict_value(self._data["options"])
        self.target_id: str = values["snowflake"]
        _log.info("target snowflake id: {}".format(self.target_id))
    
    def check(self) -> bool:
        return super().check()

    def run(self) -> None:
        super().run()
        return

    def response(self) -> None:
        try:
            dt: datetime = snowflake_time(self.target_id)
        except ValueError:
            _log.warning(f'snowflake format; target snowflake id: {self.target_id}')
            payload = {
                "type" : InteractionResponseType.channel_message.value,
                "data" : {
                    "flags" : MessageFlags.ephemeral.value,
                    "content" : "不正なフォーマットのIDです。 Illegal datetime format.\n" \
                        + f"　入力値 (Inputed Value): `{self.target_id}` \n"
                }
            }
            self.callback(payload)
            return

        dt_str: str = dt.strftime('%Y/%m/%dT%H:%M:%S%z')
        _log.info(f"datetime str: {dt_str}")
        payload = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : f'`{dt_str}`',
                "embeds" : [{
                    "color" : CommandColor.mint.value,
                    "fields" : [
                        {
                            "name" : "Input",
                            "value" : f'`{self.target_id}`'
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
