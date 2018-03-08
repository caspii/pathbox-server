from peewee import *
import os
from datetime import datetime


db = Proxy()
# Get full path of database
basedir = os.path.abspath(os.path.dirname(__file__))
database = os.path.join(basedir, 'database.db')
db.initialize(SqliteDatabase(database))
########################################################################


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    """
    Class representing one connecting client
    """
    secret_token = CharField(unique=True)   # Created by client, required to log an entry
    public_token = CharField(unique=True)   # Created by client, visible in web URL
    date_first_seen = DateTimeField()
    date_last_seen = DateTimeField()
    client_name = CharField(null=True)
    client_description = CharField(null=True)

    @classmethod
    def fetch(cls, public_token, secret_token, client_name=None):
        print("Fetching: " + public_token)
        try:
            client = Client.get(Client.public_token == public_token)
            print('Found client')
        except Client.DoesNotExist:
            # No client found
            print('Creating new client + ' + secret_token)
            now = datetime.now()
            client = Client.create(secret_token=secret_token, public_token=public_token, client_name=client_name,
                                   date_first_seen=now, date_last_seen=now)
        return client

    def log_location(self, latitude, longitude, date):
        print('Creating a log, wot? For client ' + str(self.id))

        Location.create(client=self, latitude=latitude, longitude=longitude, date_created=date,
                        date_logged=datetime.now())
        self.date_last_seen = datetime.now()
        self.save()


class Location(BaseModel):
    """
    Class representing a location log entry
    """
    client = ForeignKeyField(Client)
    latitude = CharField()
    longitude = CharField()
    date_created = DateTimeField()       # Date that client created log entry
    date_logged = DateTimeField()        # Date that client sent location to server


def initdb():
    try:
        Location.create_table(True)
        Client.create_table(True)
    except OperationalError:
        print("Error whilst creating table")

