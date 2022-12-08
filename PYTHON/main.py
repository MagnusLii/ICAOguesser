import random

from flask import Flask, request

from flask_cors import CORS

import connection

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Vars
numofobjectives = 0
listofgoals = []

class Objectives:
    def __int__(self, airportname, icao):
        self.name = airportname
        self.icao = icao

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
    rounds = request.form['Rounds']
    i = 1
    query = f'''INSERT INTO game (id, screen_name)
                VALUES ({i},"{givenName}");'''
    cursor(query)
    return '', 204


# Fetches airport names, lat- and longitude degrees for future use in map markers.
@app.route('/fetchAirportData')
def search_airport():
    query = f'''SELECT airport.name, airport.latitude_deg, airport.longitude_deg, airport.ident
                FROM airport
                WHERE type = "medium_airport";'''
    results = cursor_fetchall(query)
    json_list = []
    for row in results:
        name = row[0]
        latitude = row[1]
        longitude = row[2]
        icao = row[3]
        json = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude
            "icao": icao
        }
        json_list.append(json)
    for i in range(numofobjectives):
        randomnum = random.randint(1, len(json_list))
        listofgoals.append(
            Objectives(json_list[randomnum].name,
                       json_list[randomnum].icao))
    print(listofgoals)
    return json_list


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
