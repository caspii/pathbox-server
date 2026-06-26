# Server for the GPS tracking app
This is a webapp implemented in Python Flask which
* receives locations from multiple mobile clients
* displays those locations on a map

## Quick Reference
* gcloud get/set project: `gcloud config get-value project`
* glocud set project: `gcloud config set project location-tracker-70ccd`
* Set default region `gcloud config set run/region europe-west1`

### Deployment
Taken from here: https://cloud.google.com/run/docs/quickstarts/build-and-deploy

1. Build docker image: `gcloud builds submit --tag gcr.io/location-tracker-70ccd/pathbox`
2. Deploy docker image: `gcloud run deploy pathbox --image gcr.io/location-tracker-70ccd/pathbox --platform managed`


## Temporary bookmarks

http://www.jacquet80.eu/blog/post/2011/02/Display-GPX-tracks-using-Google-Maps-API


# Setup development environment 💻
## Mac OS
```
brew cask install google-cloud-sdk
gcloud init
```

## Ubuntu
`sudo apt install python-pip python-virtualenv python-dev`

## Virtual Env
1. Create virtual environment: `virtualenv -p python3 venv`
1. Enter virtualenv with `. venv/bin/activate`
1. `pip install -r requirements.txt`



# Pip commands
Pip is the package manager for Python.
## Installing a new package via pip
1. Enter virtualenv with `. venv/bin/activate`
1. Install: `pip install peewee`
2. Save to requirements `pip freeze > requirements.txt`
