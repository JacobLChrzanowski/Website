import os
import logging
import time
from redis import Redis
import psycopg2

def conn_redis(attempts:int = 5, wait_interval:int = 1) -> Redis:
    try:
        redis = Redis(host='inacanoe-qa-redis', port=6379)
        logging.info('redis could connect')
        return redis
    except Exception as e:
        if attempts == 0:
            logging.critical('redis failed to connect')
            raise e
        else:
            logging.info('redis failed to connect, trying again')
            time.sleep(wait_interval)
            redis = conn_redis(attempts-1, wait_interval)
            return redis

def conn_postgres(attempts:int = 5, wait_interval:int = 1) -> psycopg2.extensions.connection:
    try:
        postgres = psycopg2.connect(host='inacanoe-qa-postgres', user=os.environ['POSTGRES_DB_USER'], password=os.environ['POSTGRES_DB_PASSWORD'])
        logging.info('psycopg2 could connect')
        return postgres
    except psycopg2.OperationalError as e:
        if attempts == 0:
            logging.critical('psycopg2 failed to connect or authenticate to postgres')
            raise e
        else:
            logging.info('psycopg2 failed to connect to postgres, trying again')
            time.sleep(wait_interval)
            postgres = conn_postgres(attempts-1, wait_interval)
            return postgres
