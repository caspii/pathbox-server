from flask import Flask, request, abort, render_template
from model import init_db, Location, Client
import urllib.parse
from datetime import datetime
from lib import humantime


app = Flask(__name__)


def human_time(value):
    """Allow pretty dates via jinja2 filter"""
    return humantime.pretty_date(value)


app.jinja_env.filters['human_time'] = human_time



@app.route("/")
def hello():
    return "Hello world"


@app.route("/v1/")
def log_location():
    log_request(request)
    return "Hello World!"


@app.route("/view/<public_token>/<date_str>")
@app.route("/view/<public_token>/<date_str>/<raw>")
@app.route("/view/<public_token>")
def view_username(public_token, date_str=None, raw=None):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    else:
        date = None
    client, logs = Client.get_logs(public_token, date)

    output = "Hello " + public_token + '<br><br>'
    output += "First seen: %s, last seen %s <br><br>" %(client.date_first_seen, client.date_last_seen)

    coords = []
    for log in logs:
        output += str(log.date_created) + '<br>'
        coords.append({'lat': float(log.latitude), 'lng': float(log.longitude)})
    if raw:
        return output
    else:
        return render_template('map.html', coords=coords, client=client)


def log_request(request):
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    public_token = request.args.get('username')
    secret_token = request.args.get('username') # This is a terrible hack TODO: revert this
    # secret_token = request.args.get('sessionid')
    #print(request)
    try:
        date_str = urllib.parse.unquote(request.args.get('date'))
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
        print("New log from : " + public_token + " Date: " + str(date))
        print("----")
    except AttributeError as e:
        print("Request cannot be parsed: " + str(e))
    client = Client.fetch(public_token, secret_token)
    if client:
        client.add_log_entry(latitude=float(latitude), longitude=float(longitude), date=date)


@app.cli.command('init_db')
def init_db_command():
    """Initializes the database using the command line."""
    # TODO: prevent this from being done on production
    init_db()
    print('Initialized the database.')
