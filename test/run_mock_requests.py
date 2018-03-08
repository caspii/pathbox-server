# Generate a bunch of mock requests to the server
import requests

TARGET_SERVER='http://localhost:5000'
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&sessionid=%s&date=%s"

for i in range(1):
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'caspii', 'secret', '2018-03-06%2B23%253A46%253A59'))
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'caspii2', 'secret2', '2018-03-06%2B23%253A46%253A59'))
    # Send wrong secret
    requests.get(TARGET_SERVER + REQUEST_URL % (9000, 9000, 'caspii2', 'secret3', '2018-03-06%2B23%253A46%253A59'))



