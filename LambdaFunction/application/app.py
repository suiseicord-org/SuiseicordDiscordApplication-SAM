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
# from application.happi_setting import HappiSetting

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

BOT_TOKEN = os.getenv('DISCORD_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')
APPLICATION_PUBLIC_KEY = os.getenv('APPLICATION_PUBLIC_KEY')


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

    _log.debug("event: {}".format(str(event)))

    headers: dict = { k.lower(): v for k, v in event['headers'].items() }
    _log.debug("headers: {}".format(str(headers)))

    path: str = p if (p := event.get("rawPath")) is not None else event.get("path")
    
    if path == "/callback":
        """Discord Interations"""
        rawBody: str  = event['body']
        _log.info("rawBody: {}".format(rawBody))

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

        _log.debug("from_data")
        obj: Optional[Interaction] = from_data(req)
        _log.info(str(obj))
        if obj:
            # try:
            # _log.info("check()")
            # if not obj.check():
            #     _log.warn("no permission.")
            #     obj.no_permission()
            #     return None
            _log.debug("run()")
            obj.run()
            _log.debug("response()")
            obj.response()
            _log.debug("clean()")
            obj.clean()
            # except Exception as e:
            #     _log.error(e)
            #     return obj.error()
            
        return None
    # elif path == HappiSetting.httpPath:
    #     _log.info("GoogleForm SuiseiCord Happi App (from GAS)")
    #     rawBody: str  = event['body']
    #     _log.info("rawBody:")
    #     _log.info(rawBody)
    #     req: dict = json.loads(rawBody)
    #     url: str = req['url']
    #     payload: dict = req['payload']
    #     headers = {
    #         "Authorization": f'Bot {BOT_TOKEN}'
    #     }
    #     r = requests.post(url, headers=headers, json=payload)
    #     _log.info(r.status_code)
    #     _log.info(r.text)
    #     return {
    #         "cookies": [],
    #         "isBase64Encoded": False,
    #         "statusCode": r.status_code,
    #         "headers": r.headers,
    #         "body": r.text
    #     }
    elif path == "/test":
        return "THIS IS TEST FUNCTION."

if __name__ == '__main__':
    print(__name__)
    _log.debug("start")