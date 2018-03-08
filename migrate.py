'''Script to migrate data from a previous schema into current database'''
# from model import init_db, Location
from peewee import *
import requests
import urllib.parse
import urllib

PUBLIC_TOKEN='caspii'
SECRET_TOKEN='secret'
TARGET_SERVER='http://localhost:5000'
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&sessionid=%s&date=%s"

db = SqliteDatabase('old_database.db')
class Location(Model):
    """
    ORM model representing a location log entry
    """
    date = DateTimeField()
    username = CharField()
    latitude = CharField()
    longitude =CharField()
    class Meta:
        database = db


logs = Location.select().where(Location.username == PUBLIC_TOKEN).order_by(Location.date.desc())

for log in logs:
    date = urllib.parse.quote_plus(log.date.strftime('%Y-%m-%d+%H:%M:%S'))
    #print('lat="%s" lon="%s" %s' % (log.latitude, log.longitude, date ))
    requests.get(TARGET_SERVER + REQUEST_URL % (log.latitude, log.longitude, PUBLIC_TOKEN, SECRET_TOKEN, date))
