from flask import Flask, request
from model import db, initdb, Location
import urllib
from datetime import datetime



app = Flask(__name__)

@app.route("/")
def hello():
    log_request(request)
    return "Hello World!"



@app.route("/v1/")
def save_location():
    log_request(request)
    return "Thanks dude"



def log_request(request):

    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    username = request.args.get('username')
    sessionid = request.args.get('sessionid')

    try:
        date_str = urllib.unquote(request.args.get('date')).decode('utf8')
        date = datetime.strptime(date_str, '%Y-%m-%d+%H:%M:%S')
        print "New log from : " + username + " Date: " + str(date)
        print "----"
        location = Location(latitude=latitude, longitude=longitude, username=username, date=date)
        location.save()
    except (AttributeError):
        print "Date not parseable: " + date_str

    # response =  '%s :: (lat, long) = (%s, %s). username = %s, sessionid = %s ' % (date, latitude, longitude, username, sessionid)



@app.cli.command('initdb')
def initdb_command():
    """Initializes the database using the command line."""
    # TODO: prevent this from being done on production
    initdb()
    print 'Initialized the database.'
