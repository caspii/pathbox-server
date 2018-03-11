from peewee import *
import os
from datetime import datetime, timedelta
from flask import abort

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
            if client.secret_token != secret_token:
                print('Wrong secret provided')
                abort(405)
        except Client.DoesNotExist:
            # Client not seen before<<>
            print('Creating new client + ' + public_token)
            now = datetime.now()
            client = Client.create(secret_token=secret_token, public_token=public_token, client_name=client_name,
                                   date_first_seen=now, date_last_seen=now)
        return client

    @classmethod
    def get_logs(cls, public_token, date=None):
        try:
            client = Client.get(Client.public_token == public_token)
        except Client.DoesNotExist:
            abort(404)
        if date is None:
            logs = Location.select().where(Location.client == client).order_by(Location.date_created.desc())
        else:
            logs = Location.select().where(Location.client == client & Location.date_created.between(
                date,
                date + timedelta(days=1))
            ).order_by(Location.date_created.desc())
            print("Getting logs for " + str(date))
        return client.date_first_seen, client.date_last_seen, logs

    def add_log_entry(self, latitude, longitude, date):
        print('Creating a log for client ' + self.public_token)
        Location.create(client=self, latitude=latitude, longitude=longitude, date_created=date,
                        date_logged=datetime.now())
        self.date_last_seen = datetime.now()
        self.save()


class Location(BaseModel):
    """
    Class representing a location log entry
    """
    client = ForeignKeyField(Client)
    latitude = FloatField()
    longitude = FloatField()
    date_created = DateTimeField()       # Date that client created log entry
    date_logged = DateTimeField()        # Date that client sent location to server


def init_db():
    try:
        Location.create_table(True)
        Client.create_table(True)
    except OperationalError:
        print("Error whilst creating table")

###################################################
