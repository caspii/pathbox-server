# Generate a bunch of mock requests to the server
import requests

TARGET_SERVER='http://localhost:5000'
REQUEST_URL="/v1/?latitude=%s&longitude=%s&username=%s&date=%s"

for i in range(10):
    r = requests.get(TARGET_SERVER + REQUEST_URL % (9000,9000,'caspii', '2018-03-06%2B23%253A46%253A59'))
    #r = requests.get(TARGET_SERVER + '/v1/?date=2018-03-06%2B23%253A49%253A36&distance=0.7&latitude=52.4985543&phonenumber=e213bf78-c43f-4530-a74a-d9cebd304a14&accuracy=57&sessionid=4bf07b3a-9dfa-4884-bc4f-3de63ee4d3f0&speed=0&extrainfo=0&eventtype=android&locationmethod=fused&longitude=13.3329852&username=moto&direction=0')


