from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def hello():
    date = request.args.get('date')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    username = request.args.get('username')
    sessionid = request.args.get('sessionid')

    response =  '%s :: (lat, long) = (%s, %s). username = %s, sessionid = %s ' % (date, latitude, longitude, username, sessionid)
    print response



    return "Hello World!"



@app.route("/store/")
def save_location():
    date = request.args.get('date')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    username = request.args.get('username')
    sessionid = request.args.get('sessionid')

    response =  '%s :: (lat, long) = (%s, %s). username = %s, sessionid = %s ' % (date, latitude, longitude, username, sessionid)
    print response

    return "Thanks dude"
