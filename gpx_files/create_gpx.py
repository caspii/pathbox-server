from model import initdb, Location

username='caspii'

file = open('output.gpx','w')

logs = Location.select().where(Location.username == username).order_by(Location.date.desc())
# <trkpt lat="46.57608333" lon="8.89241667"><ele>2376</ele><time>2007-10-14T10:09:57Z</time></trkpt>
output=''
for log in logs:
    file.write('<trkpt lat="%s" lon="%s"><ele>100</ele><time>%s</time></trkpt>\n' % (log.latitude, log.longitude, log.date))

file.close()
