#!python3.9
import os
import boto3

from logging import getLogger
_log = getLogger(__name__)

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

TABLE_PREFIX: str = os.getenv('TABLE_PREFIX')

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

class DynamoDB:
    def __init__(self, table_name: str) -> None:
        name = f'{TABLE_PREFIX}-{table_name}'
        _log.debug("table name: {}".format(name))
        self.table = dynamodb.Table(name)
    
    def get_item(self):
        pass
    

class SettingDynamoDB(DynamoDB):
    def __init__(self, command: str, target_id: int = 0) -> None:
        table_name: str = "CommandSetting"
        super().__init__(table_name)
        self.command: str = command
        self.target_id: int = int(target_id)

    def get_item(self):
        keys: dict = {
            "name" : self.command,
            "id" : self.target_id
        }
        _log.debug(keys)
        res = self.table.get_item(
            Key = keys
        )
        _log.debug(res)
        return res["Item"]
