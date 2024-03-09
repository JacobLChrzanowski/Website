import os, logging
from flask import Flask
# from redis import Redis
from app import connections

_LOGGING_LEVELS = { 'debug': logging.DEBUG, 'info': logging.INFO}
LOGGING_LEVEL = _LOGGING_LEVELS[os.environ['LOGGING_LEVEL']]
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s :: %(message)s')
app = Flask(__name__, static_folder='../static')

redis = connections.conn_redis()
postgres = connections.conn_postgres()

from app import routes
