
from typing import Literal, List, TypedDict
from .snowflake import Snowflake


ApplicationCommandPermissionType = Literal[1, 2, 3]


class ApplicationCommandPermissions(TypedDict):
    id: Snowflake
    type: ApplicationCommandPermissionType
    permission: bool

ApplicationCommandPermissionsList = List[ApplicationCommandPermissions]

class GuildApplicationCommandPermissions(TypedDict):
    id: Snowflake
    application_id: Snowflake
    guild_id: Snowflake
    permissions: ApplicationCommandPermissionsList

GuildApplicationCommandPermissionsList = List[GuildApplicationCommandPermissions]