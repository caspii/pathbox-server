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

from utils import elapsed_time


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


def get_data(public_token):
    doc_ref = db.collection(u'clients').document(public_token)
    doc = doc_ref.get()
    data = doc.to_dict()
    raw_locations = data['locations']
    locations = [{'lat': x['latitude'], 'lng': x['longitude'], 'title': parse_timestamp(x['time'])}
                 for x in raw_locations]
    last_update = parse_timestamp(data['last_update'])
    first_update = parse_timestamp(raw_locations[0]['time'])
    client_name = data['client_name']
    return locations, client_name, last_update, first_update


def parse_timestamp(timestamp):
    """Return a nicely formatted string from a timestamp"""
    date = datetime.fromtimestamp(timestamp / 1e3)
    # formatted_date = date.strftime("%m/%d/%Y, %H:%M:%S")
    pretty_time = elapsed_time(date)
    return pretty_time


@app.route("/d/<public_token>/")
def view_debug(public_token):
    """"Output all logs as JSON dump for debugging purposes"""
    try:
        locations = get_data(public_token)
        return '{}'.format(locations)
    except google.cloud.exceptions.NotFound:
        return 'No such document!'


@app.route("/v/<public_token>/")
def view_client(public_token):
    """Fetch all location data for a single client and display om a map"""
    try:
        locations, client_name, last_update, first_update = get_data(public_token)
        return render_template('map.html', coords=locations, client_name=client_name, last_update=last_update,
                               first_update=first_update)
    except google.cloud.exceptions.NotFound:
        return 'No such document!'


@app.route('/faq')
def faq():
    return render_template('FAQ.md')


@app.route('/privacy')
def privacy():
    return render_template('privacy.md')


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