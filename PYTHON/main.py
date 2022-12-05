from flask import Flask, request

import connection

app = Flask(__name__)


# For POST requests.
def cursor(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)


# For GET requests.
def cursor_fetchall(query):
    sqlcursor = connection.sqlconnect.cursor()
    sqlcursor.execute(query)
    outcome = sqlcursor.fetchall()
    return outcome


# Deletes previous game data from DB.
def clearData():
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)
    return '', 204


# Adds info for new game into DB.
@app.route('/2', methods=['POST'])
def setupGame():
    clearData()
    givenName = request.form['InsertedName']
    print(givenName)
    i = 1
    query = f'''INSERT INTO game (id, screen_name) VALUES ({i},"{givenName}");'''
    cursor(query)

    return '', 204


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
