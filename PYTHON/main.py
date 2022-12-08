

# Required packages = geopy, mysql-connector-python, flask, flask-cors

# Imports
import random

import geopy.distance
from flask import Flask, request
from flask_cors import CORS

import connection

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Vars
currentgoal = 0
numofobjectives = 10  # 10 goals is default
listofairports = []
listofgoals = []


class Airports:
    def __init__(self, airportname, lat, lon, icao):
        self.name = airportname
        self.icao = icao
        self.latitude = lat
        self.longitude = lon


class Objectives:
    def __init__(self, airportname, lat, lon, icao):
        self.name = airportname
        self.icao = icao
        self.latitude = lat
        self.longitude = lon


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


def create_airports(jsonlist):
    for i in range(0, len(jsonlist)):
        listofairports.append(Objectives(str(jsonlist[i]['name']),
                                         (jsonlist[i]['latitude']),
                                         (jsonlist[i]['longitude']),
                                         str(jsonlist[i]['icao'])))


def create_goals(jsonlist):
    print('creating goals')
    for i in range(0, numofobjectives):
        randomnum = random.randint(1, len(jsonlist))
        listofgoals.append(Objectives(str(jsonlist[randomnum]['name']),
                                      (jsonlist[randomnum]['latitude']),
                                      (jsonlist[randomnum]['longitude']),
                                      str(jsonlist[randomnum]['icao'])))


# Adds info for new game into DB.
@app.route('/2', methods=['POST'])
def setupGame():
    clearData()
    givenName = request.form['InsertedName']
    global numofobjectives
    numofobjectives = int(request.form['Rounds'])
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
            "longitude": longitude,
            "icao": icao
        }
        json_list.append(json)

    create_airports(json_list)
    create_goals(json_list)
    return json_list


@app.route('/confirmation/<index>')  # index = the index number of the airport the player chose as their answer.
def calculate_points(index):
    user_selected_airport = f"{listofairports[int(index)].latitude}, {listofairports[int(index)].longitude}"
    current_goal = f"{listofgoals[currentgoal].latitude}, {listofgoals[currentgoal].longitude}"
    distance_in_km = str(geopy.distance.geodesic(user_selected_airport, current_goal))

    # Slicing the ' km' from the end of the string.
    slicedstr = slice(0, -3)
    distance_in_km = {"distance": distance_in_km[slicedstr]}
    print(distance_in_km)
    return distance_in_km, 200

@app.route('/nextgoal')
def next_goal():
    global currentgoal
    print('updating goal')
    currentgoal += 1
    return '', 204


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
