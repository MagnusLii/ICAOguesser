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
    i = 1
    query = f'''INSERT INTO game (id, screen_name)
                VALUES ({i},"{givenName}");'''
    cursor(query)
    return '', 204


# Fetches airport names, lat- and longitude degrees for future use in map markers.
def search_airport():
    query = f'''SELECT airport.name, airport.latitude_deg, airport.longitude_deg
                FROM airport;'''
    results = cursor_fetchall(query)
    json_list = []
    for row in results:
        name = row[0]
        latitude = row[1]
        longitude = row[2]
        json = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude
        }
        json_list.append(json)
    return json_list
#TODO send data to JS for marker processing.


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
