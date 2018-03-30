# Generate a bunch of mock requests to the server
import requests
import urllib.parse
from datetime import datetime
import uuid


TARGET_SERVER='http://localhost:5000'

# -------------------------------------
# Test V1 of api
# -------------------------------------
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&sessionid=%s&date=%s&accuracy=%s&clientname=%s"
date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))

requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person1', 'secret', date, 55, ""))
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret2', date, 55, ""))

# Send wrong secret
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret3', date, 100, ""))
date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))

# Test Client name
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'caspii', 'secret', date, 55, "Donald"))
requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'person2', 'secret2', date, 55, "Trump"))


# -------------------------------------
# Test V2 of api
# -------------------------------------
REQUEST_URL="/v2/?date=%s&altitude=%s&public_token=%s&latitude=%s&accuracy=%s&secret_token=%s&longitude=%s&clientname=%s"
date = urllib.parse.quote_plus(datetime.now().strftime('%Y-%m-%d+%H:%M:%S'))
secret1 = str(uuid.uuid4())
secret2 = str(uuid.uuid4())
secret3 = str(uuid.uuid4())
secret4 = str(uuid.uuid4())


requests.get(TARGET_SERVER + REQUEST_URL % (date, 90.9, 'person1_v2', 10000, 20, secret1, -1000, ''))
requests.get(TARGET_SERVER + REQUEST_URL % (date, 90.9, 'person2_v2', 10000, 30, secret2, -1000, ''))

# Send wrong secret
requests.get(TARGET_SERVER + REQUEST_URL % (date, 90.9, 'person2_v2', 10000, 20, secret1, -1000, ''))

# Test Client name
requests.get(TARGET_SERVER + REQUEST_URL % (date, 90.9, 'person3_v2', 10000, 100, secret3, -1000, 'Dude I love this'))
requests.get(TARGET_SERVER + REQUEST_URL % (date, 90.9, 'person4_v2', 10000, 22, secret4, -1000, "This is frickin' cool"))

# Real requests
R = '/v2/?date=2018-03-30%2B21%253A41%253A05&altitude=0.0&public_token=bvv5vjxf&latitude=52.4985387&accuracy=25.788&secret_token=955b9e28-429e-4262-8956-c529d2d45616&longitude=13.3331414'
requests.get(TARGET_SERVER + R)