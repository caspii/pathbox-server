from peewee import *
import os
from datetime import datetime, timedelta
from flask import abort
import gpxpy.geo

db = Proxy()
# Get full path of database
basedir = os.path.abspath(os.path.dirname(__file__))
database = os.path.join(basedir, 'database.db')
db.initialize(SqliteDatabase(database))
########################################################################
# Filter variables
# Determines what locations are discarded
ACCURACY_THRESHOLD = 160  # Accuracy above is discarded
DISTANCE_THRESHOLD = 30   # Distance below is discarded

class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    """
    Class representing one connecting client
    """
    secret_token = CharField()              # Created by client, required to log an entry
    public_token = CharField(unique=True)   # Created by client, visible in web URL
    date_first_seen = DateTimeField(default=datetime.now)
    date_last_seen = DateTimeField(default=datetime.now)
    client_name = CharField(null=True)
    client_description = CharField(null=True)

    @classmethod
    def fetch(cls, public_token, secret_token, client_name=None):
        try:
            client = Client.get(Client.public_token == public_token)
            print('Found client: ' + public_token)
            if client.secret_token != secret_token:
                print('Wrong secret provided')
                abort(405)
        except Client.DoesNotExist:
            # Client not seen before<<>
            print('Creating new client + ' + public_token)
            client = Client.create(secret_token=secret_token, public_token=public_token, client_name=client_name)
        return client

    @classmethod
    def get_newest(cls):
        """Get list of newest clients"""
        clients = Client.select().order_by(-Client.date_first_seen).paginate(0, 50)
        no_clients = Client.select().count()
        return clients, no_clients

    @classmethod
    def get_logs(cls, public_token, date=None):
        """Return a filtered list of location logs dicts."""
        try:
            client = Client.get(Client.public_token == public_token)
        except Client.DoesNotExist:
            abort(404)
        if date is None:
            logs = Location.select().where(Location.client == client).order_by(Location.date_created.desc())
        else:
            logs = Location.select().where((Location.client == client) &
               (Location.date_created.between(
                date,
                date + timedelta(days=1))))\
                .order_by(Location.date_created.desc())
        # Filter the logs for accuracy
        temp_filtered_list = [log for log in logs if log.accuracy < ACCURACY_THRESHOLD ]
        # Filter logs for distance moved
        filtered_logs = []
        previous_log = None
        for log in temp_filtered_list:

            if previous_log is None:  # First iteration
                dist = 0
            else:
                dist = gpxpy.geo.haversine_distance(previous_log.latitude, previous_log.longitude, log.latitude, log.longitude)
            if dist > DISTANCE_THRESHOLD or previous_log is None:
                filtered_logs.append({'lat': float(log.latitude), 'lng': float(log.longitude),
                       'title': log.date_created.strftime("Here at %H:%M UTC"), 'dist': dist, 'acc': log.accuracy}, )
            previous_log = log
        print("Unfiltered logs: " + str(len(logs)))
        print("Filtered logs: " + str(len(filtered_logs)))
        return client, filtered_logs

    def add_log_entry(self, latitude, longitude, date, accuracy, clientname=None):
        print('Logging for client ' + self.public_token)
        print("----")
        Location.create(client=self, latitude=latitude, longitude=longitude, date_created=date, accuracy=accuracy)
        self.date_last_seen = datetime.now()
        self.client_name = clientname
        self.save()


class Location(BaseModel):
    """
    Class representing a location log entry
    """
    client = ForeignKeyField(Client)
    latitude = FloatField()
    longitude = FloatField()
    accuracy = FloatField()
    date_created = DateTimeField()                      # Date that client created log entry
    date_logged = DateTimeField(default=datetime.now)   # Date that client sent location to server


def init_db():
    try:
        Location.create_table(True)
        Client.create_table(True)
    except OperationalError:
        print("Error whilst creating table")

###################################################
