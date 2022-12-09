#!python3.9
import os
import boto3

TABLE_PREFIX: str = os.getenv('TABLE_PREFIX')

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

class DynamoDB:
    def __init__(self, table_name: str) -> None:
        name = f'{TABLE_PREFIX}-{table_name}'
        self.table = dynamodb.Table(name)
    

class SettingDynamoDB(DynamoDB):
    def __init__(self) -> None:
        table_name: str = "CommandSetting"
        super().__init__(table_name)