from flask import Flask, request
from model import initdb, Location, Client
import urllib.parse
from datetime import datetime


app = Flask(__name__)


@app.route("/")
def hello():
    # log_request(request)
    return "Hello World!"


@app.route("/v1/")
def save_location():
    log_request(request)
    return "Hello World!"


@app.route("/view/<username>")
def view_username(username):
    output = "Hello " + username + '<br>'
    logs = Location.select().where(Location.username == username).order_by(Location.date.desc())

    for log in logs:
        output += str(log.date) + '<br>'
    return output


def log_request(request):
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    public_token = request.args.get('username')
    secret_token = request.args.get('sessionid')
    print(request)
    try:
        date_str = urllib.parse.unquote(request.args.get('date'))
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
        print("New log from : " + public_token + " Date: " + str(date))
        print("----")
        client = Client.fetch(public_token, secret_token)
        client.log_location(latitude=latitude, longitude=longitude, date=date)
    except AttributeError as e:
        print("Request cannot be parsed: " + str(e))


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database using the command line."""
    # TODO: prevent this from being done on production
    initdb()
    print('Initialized the database.')
