#!python3.9
import os
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

class DynamoDB:
    def __init__(self, table_name: str) -> None:
        pass