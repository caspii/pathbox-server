# Generate a bunch of mock requests to the server
import requests
import urllib.parse
from datetime import datetime

TARGET_SERVER='http://localhost:5000'
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&sessionid=%s&date=%s&accuracy=%s&clientname=%s"

for i in range(1):
    date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person1', 'secret', date, 55, ""))
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret2', date, 55, ""))
    # Send wrong secret
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret3', date, 100, ""))



date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'caspii', 'secret', date, 55, "Donald"))
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret2', date, 55, "Trump"))
