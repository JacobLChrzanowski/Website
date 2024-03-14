import os, sys, logging
project_parent_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_parent_dir)

from flask import Flask

# _LOGGING_LEVELS = { 'debug': logging.DEBUG, 'info': logging.INFO}
# LOGGING_LEVEL = _LOGGING_LEVELS[os.environ['LOGGING_LEVEL']]
# logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s :: %(message)s')



# @app.before_first_request
# def a_redis(*args, **kwargs) -> connections.RedisWrapper:
#     return connections.RedisWrapper(
#         host='inacanoe-qa-redis',
#         port=6379
#     )

def create_app() -> Flask:
    _LOGGING_LEVELS = { 'debug': logging.DEBUG, 'info': logging.INFO}
    LOGGING_LEVEL = _LOGGING_LEVELS[os.environ['LOGGING_LEVEL']]
    logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s :: %(message)s')

    logging.critical('hello!?')

    app = Flask(__name__, static_folder='../static')

    # from app import connections
    from app.routes import routes # type: ignore
    app.register_blueprint(routes)
    from app.routes_db import routes_db #type: ignore
    app.register_blueprint(routes_db)

    return app


# with app.app_context():
#     logging.critical('here!!')
#     logging.critical(app.debug)
#     redis = connections.RedisWrapper(
#             host='inacanoe-qa-redis',
#             port=6379
#         )
#     postgres = connections.PostgresWrapper(
#         app,
#         host='inacanoe-qa-postgres',
#         port=5432,
#         user=os.environ['POSTGRES_DB_USER'],
#         password=os.environ['POSTGRES_DB_PASSWORD'],
#         db_name='postgres'
#     )

