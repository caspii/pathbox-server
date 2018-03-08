#!/usr/bin/env bash
# This should really not be done on production. Add a test to prevent this
. venv/bin/activate
export FLASK_APP=app.py
rm -f database.db
flask init_db
