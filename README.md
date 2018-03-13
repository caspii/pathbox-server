# Server for the GPS tracking app
This is a webapp implemented in Python Flask which
* receives locations from multiple mobile clients
* displays those locations on a map

A client request looks like this:

`localhost:5000/view/?latitude=X&longitude=Y&username=Z&sessionid=A`

## Temporary bookmarks

Google maps API Key: AIzaSyD4p2Lv9o1Wgo-owLJ6xGLtVL9DEBzG2fU

http://www.jacquet80.eu/blog/post/2011/02/Display-GPX-tracks-using-Google-Maps-API


# Setup development environment 💻
1. Install packages:
   * On Ubuntu: `sudo apt install python-pip python-virtualenv python-dev`
   * On Mac OSX: `brew install bower pyenv-virtualenv`
1. Create virtual environment: `virtualenv -p python3 venv`
1. Enter virtualenv with `. venv/bin/activate`
1. `pip install -r requirements.txt`
1. Initialise database: `./init_db.sh`
1. Start dev server: `./run.sh`


# Pip commands
Pip is the package manager for Python.
## Installing a new package via pip
1. Enter virtualenv with `. venv/bin/activate`
1. Install: `pip install peewee`
2. Save to requirements `pip freeze > requirements.txt`
