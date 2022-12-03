"""Set your own DB connection settings here
DO NOT PUSH TO GIT UNDER ANY CIRCUMSTANCES!!!!
I will commit stop existence upon you if you do!"""

import mysql.connector

sqlconnect = mysql.connector.connect(
    host="localhost",
    port="3306",
    database="flight_game",
    user="root",
    password="5579",
    autocommit=True
)