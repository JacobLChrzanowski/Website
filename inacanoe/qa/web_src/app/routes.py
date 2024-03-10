from flask import Flask, render_template, send_from_directory, abort,\
    redirect, url_for, request
from app import app
from app import redis
import os
import logging
import psycopg2
# import blogPosts as bp

@app.route('/')
def hello():
    redis.r.incr('hits')
    counter = int(redis.r.get('hits'))
    return f"This webpage has been viewed {counter} time(s)"
