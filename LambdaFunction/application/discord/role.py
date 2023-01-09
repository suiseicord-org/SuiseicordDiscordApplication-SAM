#!python3.9
from application.mytypes.snowflake import Snowflake
from application.mytypes.role import (
    Role as RolePayload
)

class Role:
    def __init__(self, payload: RolePayload, guild_id: Snowflake):
        self.id: Snowflake = payload["id"]
        self.name: str = payload["name"]
        self.color: int = payload["color"]
        self.hoist: bool = payload["hoist"]
        self.position: int = payload["position"]
        self.permissions: str = payload["permissions"]
        self.managed: bool = payload["managed"]
        self.mentionable: bool = payload["mentionable"]
        self._guild_id = guild_id
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def mention(self) -> str:
        if int(self.id) == int(self._guild_id):
            # @everyone
            return "@everyone"
        return f"<@&{self.id}>"
