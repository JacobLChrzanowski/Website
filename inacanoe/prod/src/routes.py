# from flask import Flask, request, jsonify
# from pymongo import MongoClient

# app = Flask(__name__)


# def get_db():
#     client = MongoClient('mongodb://db:27017/', connect=False)
#     return client.application_database


# @app.route("/ping")
# def ping():
#     return "pong"


# # to check DB connection:
# @app.route("/users", methods=['GET', 'POST'])
# def users_route():
#     try:
#         if request.method == 'GET':
#             users = []
#             for user in get_db().users.find():
#                 users.append(user.get("name", ""))
#             return jsonify({"status": "success", "payload": users}), 200
#         elif request.method == 'POST':
#             try:
#                 name = request.form["name"]
#             except KeyError:
#                 return jsonify({"status": "failed", "payload": "Please insert a name"}), 400
#             user_id = get_db().users.insert_one({'name': name}).inserted_id
#             return jsonify({"status": "success", "payload": str(user_id)}), 200
#     except Exception:
#         return (
#             jsonify({"status": "failed", "payload": "An internal server error happened. Please try again later"}),
#             500
#         )


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)


from flask import Flask, render_template, send_from_directory, abort,\
redirect, url_for, request
from src import app
from src import redis
from src import postgres
import os, logging
import psycopg2
# import blogPosts as bp

@app.route('/')
def hello():
    redis.incr('hits')
    counter = int(redis.get('hits'))
    return f"This webpage has been viewed {counter} time(s)"

# to check DB connection:
@app.route("/testDB", methods=['GET', 'POST'])
def test_db():
    try:
        cur = postgres.cursor()
    except Exception as e:
        raise e
    
    try:
        cur.execute('SELECT VERSION()')
        row = cur.fetchone()
        # cur.execute('COMMIT')
    except (TypeError, psycopg2.errors.SyntaxError, psycopg2.errors.InFailedSqlTransaction) as e:
        logging.error('Failed to fetch from DB')
        cur.execute("ROLLBACK")
        return 'DB call working'
    
    if row == ('PostgreSQL 15.3 (Debian 15.3-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit', ):
        return 'Working'
    else:
        return 'Not working'
    # try:
    #     if request.method == 'GET':
    #         users = []
    #         for user in get_db().users.find():
    #             users.append(user.get("name", ""))
    #         return jsonify({"status": "success", "payload": users}), 200
    #     elif request.method == 'POST':
    #         try:
    #             name = request.form["name"]
    #         except KeyError:
    #             return jsonify({"status": "failed", "payload": "Please insert a name"}), 400
    #         user_id = get_db().users.insert_one({'name': name}).inserted_id
    #         return jsonify({"status": "success", "payload": str(user_id)}), 200
    # except Exception:
    #     return (
    #         jsonify({"status": "failed", "payload": "An internal server error happened. Please try again later"}),
    #         500
    #     )