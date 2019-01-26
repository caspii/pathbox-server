from flask import Flask, request, abort, render_template
from model import init_db, Client
import urllib.parse
from datetime import datetime, timedelta
from lib.humantime import pretty_date
import json
from flaskext.markdown import Markdown


app = Flask(__name__)
Markdown(app)

# Allow pretty dates via jinja2 filter
app.jinja_env.filters['human_time'] = pretty_date


@app.route("/")
def hello():
    return render_template('landing.html')


@app.route("/v1/")
def log_v1():
    """Write incoming request data to the database. NOTE: v1 of the API and not very safe!"""
    data = request.args.to_dict()
    try:
        date_str = urllib.parse.unquote(request.args.get('date'))
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
    except AttributeError as e:
        print("Date cannot be parsed: " + str(e))
    except TypeError:  # Added to test GPSLogger App.
        date = datetime.now()
    client = Client.fetch(public_token=data['username'],
                          secret_token=data['username'])  # Hack meaning no secret token is used
    if client:
        client.add_log_entry(latitude=float(data['latitude']), longitude=float(data['longitude']), date=date,
                             accuracy=float(data['accuracy']), clientname=data.get('clientname', 'GPS Tracker v1'))
    return "You did it"


@app.route("/v2/")
def log_v2():
    """Write incoming request data to the database"""
    data = request.args.to_dict()
    try:
        date_str = urllib.parse.unquote(request.args.get('date'))
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
    except AttributeError as e:
        print("Date cannot be parsed: " + str(e))
    except TypeError: # TODO: This was added to test GPSLogger App. Should probably be removed
        date = datetime.now()
    client = Client.fetch(public_token=data['public_token'], secret_token=data['secret_token'])
    if client:
        client.add_log_entry(latitude=float(data['latitude']), longitude=float(data['longitude']), date=date,
                             accuracy=float(data['accuracy']), clientname=data.get('clientname'))
    return "You did it v2"


@app.route("/v/<public_token>/<date_str>")
@app.route("/v/<public_token>/")
def view_username(public_token, date_str=None):
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.utcnow().date()
    client, logs = Client.get_logs(public_token, date)

    day_before = (date - timedelta(days=1)).strftime("%Y-%m-%d")    # Generate link for previous day
    day_after = (date + timedelta(days=1))                          # Generate link for next day
    if day_after > datetime.now().date():                           # Don't allow dates in the future
        day_after = None
    else:
        day_after = day_after.strftime("%Y-%m-%d")
    return render_template('map.html', coords=logs, client=client,
                           date=date.strftime("%B %d, %Y"), day_before=day_before, day_after=day_after)


@app.route("/d/<public_token>/<date_str>")
def debug(public_token, date_str=None):
    """"Output all logs as JSON dump for debugging purposes"""
    if date_str:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    client, logs = Client.get_logs(public_token, date)
    output = "<h1>Raw log dump</h2>"
    for log in logs:
        output += json.dumps(log) + '<br>'
    return output


@app.route('/faq')
def faq():
    return render_template('FAQ.md')


@app.route('/stats99')
def stats():
    clients, no_clients = Client.get_newest()
    return render_template('stats.html', clients=clients, no_clients=no_clients)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_500(e):
    return render_template('500.html'), 500


@app.cli.command('init_db')
def init_db_command():
    """Initializes the database using the command line."""
    # TODO: prevent this from being done on production
    init_db()
    print('Initialized the database.')
