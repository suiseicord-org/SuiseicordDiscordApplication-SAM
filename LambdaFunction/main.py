#!python3.9
import os, json, sys
from logging import getLogger, Formatter, StreamHandler
from application.app import callback

# _log = getLogger('application')
_log = getLogger()

# Logger
LOGGING_MODE: str = os.getenv('LOGGING_MODE')

if (LOGGING_MODE is not None) and (LOGGING_MODE.lower() == 'debug'):
    log_level = 10 # DEBUG
    # _log.setLevel(10) # DEBUG
else:
    loglevel = 20 # INFO
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