import google
from flask import Flask, request, abort, render_template
from model import init_db, Client
import urllib.parse
from datetime import datetime, timedelta
from lib.humantime import pretty_date
from flaskext.markdown import Markdown
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)
Markdown(app)
cred = credentials.Certificate('firestore-credentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Allow pretty dates via jinja2 filter
app.jinja_env.filters['human_time'] = pretty_date


@app.route("/")
def hello():
    return render_template('landing.html')


@app.route("/d/<public_token>/")
def debug(public_token):
    """"Output all logs as JSON dump for debugging purposes"""
    doc_ref = db.collection(u'clients').document(public_token)

    try:
        doc = doc_ref.get()
        data = doc.to_dict()
        raw_locations = data['locations']
        locations = [{'lat': x['latitude'], 'lng': x['longitude']} for x in raw_locations]
        return '{}'.format(locations)
    except google.cloud.exceptions.NotFound:
        return 'No such document!'


@app.route("/v/<public_token>/")
def view_username(public_token):
    doc_ref = db.collection(u'clients').document(public_token)

    try:
        doc = doc_ref.get()
        data = doc.to_dict()
        raw_locations = data['locations']
        locations = [{'lat': x['latitude'], 'lng': x['longitude']} for x in raw_locations]
        client_name = 'Caspar Device'
        return render_template('map.html', coords=locations, client_name=client_name)
    except google.cloud.exceptions.NotFound:
        return 'No such document!'




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
