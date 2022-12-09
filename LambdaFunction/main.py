#!python3.9
import os, json, sys

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

import boto3
ssm = boto3.client('ssm')

def get_ssm_param(name: str) -> str:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm.html#SSM.Client.get_parameter
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']

APPLICATION_NAME: str = os.getenv('APPLICATION_NAME')

os.environ['DISCORD_TOKEN'] = get_ssm_param(
    f"/DiscordApplication/{APPLICATION_NAME}/Discord/Token"
)
os.environ['APPLICATION_ID'] = get_ssm_param(
    f"/DiscordApplication/{APPLICATION_NAME}/Discord/ApplicationID"
)
os.environ['APPLICATION_PUBLIC_KEY'] = get_ssm_param(
    f"/DiscordApplication/{APPLICATION_NAME}/Discord/ApplicationPublicKey"
)
os.environ['TABLE_PREFIX'] = get_ssm_param(
    f"/DiscordApplication/{APPLICATION_NAME}/DynamoDB/TablePrefix"
)

LOGGING_MODE: str = os.getenv('LOGGING_MODE')

from logging import getLogger, Formatter, StreamHandler
_log = getLogger()

if (LOGGING_MODE is not None) and (LOGGING_MODE.lower() == 'debug'):
    log_level = 10 # DEBUG
    # _log.setLevel(10) # DEBUG
else:
    log_level = 20 # INFO
    # _log.setLevel(20) # INFO

# _log.setLevel(log_level)

fmt = Formatter(
    fmt="[%(levelname)-8s] %(name)s lines %(lineno)d %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
for hdr in _log.handlers:
    _log.removeHandler(hdr)
_log.propagate = False
handler = StreamHandler(sys.stdout)   
handler.setFormatter(fmt)
handler.setLevel(log_level)
_log.setLevel(log_level)
_log.addHandler(handler)

from application.app import callback

def lambda_function(event: dict, context: dict):
    return callback(event, context)