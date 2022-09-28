#!python3.9
import requests
from typing import (
    Any,
    Optional,
    overload,
    Union
)
from datetime import datetime

from .enums import (
    InteractionType,
    InteractionResponseType
)
from .utils import (
    snowflake_time
)

from .mytypes.snowflake import Snowflake
from .mytypes.interaction import (
    ApplicationCommandInteractionData,
    ApplicationCommandInteractionDataOption,
)
from .mytypes.user import (
    User as UserPayload,
    PartialUser as PartiaUserPayload
)

from .discord import ApiBaseUrl
from .discord.channel import Channel
from .discord.member import PartiaMember, Member
from .discord.user import PartiaUser, User

from logging import getLogger
_log = getLogger(__name__)

class Interaction:

    def __init__(self, rawdata: dict, bot_token: str):
        """Parse Data"""
        self.application_id: Snowflake  = rawdata['application_id']
        self.id: Snowflake              = rawdata['id']
        self.timestamp: datetime        = snowflake_time(self.id)
        self.type: int                  = rawdata['type']
        self.token: str                 = rawdata['token']

        if self.type != InteractionType.ping.value:
            self._data: ApplicationCommandInteractionData = rawdata['data']

            self._guild_id: Optional[Snowflake] = rawdata.get('guild_id')
            self._channel_id: Snowflake         = rawdata['channel_id']
            self.channel: Channel               = Channel(bot_token, self._channel_id)
            self.commander = PartiaMember(d) if (d := rawdata.get("member")) is not None else PartiaUser(rawdata["user"])
            self.locale: str                    = rawdata['locale']
            self.guild_locale: Optional[str]    = rawdata.get('guild_locale')

        self._bot_token: str                = bot_token
        

    @overload
    def run(self) -> None:
        """Requests Discord or other service.
        super().run() is first.
        If using run(), callback DEFERRED_ response.
        """
        ...
    
    @overload
    def response(self) -> None:
        """Main Response.
        super().response() is later.
        Also using callbask().
        """
        ...
    
    @overload
    def clean(self) -> None:
        """Clean Up Interaction funciton
        super().clean() is later.
        * Insert Database.
        * Delete temporary files
        * Report results.
        * Disabalbe Button
        """
        ...
    
    @property
    def interaction_url(self):
        return ApiBaseUrl + f"/interactions/{self.id}/{self.token}"
    
    @property
    def application_url(self):
        return ApiBaseUrl + f"/interactions/{self.application_id}/{self.token}"

    @property
    def webhook_url(self):
        return ApiBaseUrl + f"/webhooks/{self.application_id}/{self.token}"
    
    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bot {self._bot_token}"
        }

    def callback(self, payload: dict) -> requests.Response:
        url = self.interaction_url + "/callback"
        res: requests.Response = requests.post(url, json=payload)
        _log.debug("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def original_response(self, payload: dict) -> requests.Response:
        url = self.application_url + "/messages/@original"
        res: requests.Response = requests.patch(url, json=payload)
        _log.debug("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def followup(self, payload: dict) -> requests.Response:
        url = self.webhook_url
        res: requests.Response = requests.post(url, json=payload)
        _log.debug("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def deferred_channel_message(self) -> requests.Response:
        url = self.interaction_url + "/callback"
        payload: dict = {
            "type" : InteractionResponseType.deferred_channel_message
        }
        res: requests.Response = requests.post(url, json=payload)
        _log.debug("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def deferred_update_message(self) -> requests.Response:
        url = self.interaction_url + "/callback"
        payload: dict = {
            "type" : InteractionResponseType.deferred_message_update
        }
        res: requests.Response = requests.post(url, json=payload)
        _log.debug("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res


    def get_user(self) -> Optional[PartiaUser]:
        user_payload: Optional[PartiaUserPayload] = self._data

    
    def run(self) -> None:
        pass

    def response(self) -> None:
        """TEST RESPONSE"""
        payload: dict = {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : "This is test command or no define actions.\nPlease report bot operator or server admins."
            }
        }
        r: requests.Response = self.callback(payload)
    
    def clean(self) -> None:
        pass

    def run_error(self, res: requests.Response, **options) -> bool:
        if res.status_code == requests.codes.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    
    def response_error(self, res: requests.Response, **options) -> bool:
        if res.status_code == requests.codes.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    

    def clean_error(self, res: requests.Response, **options) -> bool:
        if res.status_code == requests.codes.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    
    def print_response(self, res: requests.Response):
        print("status code: ", res.status_code)
        print(res.text)

def get_options(
    options: list[ApplicationCommandInteractionDataOption],
    *,
    name:  Optional[str] = None,
    type:  Optional[int] = None,
    value: Optional[Union[str, int, bool, Snowflake, float]] = None
) -> list[ApplicationCommandInteractionDataOption]:
    match: list[ApplicationCommandInteractionDataOption] = list()
    for opt in options:
        if (type is not None) and (opt.get('type') != type):
            continue
        if (name is not None) and (opt.get('name') != name):
            continue
        if (value is not None) and (opt.get('value') != value):
            continue
        match.append(opt)
    return match


def get_resolved_data(resolved: dict, option: dict) -> Optional[dict]:
    """resolvedの中から、optionsで指定されたデータを返す関数。"""
    option_types: dict = {
        6 : 'users',
        7 : 'channels',
        8 : 'roles',
        11: 'attachments', 
    }

    data_name: str = option_types[option['type']]
    value: str = option['value']

    try:
        return resolved[data_name][value]
    except KeyError:
        return None


def parse_to_dict(options: list[ApplicationCommandInteractionDataOption]) -> dict[str, tuple[int, Any]]:
    result = {}
    for opt in options:
       result[opt["name"]] = (opt["type"], opt.get("value", opt.get("options")))
    return result 