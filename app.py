from flask import Flask, request, abort, render_template
from model import init_db, Client
import urllib.parse
from datetime import datetime, timedelta
from lib.humantime import pretty_date
import json


app = Flask(__name__)

# Allow pretty dates via jinja2 filter
app.jinja_env.filters['human_time'] = pretty_date


@app.route("/")
def hello():
    return render_template('landing.html')


@app.route("/v1/")
def log_location():
    log_request(request)
    return "You did it"


@app.route("/view/<public_token>/<date_str>")
@app.route("/view/<public_token>/")
def view_username(public_token, date_str=None):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.now().date()
    client, logs = Client.get_logs(public_token, date)

    day_before = (date - timedelta(days=1)).strftime("%Y-%m-%d")    # Generate link for previous day
    day_after = (date + timedelta(days=1))                          # Generate link for next day
    if day_after > datetime.now().date():                           # Don't allow dates in the future
        day_after = None
    else:
        day_after = day_after.strftime("%Y-%m-%d")
    return render_template('map.html', coords=logs, client=client,
                           date=date.strftime("%B %d, %Y"), day_before=day_before, day_after=day_after)


@app.route("/debug/<public_token>/<date_str>")
def debug(public_token, date_str=None):
    """"Output all logs as JSON dump for debugging purposes"""
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    client, logs = Client.get_logs(public_token, date)
    output = "<h1>Raw log dump</h2>"
    for log in logs:
        output += json.dumps(log) + '<br>'
    return output


def log_request(request):
    """Write incoming request data to the database"""
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    accuracy = request.args.get('accuracy')
    public_token = request.args.get('username')
    secret_token = request.args.get('username') # This is a terrible hack TODO: revert this
    # secret_token = request.args.get('sessionid')
    clientname = request.args.get('clientname')
    #print(request)
    try:
        date_str = urllib.parse.unquote(request.args.get('date'))
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
    except AttributeError as e:
        print("Date cannot be parsed: " + str(e))
    except TypeError: # TODO: This was added to test GPSLogger App. Should probably be removed
        date = datetime.now()
    print("New log from : " + public_token + " Date: " + str(date))
    print("----")
    client = Client.fetch(public_token, secret_token)
    if client:
        client.add_log_entry(latitude=float(latitude), longitude=float(longitude), date=date, accuracy=float(accuracy),
                             clientname=clientname)


@app.cli.command('init_db')
def init_db_command():
    """Initializes the database using the command line."""
    # TODO: prevent this from being done on production
    init_db()
    print('Initialized the database.')
