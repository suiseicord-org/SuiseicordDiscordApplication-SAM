#!python3.9
import os
import json
import requests
from typing import Optional
from logging import getLogger, config

from application import from_data
from application.interaction import Interaction
from application.enums import (
    InteractionType,
    InteractionResponseType
)
from application.happi_setting import HappiSetting

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('../.env')

# init
BOT_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
APPLICATION_PUBLIC_KEY = os.getenv('APPLICATION_PUBLIC_KEY')

# Logger
LOGGING_MODE: str = os.getenv('LOGGING_MODE')

if LOGGING_MODE.lower() == 'debug':
    fp = 'logging_format/debug.json'
else:
    fp = 'logging_format/info.json'
with open(fp, 'r') as f:
    _config = json.load(f)
config.dictConfig(_config)
_log = getLogger(__name__)

def verify(signature: str, timestamp: str, body: str) -> bool:
    from nacl.signing import VerifyKey
    verify_key = VerifyKey(bytes.fromhex(APPLICATION_PUBLIC_KEY))
    try:
        verify_key.verify(f"{timestamp}{body}".encode(), bytes.fromhex(signature))
    except Exception as e:
        print(f"failed to verify request: {e}")
        return False

    return True

def callback(event: dict, context: dict):
    """AWS Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    _log.debug("event:")
    _log.debug(str(event))

    headers: dict = { k.lower(): v for k, v in event['headers'].items() }
    _log.debug("headers:")
    _log.debug(str(headers))

    path: str = p if (p := event.get("rawPath")) is not None else event.get("path")
    
    if path == "/callback":
        """Discord Interations"""
        rawBody: str  = event['body']
        _log.info("rawBody:")
        _log.info(rawBody)

        # validate request
        signature = headers.get('x-signature-ed25519')
        timestamp = headers.get('x-signature-timestamp')
        if not verify(signature, timestamp, rawBody):
            _log.warning("not verfy.")
            return {
                "cookies": [],
                "isBase64Encoded": False,
                "statusCode": 401,
                "headers": {},
                "body": ""
            }
        _log.info("verfy!!")

        req: dict = json.loads(rawBody)

        #ping pong
        if req['type'] == InteractionType.ping.value:
            return {
                "type" : InteractionResponseType.pong.value
            }

        obj: Optional[Interaction] = from_data(req, BOT_TOKEN)
        if obj:
            _log.info("run()")
            obj.run()
            _log.info("response()")
            obj.response()
            _log.info("clean()")
            obj.clean()
            
        return None
    elif path == HappiSetting.httpPath:
        _log.info("GoogleForm SuiseiCord Happi App (from GAS)")
        rawBody: str  = event['body']
        _log.info("rawBody:")
        _log.info(rawBody)
        req: dict = json.loads(rawBody)
        url: str = req['url']
        payload: dict = req['payload']
        headers = {
            "Authorization": f'Bot {BOT_TOKEN}'
        }
        r = requests.post(url, headers=headers, json=payload)
        _log.info(r.status_code)
        _log.info(r.text)
        return {
            "cookies": [],
            "isBase64Encoded": False,
            "statusCode": r.status_code,
            "headers": r.headers,
            "body": r.text
        }
    elif path == "/test":
        return "THIS IS TEST FUNCTION."

if __name__ == '__main__':
    _log.debug("start")