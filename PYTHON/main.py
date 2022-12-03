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

def gamestart():
    query = f'''DELETE FROM game, goal_reached;'''
    cursor(query)



# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
