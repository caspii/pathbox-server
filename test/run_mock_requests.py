# Generate a bunch of mock requests to the server
import requests
import urllib.parse
from datetime import datetime

TARGET_SERVER='http://localhost:5000'
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&sessionid=%s&date=%s"

for i in range(1):
    date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person1', 'secret', date))
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret2', date))
    # Send wrong secret
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret3', date))



