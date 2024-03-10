import os
import logging
import time
from typing import Union
from flask import Flask
from redis import Redis
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import Integer, String, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column

class RedisWrapper:
    def __init__(self,
                 host: str,
                 port: int,
                 attempts: int = 5,
                 wait_interval:int = 1
                ):
        self.r: Redis
        self.host = host
        self.port = port
        self.conn_redis(attempts, wait_interval)

    def conn_redis(self, attempts: int = 5, wait_interval: int = 1):
        for _ in range(attempts):
            try:
                self.r = Redis(host=self.host, port=self.port)
                self.r.ping() #type: ignore
                logging.info(f"Connected to Redis host at {self.host} : {self.port}")
                return
            except Exception as e:
                logging.warning("Redis failed to connect\n" + str(e))
                time.sleep(wait_interval)
        logging.critical(f"Redis failed to connect after {attempts} attempts")
        raise ConnectionError("Failed to connect to Redis server")

    def set(self, key: Union[bytes, str], value: Union[bytes, str]) -> bool:
        return self.r.set(key, value) is not None

class PostgresWrapper:
    def __init__(
            self,
            app: Flask,
            host: str,
            user: str,
            password: str,
            db_name: str,
            port: int = 5432,
            attempts: int = 5,
            wait_interval: int = 1,
        ):
        self.p: psycopg2.extensions.connection
        self.host = host
        self.port = port
        # self.conn_postgres(user, password, attempts, wait_interval)

        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{db_name}'
        self.db = SQLAlchemy(model_class=Base)
        self.db.init_app(app)
        class User(self.db.Model):
            __tablename__ = 'user'
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            date_created: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
            date_modified: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP)
            username: Mapped[String] = mapped_column(String, nullable=False)
            realname: Mapped[String] = mapped_column(String, nullable=False)
            description: Mapped[String] = mapped_column(String)
            email: Mapped[String] = mapped_column(String)
            private: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
        self.User = User

    def conn_postgres(self, user: str, password: str, attempts: int, wait_interval: int):
        for _ in range(attempts):
            try:
                self.p = psycopg2.connect( host=self.host, port=self.port, user=user, password=password )
                logging.info(f"psycopg2 connected to {self.host}:{self.port}")
                return
            except psycopg2.OperationalError as _:
                logging.warning( "psycopg2 failed to connect" )
            time.sleep(wait_interval)
        logging.critical(f"psycopg2 failed to connect after {attempts} attempts")
        raise ConnectionError("Failed to connect to Postgres DB")

class Base(DeclarativeBase):
    pass
