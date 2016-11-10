#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")
sys.path.insert(1,"/var/www/FlaskApp/config")
from app import app as application
application.secret_key = 'Add your secret key'

