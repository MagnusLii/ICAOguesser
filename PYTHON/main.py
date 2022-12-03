import mysql.connector
from flask import Flask, request, Response

app = Flask(__name__)


# Server start.
if __name__ == '__main__':
    app.run(use_reloader=True, port=3000)