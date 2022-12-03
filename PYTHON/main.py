import mysql.connector
from flask import Flask, request, Response
import connection
import geopy.distance

app = Flask(__name__)


def cursor(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)


def cursor_fetchall(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)
    outcome = sqlcursor.fetchall()
    return outcome


@app.route('/1')
def gamestart():
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)
    return '', 204

# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
