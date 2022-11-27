#!python3.9
import os
import pymysql
from pymysql import Connection
from typing import Optional

if not __debug__:
    from dotenv import load_dotenv
    load_dotenv('.env')

RDS_HOST    = os.getenv('RDS_HOST')
DB_USER     = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME     = os.getenv('DB_NAME')

from logging import getLogger
_log = getLogger(__name__)

class RDS:
    def __init__(self):
        self.conn = self.connect_db()

    def connect_db(self) -> Connection:
        try:
            conn = pymysql.connect(host=RDS_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_NAME, connect_timeout=5)
            return conn
        except pymysql.MySQLError as e:
            _log.error("Unexpected error: Could not connect to MySQL instance.")
            _log.error(str(e))
            raise RDSConnectionError(e)

class RDSError(Exception):
    """RDS MySQLでエラーが起きた時に投げる"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    
    def __str__(self) -> str:
        return "RDS Error. Please check Application Log."

class RDSConnectionError(RDSError):
    """RDS MySQLでエラーが起きた時に投げる"""
    def __init__(self, error: pymysql.MySQLError, *args: object):
        super().__init__(*args)
        self.error = error
    
    def __str__(self) -> str:
        return "RDS *Connection* Error. Please check Application Log."