import os, logging
from flask import Flask
from redis import Redis
import psycopg2

_LOGGING_LEVELS = { 'debug': logging.DEBUG, 'info': logging.INFO}
LOGGING_LEVEL = _LOGGING_LEVELS[os.environ['LOGGING_LEVEL']]
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s :: %(message)s')
app = Flask(__name__, static_folder='../static')
redis = Redis(host='redis', port=6379)
try:
    postgres = psycopg2.connect(host='docker_flaskapp_prod-postgres_db-1', user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
except psycopg2.OperationalError as e:
    logging.critical('psycopg2 failed to authenticate to postgres')
    raise e

from src import routes
