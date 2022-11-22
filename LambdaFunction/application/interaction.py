#!python3.9
import requests
from typing import (
    Any,
    Callable,
    Optional,
    overload,
    Union
)
from datetime import datetime

from application.enums import (
    InteractionType,
    InteractionResponseType
)
from application.utils import (
    snowflake_time
)

from application.mytypes.snowflake import Snowflake
from application.mytypes.interaction import (
    ApplicationCommandInteractionData,
    ApplicationCommandInteractionDataOption,
)
from application.mytypes.user import (
    PartialUser as PartiaUserPayload
)
from application.mytypes.permissions import (
    ApplicationCommandPermissions as ApplicationCommandPermissionsPayload,
    ApplicationCommandPermissionsList as ApplicationCommandPermissionsListPayload,
    GuildApplicationCommandPermissionsList as GuildApplicationCommandPermissionsListPayload
)

from application.enums import (
    ApplicationCommandPermissionType as ACPT,
    MessageFlags
)
from application.components import CustomID
from application.discord import ApiBaseUrl
from application.discord.channel import Channel
from application.discord.member import Member
from application.discord.user import PartiaUser, User


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
            self.commander = Member(d, self._guild_id) \
                if (d := rawdata.get("member")) is not None else User(rawdata["user"])
            self.locale: str                    = rawdata['locale']
            self.guild_locale: Optional[str]    = rawdata.get('guild_locale')

        self._bot_token: str            = bot_token

        self._deferred: bool            = False

        # override
        self.custom_id: str = self._data.get("custom_id", "")
        
    @overload
    def check(self) -> bool:
        """Check the Command Permissions
        super().check is later.
        If using run(), callback DEFERRED_ response.
        """
        ...

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
        _log.info("target url: {}".format(url))
        _log.info("payload: {}".format(str(payload)))
        res: requests.Response = requests.post(url, json=payload)
        _log.info("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        print(res.text)
        return res
    
    def original_response(self, payload: dict) -> requests.Response:
        url = self.application_url + "/messages/@original"
        _log.info("target url: {}".format(url))
        _log.info("payload: {}".format(str(payload)))
        res: requests.Response = requests.patch(url, json=payload)
        _log.info("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def followup(self, payload: dict) -> requests.Response:
        url = self.webhook_url
        _log.info("target url: {}".format(url))
        _log.info("payload: {}".format(str(payload)))
        res: requests.Response = requests.post(url, json=payload)
        _log.info("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))
        return res
    
    def deferred_channel_message(self) -> Optional[requests.Response]:
        if self._deferred:
            _log.warning("Already deferred.")
            return None

        payload: dict = {
            "type" : InteractionResponseType.deferred_channel_message.value
        }
        res: requests.Response = self.callback(payload)
        _log.info("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))

        self._deferred = True

        return res
    
    def deferred_update_message(self) -> Optional[requests.Response]:
        if self._deferred:
            _log.warning("Already deferred.")
            return None

        payload: dict = {
            "type" : InteractionResponseType.deferred_message_update.value
        }
        res: requests.Response = self.callback(payload)
        _log.info("status code: {}".format(res.status_code))
        _log.debug("response: {}".format(res.text))

        self._deferred = True

        return res


    def get_user(self) -> Optional[PartiaUser]:
        user_payload: Optional[PartiaUserPayload] = self._data


    def check(self) -> bool:
        return True

    
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

    
    def check_permission(
        self,
        defferd_func: Optional[Callable[[], Optional[requests.Response]]] = None
    ) -> bool:
        """
        Check the component's user has command permission.
        if user CAN use command, return ture.
        else, return false
        """
        parse_data: list[str] = self.custom_id.strip('-')
        _log.debug(f"{str(parse_data)}")
        if len(parse_data) < 2:
            return False
        permission_type: str = parse_data[-2]
        target_id: str       = parse_data[-1]
        _log.debug(f"permission_type: {permission_type}")
        _log.debug(f"target_id: {target_id}")

        if permission_type == CustomID.PermissionType.all:
            return True
        if permission_type == CustomID.PermissionType.user:
            if target_id == str(self.commander.id):
                return True
            else:
                return False
        if permission_type == CustomID.PermissionType.command:
            # need API requests.
            # defferd.
            if defferd_func is not None:
                defferd_func()
            return self.__check_command_permission(target_id)
    
    def __check_command_permission(self, command_id: str) -> bool:
        acp: Optional[ApplicationCommandPermissionsListPayload] = self.get_permission(command_id)
        _log.debug(f"command_id: {command_id}")
        _log.debug(f"acp: {str(acp)}")

        if acp is None:
            return False
        
        acp: ApplicationCommandPermissionsListPayload = acp
        
        role_permissions: dict[str, str] = {}
        user_permissions: dict[str, str] = {}

        permission: ApplicationCommandPermissionsPayload
        for permission in acp:
            acpt: ACPT == ACPT(permission["id"])
            if acpt == ACPT.role:
                role_permissions[permission["id"]] = permission["permission"]
            elif acpt == ACPT.user:
                user_permissions[permission["id"]] = permission["permission"]
        
        _log.debug(f"user_permissions: {str(user_permissions)}")
        if user_permissions.get(str(self.commander.id), False):
            return True
        
        if isinstance(self.commander, User):
            # DM
            return True
        
        for r_id in self.commander._role_ids:
            perm: Optional[bool] = role_permissions.get(str(r_id))
            if perm is None:
                continue
            else:
                return perm
        return role_permissions.get(str(self._guild_id), False)


    def get_permission(self, command_id: str) -> Optional[ApplicationCommandPermissionsListPayload]:
        guild_acp = Optional[ApplicationCommandPermissionsListPayload] = None

        results: Optional[GuildApplicationCommandPermissionsListPayload] = self.get_ACP()

        guild_id = str(self._guild_id)
        for acp in results:
            _id = str(acp["id"])
            if command_id == _id:
                return acp
            elif _id == guild_id:
                guild_acp = acp

        return guild_acp

    def get_ACP(self) -> Optional[GuildApplicationCommandPermissionsListPayload]:
        url = ApiBaseUrl + f'/applications/{self.application_id}/guilds/{self._guild_id}/commands/permissions'
        headers = {
            "Authorization": f"Bot {self._bot_token}"
        }

        r: requests.Response = requests.get(url, headers=headers)

        if r.status_code == requests.codes.ok:
            _log.debug(url)
            _log.debug(str(r.status_code))
            _log.debug(r.text)
            return r.json()
        else:
            _log.warn(url)
            _log.warn(str(r.status_code))
            _log.warn(r.text)
            return None

# import asyncio, aiohttp
# import json
#
#     def get_permissions(self, command_id: str) -> Optional[ApplicationCommandPermissionsPayload]:
#         loop = asyncio.get_event_loop()
#         tasks = asyncio.gather(
#             self.get_guild_ACP(command_id),
#             self.get_ACP()
#         )
#         results: list[Optional[GuildApplicationCommandPermissionsPayload]] = loop.run_until_complete(tasks)
#
#         for res in results:
#             if res is not None:
#                 return res["permissions"]
#         return None
#
#     async def get_guild_ACP(self, command_id: str) -> Optional[GuildApplicationCommandPermissionsPayload]:
#         url = ApiBaseUrl + f'/applications/{self.application_id}/guilds/{self._guild_id}/commands/{command_id}/permissions'
#         headers = {
#             "Authorization": f"Bot {self._bot_token}"
#         }
#
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers) as resp:
#                 if resp.ok:
#                     text = await resp.text(encoding='utf-8')
#                     _log.info("Retrieves this command's permission.")
#                     _log.debug(f"{text}")
#                     return json.loads(text)[0]
#                 elif resp.status == requests.codes.not_found:
#                     _log.info("The application command's permissions could not be found. (Unchanged from the default)")
#                     return None
#                 else:
#                     text = await resp.text(encoding='utf-8')
#                     _log.error(f"HTTP Error; command id: {command_id}; guild id: {self._guild_id};")
#                     _log.error(f"HTTP Error; {text}")
#                     return None
#
#     async def get_ACP(self) -> Optional[GuildApplicationCommandPermissionsPayload]:
#         url = ApiBaseUrl + f'/applications/{self.application_id}/guilds/{self._guild_id}/commands/permissions'
#         headers = {
#             "Authorization": f"Bot {self._bot_token}"
#         }
#
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers) as resp:
#                 if resp.ok:
#                     text = await resp.text(encoding='utf-8')
#                     _log.info("Retrieves this command's permission.")
#                     _log.debug(f"{text}")
#                     return json.loads(text)[0]
#                 else:
#                     text = await resp.text(encoding='utf-8')
#                     _log.error(f"HTTP Error; command id: guild id: {self._guild_id};")
#                     _log.error(f"HTTP Error; {text}")
#                     resp.raise_for_status()
#                     return None

    # no permission
    def no_permission(self) -> None:
        _log.debug("no_permission")
        payload: dict = {
            "content" : "この操作を実行する権限がありません。\nYou do not have permission to run this command.",
            "flags" : MessageFlags.ephemeral.value,
        }
        r: requests.Response = self.followup(payload)
        _log.debug(str(r.status_code))
        _log.debug(r.text)

    def run_error(self, res: requests.Response, **options) -> bool:
        if res.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    
    def response_error(self, res: requests.Response, **options) -> bool:
        if res.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    

    def clean_error(self, res: requests.Response, **options) -> bool:
        if res.ok:
            # success
            return True
        # if error.
        _log.error("run_error")
        _log.error("status code: {}".format(res.status_code))
        _log.error(res.text)
        return False
    
    # Error
    def error(self) -> dict:
        return {
            "type" : InteractionResponseType.channel_message.value,
            "data" : {
                "content" : "ERROR;\nPlease report bot operator or server admins."
            }
        }

    # Test
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