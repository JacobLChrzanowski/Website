from flask import Flask, Blueprint, render_template
from app import app
from app import postgres
import logging
import psycopg2.errors

routes_db = Blueprint('exta_bp', __name__)

# to check DB connection:
@routes_db.route("/testDB", methods=['GET', 'POST'])
def test_db():
    try:
        cur = postgres.p.cursor()
    except Exception as e:
        raise e
    try:
        cur.execute('SELECT VERSION()')
        row = cur.fetchone()
        # cur.execute('COMMIT')
    except (TypeError, psycopg2.errors.SyntaxError, psycopg2.errors.InFailedSqlTransaction) as e:
        logging.error('Failed to fetch from DB')
        cur.execute("ROLLBACK")
        return 'DB failure\n' + str(e)
    
    if row and 'PostgreSQL' in row[0]:
        return 'Working2\n' + str(row)
    else:
        return 'Not working2\n' + str(row)

# to check DB connection:
@routes_db.route("/get_user", methods=['GET'])
def get_user():
    try:
        cur = postgres.p.cursor()
    except Exception as e:
        raise e

@routes_db.route("/users")
def user_list():
    users = postgres.db.session.execute(postgres.db.select(postgres.User).order_by(postgres.User.username)).scalars()
    # return render_template("user/list.html", users=users)
    return str(users)

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