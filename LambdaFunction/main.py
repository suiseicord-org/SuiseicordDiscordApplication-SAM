#!python3.9
import os, json, sys
from application.app import callback

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

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

def lambda_function(event: dict, context: dict):
    return callback(event, context)