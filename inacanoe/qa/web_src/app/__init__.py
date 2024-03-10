import os, logging
from flask import Flask
# from redis import Redis
from app import connections

_LOGGING_LEVELS = { 'debug': logging.DEBUG, 'info': logging.INFO}
LOGGING_LEVEL = _LOGGING_LEVELS[os.environ['LOGGING_LEVEL']]
logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s :: %(message)s')
app = Flask(__name__, static_folder='../static')

redis = connections.RedisWrapper(
    host='inacanoe-qa-redis',
    port=6379
)
postgres = connections.PostgresWrapper(
    app,
    host='inacanoe-qa-postgres',
    port=5432,
    user=os.environ['POSTGRES_DB_USER'],
    password=os.environ['POSTGRES_DB_PASSWORD'],
    db_name='postgres'
)

from app import routes # type: ignore
from app.routes_db import routes_db #type: ignore
app.register_blueprint(routes_db)
