from flask import Flask, Blueprint, render_template, send_from_directory, abort,\
    redirect, url_for, request

import os
import logging
import psycopg2
# import blogPosts as bp

routes = Blueprint('routes_main', __name__)

@routes.route('/')
def root():
    # render_template()
    return 'root'

@routes.route('/hello')
def hello():
    redis.r.incr('hits')
    counter = int(redis.r.get('hits'))
    return f"This webpage has been viewed {counter} time(s)"

