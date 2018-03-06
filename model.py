import peewee
import os
import base64
from datetime import datetime



db = peewee.Proxy()
# Get full path of database
basedir = os.path.abspath(os.path.dirname(__file__))
database = os.path.join(basedir, 'database.db')
db.initialize(peewee.SqliteDatabase(database))

########################################################################


class Location(peewee.Model):
    """
    ORM model representing a location log entry
    """
    date = peewee.DateTimeField()
    username = peewee.CharField()
    latitude = peewee.CharField()
    longitude = peewee.CharField()



    class Meta:
        database = db

def initdb():
    try:
        Location.create_table(True)
    except peewee.OperationalError:
        print("Error whilst creating table")
