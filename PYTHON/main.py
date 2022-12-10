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
listofplayers = []
listofairports = []
listofgoals = []


class Players:
    def __init__(self):
        self.points = 0


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
    print('''LOG: Clearing data from DB in "clearData():"''')
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)
    print('''LOG: Data cleared in "clearData():"''')
    return '', 204


def create_players():
    print('''LOG: Creating player objects in  "create_players()"''')
    listofplayers.append(Players())


def create_airports(jsonlist):
    print('''LOG: Creating airport objects in  "create_airport()"''')
    for i in range(0, len(jsonlist)):
        listofairports.append(Airports(str(jsonlist[i]['name']),
                                       (jsonlist[i]['latitude']),
                                       (jsonlist[i]['longitude']),
                                       str(jsonlist[i]['icao'])))
    print('''LOG: Objects done in "create_airport()"''')


def create_goals(jsonlist):
    global currentgoal
    print('''LOG: Creating goal objects in  "create_goals()"''')
    for i in range(0, numofobjectives):
        randomnum = random.randint(1, len(jsonlist))
        listofgoals.append(Objectives(str(jsonlist[randomnum]['name']),
                                      (jsonlist[randomnum]['latitude']),
                                      (jsonlist[randomnum]['longitude']),
                                      str(jsonlist[randomnum]['icao'])))
    print('''LOG: Objects done in "create_goals()"''')
    if currentgoal != 0:
        print('''LOG: Currentgoal not correct for game start, resetting currentgoal in "create_goals()"''')
        currentgoal = 0


# Adds info for new game into DB.
@app.route('/gamesetup', methods=['POST'])
def setup_game():
    print('''LOG: Initializing game in "setup_game():"''')
    clearData()
    givenName = request.form['InsertedName']
    global numofobjectives
    print('''LOG: Changing 'numofobjectives' in "setup_game():"''')
    numofobjectives = int(request.form['Rounds'])
    print(f'''"numofobjectives" = {numofobjectives}''')

    query = f'''INSERT INTO game (id, screen_name)
                VALUES ({1},"{givenName}");'''
    cursor(query)
    return '', 204


# Fetches airport names, lat- and longitude degrees for future use in map markers.
@app.route('/fetchAirportData')
def search_airport():
    query = f'''SELECT airport.name, airport.latitude_deg, airport.longitude_deg, airport.ident
                FROM airport
                WHERE type = "large_airport";'''
    print('''LOG: requesting airport data from DB in "search_airport()"''')
    results = cursor_fetchall(query)
    json_list = []
    print('''LOG: Creating JSON data for return in "search_airport()"''')
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
    print('''LOG: JSON data Done in "search_airport()"''')
    create_players()
    create_airports(json_list)
    create_goals(json_list)
    return json_list


@app.route('/confirmation/<index>')  # index = the index number of the airport the player chose as their answer.
def calculate_points(index):
    print('''LOG: Fetching Lat/lon coords in "calculate_points():"''')
    user_selected_airport = f"{listofairports[int(index)].latitude}, {listofairports[int(index)].longitude}"
    current_goal = f"{listofgoals[currentgoal].latitude}, {listofgoals[currentgoal].longitude}"
    print('''LOG: Calculating distance in "calculate_points():"''')
    distance_in_km = str(geopy.distance.geodesic(user_selected_airport, current_goal))

    # Slicing the ' km' from the end of the string.
    print('''LOG: Slicing "distance_in_km" string in "calculate_points():"''')
    slicedstr = slice(0, -3)
    distance_in_km = distance_in_km[slicedstr]
    print(distance_in_km)
    print(f'distance is {distance_in_km}')

    middlepointlat = (listofairports[int(index)].latitude + listofgoals[currentgoal].latitude) / 2
    middlepointlon = (listofairports[int(index)].longitude + listofgoals[currentgoal].longitude) / 2

    points = 10000 - float(distance_in_km)
    if points < 0:
        points = 0
    print(f'points are {points}')
    listofplayers[0].points += points

    finaljson = '{' + f'''"distance": {distance_in_km},
    "choicelat": {listofairports[int(index)].latitude},
    "choicelon": {listofairports[int(index)].longitude},
    "goallat": {listofgoals[currentgoal].latitude},
    "goallon": {listofgoals[currentgoal].longitude},
    "middlepointlat": {middlepointlat},
    "middlepointlon": {middlepointlon},
    "points": {points},
    "totalpoints": {listofplayers[0].points}''' + '}'
    print(finaljson)

    if currentgoal == (numofobjectives - 1):
        print('LOG: Returning "finaljson, 69" in calculate_points():')
        return finaljson, 69

    else:
        print('LOG: Returning "finaljson, 200" in calculate_points():')
        return finaljson, 200


@app.route('/nextgoal')
def next_goal_update():
    global currentgoal
    print('''LOG: updating "currentgoal" in "next_goal_update():"''')
    currentgoal += 1
    if currentgoal <= numofobjectives:
        print('''LOG: "currentgoal" updated in "next_goal_update():"''')
        return '', 204
    elif currentgoal > numofobjectives:
        currentgoal = numofobjectives
        return '', 204


@app.route('/nextgoalname')
def next_goal():
    global currentgoal
    global listofgoals
    print('Currentgoal index = ' + str(currentgoal))
    print('''LOG: Sending next goal hints in "next_goal():"''')
    json = {"name": str(listofgoals[currentgoal].name)}
    return json, 200


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
