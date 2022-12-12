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
current_goal = 0
num_of_objectives = 10  # 10 goals is default
list_of_players = []
list_of_airports = []
list_of_goals = []


class Players:
    def __init__(self):
        self.points = 0


class Airports:
    def __init__(self, airport_name, lat, lon, ICAO):
        self.name = airport_name
        self.icao = ICAO
        self.latitude = lat
        self.longitude = lon


class Objectives:
    def __init__(self, airport_name, lat, lon, icao):
        self.name = airport_name
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
def clear_data():
    print('''LOG: Clearing data from DB in "clearData():"''')
    query = "DELETE FROM goal_reached;"
    cursor(query)
    query = "DELETE FROM game;"
    cursor(query)
    print('''LOG: Data cleared in "clearData():"''')
    return '', 204


def create_players():
    print('''LOG: Creating player objects in  "create_players()"''')
    list_of_players.append(Players())


def create_airports(jsonlist):
    print('''LOG: Creating airport objects in  "create_airport()"''')
    for i in range(0, len(jsonlist)):
        list_of_airports.append(Airports(str(jsonlist[i]['name']),
                                         (jsonlist[i]['latitude']),
                                         (jsonlist[i]['longitude']),
                                         str(jsonlist[i]['icao'])))
    print('''LOG: Objects done in "create_airport()"''')


def create_goals(jsonlist):
    global current_goal
    print('''LOG: Creating goal objects in  "create_goals()"''')
    for i in range(0, num_of_objectives):
        randomnum = random.randint(1, len(jsonlist))
        list_of_goals.append(Objectives(str(jsonlist[randomnum]['name']),
                                        (jsonlist[randomnum]['latitude']),
                                        (jsonlist[randomnum]['longitude']),
                                        str(jsonlist[randomnum]['icao'])))
    print('''LOG: Objects done in "create_goals()"''')
    if current_goal != 0:
        print('''LOG: Currentgoal not correct for game start, resetting currentgoal in "create_goals()"''')
        current_goal = 0


# Adds info for new game into DB.
@app.route('/gamesetup', methods=['POST'])
def setup_game():
    print('''LOG: Initializing game in "setup_game():"''')
    clear_data()
    try:
        given_name = request.form['InsertedName']
    except:  # Bare except 'cause we don't have time.
        given_name = 'John Doe'
    global num_of_objectives
    print('''LOG: Changing 'numofobjectives' in "setup_game():"''')
    num_of_objectives = int(request.form['Rounds'])
    print(f'''"numofobjectives" = {num_of_objectives}''')

    query = f'''INSERT INTO game (id, screen_name)
                VALUES ({1},"{given_name}");'''
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
    user_selected_airport = f"{list_of_airports[int(index)].latitude}, {list_of_airports[int(index)].longitude}"
    current_goal = f"{list_of_goals[current_goal].latitude}, {list_of_goals[current_goal].longitude}"
    print('''LOG: Calculating distance in "calculate_points():"''')
    distance_in_km = str(geopy.distance.geodesic(user_selected_airport, current_goal))

    # Slicing the ' km' from the end of the string.
    print('''LOG: Slicing "distance_in_km" string in "calculate_points():"''')
    slicedstr = slice(0, -3)
    distance_in_km = distance_in_km[slicedstr]
    distance_in_km = int(round(float(distance_in_km), 1))
    # Int() func won't accept more than 10 decimals, so we must round the number to avoid errors above ^^.
    print(distance_in_km)
    print(f'distance is {distance_in_km}')

    middlepointlat = (list_of_airports[int(index)].latitude + list_of_goals[current_goal].latitude) / 2
    middlepointlon = (list_of_airports[int(index)].longitude + list_of_goals[current_goal].longitude) / 2

    points = 10000 - distance_in_km
    if points < 0:
        points = 0
    print(f'points are {points}')
    list_of_players[0].points += points
    finalpoints = int(round((list_of_players[0].points / num_of_objectives), 2))

    finaljson = '{' + f'''"distance": {distance_in_km},
    "choicelat": {list_of_airports[int(index)].latitude},
    "choicelon": {list_of_airports[int(index)].longitude},
    "goallat": {list_of_goals[current_goal].latitude},
    "goallon": {list_of_goals[current_goal].longitude},
    "middlepointlat": {middlepointlat},
    "middlepointlon": {middlepointlon},
    "points": {points},
    "totalpoints": {list_of_players[0].points},
    "finalpoints": {finalpoints}''' + '}'
    print(finaljson)

    if current_goal == (num_of_objectives - 1):
        print('LOG: Returning "finaljson, 69" in calculate_points():')
        return finaljson, 69

    else:
        print('LOG: Returning "finaljson, 200" in calculate_points():')
        return finaljson, 200


@app.route('/nextgoal')
def next_goal_update():
    global current_goal
    print('''LOG: updating "currentgoal" in "next_goal_update():"''')
    current_goal += 1
    if current_goal <= num_of_objectives:
        print('''LOG: "currentgoal" updated in "next_goal_update():"''')
        return '', 204
    elif current_goal > num_of_objectives:
        current_goal = num_of_objectives
        return '', 204


@app.route('/nextgoalname')
def next_goal():
    global current_goal
    global list_of_goals
    print('Currentgoal index = ' + str(current_goal))
    print('''LOG: Sending next goal hints in "next_goal():"''')
    json = {"name": str(list_of_goals[current_goal].name)}
    return json, 200


@app.route('/reset')
def factory_reset():
    # DANIEL.... this is not what I meant.....
    global current_goal
    global num_of_objectives
    global list_of_players
    global list_of_airports
    global list_of_goals
    current_goal = 0
    num_of_objectives = 10
    list_of_players = []
    list_of_airports = []
    list_of_goals = []
    clear_data()


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)
