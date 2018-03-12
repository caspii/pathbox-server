#!/usr/bin/python
# Config file used on production server
import sys
import logging


ADMINS = ['caspar.wrede@gmail.com']
CREDENTIALS = ('postmaster@mg.casparwre.de', 'e7fdb46aa807dabf10e3f1bd96b31022')

activate_this = '/var/www/keepthescore.co/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/keepthescore.co/")
from logging.handlers import SMTPHandler
mail_handler = SMTPHandler('smtp.mailgun.org',
                           'postmaster@mg.casparwre.de',
                           ADMINS, 'Exception in KeepTheScore.co', CREDENTIALS)
mail_handler.setLevel(logging.ERROR)

from app import app as application
application.secret_key = '6546423232323asd84654654654'
application.logger.addHandler(mail_handler)
