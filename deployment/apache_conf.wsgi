#!/usr/bin/python3
# Config file used on production server
import sys
import logging



logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pathbox.co/")

from app import app as application
application.secret_key = '6546423232323asd84654654654'
