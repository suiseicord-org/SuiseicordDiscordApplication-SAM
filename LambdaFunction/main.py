#!python3.9
import os, json
from logging import getLogger, config
from application.app import callback

_log = getLogger('application')

# Logger
LOGGING_MODE: str = os.getenv('LOGGING_MODE')

if (LOGGING_MODE is not None) and (LOGGING_MODE.lower() == 'debug'):
    fp = 'logging_format/debug.json'
else:
    fp = 'logging_format/info.json'
with open(fp, 'r') as f:
    _config = json.load(f)
config.dictConfig(_config)

def lambda_function(event: dict, context: dict):
    print(event.get('body'))
    return callback(event, context)